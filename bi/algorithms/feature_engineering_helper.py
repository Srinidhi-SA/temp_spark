import datetime
import math
from operator import mul
#from itertools import chain
from pyspark.sql.functions import avg, mean, stddev, when, create_map, udf, lower
from pyspark.sql.functions import to_timestamp, hour, minute, year, month, dayofmonth, dayofyear, unix_timestamp
from pyspark.sql.functions import weekofyear, from_unixtime, datediff, date_format
from pyspark.sql.functions import col, floor, concat, lit, concat_ws
from pyspark.sql.types import IntegerType, StringType, DateType
from pyspark.sql import SparkSession, Row
from pyspark.sql import functions as F
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, OneHotEncoder
#from pyspark.sql.functions import mean as _mean, stddev as _stddev, col
#from pyspark.sql.functions import *


class FeatureEngineeringHelper:
    """Contains Feature Engineering Operation Functions"""


    def __init__(self, df):
        self._data_frame = df


    def binning_all_measures(self):
        pass


    def create_new_levels_dimension(self):
        pass


    def create_new_levels_datetimes(self):
        pass


    def create_equal_sized_measure_bins(self):
        pass

    def create_custom_measure_bins(self):
        pass


    def replace_values_in_column(self, column_name, range, value):
        if len(range) == 2:
            self._data_frame = self._data_frame.withColumn(column_name, when(((self._data_frame[column_name] >= range[0]) & (self._data_frame[column_name] <= range[1])), value).otherwise(self._data_frame[column_name]))
        else:
            self._data_frame = self._data_frame.withColumn(column_name, when(self._data_frame[column_name] == range[0], value).otherwise(self._data_frame[column_name]))
        return self._data_frame


    def standardize_column_helper(mean,sd):
        return udf(lambda x: (x-mean)/sd)


    def standardize_column(self, column_name):
        mean = self._data_frame.select(F.mean(column_name)).collect()[0][0]
        StdDev = self._data_frame.select(F.stddev_samp(column_name)).collect()[0][0]
        self._data_frame = self._data_frame.withColumn(column_name + "_standardized", standardize_column_helper(mean,StdDev)(col(column_name)))
        return self._data_frame


    def replacerUDF(value, operation):
        if operation == "prod":
            return udf(lambda x: x*value)
        if operation == "add":
            return udf(lambda x: x+value)
        if operation == "subs":
            return udf(lambda x: x - value)
        if operation == "divide":
            return udf(lambda x: x/value)
        if operation == "Reciprocal":
            return udf(lambda x: 1/x)
        if operation == "NthRoot":
            return udf(lambda x: x**(1.0/value))
        if operation == "exponential":
            return udf(lambda x: x**value)
        if operation == "logTransform":
            return udf(lambda x: math.log(x, 10))
        if operation == "modulus":
            return udf(lambda x: abs(x))


    def logTransform_column(self, column_name):
        self._data_frame = self._data_frame.withColumn(column_name + "_log-transformed", replacerUDF(10, "logTransform")(col(column_name)))
        return self._data_frame


    def label_encoding_column(self, column_name):
        indexers = [StringIndexer(inputCol=column_name, outputCol=column_name+"_labelled").fit(self._data_frame)]
        pipeline = Pipeline(stages=indexers)
        self._data_frame = pipeline.fit(self._data_frame).transform(self._data_frame)
        return self._data_frame


    def character_count_string_helper():
        return udf(lambda x:x.count("")-1)


    def character_count_string(self, column_name):
        self._data_frame = self._data_frame.withColumn(column_name+"_character_count", character_count_string_helper()(col(column_name)))
        return self._data_frame


    def contains_word_helper(word):
        return udf(lambda x:False if x.lower().find(word) == -1 else True)


    def contains_word(self, column_name, word):
        word = word.lower()
        self._data_frame = self._data_frame.withColumn(column_name+"_contains_"+word, contains_word_helper(word)(col(column_name)))
        return self._data_frame


    '''Given that all datetime columns follow same string format == "dd/MM/yyyy" for date'''
    def convert_to_timestamp(self, datetime_col, timeformat):
        timestamped = datetime_col + "_timestamped"
        self._data_frame = self._data_frame.withColumn(timestamped, to_timestamp(self._data_frame[datetime_col], timeformat).alias(datetime_col))
        return self._data_frame


    def count_time_since(self, col_for_time_since, time_since_date, timeformat):
        '''Columns to be passed for calculating duration need to be in TimeStamped format'''
        '''time_since_date should be in dd/MM/yyyy format'''
        self._data_frame = self._data_frame.withColumn("TIME_SINCE_DATE", F.lit(time_since_date))
        self._data_frame = self._data_frame.withColumn("TIME_SINCE_DATE(Timestamped)", to_timestamp(self._data_frame["TIME_SINCE_DATE"], timeformat))
        self._data_frame = self._data_frame.withColumn("TIME_SINCE", datediff(self._data_frame[col_for_time_since], self._data_frame["TIME_SINCE_DATE(Timestamped)"]))
        self._data_frame = self._data_frame.drop("TIME_SINCE_DATE", "TIME_SINCE_DATE(Timestamped)")
        return self._data_frame

#TODO - Check for timestamp conversion related issues if any


    def extract_datetime_info(self, datetime_col, timeformat, info_to_extract):
        timestamped = datetime_col + "_timestamped"
        self._data_frame = self._data_frame.withColumn(datetime_col, to_timestamp(self._data_frame[datetime_col], timeformat).alias(datetime_col))
        if info_to_extract == "year":
            self._data_frame = self._data_frame.withColumn(datetime_col + "_year", year(to_timestamp(self._data_frame[datetime_col], timeformat).alias(datetime_col)))
        if info_to_extract == "month":
            self._data_frame = self._data_frame.withColumn(datetime_col + "_month", month(to_timestamp(self._data_frame[datetime_col], timeformat).alias(datetime_col)))
        if info_to_extract == "day_of_month":
            self._data_frame = self._data_frame.withColumn(datetime_col + "_day_of_month", dayofmonth(to_timestamp(self._data_frame[datetime_col], timeformat).alias(datetime_col)))
        if info_to_extract == "day_of_year":
            self._data_frame = self._data_frame.withColumn(datetime_col + "_day_of_year", dayofyear(to_timestamp(self._data_frame[datetime_col], timeformat).alias(datetime_col)))
        if info_to_extract == "day":
            self._data_frame = self._data_frame.withColumn(datetime_col, to_timestamp(self._data_frame[datetime_col], timeformat).alias(datetime_col))
            self._data_frame = self._data_frame.withColumn(datetime_col + "_day", date_format(datetime_col, 'E').alias(datetime_col))
        if info_to_extract == "week_of_year":
            self._data_frame = self._data_frame.withColumn(datetime_col + "_week_of_year", weekofyear(to_timestamp(self._data_frame[datetime_col], timeformat).alias(datetime_col)))
        if info_to_extract == "hour":
            self._data_frame = self._data_frame.withColumn(datetime_col + "_hour", hour(to_timestamp(self._data_frame[datetime_col], timeformat).alias(datetime_col)))
        if info_to_extract == "minute":
            self._data_frame = self._data_frame.withColumn(datetime_col + "_minute", minute(to_timestamp(self._data_frame[datetime_col], timeformat).alias(datetime_col)))
        if info_to_extract == "date":
            self._data_frame = self._data_frame.withColumn(datetime_col + "_date", to_timestamp(self._data_frame[datetime_col], timeformat).cast("date").alias(datetime_col))
        return self._data_frame


    def is_weekend_helper():
        return udf(lambda x:False if (int(x) < 6) else True)


    def is_weekend(self, datetime_col):
        self._data_frame = self._data_frame.withColumn(datetime_col, to_timestamp(self._data_frame[datetime_col], timeformat).alias(datetime_col))
        self._data_frame = self._data_frame.withColumn(datetime_col + "_day", date_format(datetime_col, 'u').alias(datetime_col))
        self._data_frame = self._data_frame.withColumn(datetime_col + "_is_weekend", is_weekend_helper()(col(datetime_col + "_day")))
        return df
