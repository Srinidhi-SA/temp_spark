import json
import time
import os
from datetime import datetime
from sklearn.metrics import roc_curve, auc, roc_auc_score,log_loss
import pandas as pd
import numpy as np

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
from bi.common.mlmodelclasses import PySparkGridSearchResult, PySparkTrainTestResult

from bi.stats.frequency_dimensions import FreqDimensions
from bi.narratives.dimension.dimension_column import DimensionColumnNarrative
from bi.stats.chisquare import ChiSquare
from bi.narratives.chisquare import ChiSquareNarratives
from bi.algorithms import GainLiftKS
from bi.common import NarrativesTree


from pyspark.ml.tuning import CrossValidator, ParamGridBuilder, TrainValidationSplit
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import MulticlassClassificationEvaluator, BinaryClassificationEvaluator
from pyspark.mllib.evaluation import BinaryClassificationMetrics, MulticlassMetrics
from pyspark.ml.feature import IndexToString
from pyspark.sql.functions import udf,col
from pyspark.sql.types import *

from bi.settings import setting as GLOBALSETTINGS
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.pipeline import PipelineModel
from pyspark.ml.classification import GBTClassifier, OneVsRest,DecisionTreeClassifier



# os.environ['PYSPARK_SUBMIT_ARGS'] = "--jars xgboost4j-spark-0.72.jar,xgboost4j-0.72.jar pyspark-shell"

class XGBoostPysparkScript(object):
    def __init__(self, data_frame, df_helper,df_context, spark, prediction_narrative, result_setter, meta_parser, mlEnvironment="pyspark"):
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
        self._slug = GLOBALSETTINGS.MODEL_SLUG_MAPPING["xgboost"]
        self._targetLevel = self._dataframe_context.get_target_level_for_model()
        self._targetLevel = self._dataframe_context.get_target_level_for_model()
        self._completionStatus = self._dataframe_context.get_completion_status()
        print(self._completionStatus,"initial completion status")
        self._analysisName = self._slug
        self._messageURL = self._dataframe_context.get_message_url()
        self._scriptWeightDict = self._dataframe_context.get_ml_model_training_weight()
        self._datasetName = CommonUtils.get_dataset_name(self._dataframe_context.CSV_FILE)
        self._mlEnv = mlEnvironment

        # os.environ['PYSPARK_SUBMIT_ARGS'] = "--jars xgboost4j-spark-0.72.jar,xgboost4j-0.72.jar pyspark-shell"


        self._scriptStages = {
            "initialization":{
                "summary":"Initialized the Xgboost Scripts",
                "weight":4
                },
            "training":{
                "summary":"Xgboost Model Training Started",
                "weight":2
                },
            "completion":{
                "summary":"Xgboost Model Training Finished",
                "weight":4
                },
            }


    def Train(self):
        st_global = time.time()
        # os.environ['PYSPARK_SUBMIT_ARGS'] = "--jars xgboost4j-spark-0.72.jar,xgboost4j-0.72.jar pyspark-shell"
        ##################################################################################################
        #self._spark.sparkContext.addPyFile("/home/alagappan/xgboost_spark/sparkxgb.zip")
        ##################################################################################################

        #from sparkxgb import XGBoostEstimator

        CommonUtils.create_update_and_save_progress_message(self._dataframe_context,  self._scriptWeightDict,self._scriptStages,self._slug,"initialization","info",display=True,emptyBin=False,customMsg=None,weightKey="total")

        algosToRun = self._dataframe_context.get_algorithms_to_run()
        algoSetting = [x for x in algosToRun if x.get_algorithm_slug()==self._slug][0]
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
        if model_path.startswith("file"):
            model_path = model_path[7:]
        validationDict = self._dataframe_context.get_validation_dict()
        print("model_path",model_path)
        pipeline_filepath = "file://"+str(model_path)+"/"+str(self._slug)+"/pipeline/"
        model_filepath = "file://"+str(model_path)+"/"+str(self._slug)+"/model"
        pmml_filepath = "file://"+str(model_path)+"/"+str(self._slug)+"/modelPmml"

        df = self._data_frame
        levels = df.select(result_column).distinct().count()
        print('+'*100)
        print(levels)
        print('+'*100)

        appType = self._dataframe_context.get_app_type()

        model_filepath = model_path+"/"+self._slug+"/model"
        pmml_filepath = str(model_path)+"/"+str(self._slug)+"/traindeModel.pmml"

        CommonUtils.create_update_and_save_progress_message(self._dataframe_context,self._scriptWeightDict,self._scriptStages,self._slug,"training","info",display=True,emptyBin=False,customMsg=None,weightKey="total")

        st = time.time()
        pipeline = MLUtils.create_pyspark_ml_pipeline(numerical_columns, categorical_columns, result_column)

        trainingData, validationData = MLUtils.get_training_and_validation_data(df ,result_column,0.8)   # indexed

        labelIndexer = StringIndexer(inputCol=result_column, outputCol="label")
        # OriginalTargetconverter = IndexToString(inputCol="label", outputCol="originalTargetColumn")


        # Label Mapping and Inverse
        labelIdx = labelIndexer.fit(trainingData)
        labelMapping = {k:v for k, v in enumerate(labelIdx.labels)}
        inverseLabelMapping = {v:float(k) for k, v in enumerate(labelIdx.labels)}

        #gbt = GBTClassifier()
        #clf = OneVsRest(classifier=gbt)
        clf= DecisionTreeClassifier()

        if not algoSetting.is_hyperparameter_tuning_enabled():
            algoParams = algoSetting.get_params_dict()
        else:
            algoParams = algoSetting.get_params_dict_hyperparameter()
        for k, v in algoParams.items():
            print(k, v)
        clfParams = [prm.name for prm in clf.params]
        algoParams = {getattr(clf, k):v if type(v)=='list' else [v] for k,v in algoParams.items() if k in clfParams}
        for k, v in algoParams.items():
            print(k.name, v)

        paramGrid = ParamGridBuilder()#.addGrid(clf.objective, ['binary:logistic']).build()
        if not algoSetting.is_hyperparameter_tuning_enabled():
            for k,v in algoParams.items():
                if v == [None] * len(v):
                    continue
                paramGrid = paramGrid.addGrid(k,v)
            paramGrid = paramGrid.build()
        else:
            for k,v in algoParams.items():
                print(k.name, v)
                if v[0] == [None] * len(v[0]):
                    continue
                paramGrid = paramGrid.addGrid(k,v[0])
            paramGrid = paramGrid.build()

        if len(paramGrid) > 1:
            hyperParamInitParam = algoSetting.get_hyperparameter_params()
            evaluationMetricDict = {"name":hyperParamInitParam["evaluationMetric"]}
            evaluationMetricDict["displayName"] = GLOBALSETTINGS.SKLEARN_EVAL_METRIC_NAME_DISPLAY_MAP[evaluationMetricDict["name"]]
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
                              evaluator=BinaryClassificationEvaluator().setRawPredictionCol("probability") if levels == 2 else MulticlassClassificationEvaluator(),
                              numFolds=3 if numFold is None else numFold)  # use 3+ folds in practice
                trainingData.show()
                cvspxgb = crossval.fit(trainingData)
                prediction = cvspxgb.transform(validationData)
                bestModel = cvspxgb.bestModel



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

                tvspxgb = tvs.fit(trainingData)
                prediction = tvspxgb.transform(validationData)
                bestModel = tvspxgb.bestModel
        modelmanagement_={param[0].name:param[1] for param in bestModel.stages[2].extractParamMap().items()}
        MLUtils.save_pipeline_or_model(bestModel,model_filepath)
        predsAndLabels = prediction.select(['prediction', 'label']).rdd.map(tuple)
        label_classes = prediction.select("label").distinct().collect()
        # if len(label_classes) > 2:
        #     metrics = MulticlassMetrics(predsAndLabels) # accuracy of the model
        # else:
        #     metrics = BinaryClassificationEvaluator(predsAndLabels)
        metrics = MulticlassMetrics(predsAndLabels)
        posLabel = inverseLabelMapping[self._targetLevel]



        trainingTime = time.time()-st
        f1_score = metrics.fMeasure(inverseLabelMapping[self._targetLevel], 1.0)
        precision = metrics.precision(inverseLabelMapping[self._targetLevel])
        recall = metrics.recall(inverseLabelMapping[self._targetLevel])
        accuracy = metrics.accuracy

        print(f1_score,precision,recall,accuracy)

        #gain chart implementation
        def cal_prob_eval(x):
            if len(x) == 1:
                if x == posLabel:
                    return(float(x[1]))
                else:
                    return(float(1 - x[1]))
            else:
                return(float(x[int(posLabel)]))


        column_name= 'probability'
        def y_prob_for_eval_udf():
            return udf(lambda x:cal_prob_eval(x))
        prediction = prediction.withColumn("y_prob_for_eval", y_prob_for_eval_udf()(col(column_name)))

        try:
            pys_df = prediction.select(['y_prob_for_eval','prediction','label'])
            gain_lift_ks_obj = GainLiftKS(pys_df, 'y_prob_for_eval', 'prediction', 'label', posLabel, self._spark)
            gain_lift_KS_dataframe = gain_lift_ks_obj.Run().toPandas()
        except:
            print("gain chant failed")
            pass



        act_list = prediction.select('label').collect()
        actual=[int(row.label) for row in act_list]
        pred_list = prediction.select('prediction').collect()
        predicted=[int(row.prediction) for row in pred_list]
        prob_list = prediction.select('probability').collect()
        probability=[list(row.probability) for row in prob_list]
        #feature_importance = MLUtils.calculate_sparkml_feature_importance(df, bestModel.stages[-1], categorical_columns, numerical_columns)
        objs = {"trained_model":bestModel,"actual":actual,"predicted":predicted,
        "probability":probability,"feature_importance":None,
        "featureList":list(categorical_columns) + list(numerical_columns),"labelMapping":labelMapping}

        conf_mat_ar = metrics.confusionMatrix().toArray()
        print(conf_mat_ar)
        confusion_matrix = {}
        for i in range(len(conf_mat_ar)):
            confusion_matrix[labelMapping[i]] = {}
            for j, val in enumerate(conf_mat_ar[i]):
                confusion_matrix[labelMapping[i]][labelMapping[j]] = val
        print(confusion_matrix) # accuracy of the model

        '''ROC CURVE IMPLEMENTATION'''
        y_prob = probability
        y_score = predicted
        y_test = actual
        logLoss = log_loss(y_test,y_prob)
        if levels <= 2:
            positive_label_probs = []
            for val in y_prob:
                positive_label_probs.append(val[int(posLabel)])
            roc_auc = roc_auc_score(y_test,y_score)

            roc_data_dict = {
                                "y_score" : y_score,
                                "y_test" : y_test,
                                "positive_label_probs" : positive_label_probs,
                                "y_prob" : y_prob,
                                "positive_label" : posLabel
                            }
            roc_dataframe = pd.DataFrame(
                                            {
                                                "y_score" : y_score,
                                                "y_test" : y_test,
                                                "positive_label_probs" : positive_label_probs
                                            }
                                        )
            #roc_dataframe.to_csv("binary_roc_data.csv")
            fpr, tpr, thresholds = roc_curve(y_test, positive_label_probs, pos_label = posLabel)
            roc_df = pd.DataFrame({"FPR" : fpr, "TPR" : tpr, "thresholds" : thresholds})
            roc_df["tpr-fpr"] = roc_df["TPR"] - roc_df["FPR"]

            optimal_index = np.argmax(np.array(roc_df["tpr-fpr"]))
            fpr_optimal_index =  roc_df.loc[roc_df.index[optimal_index], "FPR"]
            tpr_optimal_index =  roc_df.loc[roc_df.index[optimal_index], "TPR"]

            rounded_roc_df = roc_df.round({'FPR': 2, 'TPR': 4})

            unique_fpr = rounded_roc_df["FPR"].unique()

            final_roc_df = rounded_roc_df.groupby("FPR", as_index = False)[["TPR"]].mean()
            endgame_roc_df = final_roc_df.round({'FPR' : 2, 'TPR' : 3})

        elif levels > 2:
            positive_label_probs = []
            for val in y_prob:
                positive_label_probs.append(val[int(posLabel)])

            y_test_roc_multi = []
            for val in y_test:
                if val != posLabel:
                    val = posLabel + 1
                    y_test_roc_multi.append(val)
                else:
                    y_test_roc_multi.append(val)

            y_score_roc_multi = []
            for val in y_score:
                if val != posLabel:
                    val = posLabel + 1
                    y_score_roc_multi.append(val)
                else:
                    y_score_roc_multi.append(val)

            roc_auc = roc_auc_score(y_test_roc_multi, y_score_roc_multi)

            fpr, tpr, thresholds = roc_curve(y_test_roc_multi, positive_label_probs, pos_label = posLabel)
            roc_df = pd.DataFrame({"FPR" : fpr, "TPR" : tpr, "thresholds" : thresholds})
            roc_df["tpr-fpr"] = roc_df["TPR"] - roc_df["FPR"]

            optimal_index = np.argmax(np.array(roc_df["tpr-fpr"]))
            fpr_optimal_index =  roc_df.loc[roc_df.index[optimal_index], "FPR"]
            tpr_optimal_index =  roc_df.loc[roc_df.index[optimal_index], "TPR"]

            rounded_roc_df = roc_df.round({'FPR': 2, 'TPR': 4})
            unique_fpr = rounded_roc_df["FPR"].unique()
            final_roc_df = rounded_roc_df.groupby("FPR", as_index = False)[["TPR"]].mean()
            endgame_roc_df = final_roc_df.round({'FPR' : 2, 'TPR' : 3})
        # Calculating prediction_split
        val_cnts = prediction.groupBy('label').count()
        val_cnts = map(lambda row: row.asDict(), val_cnts.collect())
        prediction_split = {}
        total_nos = prediction.select('label').count()
        for item in val_cnts:
            print(labelMapping)
            classname = labelMapping[item['label']]
            prediction_split[classname] = round(item['count']*100 / float(total_nos), 2)

        if not algoSetting.is_hyperparameter_tuning_enabled():
            modelName = "M"+"0"*(GLOBALSETTINGS.MODEL_NAME_MAX_LENGTH-1)+"1"
            modelFilepathArr = model_filepath.split("/")[:-1]
            modelFilepathArr.append(modelName)
            objs["trained_model"].save("/".join(modelFilepathArr))
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
        self._model_summary.set_algorithm_name("XGBoost")
        self._model_summary.set_algorithm_display_name("XGBoost")
        self._model_summary.set_slug(self._slug)
        self._model_summary.set_training_time(runtime)
        self._model_summary.set_confusion_matrix(confusion_matrix)
        #self._model_summary.set_feature_importance(objs["feature_importance"])
        self._model_summary.set_feature_list(objs["featureList"])
        self._model_summary.set_model_accuracy(accuracy)
        self._model_summary.set_training_time(round((time.time() - st),2))
        self._model_summary.set_precision_recall_stats([precision, recall])
        self._model_summary.set_model_precision(precision)
        self._model_summary.set_model_recall(recall)
        self._model_summary.set_model_F1_score(f1_score)
        self._model_summary.set_model_log_loss(logLoss)
        self._model_summary.set_gain_lift_KS_data(gain_lift_KS_dataframe)
        self._model_summary.set_AUC_score(roc_auc)
        self._model_summary.set_target_variable(result_column)
        self._model_summary.set_prediction_split(prediction_split)
        self._model_summary.set_validation_method("KFold")
        self._model_summary.set_level_map_dict(objs["labelMapping"])
        # self._model_summary.set_model_features(list(set(x_train.columns)-set([result_column])))
        self._model_summary.set_model_features(objs["featureList"])
        self._model_summary.set_level_counts(self._metaParser.get_unique_level_dict(list(set(categorical_columns)) + [result_column]))
        #self._model_summary.set_num_trees(objs['trained_model'].getNumTrees)
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
        print(modelmanagement_)
        self._model_management = MLModelSummary()
        self._model_management.set_cacheNodeIds(data=modelmanagement_['cacheNodeIds'])
        self._model_management.set_checkpoint_interval(data=modelmanagement_['checkpointInterval'])
        self._model_management.set_max_bins(data=modelmanagement_['maxBins'])
        self._model_management.set_impurity(data=modelmanagement_['impurity'])
        self._model_management.set_max_depth(data=modelmanagement_['maxDepth'])
        self._model_management.set_min_instances_per_node(data=modelmanagement_['minInstancesPerNode'])
        self._model_management.set_min_info_gain(data=modelmanagement_['minInfoGain'])
        self._model_management.set_job_type(self._dataframe_context.get_job_name()) #Project name
        self._model_management.set_training_status(data="completed")# training status
        self._model_management.set_no_of_independent_variables(data=df) #no of independent varables
        self._model_management.set_target_level(self._targetLevel) # target column value
        self._model_management.set_training_time(runtime) # run time
        self._model_management.set_model_accuracy(round(metrics.accuracy,2))#accuracy
        self._model_management.set_algorithm_name("XGBoost")#algorithm name
        self._model_management.set_validation_method(str(validationDict["displayName"])+"("+str(validationDict["value"])+")")#validation method
        self._model_management.set_target_variable(result_column)#target column name
        self._model_management.set_creation_date(data=str(datetime.now().strftime('%b %d ,%Y  %H:%M ')))#creation date
        self._model_management.set_datasetName(self._datasetName)



        modelManagementSummaryJson = [

                            ["Project Name",self._model_management.get_job_type()],
                            ["Algorithm",self._model_management.get_algorithm_name()],
                            ["Training Status",self._model_management.get_training_status()],
                            ["Accuracy",self._model_management.get_model_accuracy()],
                            ["RunTime",self._model_management.get_training_time()],
                            ["Created On",self._model_management.get_creation_date()]

                                        ]

        modelManagementModelSettingsJson = [

                                  ["Training Dataset",self._model_management.get_datasetName()],
                                  ["Target Column",self._model_management.get_target_variable()],
                                  ["Target Column Value",self._model_management.get_target_level()],
                                  ["Number Of Independent Variables",self._model_management.get_no_of_independent_variables()],
                                  ["Algorithm",self._model_management.get_algorithm_name()],
                                  ["CacheNodeIds",self._model_management.get_cacheNodeIds()],
                                  ["Max Bins",self._model_management.get_max_bins()],
                                  ["Max Depth",self._model_management.get_max_depth()],
                                  ["Minimum Instances Per Node",self._model_management.get_min_instances_per_node()],
                                  ["Minimum Information Gain",self._model_management.get_min_info_gain()],
                                  ["Checkpoint Interval",self._model_management.get_checkpoint_interval()],
                                  ["Impurity",self._model_management.get_impurity()],
                                  ["Model Validation",self._model_management.get_validation_method()],]

        xgbOverviewCards = [json.loads(CommonUtils.convert_python_object_to_json(cardObj)) for cardObj in MLUtils.create_model_management_card_overview(self._model_management,modelManagementSummaryJson,modelManagementModelSettingsJson)]
        xgbPerformanceCards = [json.loads(CommonUtils.convert_python_object_to_json(cardObj)) for cardObj in MLUtils.create_model_management_cards(self._model_summary, endgame_roc_df)]
        xgbDeploymentCards = [json.loads(CommonUtils.convert_python_object_to_json(cardObj)) for cardObj in MLUtils.create_model_management_deploy_empty_card()]
        xgbCards = [json.loads(CommonUtils.convert_python_object_to_json(cardObj)) for cardObj in MLUtils.create_model_summary_cards(self._model_summary)]
        XGB_Overview_Node = NarrativesTree()
        XGB_Overview_Node.set_name("Overview")
        XGB_Performance_Node = NarrativesTree()
        XGB_Performance_Node.set_name("Performance")
        XGB_Deployment_Node = NarrativesTree()
        XGB_Deployment_Node.set_name("Deployment")
        for card in xgbOverviewCards:
            XGB_Overview_Node.add_a_card(card)
        for card in xgbPerformanceCards:
            XGB_Performance_Node.add_a_card(card)
        for card in xgbDeploymentCards:
            XGB_Deployment_Node.add_a_card(card)
        for card in xgbCards:
            self._prediction_narrative.add_a_card(card)

        self._result_setter.set_model_summary({"xgboost":json.loads(CommonUtils.convert_python_object_to_json(self._model_summary))})
        self._result_setter.set_xgboost_model_summary(modelSummaryJson)
        # self._result_setter.set_xgboost_management_summary(modelManagementJson)
        self._result_setter.set_xgb_cards(xgbCards)
        self._result_setter.set_xgb_nodes([XGB_Overview_Node,XGB_Performance_Node,XGB_Deployment_Node])
        self._result_setter.set_xgb_fail_card({"Algorithm_Name":"xgboost","success":"True"})

        CommonUtils.create_update_and_save_progress_message(self._dataframe_context,self._scriptWeightDict,self._scriptStages,self._slug,"completion","info",display=True,emptyBin=False,customMsg=None,weightKey="total")
