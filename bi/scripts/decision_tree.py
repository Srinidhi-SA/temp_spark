import json
from bi.algorithms import DecisionTrees
from bi.common import DataWriter
from bi.common import utils as CommonUtils
from bi.narratives.decisiontree.decision_tree import DecisionTreeNarrative


class DecisionTreeScript:
    def __init__(self, data_frame, df_helper,df_context, spark, story_narrative,result_setter):
        self._story_narrative = story_narrative
        self._result_setter = result_setter
        self._data_frame = data_frame
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context
        self._spark = spark

    def Run(self):

        self._completionStatus = 80
        self._analysisName = "decisionTree"
        self._messageURL = self._dataframe_context.get_message_url()
        self._scriptStages = {
            "initialization":{
                "summary":"Initialized the Decision Tree Script",
                "weight":0
                },
            "treegeneration":{
                "summary":"Decision tree generation finished",
                "weight":10
                },
            "summarygeneration":{
                "summary":"summary generation finished",
                "weight":10
                },
            "completion":{
                "summary":"decision tree  done",
                "weight":0
                },
            }
        self._completionStatus += self._scriptStages["initialization"]["weight"]
        progressMessage = CommonUtils.create_progress_message_object(self._analysisName,\
                                    "initialization",\
                                    "info",\
                                    self._scriptStages["initialization"]["summary"],\
                                    self._completionStatus,\
                                    self._completionStatus)
        CommonUtils.save_progress_message(self._messageURL,progressMessage)

        df_decision_tree_obj = DecisionTrees(self._data_frame, self._dataframe_helper, self._dataframe_context, self._spark).test_all(dimension_columns=(self._dataframe_context.get_result_column(),))
        df_decision_tree_result = CommonUtils.as_dict(df_decision_tree_obj)
        self._completionStatus += self._scriptStages["treegeneration"]["weight"]
        progressMessage = CommonUtils.create_progress_message_object(self._analysisName,\
                                    "treegeneration",\
                                    "info",\
                                    self._scriptStages["treegeneration"]["summary"],\
                                    self._completionStatus,\
                                    self._completionStatus)
        CommonUtils.save_progress_message(self._messageURL,progressMessage)
        # print 'RESULT: %s' % (json.dumps(df_decision_tree_result, indent=2))
        # df_decision_tree_result['tree']["children"] = json.dumps(df_decision_tree_result['tree']["children"])
        # DataWriter.write_dict_as_json(self._spark, df_decision_tree_result, self._dataframe_context.get_result_file()+'DecisionTree/')

        #Narratives
        narratives_obj = DecisionTreeNarrative(self._dataframe_context.get_result_column(), df_decision_tree_obj, self._dataframe_helper, self._story_narrative,self._result_setter)
        # narratives = CommonUtils.as_dict(narratives_obj)

        # print "Narratives: %s" % (json.dumps(narratives, indent=2))
        # DataWriter.write_dict_as_json(self._spark, narratives, self._dataframe_context.get_narratives_file()+'DecisionTree/')
        self._completionStatus += self._scriptStages["summarygeneration"]["weight"]
        progressMessage = CommonUtils.create_progress_message_object(self._analysisName,\
                                    "summarygeneration",\
                                    "info",\
                                    self._scriptStages["summarygeneration"]["summary"],\
                                    self._completionStatus,\
                                    self._completionStatus)
        CommonUtils.save_progress_message(self._messageURL,progressMessage)
        self._completionStatus += self._scriptStages["completion"]["weight"]
        progressMessage = CommonUtils.create_progress_message_object(self._analysisName,\
                                    "completion",\
                                    "info",\
                                    self._scriptStages["completion"]["summary"],\
                                    self._completionStatus,\
                                    self._completionStatus)
        CommonUtils.save_progress_message(self._messageURL,progressMessage)
