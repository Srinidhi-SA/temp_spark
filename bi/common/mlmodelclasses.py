from decorators import accepts
from exception import BIException

class MLModelSummary:
    def __init__(self):
        self.confusionMatrix = None
        self.featureImportance = None
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

    def set_confusion_matrix(self,data):
        self.confusionMatrix = data

    def set_feature_importance(self,data):
        self.featureImportance = data

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

    def __init__():
        self.algorithmName = None
        self.modelType = None                   #ensemble or single model
        self.trainingTime = None
        self.packageUsed = None
        self.packageVersion = None
