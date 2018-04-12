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
    def __init__(self, model_summary=None, model_dropdown=None, modelConfig=None):
        if model_summary is None:
            model_summary = {}
        if model_dropdown is None:
            model_dropdown = []
        if modelConfig is None:
            modelConfig = {}
        self.model_summary = model_summary
        self.model_dropdown = model_dropdown
        self.config = modelConfig

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
    def get_json_data(self):
        output =  {
                "model_summary":self.model_summary,
                "model_dropdown":self.model_dropdown,
                "config":self.config,
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
