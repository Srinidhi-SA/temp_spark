import json
from bi.algorithms import DecisionTrees
from bi.common import DataWriter
from bi.common import utils as CommonUtils
from bi.narratives.decisiontree.decision_tree import DecisionTreeNarrative


class DecisionTreeScript:
    def __init__(self, data_frame, df_helper,df_context, spark, story_narrative,result_setter,meta_parser):
        self._story_narrative = story_narrative
        self._result_setter = result_setter
        self._data_frame = data_frame
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context
        self._spark = spark
        self._metaParser = meta_parser

    def Run(self):

        df_decision_tree_obj = DecisionTrees(self._data_frame, self._dataframe_helper, self._dataframe_context, self._spark,self._metaParser).test_all(dimension_columns=(self._dataframe_context.get_result_column(),))

        # print 'RESULT: %s' % (json.dumps(df_decision_tree_result, indent=2))
        # df_decision_tree_result['tree']["children"] = json.dumps(df_decision_tree_result['tree']["children"])
        # DataWriter.write_dict_as_json(self._spark, df_decision_tree_result, self._dataframe_context.get_result_file()+'DecisionTree/')

        #Narratives
        narratives_obj = DecisionTreeNarrative(self._dataframe_context.get_result_column(), df_decision_tree_obj, self._dataframe_helper, self._dataframe_context,self._metaParser,self._result_setter,self._story_narrative)
        # narratives = CommonUtils.as_dict(narratives_obj)

        # print "Narratives: %s" % (json.dumps(narratives, indent=2))
        # DataWriter.write_dict_as_json(self._spark, narratives, self._dataframe_context.get_narratives_file()+'DecisionTree/')
