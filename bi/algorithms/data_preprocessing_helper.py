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
    			if self._data_frame.where(self._data_frame[numerical_col[i]] == self._data_frame[numerical_col[j]]).count() == self._data_frame.count():
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



    def get_frequency_of_unique_val(self, col_for_uvf):
        df_counts = self._data_frame.groupBy(col_for_uvf).count()
        return df_counts


    def get_n_most_common(self, col_for_nmc, n):
        '''Only returns first n most commmon even if there are multiple duplicate values'''
        df_nmc = self.get_frequency_of_unique_val(col_for_nmc)
        df_nmc = df_nmc.orderBy("count", ascending=False)
        row_count = df_nmc.count()
        if n >= row_count:
            n = row_count
            df_nmc = df_nmc.limit(n)
        else:
            df_nmc = df_nmc.limit(n)
        return df_nmc


    def get_proportion_of_unique_val(self, col_for_uvpro):
        df_counts = self._data_frame.groupBy(col_for_uvpro).count()
        total =  df_counts.select(F.sum("count")).collect()[0][0]
        df_prop = df_counts.withColumn("PROPORTION", (df_counts["count"] / total))
        df_prop = df_prop.drop("count")
        return df_prop


    def get_percentage_of_unique_val(self, col_for_uvper):
        df_counts = self._data_frame.groupBy(col_for_uvper).count()
        total =  df_counts.select(F.sum("count")).collect()[0][0]
        df_prop = df_counts.withColumn("PERCENTAGE", 100*(df_counts["count"] / total))
        df_prop = df_prop.drop("count")
        return df_prop


    def get_count_of_unique_val(self):
        df_temp = self._data_frame.agg(*(countDistinct(col(c)).alias(c) for c in self._data_frame.columns))
        df_pandas = df_temp.toPandas().transpose()
        print df_pandas


    def get_mode(self, col_for_mode):
        '''Only returns one mode even in case of multiple available modes'''
        df_mode = self.get_frequency_of_unique_val(col_for_mode)
        df_mode = df_mode.orderBy("count", ascending=False)
        df_mode = df_mode.limit(1)
        mode = df_mode.collect()[0][0]
        return mode


    def get_median(self, col_for_median):
        median_val = self._data_frame.approxQuantile(col_for_median, [0.5], 0)
        median =  median_val[0]
        return median


    def mean_impute_missing_values(self, col_to_impute):
        df_copy = self._data_frame
        self._data_frame = self._data_frame.filter(self._data_frame[col_to_impute].isNotNull())
        mean_value = self._data_frame.agg(avg(col_to_impute)).first()[0]
        df_copy = df_copy.fillna({col_to_impute : mean_value})
        return df_copy


    def median_impute_missing_values(self, col_to_impute):
        df_copy = self._data_frame
        self._data_frame = self._data_frame.filter(self._data_frame[col_to_impute].isNotNull())
        median_value = self.get_median(col_to_impute)
        df_copy = df_copy.fillna({col_to_impute : median_value})
        return df_copy


    def mode_impute_missing_values(self, col_to_impute):
        df_copy = self._data_frame
        self._data_frame = self._data_frame.filter(self._data_frame[col_to_impute].isNotNull())
        mode_value = self.get_mode(col_to_impute)
        df_copy = df_copy.fillna({col_to_impute : mode_value})
        return df_copy


    def user_impute_missing_values(self, col_to_impute, mvt_value):
        df_copy = self._data_frame
        self._data_frame = self._data_frame.filter(self._data_frame[col_to_impute].isNotNull())
        df_copy = df_copy.fillna({col_to_impute : mvt_value})
        return df_copy


    def remove_missing_values(self, null_removal_col):
        self._data_frame = self._data_frame.na.drop()
        return self._data_frame


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


    def remove_outliers(self, outlier_removal_col, ol_lower_range, ol_upper_range):
        '''Need to check how it will affect multiple columns'''
        self._data_frame = self._data_frame.filter(self._data_frame[outlier_removal_col] > ol_lower_range)
        self._data_frame = self._data_frame.filter(self._data_frame[outlier_removal_col] < ol_upper_range)
        return self._data_frame


    def mean_impute_outliers(self, outlier_imputation_col, ol_lower_range, ol_upper_range):
        df_dup = self._data_frame
        df_without_outliers = self.remove_outliers(outlier_imputation_col, ol_lower_range, ol_upper_range)
        mean_without_outliers = df_without_outliers.agg(avg(outlier_imputation_col)).first()[0]
        self._data_frame = df_dup.withColumn(outlier_imputation_col, when((df_dup[outlier_imputation_col] < ol_lower_range) | (df_dup[outlier_imputation_col] > ol_upper_range), mean_without_outliers).otherwise(df_dup[outlier_imputation_col]))
        return self._data_frame


    def median_impute_outliers(self, outlier_imputation_col, ol_lower_range, ol_upper_range):
        df_dup = self._data_frame
        df_without_outliers = self.remove_outliers(outlier_imputation_col, ol_lower_range, ol_upper_range)
        median_without_outliers = self.get_median(outlier_imputation_col)
        self._data_frame = df_dup.withColumn(outlier_imputation_col, when((df_dup[outlier_imputation_col] < ol_lower_range) | (df_dup[outlier_imputation_col] > ol_upper_range), median_without_outliers).otherwise(df_dup[outlier_imputation_col]))
        return self._data_frame


    def mode_impute_outliers(self, outlier_imputation_col, ol_lower_range, ol_upper_range):
        df_dup = self._data_frame
        df_without_outliers = self.remove_outliers(outlier_imputation_col, ol_lower_range, ol_upper_range)
        mode_without_outliers = self.get_mode(df_without_outliers[outlier_imputation_col])
        self._data_frame = df_dup.withColumn(outlier_imputation_col, when((df_dup[outlier_imputation_col] < ol_lower_range) | (df_dup[outlier_imputation_col] > ol_upper_range), mode_without_outliers).otherwise(df_dup[outlier_imputation_col]))
        return self._data_frame


    def user_impute_outliers(self, outlier_imputation_col, ol_lower_range, ol_upper_range, mvt_value):
        pass

    # def remove_missing_values(self, col):
    #     pass
