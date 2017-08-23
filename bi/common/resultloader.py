from bi.common import utils as CommonUtils
import json

class ResultSetter:
    """
    Provides helper method to store all the different result and narratives.
    """

    def __init__(self, data_frame, df_context):
        self._data_frame = data_frame
        self.executiveSummaryDataDict = {}
        self.trend_subsection_name = None
        self.trend_subsection_data = None
        self.trend_subsection_complete = False
        self.model_summary = {}
        self.distributionNode = None
        self.chisquareNode = None
        self.trendNode = None
        self.decisionTreeNode = None
        self.regressionNode = None
        self.anovaNode = None
        self.headNode = None
        self.randomForestModelSummary = None
        self.xgboostModelSummary = None
        self.logisticRegressionModelSummary = None
        self.rfcards = []
        self.lrcards = []
        self.xgbcards = []
        self.scorecard = None


    # def set_params(self):
    #     self.columns = [field.name for field in self._data_frame.schema.fields]
    #     self.ignorecolumns = self._df_context.get_ignore_column_suggestions()
    def set_score_card(self,data):
        self.scorecard = data
    def get_score_card(self):
        return self.scorecard
    def set_lr_cards(self,data):
        self.lrcards = data
    def set_rf_cards(self,data):
        self.rfcards = data
    def set_xgb_cards(self,data):
        self.xgbcards = data
    def get_all_algos_cards(self):
        return self.rfcards + self.lrcards + self.xgbcards

    def set_random_forest_model_summary(self,data):
        self.randomForestModelSummary = data
    def set_xgboost_model_summary(self,data):
        self.xgboostModelSummary = data
    def set_logistic_regression_model_summary(self,data):
        self.logisticRegressionModelSummary = data
    def get_random_forest_model_summary(self):
        return self.randomForestModelSummary
    def get_xgboost_model_summary(self):
        return self.xgboostModelSummary
    def get_logistic_regression_model_summary(self):
        return self.logisticRegressionModelSummary

    def set_head_node(self,node):
        self.headNode = json.loads(CommonUtils.convert_python_object_to_json(node))
    def set_trend_node(self,node):
        self.trendNode = json.loads(CommonUtils.convert_python_object_to_json(node))
    def set_chisquare_node(self,node):
        self.chisquareNode = json.loads(CommonUtils.convert_python_object_to_json(node))
    def set_distribution_node(self,node):
        self.distributionNode = json.loads(CommonUtils.convert_python_object_to_json(node))
    def set_decision_tree_node(self,node):
        self.decisionTreeNode = json.loads(CommonUtils.convert_python_object_to_json(node))
    def set_anova_node(self,node):
        self.anovaNode = json.loads(CommonUtils.convert_python_object_to_json(node))
    def set_regression_node(self,node):
        self.regressionNode = json.loads(CommonUtils.convert_python_object_to_json(node))
    def get_head_node(self):
        return self.headNode
    def get_trend_node(self):
        return self.trendNode
    def get_chisquare_node(self):
        return self.chisquareNode
    def get_distribution_node(self):
        return self.distributionNode
    def get_decision_tree_node(self):
        return self.decisionTreeNode
    def get_anova_node(self):
        return self.anovaNode
    def get_regression_node(self):
        return self.regressionNode

    def update_executive_summary_data(self,data_dict):
        if data_dict != None:
            self.executiveSummaryDataDict.update(data_dict)

    def get_executive_summary_data(self):
        return self.executiveSummaryDataDict

    def set_trend_section_name(self,name):
        self.trend_subsection_name = name

    def set_trend_section_completion_status(self,status):
        self.trend_subsection_complete = status

    def set_model_summary(self,data):
        """data will be a key value dictionary
        {"model_name":"model_summary"}
        """
        self.model_summary.update(data)


    def get_trend_section_name(self):
        return self.trend_subsection_name

    def set_trend_section_data(self,dataDict):
        self.trend_subsection_data = dataDict

    def get_trend_section_data(self):
        return self.trend_subsection_data

    def get_trend_section_completion_status(self):
        return self.trend_subsection_complete

    def get_model_summary(self):
        return self.model_summary
