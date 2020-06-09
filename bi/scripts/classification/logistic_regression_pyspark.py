from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import object
import json
import time

try:
    import pickle as pickle
except:
    import pickle

from pyspark.sql import SQLContext
from bi.common import utils as CommonUtils
from bi.algorithms import utils as MLUtils
from bi.algorithms import DecisionTrees
from bi.common import DataFrameHelper
from bi.stats.frequency_dimensions import FreqDimensions
from bi.narratives.dimension.dimension_column import DimensionColumnNarrative
from bi.stats.chisquare import ChiSquare
from bi.narratives.chisquare import ChiSquareNarratives
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.feature import IndexToString
from pyspark.sql.functions import udf
from pyspark.sql.types import *

from pyspark.ml.classification import LogisticRegression, OneVsRest
from pyspark2pmml import PMMLBuilder

from pyspark.sql import SQLContext
from bi.common import utils as CommonUtils
from bi.algorithms import utils as MLUtils
from bi.common import DataFrameHelper
from bi.common import MLModelSummary, NormalCard, KpiData, C3ChartData, HtmlData
from bi.common import PySparkTrainTestResult, PySparkGridSearchResult
from bi.narratives.decisiontree.decision_tree import DecisionTreeNarrative

from bi.stats.frequency_dimensions import FreqDimensions
from bi.narratives.dimension.dimension_column import DimensionColumnNarrative
from bi.stats.chisquare import ChiSquare
from bi.narratives.chisquare import ChiSquareNarratives

from pyspark.ml.tuning import CrossValidator, ParamGridBuilder, TrainValidationSplit
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import MulticlassClassificationEvaluator, BinaryClassificationEvaluator
from pyspark.mllib.evaluation import BinaryClassificationMetrics, MulticlassMetrics
from pyspark.ml.feature import IndexToString
from pyspark.sql.functions import udf
from pyspark.sql.types import *

from bi.settings import setting as GLOBALSETTINGS
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.pipeline import PipelineModel

from py4j.protocol import Py4JError




class LogisticRegressionPysparkScript(object):
    def __init__(self, data_frame, df_helper,df_context, spark):
        self._metaParser = meta_parser
        self._prediction_narrative = prediction_narrative
        self._result_setter = result_setter
        self._data_frame = data_frame
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context
        self._ignoreMsg = self._dataframe_context.get_message_ignore()
        self._spark = spark
        self._model_summary =  MLModelSummary()
        self._score_summary = {}
        self._slug = GLOBALSETTINGS.MODEL_SLUG_MAPPING["sparklogisticregression"]
        self._targetLevel = self._dataframe_context.get_target_level_for_model()

        self._completionStatus = self._dataframe_context.get_completion_status()
        self._analysisName = self._slug
        self._messageURL = self._dataframe_context.get_message_url()
        self._scriptWeightDict = self._dataframe_context.get_ml_model_training_weight()
        self._mlEnv = mlEnvironment

        self._scriptStages = {
            "initialization":{
                "summary":"Initialized the Logistic Regression Scripts",
                "weight":4
                },
            "training":{
                "summary":"Logistic Regression Model Training Started",
                "weight":2
                },
            "completion":{
                "summary":"Logistic Regression Model Training Finished",
                "weight":4
                },
            }

    def Train(self):
        st_global = time.time()

        CommonUtils.create_update_and_save_progress_message(self._dataframe_context,  self._scriptWeightDict,self._scriptStages,self._slug,"initialization","info",display=True,emptyBin=False,customMsg=None,weightKey="total")

        algosToRun = self._dataframe_context.get_algorithms_to_run()
        algoSetting = filter(lambda x: x.get_algorithm_slug()==self._slug,algosToRun)[0]
        categorical_columns = self._dataframe_helper.get_string_columns()
        uid_col = self._dataframe_context.get_uid_column()

        if self._metaParser.check_column_isin_ignored_suggestion(uid_col):
            categorical_columns = list(set(categorical_columns) - {uid_col})

        allDateCols = self._dataframe_context.get_date_columns()
        categorical_columns = list(set(categorical_columns)-set(allDateCols))
        numerical_columns = self._dataframe_helper.get_numeric_columns()
        result_column = self._dataframe_context.get_result_column()
        categorical_columns = [x for x in categorical_columns if x != result_column]

        appType = self._dataframe_context.get_app_type()

        model_path = self._dataframe_context.get_model_path()
        pipeline_filepath = model_path+"/LogisticRegression/TrainedModels/pipeline"
        model_filepath = model_path+"/LogisticRegression/TrainedModels/model"
        summary_filepath = model_path+"/LogisticRegression/ModelSummary/summary.json"

        df=self._data_frame
        pipeline = MLUtils.create_pyspark_ml_pipeline(numerical_columns,categorical_columns,result_column)
        pipelineModel = pipeline.fit(df)
        indexed = pipelineModel.transform(df)
        MLUtils.save_pipeline_or_model(pipelineModel,pipeline_filepath)
        trainingData,validationData = MLUtils.get_training_and_validation_data(indexed,result_column,0.8)
        OriginalTargetconverter = IndexToString(inputCol="label", outputCol="originalTargetColumn")
        levels = trainingData.select("label").distinct().collect()

        if self._classifier == "lr":
            if len(levels) == 2:
                lr = LogisticRegression(maxIter=10, regParam=0.3, elasticNetParam=0.8)
            elif len(levels) > 2:
                lr = LogisticRegression(maxIter=10, regParam=0.3, elasticNetParam=0.8,family="multinomial")
            fit = lr.fit(trainingData)
        elif self._classifier == "OneVsRest":
            lr = LogisticRegression()
            ovr = OneVsRest(classifier=lr)
            fit = ovr.fit(trainingData)
        transformed = fit.transform(validationData)
        MLUtils.save_pipeline_or_model(fit,model_filepath)

        print(fit.coefficientMatrix)
        print(fit.interceptVector)

        # feature_importance = MLUtils.calculate_sparkml_feature_importance(indexed,fit,categorical_columns,numerical_columns)
        label_classes = transformed.select("label").distinct().collect()
        results = transformed.select(["prediction","label"])
        if len(label_classes) > 2:
            evaluator = MulticlassClassificationEvaluator(predictionCol="prediction")
            evaluator.evaluate(results)
            self._model_summary["model_accuracy"] = evaluator.evaluate(results,{evaluator.metricName: "accuracy"}) # accuracy of the model
        else:
            evaluationMetricDict = {"name":GLOBALSETTINGS.CLASSIFICATION_MODEL_EVALUATION_METRIC}
            evaluationMetricDict["displayName"] = GLOBALSETTINGS.SKLEARN_EVAL_METRIC_NAME_DISPLAY_MAP[evaluationMetricDict["name"]]

        self._result_setter.set_hyper_parameter_results(self._slug,None)

        if validationDict["name"] == "kFold":
            numFold = int(validationDict["value"])
            estimator = Pipeline(stages=[pipeline, labelIndexer, clf])
            if algoSetting.is_hyperparameter_tuning_enabled():
                modelFilepath = "/".join(model_filepath.split("/")[:-1])
                pySparkHyperParameterResultObj = PySparkGridSearchResult(estimator, paramGrid, appType, modelFilepath, levels,
                evaluationMetricDict, trainingData, validationData, numFold, self._targetLevel, labelMapping, inverseLabelMapping,
                df)
                resultArray = pySparkHyperParameterResultObj.train_and_save_classification_models()
                self._result_setter.set_hyper_parameter_results(self._slug,resultArray)
                self._result_setter.set_metadata_parallel_coordinates(self._slug,
                {"ignoreList":pySparkHyperParameterResultObj.get_ignore_list(),
                "hideColumns":pySparkHyperParameterResultObj.get_hide_columns(),
                "metricColName":pySparkHyperParameterResultObj.get_comparison_metric_colname(),
                "columnOrder":pySparkHyperParameterResultObj.get_keep_columns()})

                bestModel = pySparkHyperParameterResultObj.getBestModel()
                prediction = pySparkHyperParameterResultObj.getBestPrediction()

            else:
                crossval = CrossValidator(estimator=estimator,
                              estimatorParamMaps=paramGrid,
                              evaluator=BinaryClassificationEvaluator() if levels == 2 else MulticlassClassificationEvaluator(),
                              numFolds=3 if numFold is None else numFold)  # use 3+ folds in practice
                cvrf = crossval.fit(trainingData)
                prediction = cvrf.transform(validationData)
                bestModel = cvrf.bestModel

        else:
            train_test_ratio = float(self._dataframe_context.get_train_test_split())
            estimator = Pipeline(stages=[pipeline, labelIndexer, clf])
            if algoSetting.is_hyperparameter_tuning_enabled():
                modelFilepath = "/".join(model_filepath.split("/")[:-1])
                pySparkHyperParameterResultObj = PySparkTrainTestResult(estimator, paramGrid, appType, modelFilepath, levels,
                evaluationMetricDict, trainingData, validationData, train_test_ratio, self._targetLevel, labelMapping, inverseLabelMapping,
                df)
                resultArray = pySparkHyperParameterResultObj.train_and_save_classification_models()
                self._result_setter.set_hyper_parameter_results(self._slug,resultArray)
                self._result_setter.set_metadata_parallel_coordinates(self._slug,
                {"ignoreList":pySparkHyperParameterResultObj.get_ignore_list(),
                "hideColumns":pySparkHyperParameterResultObj.get_hide_columns(),
                "metricColName":pySparkHyperParameterResultObj.get_comparison_metric_colname(),
                "columnOrder":pySparkHyperParameterResultObj.get_keep_columns()})

                bestModel = pySparkHyperParameterResultObj.getBestModel()
                prediction = pySparkHyperParameterResultObj.getBestPrediction()

            else:
                tvs = TrainValidationSplit(estimator=estimator,
                estimatorParamMaps=paramGrid,
                evaluator=BinaryClassificationEvaluator() if levels == 2 else MulticlassClassificationEvaluator(),
                trainRatio=train_test_ratio)

                tvrf = tvs.fit(trainingData)
                prediction = tvrf.transform(validationData)
                bestModel = tvrf.bestModel

        predsAndLabels = prediction.select(['prediction', 'label']).rdd.map(tuple)
        metrics = MulticlassMetrics(predsAndLabels)
        posLabel = inverseLabelMapping[self._targetLevel]

        conf_mat_ar = metrics.confusionMatrix().toArray()
        print(conf_mat_ar)
        confusion_matrix = {}
        for i in range(len(conf_mat_ar)):
        	confusion_matrix[labelMapping[i]] = {}
        	for j, val in enumerate(conf_mat_ar[i]):
        		confusion_matrix[labelMapping[i]][labelMapping[j]] = val
        print(confusion_matrix)

        trainingTime = time.time()-st

        f1_score = metrics.fMeasure(inverseLabelMapping[self._targetLevel], 1.0)
        precision = metrics.precision(inverseLabelMapping[self._targetLevel])
        recall = metrics.recall(inverseLabelMapping[self._targetLevel])
        accuracy = metrics.accuracy

        objs = {"trained_model":bestModel,"actual":prediction.select('label'),"predicted":prediction.select('prediction'),
        "probability":prediction.select('probability'),"feature_importance":None,
        "featureList":list(categorical_columns) + list(numerical_columns),"labelMapping":labelMapping}

        # Calculating prediction_split
        val_cnts = prediction.groupBy('label').count()
        val_cnts = map(lambda row: row.asDict(), val_cnts.collect())
        prediction_split = {}
        total_nos = objs['actual'].count()
        for item in val_cnts:
            classname = labelMapping[item['label']]
            prediction_split[classname] = round(item['count']*100 / float(total_nos), 2)

        if not algoSetting.is_hyperparameter_tuning_enabled():
            modelName = "M"+"0"*(GLOBALSETTINGS.MODEL_NAME_MAX_LENGTH-1)+"1"
            modelFilepathArr = model_filepath.split("/")[:-1]
            modelFilepathArr.append(modelName)
            bestModel.save("/".join(modelFilepathArr))
        runtime = round((time.time() - st_global),2)

        try:
            print(pmml_filepath)
            pmmlBuilder = PMMLBuilder(self._spark, trainingData, bestModel).putOption(clf, 'compact', True)
            pmmlBuilder.buildFile(pmml_filepath)
            pmmlfile = open(pmml_filepath,"r")
            pmmlText = pmmlfile.read()
            pmmlfile.close()
            self._result_setter.update_pmml_object({self._slug:pmmlText})
        except Exception as e:
            print("PMML failed...", str(e))
            pass

        cat_cols = list(set(categorical_columns) - {result_column})
        self._model_summary = MLModelSummary()
        self._model_summary.set_algorithm_name("Spark ML Logistic Regression")
        self._model_summary.set_algorithm_display_name("Spark ML Logistic Regression")
        self._model_summary.set_slug(self._slug)
        self._model_summary.set_training_time(runtime)
        self._model_summary.set_confusion_matrix(confusion_matrix)
        self._model_summary.set_feature_importance(objs["feature_importance"])
        self._model_summary.set_feature_list(objs["featureList"])
        self._model_summary.set_model_accuracy(accuracy)
        self._model_summary.set_training_time(round((time.time() - st),2))
        self._model_summary.set_precision_recall_stats([precision, recall])
        self._model_summary.set_model_precision(precision)
        self._model_summary.set_model_recall(recall)
        self._model_summary.set_target_variable(result_column)
        self._model_summary.set_prediction_split(prediction_split)
        self._model_summary.set_validation_method("KFold")
        self._model_summary.set_level_map_dict(objs["labelMapping"])
        self._model_summary.set_model_features(objs["featureList"])
        self._model_summary.set_level_counts(self._metaParser.get_unique_level_dict(list(set(categorical_columns)) + [result_column]))
        self._model_summary.set_num_trees(None)
        self._model_summary.set_num_rules(300)
        self._model_summary.set_target_level(self._targetLevel)

        if not algoSetting.is_hyperparameter_tuning_enabled():
            modelDropDownObj = {
                        "name":self._model_summary.get_algorithm_name(),
                        "evaluationMetricValue":accuracy,
                        "evaluationMetricName":"accuracy",
                        "slug":self._model_summary.get_slug(),
                        "Model Id": modelName
                        }
            modelSummaryJson = {
                "dropdown":modelDropDownObj,
                "levelcount":self._model_summary.get_level_counts(),
                "modelFeatureList":self._model_summary.get_feature_list(),
                "levelMapping":self._model_summary.get_level_map_dict(),
                "slug":self._model_summary.get_slug(),
                "name":self._model_summary.get_algorithm_name()
            }
        else:
            modelDropDownObj = {
                        "name":self._model_summary.get_algorithm_name(),
                        "evaluationMetricValue":accuracy,
                        "evaluationMetricName":"accuracy",
                        "slug":self._model_summary.get_slug(),
                        "Model Id":resultArray[0]["Model Id"]
                        }
            modelSummaryJson = {
                "dropdown":modelDropDownObj,
                "levelcount":self._model_summary.get_level_counts(),
                "modelFeatureList":self._model_summary.get_feature_list(),
                "levelMapping":self._model_summary.get_level_map_dict(),
                "slug":self._model_summary.get_slug(),
                "name":self._model_summary.get_algorithm_name()
            }

        lrCards = [json.loads(CommonUtils.convert_python_object_to_json(cardObj)) for cardObj in MLUtils.create_model_summary_cards(self._model_summary)]
        for card in lrCards:
            self._prediction_narrative.add_a_card(card)

        self._result_setter.set_model_summary({"logistic":json.loads(CommonUtils.convert_python_object_to_json(self._model_summary))})
        self._result_setter.set_spark_logistic_regression_model_summary(modelSummaryJson)
        self._result_setter.set_lr_cards(lrCards)

        CommonUtils.create_update_and_save_progress_message(self._dataframe_context,self._scriptWeightDict,self._scriptStages,self._slug,"completion","info",display=True,emptyBin=False,customMsg=None,weightKey="total")


    def Predict(self):
        self._scriptWeightDict = self._dataframe_context.get_ml_model_prediction_weight()
        self._scriptStages = {
            "initialization":{
                "summary":"Initialized the Logistic Regression Scripts",
                "weight":2
                },
            "prediction":{
                "summary":"Logistic Regression Model Prediction Finished",
                "weight":2
                },
            "frequency":{
                "summary":"descriptive analysis finished",
                "weight":2
                },
            "chisquare":{
                "summary":"chi Square analysis finished",
                "weight":4
                },
            "completion":{
                "summary":"all analysis finished",
                "weight":4
                },
            }

        self._completionStatus += self._scriptWeightDict[self._analysisName]["total"]*self._scriptStages["initialization"]["weight"]/10
        progressMessage = CommonUtils.create_progress_message_object(self._analysisName,\
                                    "initialization",\
                                    "info",\
                                    self._scriptStages["initialization"]["summary"],\
                                    self._completionStatus,\
                                    self._completionStatus)
        CommonUtils.save_progress_message(self._messageURL,progressMessage)
        self._dataframe_context.update_completion_status(self._completionStatus)

        SQLctx = SQLContext(sparkContext=self._spark.sparkContext, sparkSession=self._spark)
        dataSanity = True
        level_counts_train = self._dataframe_context.get_level_count_dict()
        categorical_columns = self._dataframe_helper.get_string_columns()
        numerical_columns = self._dataframe_helper.get_numeric_columns()
        time_dimension_columns = self._dataframe_helper.get_timestamp_columns()
        result_column = self._dataframe_context.get_result_column()
        categorical_columns = [x for x in categorical_columns if x != result_column]

        level_counts_score = CommonUtils.get_level_count_dict(self._data_frame,categorical_columns,self._dataframe_context.get_column_separator(),output_type="dict",dataType="spark")
        print('+'*100)
        print(level_counts_train)
        print(level_counts_train)
        print('+'*100)
        for key in level_counts_train:
            if key in level_counts_score:
                if level_counts_train[key] != level_counts_score[key]:
                    dataSanity = False
            else:
                dataSanity = False

        test_data_path = self._dataframe_context.get_input_file()
        score_data_path = self._dataframe_context.get_score_path()+"/data.csv"
        trained_model_path = self._dataframe_context.get_model_path()
        trained_model_path = "/".join(trained_model_path.split("/")[:-1])+"/"+self._slug+"/"+self._dataframe_context.get_model_for_scoring()
        score_summary_path = self._dataframe_context.get_score_path()+"/Summary/summary.json"

        pipelineModel = MLUtils.load_pipeline(trained_model_path)

        df = self._data_frame
        transformed = pipelineModel.transform(df)
        label_indexer_dict = MLUtils.read_string_indexer_mapping(trained_model_path,SQLctx)
        prediction_to_levels = udf(lambda x:label_indexer_dict[x],StringType())
        transformed = transformed.withColumn(result_column,prediction_to_levels(transformed.prediction))

        if "probability" in transformed.columns:
            probability_dataframe = transformed.select([result_column,"probability"]).toPandas()
            probability_dataframe = probability_dataframe.rename(index=str, columns={result_column: "predicted_class"})
            probability_dataframe["predicted_probability"] = probability_dataframe["probability"].apply(lambda x:max(x))
            self._score_summary["prediction_split"] = MLUtils.calculate_scored_probability_stats(probability_dataframe)
            self._score_summary["result_column"] = result_column
            scored_dataframe = transformed.select(categorical_columns+time_dimension_columns+numerical_columns+[result_column,"probability"]).toPandas()
            # scored_dataframe = scored_dataframe.rename(index=str, columns={"predicted_probability": "probability"})
        else:
            self._score_summary["prediction_split"] = []
            self._score_summary["result_column"] = result_column
            scored_dataframe = transformed.select(categorical_columns+time_dimension_columns+numerical_columns+[result_column]).toPandas()

        labelMappingDict = self._dataframe_context.get_label_map()
        if score_data_path.startswith("file"):
            score_data_path = score_data_path[7:]
        scored_dataframe.to_csv(score_data_path, header=True, index=False)

        uidCol = self._dataframe_context.get_uid_column()
        if uidCol == None:
            uidCols = self._metaParser.get_suggested_uid_columns()
            if len(uidCols) > 0:
                uidCol = uidCols[0]
        uidTableData = []
        predictedClasses = list(scored_dataframe[result_column].unique())
        if uidCol:
            if uidCol in df.columns:
                for level in predictedClasses:
                    levelDf = scored_dataframe[scored_dataframe[result_column] == level]
                    levelDf = levelDf[[uidCol,"predicted_probability",result_column]]
                    levelDf.sort_values(by="predicted_probability", ascending=False,inplace=True)
                    levelDf["predicted_probability"] = levelDf["predicted_probability"].apply(lambda x: humanize.apnumber(x*100)+"%" if x*100 >=10 else str(int(x*100))+"%")
                    uidTableData.append(levelDf[:5])
                uidTableData = pd.concat(uidTableData)
                uidTableData  = [list(arr) for arr in list(uidTableData.values)]
                uidTableData = [[uidCol,"Probability",result_column]] + uidTableData
                uidTable = TableData()
                uidTable.set_table_width(25)
                uidTable.set_table_data(uidTableData)
                uidTable.set_table_type("normalHideColumn")
                self._result_setter.set_unique_identifier_table(json.loads(CommonUtils.convert_python_object_to_json(uidTable)))

        self._completionStatus += self._scriptWeightDict[self._analysisName]["total"]*self._scriptStages["prediction"]["weight"]/10
        progressMessage = CommonUtils.create_progress_message_object(self._analysisName,\
                                    "prediction",\
                                    "info",\
                                    self._scriptStages["prediction"]["summary"],\
                                    self._completionStatus,\
                                    self._completionStatus)
        CommonUtils.save_progress_message(self._messageURL,progressMessage)
        self._dataframe_context.update_completion_status(self._completionStatus)

        # CommonUtils.write_to_file(score_summary_path,json.dumps({"scoreSummary":self._score_summary}))


        print("STARTING DIMENSION ANALYSIS ...")
        columns_to_keep = []
        columns_to_drop = []
        # considercolumnstype = self._dataframe_context.get_score_consider_columns_type()
        columns_to_keep = self._dataframe_context.get_score_consider_columns()
        # if considercolumnstype != None:
        #     if considercolumns != None:
        #         if considercolumnstype == ["excluding"]:
        #             columns_to_drop = considercolumns
        #         elif considercolumnstype == ["including"]:
        #             columns_to_keep = considercolumns
        if len(columns_to_keep) > 0:
            columns_to_drop = list(set(df.columns)-set(columns_to_keep))
        else:
            columns_to_drop += ["predicted_probability"]

        # columns_to_drop = [x for x in columns_to_drop if x in df.columns and x != result_column]
        # spark_scored_df = transformed.select(categorical_columns+time_dimension_columns+numerical_columns+[result_column])
        scored_df = transformed.select(categorical_columns+time_dimension_columns+numerical_columns+[result_column])
        # scored_df = scored_df.drop(','.join(columns_to_drop))

        # SQLctx = SQLContext(sparkContext=self._spark.sparkContext, sparkSession=self._spark)
        # spark_scored_df = SQLctx.createDataFrame(scored_df.toPandas())
        columns_to_drop = [x for x in columns_to_drop if x in scored_df.columns]
        modified_df = scored_df.select([x for x in scored_df.columns if x not in columns_to_drop])
        resultColLevelCount = dict(modified_df.groupby(result_column).count().collect())
        self._metaParser.update_column_dict(result_column,{"LevelCount":resultColLevelCount,
        "numberOfUniqueValues":len(resultColLevelCount.keys())})
        self._dataframe_context.set_story_on_scored_data(True)

        self._dataframe_context.update_consider_columns(columns_to_keep)
        df_helper = DataFrameHelper(modified_df, self._dataframe_context, self._metaParser)
        df_helper.set_params()

        df = df_helper.get_data_frame()
        try:
            fs = time.time()
            narratives_file = self._dataframe_context.get_score_path()+"/narratives/FreqDimension/data.json"
            result_file = self._dataframe_context.get_score_path()+"/results/FreqDimension/data.json"
            df_freq_dimension_obj = FreqDimensions(spark_scored_df, df_helper, self._dataframe_context).test_all(dimension_columns=[result_column])
            df_freq_dimension_result = CommonUtils.as_dict(df_freq_dimension_obj)
            CommonUtils.write_to_file(result_file,json.dumps(df_freq_dimension_result))
            narratives_obj = DimensionColumnNarrative(df, result_column, df_helper, self._dataframe_context, df_freq_dimension_obj)
            narratives = CommonUtils.as_dict(narratives_obj)
            CommonUtils.write_to_file(narratives_file,json.dumps(narratives))
            print("Frequency Analysis Done in ", time.time() - fs,  " seconds.")
        except:
            print("Frequency Analysis Failed ")

        try:
            fs = time.time()
            narratives_file = self._dataframe_context.get_score_path()+"/narratives/ChiSquare/data.json"
            result_file = self._dataframe_context.get_score_path()+"/results/ChiSquare/data.json"
            df_chisquare_obj = ChiSquare(df, df_helper, self._dataframe_context).test_all(dimension_columns= [result_column])
            df_chisquare_result = CommonUtils.as_dict(df_chisquare_obj)
            # print 'RESULT: %s' % (json.dumps(df_chisquare_result, indent=2))
            CommonUtils.write_to_file(result_file,json.dumps(df_chisquare_result))
            chisquare_narratives = CommonUtils.as_dict(ChiSquareNarratives(df_helper, df_chisquare_obj, self._dataframe_context,df))
            # print 'Narrarives: %s' %(json.dumps(chisquare_narratives, indent=2))
            CommonUtils.write_to_file(narratives_file,json.dumps(chisquare_narratives))
            print("ChiSquare Analysis Done in ", time.time() - fs, " seconds.")
        except:
           print("ChiSquare Analysis Failed ")
        spark_scored_df = df_helper.get_data_frame()
        # spark_scored_df.show(5)
        # try:
        #     fs = time.time()
        #     narratives_file = self._dataframe_context.get_score_path()+"/narratives/FreqDimension/data.json"
        #     result_file = self._dataframe_context.get_score_path()+"/results/FreqDimension/data.json"
        #     df_freq_dimension_obj = FreqDimensions(spark_scored_df, df_helper, self._dataframe_context).test_all(dimension_columns=[result_column])
        #     df_freq_dimension_result = CommonUtils.as_dict(df_freq_dimension_obj)
        #     CommonUtils.write_to_file(result_file,json.dumps(df_freq_dimension_result))
        #     narratives_obj = DimensionColumnNarrative(result_column, df_helper, self._dataframe_context, df_freq_dimension_obj)
        #     narratives = CommonUtils.as_dict(narratives_obj)
        #     CommonUtils.write_to_file(narratives_file,json.dumps(narratives))
        #     print "Frequency Analysis Done in ", time.time() - fs,  " seconds."
        # except:
        #     print "Frequency Analysis Failed "
        #
        # try:
        #     fs = time.time()
        #     narratives_file = self._dataframe_context.get_score_path()+"/narratives/ChiSquare/data.json"
        #     result_file = self._dataframe_context.get_score_path()+"/results/ChiSquare/data.json"
        #     df_chisquare_obj = ChiSquare(df, df_helper, self._dataframe_context).test_all(dimension_columns= [result_column])
        #     df_chisquare_result = CommonUtils.as_dict(df_chisquare_obj)
        #     # print 'RESULT: %s' % (json.dumps(df_chisquare_result, indent=2))
        #     CommonUtils.write_to_file(result_file,json.dumps(df_chisquare_result))
        #     chisquare_narratives = CommonUtils.as_dict(ChiSquareNarratives(df_helper, df_chisquare_obj, self._dataframe_context,df))
        #     # print 'Narrarives: %s' %(json.dumps(chisquare_narratives, indent=2))
        #     CommonUtils.write_to_file(narratives_file,json.dumps(chisquare_narratives))
        #     print "ChiSquare Analysis Done in ", time.time() - fs, " seconds."
        # except:
        #    print "ChiSquare Analysis Failed "
        if len(predictedClasses) >=2:
            try:
                fs = time.time()
                df_decision_tree_obj = DecisionTrees(spark_scored_df, df_helper, self._dataframe_context,self._spark,self._metaParser,scriptWeight=self._scriptWeightDict, analysisName=self._analysisName).test_all(dimension_columns=[result_column])
                narratives_obj = CommonUtils.as_dict(DecisionTreeNarrative(result_column, df_decision_tree_obj, self._dataframe_helper, self._dataframe_context,self._metaParser,self._result_setter,story_narrative=None, analysisName=self._analysisName,scriptWeight=self._scriptWeightDict))
                print(narratives_obj)
            except Exception as e:
                print("DecisionTree Analysis Failed ", str(e))
        else:
            data_dict = {"npred": len(predictedClasses), "nactual": len(labelMappingDict.values())}

            if data_dict["nactual"] > 2:
                levelCountDict[predictedClasses[0]] = resultColLevelCount[predictedClasses[0]]
                levelCountDict["Others"]  = sum([v for k,v in resultColLevelCount.items() if k != predictedClasses[0]])
            else:
                levelCountDict = resultColLevelCount
                otherClass = list(set(labelMappingDict.values())-set(predictedClasses))[0]
                levelCountDict[otherClass] = 0

                print(levelCountDict)

            total = float(sum([x for x in levelCountDict.values() if x != None]))
            levelCountTuple = [({"name":k,"count":v,"percentage":humanize.apnumber(v*100/total)+"%"}) for k,v in levelCountDict.items() if v != None]
            levelCountTuple = sorted(levelCountTuple,key=lambda x:x["count"],reverse=True)
            data_dict["blockSplitter"] = "|~NEWBLOCK~|"
            data_dict["targetcol"] = result_column
            data_dict["nlevel"] = len(levelCountDict.keys())
            data_dict["topLevel"] = levelCountTuple[0]
            data_dict["secondLevel"] = levelCountTuple[1]
            maincardSummary = NarrativesUtils.get_template_output("/apps/",'scorewithoutdtree.html',data_dict)

            main_card = NormalCard()
            main_card_data = []
            main_card_narrative = NarrativesUtils.block_splitter(maincardSummary,"|~NEWBLOCK~|")
            main_card_data += main_card_narrative

            chartData = NormalChartData([levelCountDict]).get_data()
            chartJson = ChartJson(data=chartData)
            chartJson.set_title(result_column)
            chartJson.set_chart_type("donut")
            mainCardChart = C3ChartData(data=chartJson)
            mainCardChart.set_width_percent(33)
            main_card_data.append(mainCardChart)

            uidTable = self._result_setter.get_unique_identifier_table()
            if uidTable != None:
                main_card_data.append(uidTable)
            main_card.set_card_data(main_card_data)
            main_card.set_card_name("Predicting Key Drivers of {}".format(result_column))
            self._result_setter.set_score_dtree_cards([main_card])
