from pyspark.sql.dataframe import DataFrame
from pyspark.sql import functions as FN
from pyspark.sql.types import DateType
from pyspark.sql.types import TimestampType
from decorators import accepts
from datetime import datetime
from pyspark.sql.functions import col

from utils import accepts
#import bi.common.dataframe

class DataFrameFilterer:
    @accepts(object,DataFrame)
    def __init__(self, dataframe):
        self._data_frame = dataframe

    def values_between(self,colname,start_value, end_value, greater_than_equal = 0, less_than_equal=1):
        if (greater_than_equal == 0) and (less_than_equal==1):
            self._data_frame = self._data_frame.filter((col(colname) > start_value) & (col(colname) <= end_value))
        elif (greater_than_equal == 0) and (less_than_equal==0):
            self._data_frame = self._data_frame.filter((col(colname) > start_value) & (col(colname) < end_value))
        elif (greater_than_equal == 1) and (less_than_equal==1):
            self._data_frame = self._data_frame.filter((col(colname) >= start_value) & (col(colname) <= end_value))
        elif (greater_than_equal == 1) and (less_than_equal==0):
            self._data_frame = self._data_frame.filter((col(colname) >= start_value) & (col(colname) < end_value))

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
        if type(values) == str:
            values = values[1:-1]
            values = values.split(',')
        self._data_frame = self._data_frame.where(col(colname).isin(values))
        #print self._data_frame.take(10)
        #print '-'*90

    def values_not_in(self, colname, values):
        if type(values) == str:
            values = values[1:-1]
            values = values.split(',')
        self._data_frame = self._data_frame.where(col(colname).isin(values)==False)
        #print self._data_frame.take(10)
        #print '-'*90

    def get_aggregated_result(self, colname, target):
        return self._data_frame.select(colname).groupBy(colname).agg({'*': 'count'}).collect()

    def get_filtered_data_frame(self):
        return self._data_frame
