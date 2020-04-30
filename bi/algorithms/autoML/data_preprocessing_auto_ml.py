import locale
import pandas as pd
import numpy as np
import re
import pint
from pint import UnitRegistry
import random
import pickle
from validate_email import validate_email
from scipy import stats
from bi.algorithms.autoML.utils_automl import *

class DataPreprocessingAutoML:

    def __init__(self, data_frame, target, data_change_dict, numeric_cols, dimension_cols, datetime_cols,problem_type):
        self.data_frame = data_frame
        self.target = target
        self.problem_type = problem_type
        self.numeric_cols = numeric_cols
        self.dimension_cols = dimension_cols
        self.datetime_cols = datetime_cols
        self.data_change_dict = data_change_dict
        self.data_change_dict["MeasureColsToDim"] = []
        self.data_change_dict['MeanImputeCols'] = []
        self.data_change_dict['ModeImputeCols'] = []
        self.col_with_nulls = list(self.data_frame .loc[:, (self.data_frame.isna().sum() > 0)])

    def drop_duplicate_rows(self):
        """Drops Duplicate rows of a dataframe and returns a new dataframe"""
        self.data_frame = self.data_frame.drop_duplicates()

    def drop_constant_unique_cols(self):
        self.data_frame  = self.data_frame .loc[:, (self.data_frame .nunique() != 1)]
        new_df  = self.data_frame .loc[:, (self.data_frame.nunique() != self.data_frame .shape[0])]
        if self.target not in new_df.columns:
            new_df[self.target] = self.data_frame[self.target]
            self.data_frame = new_df
        else:
            self.data_frame = new_df
        self.data_change_dict['dropped_columns_list'] = []
        def dropped_col_update(list_element):
            if list_element["column_name"] not in self.data_frame.columns:
                list_element["dropped_column_flag"] = True
                self.data_change_dict['dropped_columns_list'].append(list_element["column_name"])
                self.numeric_cols, self.dimension_cols, self.col_with_nulls = drop_cols_from_list(list_element["column_name"],self.numeric_cols, self.dimension_cols, self.col_with_nulls)
            else:
                pass
            return list_element
        self.data_change_dict['Column_settings'] = [dropped_col_update(list_element) for list_element in self.data_change_dict['Column_settings']]

    def drop_null_cols(self):
        '''Dropping columns with more than 75% null values'''
        self.data_frame  = self.data_frame .loc[:, (self.data_frame.isna().sum() < (0.75 * self.data_frame.shape[0]))]
        def dropped_col_update(list_element):
            if list_element["column_name"] not in self.data_frame.columns:
                list_element["dropped_column_flag"] = True
                self.data_change_dict['dropped_columns_list'].append(list_element["column_name"])
                self.numeric_cols, self.dimension_cols, self.col_with_nulls = drop_cols_from_list(list_element["column_name"],self.numeric_cols, self.dimension_cols, self.col_with_nulls)
            else:
                pass
            return list_element
        self.data_change_dict['Column_settings'] = [dropped_col_update(list_element) for list_element in self.data_change_dict['Column_settings']]

    def dimension_measure(self, columns):
            """Identifies columns which are measures and have been wrongly identified as dimension
            returns a list of columns to be converted to measure and removes the rows which have other than numeric
            for that particular column"""
            # column_val = self.data_frame[column]
            for column in columns:
                column_val = self.data_frame[column]
                updated_row_num = self.data_frame[column].index
                r1 = random.randint(0, len(updated_row_num) - 1)
                if re.match("^\d*[.]?\d*$", str(self.data_frame.iloc[r1][column])):
                    # out=column_val.str.isdigit()
                    out = column_val.str.contains("^[0-9]+[.]{0,1}[0-9]*\s*$")
                    if out[out == False].count() <= 0.01 * self.data_frame.shape[0]:
                        row_index = out.index[out == False].tolist()
                        self.data_frame = self.data_frame.drop(row_index, axis=0)
                        self.data_change_dict["MeasureColsToDim"].append(column)
                        self.dimension_cols.remove(column)
                        ## below line code change during optimization
                        self.data_frame[column] = pd.to_numeric(self.data_frame[column])
                        self.numeric_cols.append(column)

    def dimension_measure_test(self, columns):
        for column in columns:
            if (str(self.data_frame[column].dtype).startswith('int')) | (str(self.data_frame[column].dtype).startswith('float')):
                continue
            else:
                column_val = self.data_frame[column]
                out = column_val.str.contains("^[0-9]+[.]{0,1}[0-9]*\s*$")
                if out[out == False].count() <= 0.01 * self.data_frame.shape[0]:
                    row_index = out.index[out == False].tolist()
                    pure_column = self.data_frame[column].drop(row_index, axis=0)
                    self.data_frame[column] = pd.to_numeric(self.data_frame[column])
                    self.data_frame.iloc[row_index] = int(np.mean(pure_column))
                    self.dimension_cols.remove(column)
                    self.numeric_cols.append(column)

    def handle_outliers(self):
        '''
        Needs to be fixed
        '''
        # #Ref: https://stackoverflow.com/questions/23199796/detect-and-exclude-outliers-in-pandas-data-frame
        # df = self.data_frame[columns]
        # df1 = self.data_frame[self.dimension_cols]
        # idx = np.all(stats.zscore(df) < 3, axis=1)
        # self.data_frame.loc[idx]

    def mean_impute(self, column_val):
        """Returns a column with mean impute"""
        mean = np.mean(column_val)
        column_val = column_val.fillna(mean)
        return column_val

    def median_impute(self, column_val):
        """Returns a column with median impute"""
        median = np.median(column_val)
        column_val = column_val.fillna(median)
        return column_val

    def mode_impute(self, column_val):
        """Returns a column with mode impute"""
        mode = column_val.mode()[0]
        column_val = column_val.fillna(mode)
        return column_val

    def measure_col_imputation(self, columns):
        """Does missing value imputation for measure columns"""
        mean_impute_cols = []
        median_impute_cols = []
        for column in columns:
            if column in self.col_with_nulls:
                self.data_frame[column] = self.mean_impute(self.data_frame[column])
                self.data_change_dict['MeanImputeCols'].append(column)

    def dim_col_imputation(self, columns):
        """Does missing value imputation for dimension columns"""
        for column in columns:
            if column in self.col_with_nulls:
                self.data_frame[column] = self.mode_impute(self.data_frame[column])
                self.data_change_dict['ModeImputeCols'].append(column)

    def test_data_imputation(self):
        null_cols = self.data_frame.columns[self.data_frame.isna().any()].tolist()
        if len(null_cols) != 0:
            numeric_columns = self.data_frame[null_cols]._get_numeric_data().columns
            cat_col_names = list(set(null_cols) - set(numeric_columns))
            for col in null_cols:
                if col in cat_col_names:
                    mode_df = self.mode_impute(self.data_frame[col])
                    self.data_frame[col] = mode_df
                else:
                    mean_df = self.mean_impute(self.data_frame[col])
                    self.data_frame[col] = mean_df
    #ON HOLD
    def regex_catch(self, column):
        """Returns a list of columns and the pattern it has"""
        ## considering currency_list and metric_list are globally defined.
        pattern_dict = {"Column_name": column, "email-id": False, "website": False, "Percentage": False,
                "CurrencyCol": {"value": False, "currency": None}, "MetricCol": {"value": False, "metric": None},
                "SepSymbols": {"value": False, "Symbol": None}}
        column_val = self.data_frame[column].astype(str).str.strip()
        df1 = self.data_frame[column_val.apply(validate_email)]
        if df1.shape[0] >= (0.8 * self.data_frame.shape[0]):
            pattern_dict["email-id"] = True
        elif column_val.str.contains("%$", na=True).all():
            pattern_dict["Percentage"] = True
        elif column_val.str.contains("^https:|^http:|^www.", na=True).all():
            pattern_dict["website"] = True
        elif column_val.str.contains("[0-9]+[.]{0,1}[0-9]*\s*[Aa-zZ]{1,2}$").all():
            metric = list(map(lambda x: re.sub("[0-9]+[.]{0,1}[0-9]*\s*", "", x), column_val))
            if len(set(metric)) == 1:
                if metric[0] in Metric_list:
                    pattern_dict["MetricCol"]["value"] = True
                    pattern_dict["MetricCol"]["metric"] = metric[0]
        elif column_val.str.contains("([0-9]+[.]{0,1}[0-9]*\s*\W$)|(^\W[0-9]+[.]{0,1}[0-9]*)").all():
            currency = list(map(lambda x: re.sub("[0-9.\s]+", "", x), column_val))
            if len(set(currency)) == 1:
                if currency[0] in currency_list:
                    pattern_dict["CurrencyCol"]["value"] = True
                    pattern_dict["CurrencyCol"]["currency"] = currency[0]
        elif column_val.str.contains("\S+\s*[\W_]+\s*\S+").all():
            seperators = list(map(lambda x: re.sub("\s*[a-zA-Z0-9]+$", "", x),
                                  list(map(lambda x: re.sub('^[a-zA-Z0-9]+\s*', '', x), column_val))))
            if len(set(seperators)) == 1:
                if seperators[0] == "":
                    seperators[0] = ' '
                pattern_dict["SepSymbols"]["value"] = True
                pattern_dict["SepSymbols"]["Symbol"] = seperators[0]
        return pattern_dict

    #ON HOLD
    def target_analysis(self, targetname, m_type):
        '''Gives information of target column'''
        self.dataframe = self.dataframe.dropna(axis=0, subset=[targetname])
        output_dict = {
            "target_analysis": {"target": targetname, "unique_count": int, "value_counts": {}, "balanced": None,
                                "binary": None}}
        target_variable = self.dataframe[targetname]
        counts = target_variable.value_counts()
        self.dataframe = self.dataframe[~target_variable.isin(counts[counts <= 10].index)]
        if (m_type.lower() == 'classification'):
            ## convert target column into object
            output_dict['target_analysis']['converted_to_str'] = False
            if self.dataframe[targetname].dtype != 'O':
                self.dataframe[targetname] = "'" + self.dataframe[targetname].astype(str) + "'"
                output_dict['target_analysis']['converted_to_str'] = True
                print("!!!!!!! Converted to str!!!!!!")
            unique_count = target_variable.nunique()
            output_dict['target_analysis']['unique_count'] = unique_count
            level_count = target_variable.value_counts()
            count_check = level_count[level_count >= 10]
            output_dict['target_analysis']['value_counts'] = count_check.to_dict()
            percen_level_count = round((count_check / count_check.sum()) * 100)
            n = len(count_check)
            if (n == 0):
                out_dict = {"target_analysis": {"target_name": targetname, "descrp_status": {}}}
                out_dict['target_analysis']['descrp_status'] = target_variable.describe().to_dict()
                return out_dict, self.dataframe
            if not (percen_level_count[percen_level_count < ((1 / (2 * n)) * 100)]).empty:
                output_dict['target_analysis']['balanced'] = False
                if (len(count_check) == 2):
                    output_dict['target_analysis']['binary'] = True  # binary (true)
                else:
                    output_dict['target_analysis']['binary'] = False  # not binary(False)
            else:
                output_dict['target_analysis']['balanced'] = True  # balanced (True)
                if (len(count_check) == 2):
                    output_dict['target_analysis']['binary'] = True  # binary (true)
                else:
                    output_dict['target_analysis']['binary'] = False  # not binary(False)
            return output_dict
        else:
            out_dict = {"target_analysis": {"target_name": targetname, "descrp_status": {}}}
            out_dict['target_analysis']['descrp_status'] = target_variable.describe().to_dict()
            return out_dict

    def data_preprocessing_run(self):
        self.drop_duplicate_rows()
        self.drop_constant_unique_cols()
        self.drop_null_cols()
        self.dimension_measure(self.dimension_cols)
        # self.handle_outliers()
        self.measure_col_imputation(self.numeric_cols)
        self.dim_col_imputation(self.dimension_cols)
