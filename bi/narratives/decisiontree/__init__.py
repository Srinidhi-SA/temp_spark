import os

from bi.common.results.decision_tree import DecisionTreeResult
from bi.common.utils import accepts
from decision_tree import DecisionTreeNarrative


class DecisionNarrative:

    @accepts(object, (int, long), DecisionTreeResult)
    def __init__(self, num_measure_columns, decision_tree_rules):
        self._df_regression_result = df_freq_dimension_obj
        self._num_measure_columns = num_measure_columns
        self._dataframe_context = context

        self.title = None
        self.summary = None
        self._base_dir = self._dataframe_context.get_base_directory()+"/templates/decisiontree/"
