
from bi.common import utils
from bi.transformations import Density_Binner
from bi.common import DataWriter


class Density_HistogramsScript:
    def __init__(self, data_frame, df_helper, df_context, spark):
        self._data_frame = data_frame
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context
        self._spark = spark

    def Run(self):
        binner = Density_Binner(self._data_frame, self._dataframe_helper)
        #histogram_data = utils.as_dict(binner.get_bins_for_all_measure_columns())
        histogram_data = utils.as_dict(binner.get_bins(self._dataframe_context.get_result_column()))
        print "%r" % histogram_data
        DataWriter.write_dict_as_json(self._spark, histogram_data, self._dataframe_context.get_result_file()+'Density_Histogram/')
