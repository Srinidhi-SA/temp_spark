import math
from datetime import datetime
from pyspark.sql.functions import avg, mean, stddev, when, create_map, udf, lower
from pyspark.sql.functions import to_timestamp, hour, minute, year, month, dayofmonth, dayofyear, unix_timestamp
from pyspark.sql.functions import weekofyear, from_unixtime, datediff, date_format
from pyspark.sql.functions import col, floor, concat, lit, concat_ws
from pyspark.sql.types import IntegerType, StringType, DateType
from pyspark.sql import SparkSession, Row
from pyspark.sql import functions as F
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, OneHotEncoder, Bucketizer
from scipy import linspace
#from pyspark.sql.functions import mean as _mean, stddev as _stddev, col
#from pyspark.sql.functions import *
from bi.common.column import ColumnType

from data_preprocessing_helper import DataPreprocessingHelper


class FeatureEngineeringHelper:
    """Contains Feature Engineering Operation Functions"""


    def __init__(self, df):
        self._data_frame = df
        # self._dataframe_helper = dataframe_helper

    def binning_all_measures(self,number_of_bins):
        dfSchemaFields = self._data_frame.schema.fields
        numeric_columns = []
        for field in dfSchemaFields:
            if ColumnType(type(field.dataType)).get_abstract_data_type() == ColumnType.MEASURE:
                numeric_columns.append(field.name)
        for column_name in numeric_columns:
            self._data_frame = self.create_equal_sized_measure_bins(column_name,number_of_bins)
        return self._data_frame


    def create_bin_udf(self,dict):
          def check_key(x, dict):
              for key in dict.keys():
                  if (x >= dict[key][0] and x <= dict[key][1]):
                      return key
          return udf(lambda x: check_key(x,dict))



    # def binning_all_measures_sumeet(self, n_bins):
    #     dfSchemaFields = self._data_frame.schema.fields
    #     numeric_columns = []
    #     for field in dfSchemaFields:
    #         if ColumnType(type(field.dataType)).get_abstract_data_type() == ColumnType.MEASURE:
    #             numeric_columns.append(field.name)
    #     for column_name in numeric_columns:
    #         col_min = self._data_frame.select(F.min(column_name)).collect()[0][0]
    #         col_max = self._data_frame.select(F.max(column_name)).collect()[0][0]
    #         bins_unrounded = linspace(col_min, col_max, n_bins + 1)
    #
    #         bins = []
    #         bins.insert(0, col_min)
    #         for val in bins_unrounded[1:n_bins]:
    #             bins.append(round(val, 2))
    #         bins.append(col_max)
    #
    #         bucketizer = Bucketizer(splits = bins, inputCol = column_name, outputCol = column_name + "_binned")
    #         self._data_frame = bucketizer.transform(self._data_frame)
    #
    #         keys = []
    #         lists = []
    #         for val in range(0, n_bins):
    #             keys.append(str(bins[val]) + "-" + str(bins[val + 1]))
    #             list = []
    #             list.append(bins[val])
    #             list.append(bins[val + 1])
    #             lists.append(list)
    #
    #         dict = {}
    #         for i in range(0, n_bins):
    #             dict[keys[i]] = lists[i]
    #
    #         map_list = [x for x in range(n_bins)]
    #         dict_new = {}
    #         for n in range(0, n_bins):
    #             dict_new[map_list[n]] = keys[n]
    #
    #         def create_level_udf_sumeet(dict):
    #             def check_key(x, dict):
    #                 for key in dict.keys():
    #                     if x == key:
    #                         return dict[key]
    #             return udf(lambda x: check_key(x,dict))
    #
    #         self._data_frame = self._data_frame.withColumn(column_name + "_binned", create_level_udf_sumeet(dict_new)(col(column_name + "_binned")))
    #     return self._data_frame


    def create_level_udf(self, dict):
        def check_key(x, dict):
            for key in dict.keys():
                if x in dict[key]:
                    return key
        return udf(lambda x: check_key(x,dict))

    def create_new_levels_dimension(self, column_name, dict):
        self._data_frame = self._data_frame.withColumn(column_name+"_level", self.create_level_udf(dict)(col(column_name)))
        return self._data_frame

    def create_level_udf_time(self, dict):
        def convert_to_date( value):
            value = datetime.strptime(value, "%d/%m/%Y")
            return value
        def check_key(date, dict):
            date = convert_to_date(date)
            for key, value in dict.items():
                val1_date = convert_to_date(value[0])
                val2_date = convert_to_date(value[1])
                date_range = [val1_date, val2_date]
                if (date >= date_range[0] and date <= date_range[1]):
                    return key
        return udf(lambda x: check_key(x, dict))


    def create_new_levels_datetimes(self, col_for_timelevels, dict):
        self._data_frame = self._data_frame.withColumn(col_for_timelevels+"_t_level", self.create_level_udf_time(dict)(col(col_for_timelevels)))
        return self._data_frame

    def create_bin_udf(self,dict):
        def check_key(x, dict):
            for key in dict.keys():
                if (x >= dict[key][0] and x <= dict[key][1]):
                    return key
        return udf(lambda x: check_key(x,dict))


    def create_equal_sized_measure_bins(self, column_name,number_of_bins):
        def create_dict_for_bin():
            min_max = self._data_frame.agg(F.min(column_name).alias('min'), F.max(column_name).alias('max')).collect()
            min_value = min_max[0]['min']
            max_value = min_max[0]['max']
            interval_size = ((max_value - min_value)*1.0/(number_of_bins-1))
            dict = {}
            temp = min_value
            while temp <=max_value:
                dict[str(temp)+"-"+str(temp+interval_size)] = [temp, temp+interval_size]
                temp = temp+interval_size
            return dict
        dict = create_dict_for_bin()
        self._data_frame = self._data_frame.withColumn(column_name+"_bin", self.create_bin_udf(dict)(col(column_name)))
        return self._data_frame


    def create_custom_measure_bins(self,column_name,list_of_intervals):
        def create_dict_for_bin():
            min_max = self._data_frame.agg(F.min(column_name).alias('min'), F.max(column_name).alias('max')).collect()
            min_value = min_max[0]['min']
            max_value = min_max[0]['max']
            dict = {}
            if list_of_intervals[0]>min_value:
                dict[str(min_value)+"-"+str(list_of_intervals[0])] = [min_value, list_of_intervals[0]]
            for i in range(len(list_of_intervals)):
                if i+2<=len(list_of_intervals):
                    dict[str(list_of_intervals[i])+"-"+str(list_of_intervals[i+1])] = [list_of_intervals[i], list_of_intervals[i+1]]
            if list_of_intervals[-1]<max_value:
                dict[str(list_of_intervals[-1])+"-"+str(max_value)] = [list_of_intervals[-1], max_value]

            return dict
        dict = create_dict_for_bin()
        self._data_frame = self._data_frame.withColumn(column_name+"_c_bin", self.create_bin_udf(dict)(col(column_name)))
        return self._data_frame


    '''To be verified'''
    def replace_values_in_column(self, column_name, range, value):
        if False:
            if value == "median":
                dp_helper_obj = DataPreprocessingHelper(self._data_frame)
                median_val = dp_helper_obj.get_median(column_name)
                replace_value = median_val
                self._data_frame = self._data_frame.withColumn(column_name, when(((self._data_frame[column_name] >= range[0]) & (self._data_frame[column_name] <= range[1])), replace_value).otherwise(self._data_frame[column_name]))
            if value == "mode":
                dp_helper_obj = DataPreprocessingHelper(self._data_frame)
                mode_val = dp_helper_obj.get_mode(column_name)
                replace_value = mode_val
                self._data_frame = self._data_frame.withColumn(column_name, when(((self._data_frame[column_name] >= range[0]) & (self._data_frame[column_name] <= range[1])), replace_value).otherwise(self._data_frame[column_name]))
            else:
                replace_value = value
                self._data_frame = self._data_frame.withColumn(column_name, when(((self._data_frame[column_name] >= range[0]) & (self._data_frame[column_name] <= range[1])), replace_value).otherwise(self._data_frame[column_name]))
        else:
            if value == "median":
                dp_helper_obj = DataPreprocessingHelper(self._data_frame)
                median_val = dp_helper_obj.get_median(column_name)
                replace_value = median_val
                self._data_frame = self._data_frame.withColumn(column_name+"_treated_"+str(range)+"_median", when(self._data_frame[column_name] == range, replace_value).otherwise(self._data_frame[column_name]))
            if value == "mode":
                dp_helper_obj = DataPreprocessingHelper(self._data_frame)
                mode_val = dp_helper_obj.get_mode(column_name)
                replace_value = mode_val
                self._data_frame = self._data_frame.withColumn(column_name+"_treated_"+str(range)+"_mode", when(self._data_frame[column_name] == range, replace_value).otherwise(self._data_frame[column_name]))
            if value == "mean":
                dp_helper_obj = DataPreprocessingHelper(self._data_frame)
                mean_value = self._data_frame.agg(avg(column_name)).first()[0]
                replace_value = mean_value
                self._data_frame = self._data_frame.withColumn(column_name+"_treated_"+str(range)+"_mean", when(self._data_frame[column_name] == range, replace_value).otherwise(self._data_frame[column_name]))
            '''
            else:
                replace_value = value
                self._data_frame = self._data_frame.withColumn(column_name+"_treated_"+str(range)+"_"+str(replace_value), when(self._data_frame[column_name] == range, replace_value).otherwise(self._data_frame[column_name]))
            '''
        return self._data_frame


    def standardize_column(self, column_name):
        def standardize_column_helper(mean, sd):
            return udf(lambda x: (x-mean)*1.0/sd)
        mean = self._data_frame.select(F.mean(column_name)).collect()[0][0]
        StdDev = self._data_frame.select(F.stddev_samp(column_name)).collect()[0][0]
        self._data_frame = self._data_frame.withColumn(column_name + "_fs_standardized", standardize_column_helper(mean,StdDev)(col(column_name)))
        self._data_frame = self._data_frame.withColumn(column_name + "_fs_standardized", self._data_frame[column_name + "_fs_standardized"].cast('float'))
        return self._data_frame


    '''Rounds off the returned value ==> values formed are either 0 or 1'''
    def normalize_column(self, column_name):
        def normalize_column_helper(min, max):
            return udf(lambda x: (x - min)*1.0/(max - min))
        max = self._data_frame.select(F.max(column_name)).collect()[0][0]
        min = self._data_frame.select(F.min(column_name)).collect()[0][0]
        self._data_frame = self._data_frame.withColumn(column_name + "_fs_normalized", normalize_column_helper(min, max)(col(column_name)))
        self._data_frame = self._data_frame.withColumn(column_name + "_fs_normalized", self._data_frame[column_name + "_fs_normalized"].cast('float'))
        return self._data_frame


    def replacerUDF(self, value, operation):
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
        self._data_frame = self._data_frame.withColumn(column_name + "_vt_log_transform", self.replacerUDF(10, "logTransform")(col(column_name)))
        self._data_frame = self._data_frame.withColumn(column_name + "_vt_log_transform", self._data_frame[column_name + "_vt_log_transform"].cast('float'))
        return self._data_frame

    def modulus_transform_column(self, column_name):
        self._data_frame = self._data_frame.withColumn(column_name + "_vt_modulus_transformed", self.replacerUDF(10, "modulus")(col(column_name)))
        self._data_frame = self._data_frame.withColumn(column_name + "_vt_modulus_transformed", self._data_frame[column_name + "_vt_modulus_transformed"].cast('float'))
        return self._data_frame

    def cuberoot_transform_column(self, column_name):
        self._data_frame = self._data_frame.withColumn(column_name + "_vt_cuberoot_transformed", self.replacerUDF(3, "NthRoot")(col(column_name)))
        self._data_frame = self._data_frame.withColumn(column_name + "_vt_cuberoot_transformed", self._data_frame[column_name + "_vt_cuberoot_transformed"].cast('float'))
        return self._data_frame

    def squareroot_transform_column(self, column_name):
        self._data_frame = self._data_frame.withColumn(column_name + "vt__squareroot_transformed", self.replacerUDF(2, "NthRoot")(col(column_name)))
        self._data_frame = self._data_frame.withColumn(column_name + "vt__squareroot_transformed", self._data_frame[column_name + "vt__squareroot_transformed"].cast('float'))
        return self._data_frame


    def label_encoding_column(self, column_name):
        indexers = [StringIndexer(inputCol=column_name, outputCol=column_name+"_ed_label_encoding").fit(self._data_frame)]
        pipeline = Pipeline(stages=indexers)
        self._data_frame = pipeline.fit(self._data_frame).transform(self._data_frame)
        return self._data_frame
#Need to check for an alternative for oneHot Encoding for Pyspark

    def onehot_encoding_column(self, column_name):
        self._data_frame = self.label_encoding_column(column_name)
        encoder = OneHotEncoder(dropLast=False, inputCol = column_name+"_ed_label_encoding", outputCol = column_name+"_ed_one_hot_encoding")
        self._data_frame = encoder.transform(self._data_frame)
        self._data_frame = self._data_frame.withColumn(column_name + "_ed_one_hot_encoding", self._data_frame[column_name + "_ed_one_hot_encoding"].cast('string'))
        self._data_frame.drop(column_name+"_l_encoded").collect()
        return self._data_frame


    def character_count_string(self, column_name):
        def character_count_string_helper():
            return udf(lambda x:x.count("")-1)
        self._data_frame = self._data_frame.withColumn(column_name+"_character_count", character_count_string_helper()(col(column_name)))
        self._data_frame = self._data_frame.withColumn(column_name + "_character_count", self._data_frame[column_name + "_character_count"].cast('float'))
        return self._data_frame


    def contains_word_helper(self, word):
        return udf(lambda x:False if x.lower().find(word) == -1 else True)


    def contains_word(self, column_name, word):
        # word = word.lower()
        self._data_frame = self._data_frame.withColumn(column_name+"_contains_"+word, self.contains_word_helper(word)(col(column_name)))
        return self._data_frame


    '''Given that all datetime columns follow same string format == "dd/MM/yyyy" for date'''
    def convert_to_timestamp(self, datetime_col, timeformat):
        timestamped = datetime_col + "_timestamped"
        self._data_frame = self._data_frame.withColumn(timestamped, to_timestamp(self._data_frame[datetime_col], timeformat).alias(datetime_col))
        return self._data_frame

#Timeformat is hardcoded as "dd/MM/yyyy"
    def count_time_since(self, col_for_time_since, time_since_date):
        '''Columns to be passed for calculating duration need to be in TimeStamped format'''
        '''time_since_date should be in dd/MM/yyyy format'''
        self._data_frame = self._data_frame.withColumn("TIME_SINCE_DATE", F.lit(time_since_date))
        self._data_frame = self._data_frame.withColumn("TIME_SINCE_DATE(Timestamped)", to_timestamp(self._data_frame["TIME_SINCE_DATE"], "dd/MM/yyyy"))
        self._data_frame = self._data_frame.withColumn("TIME_SINCE", datediff(self._data_frame[col_for_time_since], self._data_frame["TIME_SINCE_DATE(Timestamped)"]))
        self._data_frame = self._data_frame.drop("TIME_SINCE_DATE", "TIME_SINCE_DATE(Timestamped)")
        return self._data_frame

#TODO - Check for timestamp conversion related issues if any

    def month_to_string(self,dict):
        def month_to_string_helper(x,dict):
            for key in dict.keys():
                if int(x) == key:
                    return dict[key]
        return udf(lambda x: dict_for_month_helper(x,dict))


#Timeformat is hardcoded as "dd/MM/yyyy"
    def extract_datetime_info(self, datetime_col, info_to_extract):
        timestamped = datetime_col + "_timestamped"
        self._data_frame = self._data_frame.withColumn(datetime_col, to_timestamp(self._data_frame[datetime_col], "dd/MM/yyyy").alias(datetime_col))
        if info_to_extract == "year":
            self._data_frame = self._data_frame.withColumn(datetime_col + "_year", year(to_timestamp(self._data_frame[datetime_col], "dd/MM/yyyy").alias(datetime_col)))
        if info_to_extract == "month":
            dict = {1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}
            self._data_frame = self._data_frame.withColumn(datetime_col + "_month", month(to_timestamp(self._data_frame[datetime_col], "dd/MM/yyyy").alias(datetime_col)))
            self._data_frame = self._data_frame.withColumn(datetime_col + "_month", self.month_to_string(dict)(col(datetime_col + "_month")))
        if info_to_extract == "day_of_month":
            self._data_frame = self._data_frame.withColumn(datetime_col + "_day_of_month", dayofmonth(to_timestamp(self._data_frame[datetime_col], "dd/MM/yyyy").alias(datetime_col)))
        if info_to_extract == "day_of_year":
            self._data_frame = self._data_frame.withColumn(datetime_col + "_day_of_year", dayofyear(to_timestamp(self._data_frame[datetime_col], "dd/MM/yyyy").alias(datetime_col)))
        if info_to_extract == "day":
            self._data_frame = self._data_frame.withColumn(datetime_col, to_timestamp(self._data_frame[datetime_col], "dd/MM/yyyy").alias(datetime_col))
            self._data_frame = self._data_frame.withColumn(datetime_col + "_day", date_format(datetime_col, 'E').alias(datetime_col))
        if info_to_extract == "week_of_year":
            self._data_frame = self._data_frame.withColumn(datetime_col + "_week_of_year", weekofyear(to_timestamp(self._data_frame[datetime_col], "dd/MM/yyyy").alias(datetime_col)))
        if info_to_extract == "hour":
            self._data_frame = self._data_frame.withColumn(datetime_col + "_hour", hour(to_timestamp(self._data_frame[datetime_col], "dd/MM/yyyy").alias(datetime_col)))
        if info_to_extract == "minute":
            self._data_frame = self._data_frame.withColumn(datetime_col + "_minute", minute(to_timestamp(self._data_frame[datetime_col], "dd/MM/yyyy").alias(datetime_col)))
        if info_to_extract == "date":
            self._data_frame = self._data_frame.withColumn(datetime_col + "_date", to_timestamp(self._data_frame[datetime_col], "dd/MM/yyyy").cast("date").alias(datetime_col))
        return self._data_frame


    def is_weekend_helper(self):
        return udf(lambda x:False if (int(x) < 6) else True)

#Timeformat is hardcoded as "dd/MM/yyyy"
    def is_weekend(self, datetime_col):
        self._data_frame = self._data_frame.withColumn(datetime_col, to_timestamp(self._data_frame[datetime_col], "dd/MM/yyyy").alias(datetime_col))
        self._data_frame = self._data_frame.withColumn(datetime_col + "_day", date_format(datetime_col, 'u').alias(datetime_col))
        self._data_frame = self._data_frame.withColumn(datetime_col + "_is_weekend", self.is_weekend_helper()(col(datetime_col + "_day")))
        return self._data_frame
