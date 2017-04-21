from pyspark.sql import functions as FN
from exception import BIException
from decorators import accepts
from column import ColumnType
from pyspark.sql.functions import udf,col,unix_timestamp
from pyspark.sql.types import StringType
from pyspark.sql.types import DateType
from bi.common.datafilterer import DataFrameFilterer
import pandas as pd

class DataFilterHelper:
    def __init__(self, data_frame, df_context):
        self._data_frame = data_frame
        self._df_context = df_context

    def set_params(self):
        self.subset_columns = self._df_context.get_column_subset()
        if not self.subset_columns==None:
            self._data_frame = self.subset_data_frame(self.subset_columns)
        self.df_filterer = DataFrameFilterer(self._data_frame)
        self.dimension_filter = self._df_context.get_dimension_filters()
        if not self.dimension_filter==None:
            for colmn in self.dimension_filter.keys():
                self.df_filterer.values_in(colmn, self.dimension_filter[colmn])
        self.measure_filter = self._df_context.get_measure_filters()
        if not self.measure_filter==None:
            for colmn in self.measure_filter.keys():
                self.df_filterer.values_between(colmn, self.measure_filter[colmn][0],self.measure_filter[colmn][1],1,1)

        self._data_frame = self.df_filterer.get_filtered_data_frame()

    def get_data_frame(self):
        return self._data_frame

    def subset_data_frame(self, columns):
        return self._data_frame.select(*columns)
