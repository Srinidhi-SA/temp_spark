import json
import time

try:
    import cPickle as pickle
except:
    import pickle

from pyspark.sql import SQLContext
from bi.common import utils as CommonUtils
from bi.algorithms import utils as MLUtils
from bi.common import DataFrameHelper
from bi.common import MLModelSummary, NormalCard, KpiData, C3ChartData, HtmlData
from bi.common import SklearnGridSearchResult, SkleanrKFoldResult

from bi.stats.frequency_dimensions import FreqDimensions
from bi.narratives.dimension.dimension_column import DimensionColumnNarrative
from bi.stats.chisquare import ChiSquare
from bi.narratives.chisquare import ChiSquareNarratives

from pyspark.ml.classification import RandomForestClassifier
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








class RandomForestPysparkScript:
    def __init__(self, data_frame, df_helper,df_context, spark, prediction_narrative, result_setter, meta_parser, mlEnvironment="pyspark"):
        # self._data_frame = data_frame
        # self._dataframe_helper = df_helper
        # self._dataframe_context = df_context
        # self._spark = spark
        # self._model_summary = MLModelSummary()
        # self._score_summary = {}
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
        self._slug = GLOBALSETTINGS.MODEL_SLUG_MAPPING["sparkrandomforest"]
        self._targetLevel = self._dataframe_context.get_target_level_for_model()

        self._completionStatus = self._dataframe_context.get_completion_status()
        print self._completionStatus,"initial completion status"
        self._analysisName = self._slug
        self._messageURL = self._dataframe_context.get_message_url()
        self._scriptWeightDict = self._dataframe_context.get_ml_model_training_weight()
        self._mlEnv = mlEnvironment

        self._scriptStages = {
            "initialization":{
                "summary":"Initialized the Random Forest Scripts",
                "weight":4
                },
            "training":{
                "summary":"Random Forest Model Training Started",
                "weight":2
                },
            "completion":{
                "summary":"Random Forest Model Training Finished",
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

        model_path = self._dataframe_context.get_model_path()
        if model_path.startswith("file"):
            model_path = model_path[7:]
        validationDict = self._dataframe_context.get_validation_dict()
        print "model_path",model_path
        pipeline_filepath = "file://"+str(model_path)+"/"+str(self._slug)+"/pipeline/"
        model_filepath = "file://"+str(model_path)+"/"+str(self._slug)+"/model"
        pmml_filepath = "file://"+str(model_path)+"/"+str(self._slug)+"/modelPmml"

        df = self._data_frame

        print "########################## ", df
        levels = df.select(result_column).distinct().count()

        model_filepath = model_path+"/"+self._slug+"/model.pkl"
        pmml_filepath = str(model_path)+"/"+str(self._slug)+"/traindeModel.pmml"

        CommonUtils.create_update_and_save_progress_message(self._dataframe_context,self._scriptWeightDict,self._scriptStages,self._slug,"training","info",display=True,emptyBin=False,customMsg=None,weightKey="total")

        st = time.time()
        pipeline = MLUtils.create_pyspark_ml_pipeline(numerical_columns, categorical_columns, result_column)
        # pipelineModel = pipeline.fit(df)
        # indexed = pipelineModel.transform(df)
        # MLUtils.save_pipeline_or_model(pipelineModel,pipeline_filepath)
        trainingData,validationData = MLUtils.get_training_and_validation_data(df ,result_column,0.8)   # indexed

        labelIndexer = StringIndexer(inputCol=result_column, outputCol="label")
        OriginalTargetconverter = IndexToString(inputCol="label", outputCol="originalTargetColumn")

        clf = RandomForestClassifier()
        algoParams = algoSetting.get_params_dict()
        clfParams = [prm.name for prm in clf.params]
        algoParams = {getattr(clf, k):v if type(v)=='list' else [v] for k,v in algoParams.items() if k in clfParams}

        paramGrid = ParamGridBuilder()
        for k,v in algoParams.items():
            paramGrid = paramGrid.addGrid(k,v)
        paramGrid = paramGrid.build()

        evaluationMetricDict = {"name":GLOBALSETTINGS.CLASSIFICATION_MODEL_EVALUATION_METRIC}
        evaluationMetricDict["displayName"] = GLOBALSETTINGS.SKLEARN_EVAL_METRIC_NAME_DISPLAY_MAP[evaluationMetricDict["name"]]
        self._result_setter.set_hyper_parameter_results(self._slug,None)

        if validationDict["name"] == "kFold":
            numFold = int(validationDict["value"])
            crossval = CrossValidator(estimator=Pipeline(stages=[pipeline, labelIndexer, clf]),
                          estimatorParamMaps=paramGrid,
                          evaluator=BinaryClassificationEvaluator(),
                          numFolds=3 if numFold == 0 else numFold)  # use 3+ folds in practice
            cvrf = crossval.fit(trainingData)
            prediction = cvrf.transform(validationData)
            bestModel = cvrf.bestModel
        else:
            tvs = TrainValidationSplit(estimator=Pipeline(stages=[pipeline, labelIndexer, clf]),
                       estimatorParamMaps=paramGrid,
                       evaluator=BinaryClassificationEvaluator(),
                       trainRatio=0.8)

            model = tvs.fit(train)
            bestModel = model

        predsAndLabels = prediction.select(['prediction', 'label']).rdd.map(tuple)
        metrics = MulticlassMetrics(predsAndLabels)
        labelMapping = {k:v for k, v in enumerate(bestModel.stages[-2].labels)}
        inverseLabelMapping = {v:float(k) for k, v in enumerate(bestModel.stages[-2].labels)}

        conf_mat_ar = metrics.confusionMatrix().toArray()
        print conf_mat_ar
        confusion_matrix = {}
        for i in range(len(conf_mat_ar)):
        	confusion_matrix[labelMapping[i]] = {}
        	for j, val in enumerate(conf_mat_ar[i]):
        		confusion_matrix[labelMapping[i]][labelMapping[j]] = val
        print confusion_matrix

        trainingTime = time.time()-st
        print "="*100
        print "Target level", inverseLabelMapping[self._targetLevel]
        print "="*100
        f1_score = metrics.fMeasure(inverseLabelMapping[self._targetLevel], 1.0)
        precision = metrics.precision(inverseLabelMapping[self._targetLevel])
        recall = metrics.recall(inverseLabelMapping[self._targetLevel])
        accuracy = metrics.accuracy
        print "F1 score is ", f1_score
        print "Precision score is ", precision
        print "Recall score is ", recall
        print "Accuracy score is ", accuracy

        feature_importance = MLUtils.calculate_sparkml_feature_importance(df, bestModel.stages[-1], categorical_columns, numerical_columns)

        objs = {"trained_model":cvrf,"actual":prediction.select('label'),"predicted":prediction.select('prediction'),
        "probability":prediction.select('probability'),"feature_importance":feature_importance,
        "featureList":list(categorical_columns) + list(numerical_columns),"labelMapping":labelMapping}

        # Calculating prediction_split
        val_cnts = prediction.groupBy('label').count()
        val_cnts = map(lambda row: row.asDict(), val_cnts.collect())
        prediction_split = {}
        total_nos = objs['actual'].count()
        for item in val_cnts:
            prediction_split[item['label']] = round(item['count']*100 / float(total_nos), 2)

        if not algoSetting.is_hyperparameter_tuning_enabled():
            modelName = "M"+"0"*(GLOBALSETTINGS.MODEL_NAME_MAX_LENGTH-1)+"1"
            modelFilepathArr = model_filepath.split("/")[:-1]
            modelFilepathArr.append(modelName+".pkl")
            # joblib.dump(objs["trained_model"],"/".join(modelFilepathArr))
        runtime = round((time.time() - st_global),2)

        cat_cols = list(set(categorical_columns) - {result_column})
        self._model_summary = MLModelSummary()
        self._model_summary.set_algorithm_name("Spark ML Random Forest")
        self._model_summary.set_algorithm_display_name("Spark ML Random Forest")
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
        # self._model_summary.set_model_features(list(set(x_train.columns)-set([result_column])))
        self._model_summary.set_model_features(objs["featureList"])
        self._model_summary.set_level_counts(self._metaParser.get_unique_level_dict(list(set(categorical_columns)) + [result_column]))
        self._model_summary.set_num_trees(20)
        self._model_summary.set_num_rules(300)
        self._model_summary.set_target_level(self._targetLevel)

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
        print "="*100
        print self._model_summary.get_feature_importance()
        print "="*100

        rfCards = [json.loads(CommonUtils.convert_python_object_to_json(cardObj)) for cardObj in MLUtils.create_model_summary_cards(self._model_summary)]
        for card in rfCards:
            self._prediction_narrative.add_a_card(card)

        self._result_setter.set_model_summary({"randomforest":json.loads(CommonUtils.convert_python_object_to_json(self._model_summary))})
        self._result_setter.set_spark_random_forest_model_summary(modelSummaryJson)
        self._result_setter.set_rf_cards(rfCards)

        CommonUtils.create_update_and_save_progress_message(self._dataframe_context,self._scriptWeightDict,self._scriptStages,self._slug,"completion","info",display=True,emptyBin=False,customMsg=None,weightKey="total")


    def Predict(self):
        SQLctx = SQLContext(sparkContext=self._spark.sparkContext, sparkSession=self._spark)
        dataSanity = True
        level_counts_train = self._dataframe_context.get_level_count_dict()
        categorical_columns = self._dataframe_helper.get_string_columns()
        numerical_columns = self._dataframe_helper.get_numeric_columns()
        time_dimension_columns = self._dataframe_helper.get_timestamp_columns()
        result_column = self._dataframe_context.get_result_column()
        categorical_columns = [x for x in categorical_columns if x != result_column]

        level_counts_score = CommonUtils.get_level_count_dict(self._data_frame,categorical_columns,self._dataframe_context.get_column_separator(),output_type="dict",dataType="spark")
        for key in level_counts_train:
            if key in level_counts_score:
                if level_counts_train[key] != level_counts_score[key]:
                    dataSanity = False
            else:
                dataSanity = False

        test_data_path = self._dataframe_context.get_input_file()
        score_data_path = self._dataframe_context.get_score_path()+"/ScoredData/data.csv"
        trained_model_path = self._dataframe_context.get_model_path()
        if trained_model_path.endswith(".pkl"):
            trained_model_path = "/".join(trained_model_path.split("/")[:-1])+"/model"
        pipeline_path = "/".join(trained_model_path.split("/")[:-1])+"/pipeline"
        score_summary_path = self._dataframe_context.get_score_path()+"/Summary/summary.json"

        pipelineModel = MLUtils.load_pipeline(pipeline_path)
        trained_model = MLUtils.load_rf_model(trained_model_path)
        df = self._data_frame
        indexed = pipelineModel.transform(df)
        transformed = trained_model.transform(indexed)
        label_indexer_dict = MLUtils.read_string_indexer_mapping(pipeline_path,SQLctx)
        prediction_to_levels = udf(lambda x:label_indexer_dict[x],StringType())
        transformed = transformed.withColumn(result_column,prediction_to_levels(transformed.prediction))
        # udf_to_calculate_probability = udf(lambda x:max(x[0]))
        # transformed = transformed.withColumn("predicted_probability",udf_to_calculate_probability(transformed.probability))
        # print transformed.select("predicted_probability").show(5)
        probability_dataframe = transformed.select([result_column,"probability"]).toPandas()
        probability_dataframe = probability_dataframe.rename(index=str, columns={result_column: "predicted_class"})
        probability_dataframe["predicted_probability"] = probability_dataframe["probability"].apply(lambda x:max(x))
        self._score_summary["prediction_split"] = MLUtils.calculate_scored_probability_stats(probability_dataframe)
        self._score_summary["result_column"] = result_column
        scored_dataframe = transformed.select(categorical_columns+time_dimension_columns+numerical_columns+[result_column,"probability"]).toPandas()
        # scored_dataframe = scored_dataframe.rename(index=str, columns={"predicted_probability": "probability"})
        if score_data_path.startswith("file"):
            score_data_path = score_data_path[7:]
        scored_dataframe.to_csv(score_data_path,header=True,index=False)
        # print json.dumps({"scoreSummary":self._score_summary},indent=2)
        CommonUtils.write_to_file(score_summary_path,json.dumps({"scoreSummary":self._score_summary}))


        print "STARTING DIMENSION ANALYSIS ..."
        columns_to_keep = []
        columns_to_drop = []
        considercolumnstype = self._dataframe_context.get_score_consider_columns_type()
        considercolumns = self._dataframe_context.get_score_consider_columns()
        if considercolumnstype != None:
            if considercolumns != None:
                if considercolumnstype == ["excluding"]:
                    columns_to_drop = considercolumns
                elif considercolumnstype == ["including"]:
                    columns_to_keep = considercolumns
        if len(columns_to_keep) > 0:
            columns_to_drop = list(set(df.columns)-set(columns_to_keep))
        # spark_scored_df = transformed.select(categorical_columns+time_dimension_columns+numerical_columns+[result_column])
        scored_df = transformed.select(categorical_columns+time_dimension_columns+numerical_columns+[result_column])

        SQLctx = SQLContext(sparkContext=self._spark.sparkContext, sparkSession=self._spark)
        spark_scored_df = SQLctx.createDataFrame(scored_df.toPandas())
        columns_to_drop = [x for x in columns_to_drop if x in spark_scored_df.columns]
        modified_df = spark_scored_df.select([x for x in spark_scored_df.columns if x not in columns_to_drop])
        df_helper = DataFrameHelper(modified_df, self._dataframe_context)
        df_helper.set_params()
        df = df_helper.get_data_frame()
        try:
            fs = time.time()
            narratives_file = self._dataframe_context.get_score_path()+"/narratives/FreqDimension/data.json"
            result_file = self._dataframe_context.get_score_path()+"/results/FreqDimension/data.json"
            df_freq_dimension_obj = FreqDimensions(df, df_helper, self._dataframe_context).test_all(dimension_columns=[result_column])
            df_freq_dimension_result = CommonUtils.as_dict(df_freq_dimension_obj)
            CommonUtils.write_to_file(result_file,json.dumps(df_freq_dimension_result))
            narratives_obj = DimensionColumnNarrative(result_column, df_helper, self._dataframe_context, df_freq_dimension_obj)
            narratives = CommonUtils.as_dict(narratives_obj)
            CommonUtils.write_to_file(narratives_file,json.dumps(narratives))
            print "Frequency Analysis Done in ", time.time() - fs,  " seconds."
        except:
            print "Frequency Analysis Failed "

        try:
            fs = time.time()
            narratives_file = self._dataframe_context.get_score_path()+"/narratives/ChiSquare/data.json"
            result_file = self._dataframe_context.get_score_path()+"/results/ChiSquare/data.json"
            df_chisquare_obj = ChiSquare(df, df_helper, self._dataframe_context).test_all(dimension_columns= [result_column])
            df_chisquare_result = CommonUtils.as_dict(df_chisquare_obj)
            print 'RESULT: %s' % (json.dumps(df_chisquare_result, indent=2))
            CommonUtils.write_to_file(result_file,json.dumps(df_chisquare_result))
            chisquare_narratives = CommonUtils.as_dict(ChiSquareNarratives(df_helper, df_chisquare_obj, self._dataframe_context,df))
            # print 'Narrarives: %s' %(json.dumps(chisquare_narratives, indent=2))
            CommonUtils.write_to_file(narratives_file,json.dumps(chisquare_narratives))
            print "ChiSquare Analysis Done in ", time.time() - fs, " seconds."
        except:
           print "ChiSquare Analysis Failed "
