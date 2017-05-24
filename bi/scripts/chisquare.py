
import json
from functools import reduce

from bi.common import utils
from bi.common import DataLoader
from bi.common import DataWriter
from bi.common import DataFrameHelper
from bi.common import BIException
from bi.stats.chisquare import ChiSquare
from bi.narratives.chisquare import ChiSquareNarratives

class ChiSquareScript:
    def __init__(self, data_frame, df_helper, df_context, spark):
        self._data_frame = data_frame
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context
        self._spark = spark

    def Run(self):
        df_chisquare_obj = ChiSquare(self._data_frame, self._dataframe_helper, self._dataframe_context).test_all(dimension_columns=(self._dataframe_context.get_result_column(),))
        df_chisquare_result = utils.as_dict(df_chisquare_obj)
        # print 'RESULT: %s' % (json.dumps(df_chisquare_result, indent=2))
        DataWriter.write_dict_as_json(self._spark, df_chisquare_result, self._dataframe_context.get_result_file()+'ChiSquare/')

        # Narratives
        chisquare_narratives = utils.as_dict(ChiSquareNarratives(len(self._dataframe_helper.get_string_columns()), df_chisquare_obj, self._dataframe_context))
        # print 'Narrarives: %s' %(json.dumps(chisquare_narratives, indent=2))
        DataWriter.write_dict_as_json(self._spark, chisquare_narratives, self._dataframe_context.get_narratives_file()+'ChiSquare/')
