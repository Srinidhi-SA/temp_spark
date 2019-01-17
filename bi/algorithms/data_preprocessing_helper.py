import datetime
from pyspark.sql.functions import col, floor, concat, lit, concat_ws, unix_timestamp, from_unixtime, datediff, to_timestamp, avg, mean, stddev, when
from pyspark.sql.types import IntegerType, StringType, DateType
from pyspark.sql import functions as F

#from pyspark.sql.functions import mean as _mean, stddev as _stddev, col
#from pyspark.sql.functions import *


class DataPreprocessingHelper():
    """Docstring for data Preprocessing Operations"""

    def __init__(self, df):
        self._data_frame = df

    def drop_duplicate_rows(self):
        self._data_frame = self._data_frame.dropDuplicates()
        #self._data_frame.show()
        return self._data_frame


    def drop_duplicate_cols(self):

    	numerical_col = [i_val for (i_val,i_type) in self._data_frame.dtypes if i_type == 'int' ]
    	categorical_col = [i_val for (i_val,i_type) in self._data_frame.dtypes if i_type == 'string' ]
    	timestamp_col = [i_val for (i_val,i_type) in self._data_frame.dtypes if i_type == 'timestamp' ]

    	removed_col = []

    	for i in range(len(numerical_col) - 1):
    		for j in range(i+1, len(numerical_col)):
    			if numerical_col[i] in removed_col or numerical_col[j] in removed_col:
    				continue
    			if self._data_frame.where(self._data_frame[numerical_col[i]] == self._data_frame[numerical_col[j]]).count() == df.count():
    				removed_col.append(numerical_col[j])
    				self._data_frame = self._data_frame.drop(numerical_col[j])

    	for i in range(len(categorical_col) - 1):
    		for j in range(i+1, len(categorical_col)):
    			if categorical_col[i] in removed_col or categorical_col[j] in removed_col:
    				continue
    			if self._data_frame.where(self._data_frame[categorical_col[i]] == self._data_frame[categorical_col[j]]).count() == self._data_frame.count():
    				removed_col.append(categorical_col[j])
    				self._data_frame= self._data_frame.drop(categorical_col[j])

    	for i in range(len(timestamp_col) - 1):
    		for j in range(i+1, len(timestamp_col)):
    			if timestamp_col[i] in removed_col or timestamp_col[j] in removed_col:
    				continue
    			if self._data_frame.where(self._data_frame[timestamp_col[i]] == self._data_frame[timestamp_col[j]]).count() == df.count():
    				removed_col.append(timestamp_col[j])
    				self._data_frame = self._data_frame.drop(timestamp_col[j])
        return self._data_frame
    	#print("Removing duplicate measures, dimensions and dates")

    def mean_impute_missing_values(self, col_to_impute):
        df_copy = self._data_frame
        self._data_frame = self._data_frame.filter(self._data_frame[col_to_impute].isNotNull())
        mean_value = self._data_frame.agg(avg(col_to_impute)).first()[0]
        df_copy = df_copy.fillna({col_to_impute : mean_value})
        return df_copy

    def median_impute_missing_values(self, col_to_impute):
        df_copy = self._data_frame
        self._data_frame = self._data_frame.filter(df[col_to_impute].isNotNull())
        median_value = get_median(df, col_to_impute)
        df_copy = df_copy.fillna({col_to_impute : median_value})
        return df_copy

    def mode_impute_missing_values(self, col_to_impute):
        df_copy = self._data_frame
        self._data_frame = self._data_frame.filter(df[col_to_impute].isNotNull())
        mode_value = get_mode(df, col_to_impute)
        df_copy = df_copy.fillna({col_to_impute : mode_value})
        return df_copy


    def detect_outliers(self, outlier_detection_col):
        df_stats = self._data_frame.select(mean(col(outlier_detection_col)).alias('mean'), stddev(col(outlier_detection_col)).alias('std')).collect()
        mean_val = df_stats[0]['mean']
        std_val = df_stats[0]['std']
        upper_val = mean_val + (3*std_val)
        lower_val = mean_val - (3*std_val)
        outliers = [lower_val, upper_val]
        #print mean_val
        #print std_val
        #print outliers
        return outliers


    def remove_outliers(self, outlier_removal_col, ol_lower_range,ol_upper_range):
        '''Need to check how it will affect multiple columns'''
        self._data_frame = self._data_frame.filter(self._data_frame[outlier_removal_col] > ol_lower_range)
        self._data_frame = self._data_frame.filter(self._data_frame[outlier_removal_col] < ol_upper_range)
        return self._data_frame







'''
class dataPreprocessing():
    """Docstring for data Preprocessing Operations"""

    def __init__(self, df):
        self._data_frame = df

    def drop_duplicate_rows(df):
        df = df.dropDuplicates()
        df.show()
        return df


    def drop_duplicate_cols(df):

    	numerical_col = [i_val for (i_val,i_type) in df.dtypes if i_type == 'int' ]
    	categorical_col = [i_val for (i_val,i_type) in df.dtypes if i_type == 'string' ]
    	timestamp_col = [i_val for (i_val,i_type) in df.dtypes if i_type == 'timestamp' ]

    	removed_col = []

    	for i in range(len(numerical_col) - 1):
    		for j in range(i+1, len(numerical_col)):
    			if numerical_col[i] in removed_col or numerical_col[j] in removed_col:
    				continue
    			if df.where(df[numerical_col[i]] == df[numerical_col[j]]).count() == df.count():
    				removed_col.append(numerical_col[j])
    				df = df.drop(numerical_col[j])

    	for i in range(len(categorical_col) - 1):
    		for j in range(i+1, len(categorical_col)):
    			if categorical_col[i] in removed_col or categorical_col[j] in removed_col:
    				continue
    			if df.where(df[categorical_col[i]] == df[categorical_col[j]]).count() == df.count():
    				removed_col.append(categorical_col[j])
    				df= df.drop(categorical_col[j])

    	for i in range(len(timestamp_col) - 1):
    		for j in range(i+1, len(timestamp_col)):
    			if timestamp_col[i] in removed_col or timestamp_col[j] in removed_col:
    				continue
    			if df.where(df[timestamp_col[i]] == df[timestamp_col[j]]).count() == df.count():
    				removed_col.append(timestamp_col[j])
    				df = df.drop(timestamp_col[j])
        return df
    	#print("Removing duplicate measures, dimensions and dates")

    def impute_missing_values(df, col_to_impute):
        df_copy = df
        df = df.filter(df[col_to_impute].isNotNull())
        mean_value = df.agg(avg(col_to_impute)).first()[0]
        #print mean_value
        df_copy = df_copy.fillna({col_to_impute : mean_value})
        df_copy.show()
        df.show()
        return df_copy


    def detect_outliers(df, outlier_detection_col):
        df_stats = df.select(mean(col(outlier_detection_col)).alias('mean'), stddev(col(outlier_detection_col)).alias('std')).collect()
        mean_val = df_stats[0]['mean']
        std_val = df_stats[0]['std']
        upper_val = mean_val + (3*std_val)
        lower_val = mean_val - (3*std_val)
        outliers = [lower_val, upper_val]
        #print mean_val
        #print std_val
        #print outliers
        return outliers


    def remove_outliers(df, outlier_removal_col, outlier_range):
        """Need to check how it will affect multiple columns"""
        df = df.filter(df[outlier_removal_col] > outlier_range[0])
        df = df.filter(df[outlier_removal_col] < outlier_range[1])
        df.show()
        return df



'''
