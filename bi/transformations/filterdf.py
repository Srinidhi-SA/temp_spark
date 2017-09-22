from pyspark.ml.feature import Bucketizer
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import col
from pyspark.sql.types import DoubleType
from bi.common.utils import accepts
from bi.common import DataFilterHelper
#import bi.common.dataframe

class DataFrameFilterer:
    # @accepts(object,DataFrame,DataFrameHelper,ContextSetter)
    def __init__(self, dataframe, df_helper, df_context):
        self._data_frame = dataframe
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context

    def applyFilter(self):
        """
        here all the filter settings will come from the df_context
        """
        dimension_filters = self._dataframe_context.get_dimension_filters()
        measure_filters = self._dataframe_context.get_measure_filters()
        time_dimension_filters = self._dataframe_context.get_time_dimension_filters()

        if len(dimension_filters) > 0:
            for filter_dict in dimension_filters:
                if filter_dict["filterType"] == "valueIn":
                    self._data_frame = self.values_in(filter_dict["colname"],filter_dict["values"])
        if len(measure_filters) > 0:
            for filter_dict in measure_filters:
                if filter_dict["filterType"] == "valueRange":
                    self._data_frame = self.values_between(filter_dict["colname"],\
                                                           filter_dict["lowerBound"],\
                                                           filter_dict["upperBound"],\
                                                           greater_than_equal=1,\
                                                           less_than_equal =1)
        return self._data_frame

    def values_between(self,colname,start_value, end_value, greater_than_equal = 0, less_than_equal=1):
        if (greater_than_equal == 0) and (less_than_equal==1):
            self._data_frame = self._data_frame.filter(col(colname) > start_value).filter(col(colname) <= end_value)
        elif (greater_than_equal == 0) and (less_than_equal==0):
            self._data_frame = self._data_frame.filter(col(colname) > start_value).filter(col(colname) < end_value)
        elif (greater_than_equal == 1) and (less_than_equal==1):
            self._data_frame = self._data_frame.filter(col(colname) >= start_value).filter(col(colname) <= end_value)
        elif (greater_than_equal == 1) and (less_than_equal==0):
            self._data_frame = self._data_frame.filter(col(colname) >= start_value).filter(col(colname) < end_value)

    def dates_between(self,colname,start_value, end_value, greater_than_equal = 1, less_than_equal=1):
        if (greater_than_equal == 0) and (less_than_equal==1):
            self._data_frame = self._data_frame.filter(col(colname) > start_value and col(colname) <= end_value)
        elif (greater_than_equal == 0) and (less_than_equal==0):
            self._data_frame = self._data_frame.filter(col(colname) > start_value and col(colname) < end_value)
        elif (greater_than_equal == 1) and (less_than_equal==1):
            self._data_frame = self._data_frame.filter(col(colname) >= start_value and col(colname) <= end_value)
        elif (greater_than_equal == 1) and (less_than_equal==0):
            self._data_frame = self._data_frame.filter(col(colname) >= start_value and col(colname) < end_value)

    def values_above(self,colname, start_value, greater_than_equal=0):
        if greater_than_equal == 0:
            self._data_frame = self._data_frame.filter(col(colname) > start_value)
        elif greater_than_equal == 1:
            self._data_frame = self._data_frame.filter(col(colname) >= start_value)

    def values_below(self, colname, end_value, less_than_equal=1):
        if less_than_equal==0:
            self._data_frame = self._data_frame.filter(col(colname) < end_value)
        elif less_than_equal==1:
            self._data_frame = self._data_frame.filter(col(colname) <= end_value)

    def values_in(self, colname, values):
        self._data_frame = self._data_frame.where(col(colname).isin(values))

    def values_not_in(self, colname, values):
        self._data_frame = self._data_frame.where(col(colname).isin(values)==False)

    def get_aggregated_result(self, colname, target):
        return self._data_frame.select(colname).groupBy(colname).agg({'*': 'count'}).collect()

    def get_filtered_data_frame(self):
        return self._data_frame
