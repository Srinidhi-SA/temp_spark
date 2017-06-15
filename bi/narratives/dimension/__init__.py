import os
import jinja2
import re

from bi.common.utils import accepts
from bi.common.results.frequency_dimensions import FreqDimensionResult

from collections import OrderedDict
from dimension_column import DimensionColumnNarrative


class DimensionNarrative:

    @accepts(object, (int, long), FreqDimensionResult)
    def __init__(self, num_measure_columns, df_freq_dimension_obj):
        self._df_regression_result = df_freq_dimension_obj
        self._num_measure_columns = num_measure_columns
        self._dataframe_context = context

        self.title = None
        self.summary = None
        # self._base_dir = os.path.dirname(os.path.realpath(__file__))+"/../../templates/dimensions/"
        self._base_dir = os.environ.get('MADVISOR_BI_HOME')+"/templates/dimensions/"

    #     self._generate_narratives()
    #
    # def _generate_narratives(self):
    #     for measure_column in self._df_regression_result.get_measures():
    #         dimension_narrative = LinearRegressionNarrative(
    #                                     self._num_measure_columns,
    #                                     self._df_regression_result.get_regression_result(measure_column),
    #                                     self._correlations.get_correlation_stats(measure_column))
    #         self.narratives[measure_column] = dimension_narrative


# __all__ = [
#     'LinearRegressionNarrative',
#     'RegressionNarrative'
# ]
