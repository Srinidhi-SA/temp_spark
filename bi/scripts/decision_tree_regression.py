
import json

from bi.common import utils
from bi.common import DataWriter
from bi.common import BIException
from bi.algorithms import DecisionTreeRegression
from bi.narratives.decisiontree import DecisionNarrative
from bi.narratives.decisiontree.decision_tree import DecisionTreeNarrative

class DecisionTreeRegressionScript:
    def __init__(self, data_frame, df_helper,df_context, spark):
        self._data_frame = data_frame
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context
        self._spark = spark

    def Run(self):

        df_decision_tree_obj = DecisionTreeRegression(self._data_frame, self._dataframe_helper, self._spark).test_all(measure_columns=(self._dataframe_context.get_result_column(),))
        df_decision_tree_result = utils.as_dict(df_decision_tree_obj)

        # print 'RESULT: %s' % (json.dumps(df_decision_tree_result, indent=2))
        df_decision_tree_result['tree']["children"] = json.dumps(df_decision_tree_result['tree']["children"])
        DataWriter.write_dict_as_json(self._spark, df_decision_tree_result, self._dataframe_context.get_result_file()+'DecisionTreeReg/')

        #Narratives
        narratives_obj = DecisionTreeNarrative(self._dataframe_context.get_result_column(), df_decision_tree_obj, self._dataframe_helper)
        narratives = utils.as_dict(narratives_obj)
        # print "Narratives: %s" % (json.dumps(narratives, indent=2))
        DataWriter.write_dict_as_json(self._spark, narratives, self._dataframe_context.get_narratives_file()+'DecisionTreeReg/')