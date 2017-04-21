
from pyspark.sql import functions as FN

from bi.common.decorators import accepts
from bi.common import BIException
from bi.common.results import FreqDimensionResult
import collections

import json
import pandas as pd

"""
Count Frequency in a Dimension
"""


class FreqDimensions:

    def __init__(self, data_frame, df_helper, df_context):
        self._data_frame = data_frame
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context

    @accepts(object, measure_columns=(list, tuple), dimension_columns=(list, tuple))
    def test_all(self, measure_columns=None, dimension_columns=None):
        freq_dimension_result = FreqDimensionResult()
        dimension = dimension_columns[0]
        frequency_dict = {}
        grouped_dataframe = self._data_frame.groupby(dimension).count().toPandas()
        frequency_dict[dimension] = grouped_dataframe.to_dict()
        grouped_dataframe = grouped_dataframe.dropna()
        frequency_dict = json.dumps(frequency_dict)
        freq_dimension_result.set_params(frequency_dict)
        return freq_dimension_result
