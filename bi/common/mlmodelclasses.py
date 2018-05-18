import time
import pandas as pd
from sklearn import metrics
from math import sqrt
from sklearn.externals import joblib
from bi.settings import setting as GLOBALSETTINGS
from bi.common import utils as CommonUtils



class ModelSummary:
    """
    modelJsonOutput = {
                        "model_summary":modelResult,
                        "model_dropdown":[
                                    {"name":"Random Forest","accuracy":89,"slug":"djksjkdsjdsk12NN2156"},
                                    {"name":"Logistic Regression","accuracy":86,"slug":"djk18jjsjdsk12NN2156"},
                                    {"name":"Xgboost","accuracy":80,"slug":"djkjkd77661sk12NN2156"}
                        ],
                        "config":{
                            "target_variable":[None],
                            "targetVariableLevelcount":[],
                            "modelFeatures":{
                                "slug1":[],
                                "slug2":[],
                                "slug3":[],
                            }
                        }
                    }
    """
    def __init__(self, model_summary=None, model_dropdown=None, modelConfig=None, modelHyperparameter=None):
        if model_summary is None:
            model_summary = {}
        if model_dropdown is None:
            model_dropdown = []
        if modelConfig is None:
            modelConfig = {}
        self.model_summary = model_summary
        self.model_dropdown = model_dropdown
        self.config = modelConfig
        self.model_hyperparameter_summary = modelHyperparameter

    def set_model_summary(self,data):
        self.model_summary = data
    def get_model_summary(self):
        return self.model_summary
    def set_model_dropdown(self,data):
        self.model_dropdown = data
    def get_model_dropdown(self):
        return self.model_dropdown
    def set_model_config(self,data):
        self.config = data
    def get_model_config(self):
        return self.config
    def get_model_hyperparameter_summary(self):
        return self.model_hyperparameter_summary
    def set_model_hyperparameter_summary(self,data):
        self.model_hyperparameter_summary = data
    def get_json_data(self):
        output =  {
                "model_summary":self.model_summary,
                "model_dropdown":self.model_dropdown,
                "config":self.config,
                "model_hyperparameter":self.model_hyperparameter_summary
                }
        return output

class MLModelSummary:
    def __init__(self):
        self.confusionMatrix = None
        self.featureImportance = None
        self.featureList = None
        self.trainingTime = None
        self.precisionRecallStats = None
        self.modelAccuracy = None
        self.modelPrecision = None
        self.modelRecall = None
        self.targetVariable = None
        self.predictionSplit = None
        self.algorithmName = None
        self.algorithmDisplayName = None
        self.validationMethod = None
        self.modelFeatures = None
        self.levelCounts = None
        self.nTrees = None
        self.nRules = None
        self.slug = None
        self.levelMap = None
        self.modelParams = None
        self.modelEvaluationMetrics = None
        self.modelType = None #can be "regression", or "classification"
        self.quantileSummary = None
        self.mapeStats = None
        self.sampleData = None
        self.coefficinetsArray = []
        self.interceptValue = None

    def set_intercept(self,data):
        self.interceptValue = data
    def get_intercept(self):
        return self.interceptValue
    def set_coefficinets_array(self,data):
        self.coefficinetsArray = data
    def get_coefficinets_array(self):
        return self.coefficinetsArray
    def set_sample_data(self,data):
        self.sampleData = data
    def get_sample_data(self):
        return self.sampleData
    def set_mape_stats(self,data):
        self.mapeStats = data
    def get_mape_stats(self):
        return self.mapeStats
    def set_quantile_summary(self,data):
        self.quantileSummary = data
    def get_quantile_summary(self):
        return self.quantileSummary
    def set_model_type(self,data):
        self.modelType = data

    def get_model_type(self):
        return self.modelType

    def set_model_evaluation_metrics(self,data):
        self.modelEvaluationMetrics = data

    def get_model_evaluation_metrics(self):
        return self.modelEvaluationMetrics

    def set_model_params(self,data):
        self.modelParams = data

    def get_model_params(self):
        return self.modelParams

    def set_level_map_dict(self,data):
        self.levelMap = data

    def get_level_map_dict(self):
        return self.levelMap

    def set_confusion_matrix(self,data):
        self.confusionMatrix = data

    def set_feature_importance(self,data):
        self.featureImportance = data

    def set_feature_list(self,data):
        self.featureList = data

    def set_training_time(self,data):
        self.trainingTime = data

    def set_precision_recall_stats(self,data):
        self.precisionRecallStats = data

    def set_model_accuracy(self,data):
        self.modelAccuracy = data

    def set_model_precision(self,data):
        self.modelPrecision = data

    def set_model_recall(self,data):
        self.modelRecall = data

    def set_target_variable(self,data):
        self.targetVariable = data

    def set_prediction_split(self,data):
        self.predictionSplit = data

    def set_algorithm_name(self,data):
        self.algorithmName = data

    def set_algorithm_display_name(self,data):
        self.algorithmDisplayName = data

    def set_validation_method(self,data):
        self.validationMethod = data

    def set_model_features(self,data):
        self.modelFeatures = data

    def set_level_counts(self,data):
        self.levelCounts = data

    def set_num_trees(self,data):
        self.nTrees = data

    def set_num_rules(self,data):
        self.nRules = data

    def set_slug(self,data):
        self.slug = data

    def get_confusion_matrix(self):
        return self.confusionMatrix

    def get_feature_importance(self):
        return self.featureImportance

    def get_feature_list(self):
        return self.featureList

    def get_training_time(self):
        return self.trainingTime

    def get_precision_recall_stats(self):
        return self.precisionRecallStats

    def get_model_accuracy(self):
        return self.modelAccuracy

    def get_model_precision(self):
        return self.modelPrecision

    def get_model_recall(self):
        return self.modelRecall

    def get_target_variable(self):
        return self.targetVariable

    def get_prediction_split(self):
        return self.predictionSplit

    def get_algorithm_name(self):
        return self.algorithmName

    def get_algorithm_display_name(self):
        return self.algorithmDisplayName

    def get_validation_method(self):
        return self.validationMethod

    def get_model_features(self):
        return self.modelFeatures

    def get_level_counts(self):
        return self.levelCounts

    def get_num_trees(self):
        return self.nTrees

    def get_num_rules(self):
        return self.nRules

    def get_slug(self):
        return self.slug


class MLModelMetaData:
    """
    This module contains Meta Data for a corresponding ML Model
    """
    def __init__(self):
        self.algorithmName = None
        self.modelType = None                   #ensemble or single model
        self.trainingTime = None
        self.packageUsed = None
        self.packageVersion = None


class ParamsGrid:
    """

    """

class SklearnGridSearchResult:
    def __init__(self,resultDict = {},estimator=None,x_train=None,x_test=None,y_train=None,y_test=None,appType=None,modelFilepath = None,levels=None,posLabel=None):
        self.resultDict = resultDict
        self.estimator = estimator
        self.appType = appType
        self.x_train = x_train
        self.x_test = x_test
        self.y_train = y_train
        self.y_test = y_test
        self.posLabel = posLabel
        self.levels = levels
        self.modelFilepath = modelFilepath
        if self.resultDict != {}:
            self.resultDf = pd.DataFrame(self.resultDict)
        else:
            self.resultDf = None
        self.ignoreList = ["Model Id","Precision","Recall","ROC-AUC","RMSE","MAE","MSE","R-Squared","Slug","Selected","Run Time","comparisonMetricUsed","algorithmName","alwaysSelected"]
        self.hideFromTable = ["Selected","alwaysSelected","Slug","comparisonMetricUsed","algorithmName"]
        self.metricColName = "comparisonMetricUsed"
        self.keepColumns = ["Model Id"]

    def get_ignore_list(self):
        return self.ignoreList

    def get_hide_columns(self):
        return self.hideFromTable

    def get_comparison_metric_colname(self):
        return self.metricColName

    def get_keep_columns(self):
        return self.keepColumns

    def train_and_save_models(self):
        tableOutput = []
        evaluationMetric = None
        for idx,paramsObj in enumerate(self.resultDf["params"]):
            st = time.time()
            estimator = self.estimator.set_params(**paramsObj)
            estimator.fit(self.x_train, self.y_train)
            y_score = estimator.predict(self.x_test)
            modelName = "M"+"0"*(GLOBALSETTINGS.MODEL_NAME_MAX_LENGTH-len(str(idx+1)))+str(idx+1)
            slug = self.modelFilepath.split("/")[-1]
            algoName = GLOBALSETTINGS.SLUG_MODEL_DISPLAY_NAME_MAPPING[slug]
            joblib.dump(estimator,self.modelFilepath+"/"+modelName+".pkl")
            row = {"Model Id":modelName,"Slug":slug,"Selected":"False","alwaysSelected":"False","Run Time":CommonUtils.round_sig(time.time()-st),"comparisonMetricUsed":None,"algorithmName":algoName}
            # row = {"Model Id":modelName,"Slug":slug,"Selected":"False","Run Time":str(CommonUtils.round_sig(time.time()-st))}
            evaluationMetrics = {}
            if self.appType == "REGRESSION":
                evaluationMetrics["R-Squared"] = metrics.r2_score(self.y_test, y_score)
                evaluationMetrics["MSE"] = metrics.mean_squared_error(self.y_test, y_score)
                evaluationMetrics["MAE"] = metrics.mean_absolute_error(self.y_test, y_score)
                evaluationMetrics["RMSE"] = sqrt(evaluationMetrics["MSE"])
                row["comparisonMetricUsed"] = "R-Squared"
            elif self.appType == "CLASSIFICATION":
                evaluationMetrics["Accuracy"] = metrics.accuracy_score(self.y_test,y_score)
                if len(self.levels) <= 2:
                    evaluationMetrics["Precision"] = metrics.precision_score(self.y_test,y_score,pos_label=self.posLabel,average="binary")
                    evaluationMetrics["Recall"] = metrics.recall_score(self.y_test,y_score,pos_label=self.posLabel,average="binary")
                    evaluationMetrics["ROC-AUC"] = metrics.roc_auc_score(self.y_test,y_score)
                    row["comparisonMetricUsed"] = "ROC-AUC"
                elif len(self.levels) > 2:
                    evaluationMetrics["Precision"] = metrics.precision_score(self.y_test,y_score,pos_label=self.posLabel,average="macro")
                    evaluationMetrics["Recall"] = metrics.recall_score(self.y_test,y_score,pos_label=self.posLabel,average="macro")
                    evaluationMetrics["ROC-AUC"] = None
                    row["comparisonMetricUsed"] = "Accuracy"


            evaluationMetrics = {k:CommonUtils.round_sig(v) for k,v in evaluationMetrics.items()}
            # evaluationMetrics = {k:str(CommonUtils.round_sig(v)) for k,v in evaluationMetrics.items()}
            row.update(evaluationMetrics)
            paramsObj = dict([(k,str(v)) if (v == None) | (v in [True,False]) else (k,v) for k,v in paramsObj.items()])
            row.update(paramsObj)
            self.keepColumns += paramsObj.keys()
            tableOutput.append(row)
        if self.appType == "REGRESSION":
            self.keepColumns += ["RMSE","MAE","MSE","R-Squared"]
            tableOutput = sorted(tableOutput,key=lambda x:float(x[tableOutput[0]["comparisonMetricUsed"]]),reverse=True)
        elif self.appType == "CLASSIFICATION":
            tableOutput = sorted(tableOutput,key=lambda x:float(x[tableOutput[0]["comparisonMetricUsed"]]),reverse=True)
            self.keepColumns += ["Precision","Recall","ROC-AUC"]
        self.keepColumns += paramsObj.keys()
        self.keepColumns.append("Selected")
        bestMod = tableOutput[0]
        bestMod["Selected"] = "True"
        bestMod["alwaysSelected"] = "True"
        tableOutput[0] = bestMod
        return tableOutput
