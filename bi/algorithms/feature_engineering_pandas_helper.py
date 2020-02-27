from __future__ import absolute_import
from __future__ import division
from builtins import str
from builtins import range
from builtins import object
from past.utils import old_div
import numpy as np
import math
from datetime import datetime
from scipy import linspace
from bi.common.column import ColumnType
from bi.common import MetaDataHelper
from bi.settings import setting as GLOBALSETTINGS

from .data_preprocessing_helper_pandas import DataPreprocessingHelperPandas

class FeatureEngineeringHelperPandas(object):
    """Contains Feature Engineering Operation Functions"""

    def __init__(self, df, dataframe_context):
        self._data_frame = df
        self._metaHelperInstance = MetaDataHelper(self._data_frame, self._data_frame.shape[0])
        self._dataframe_context = dataframe_context

        # self._dataframe_helper = dataframe_helper

    def binning_all_measures(self,number_of_bins,consider_cols):
        numeric_columns = []
        cols_to_be_binned=[x[:-4] for x in consider_cols if x[-4:]=="_bin"]
        numeric_columns = [col for col in self._data_frame.columns if self._data_frame[col].dtypes in ['int32','int64','float32','float64','int','float']]
        for column_name in numeric_columns and cols_to_be_binned:
            self._data_frame = self.create_equal_sized_measure_bins(column_name,number_of_bins)
        return self._data_frame

    def check_key(self, x, bin_label):
        if x!= None:
            for key in list(bin_label.keys()):
                if (x >= bin_label[key][0] and x <= bin_label[key][1]):
                    return key
        else :
            return "None"

    def create_level(self, x, level_dict, selected_list):
        for key in list(level_dict.keys()):
            if x in selected_list:
                if x in level_dict[key]:
                    return key
            else:
                return x

    def create_new_levels_dimension(self, column_name, level_dict):
        selected_list = []
        for key in list(level_dict.keys()):
            selected_list = selected_list + level_dict[key]
        self._data_frame[column_name+"_level"] = self._data_frame[column_name].apply(self.create_level,level_dict=level_dict,selected_list=selected_list)
        return self._data_frame

    def create_level_udf_time(self, dict, date_format):
        pass

    def create_new_levels_datetimes(self, col_for_timelevels, dict):
        pass

    def create_equal_sized_measure_bins(self, column_name,number_of_bins):
        def create_dict_for_bin():
            min_value = np.min(self._data_frame[column_name])
            max_value = np.max(self._data_frame[column_name])
            interval_size = (old_div((max_value - min_value)*1.0,(number_of_bins-1)))
            bin_dict = {}
            temp = min_value
            while temp <=max_value:
                bin_dict[str(round(temp,3))+"-"+str(round(temp+interval_size,3))] = [temp, temp+interval_size]
                temp = temp+interval_size
            return bin_dict
        bin_dict = create_dict_for_bin()
        self._data_frame[column_name+"_bin"] = self._data_frame[column_name].apply(self.check_key, bin_label=bin_dict)
        return self._data_frame

    def create_custom_measure_bins(self,column_name,list_of_intervals):
        def create_dict_for_bin():
            min_value = np.min(self._data_frame[column_name])
            max_value = np.max(self._data_frame[column_name])
            bin_dict = {}
            if list_of_intervals[0]>min_value:
                bin_dict[str(min_value)+"-"+str(list_of_intervals[0])] = [min_value, list_of_intervals[0]]
            for i in range(len(list_of_intervals)):
                if i+2<=len(list_of_intervals):
                    bin_dict[str(list_of_intervals[i])+"-"+str(list_of_intervals[i+1])] = [list_of_intervals[i], list_of_intervals[i+1]]
            if list_of_intervals[-1]<max_value:
                bin_dict[str(list_of_intervals[-1])+"-"+str(max_value)] = [list_of_intervals[-1], max_value]

            return bin_dict
        bin_dict = create_dict_for_bin()
        self._data_frame[column_name+"_c_bin"] = self._data_frame[column_name].apply(self.check_key,bin_label=bin_dict)
        return self._data_frame

    def replace_values_in_column(self, column_name, range, value):
        if value == "median":
            dp_helper_obj = DataPreprocessingHelperPandas(self._data_frame, self._dataframe_context)
            median_val = dp_helper_obj.get_median(self._data_frame, column_name)
            replace_value = median_val
            self._data_frame[column_name+"_treated_"+str(range)+"_median"] = self._data_frame[column_name].apply(lambda x: replace_value if x==range else x)
        elif value == "mode":
            dp_helper_obj = DataPreprocessingHelperPandas(self._data_frame, self._dataframe_context)
            mode_val = dp_helper_obj.get_mode(self._data_frame, column_name)
            replace_value = mode_val
            self._data_frame[column_name+"_treated_"+str(range)+"_mode"] = self._data_frame[column_name].apply(lambda x: replace_value if x==range else x)
        elif value == "mean":
            dp_helper_obj = DataPreprocessingHelperPandas(self._data_frame, self._dataframe_context)
            mean_value = np.mean(self._data_frame[column_name])
            replace_value = mean_value
            self._data_frame[column_name+"_treated_"+str(range)+"_mean"] = self._data_frame[column_name].apply(lambda x: replace_value if x==range else x)
        else:
            replace_value = value
            self._data_frame[column_name+"_treated_"+str(range)+"_"+str(replace_value)] = self._data_frame[column_name].apply(lambda x: replace_value if x==range else x)
        return self._data_frame

    def standardize_column(self, column_name):
        pass

    def normalize_column(self, column_name):
        pass

    def replacerUDF(self, value, operation):
        pass

    def logTransform_column(self, column_name):
        pass

    def modulus_transform_column(self, column_name):
        pass

    def cuberoot_transform_column(self, column_name):
        pass

    def squareroot_transform_column(self, column_name):
        pass

    def label_encoding_column(self, column_name):
        pass

    def onehot_encoding_column(self, column_name):
        pass

    def character_count_string(self, column_name):
        self._data_frame[column_name+"_character_count"] = self._data_frame[column_name].apply(lambda x:x.count("")-1 if x!=None else 0)
        self._data_frame[column_name+"_character_count"] = self._data_frame[column_name + "_character_count"].astype('float')
        return self._data_frame

    def contains_word(self, column_name, word):
        # word = word.lower()
        self._data_frame[column_name+"_contains_"+word] = self._data_frame[column_name].apply(lambda x:False if x == None or x.lower().find(word) == -1 else True)
        return self._data_frame

    def convert_to_timestamp(self, datetime_col, timeformat):
        pass

    def count_time_since(self, col_for_time_since, time_since_date):
        pass

    def month_to_string(self,dict):
        pass

    def extract_datetime_info(self, datetime_col, info_to_extract):
        pass

    def is_weekend_helper(self):
        pass

    def is_weekend(self, datetime_col):
        pass
