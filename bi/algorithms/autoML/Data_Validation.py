### Necessary Libraries :
import glob
import pandas as pd
import numpy as np
import pickle
import re
import chardet
import warnings

warnings.filterwarnings('ignore')


# from IPython import get_ipython
# get_ipython().run_line_magic('matplotlib', 'inline')

class DataValidation:

    def __init__(self, path, target, method):
        self.dataframe = path
        self.target = target
        self.df = None
        self.charencode = None
        self.method = method
        self.data_dict = {}

    def find_encoding(self):
        """ This Function Finds and returns the Encoding required for the Dataset """
        r_file = open(self.dataframe, 'rb').read()
        result = chardet.detect(r_file)
        self.charencode = result['encoding']
        return self.charencode

    def deal_columns(self, column):
        Dict = {
            "column_name": column,
            "re_column_name": column,
            "data_type": False,
            "re_name": False,
            "special_char": False,
            "droped_column": False
        }
        re_column = column
        if self.df[re_column].dtype != 'object':
            Dict["data_type"] = "{}".format(self.df[column].dtype)  ## Dict["data_type"] = self.df[column].dtype
        elif self.df[column].dtype == 'object':
            try:
                self.df[column] = pd.to_datetime(self.df[column], infer_datetime_format=True)
                Dict["data_type"] = str(self.df[column].dtype)
            except:
                Dict["data_type"] = str(self.df[column].dtype)

        # if re.search(r'[\W_]+',column):
        #
        #     Dict["Special_char"] = True
        #
        #     Dict["re_name"] = True
        #
        #     Dict["data_type"] = "{}".format(self.df[column].dtype)
        # re_column = re.sub(r'[\W_]', '_',column)
        # Dict["re_column_name"] = re_column
        # self.df.rename(columns = {column:re_column}, inplace = True)

        if column == self.target:
            self.data_dict['target'] = self.df[re_column].name
            self.target = self.data_dict['target']
        if re_column != self.target:
            if len(self.df[re_column].value_counts()) == 1 or len(self.df[re_column].value_counts()) == self.df.shape[0]:
                Dict["droped_column"] = True
                self.df.drop([re_column], axis=1, inplace=True)
        self.df.dropna(how='all', axis=0, inplace=True)
        return Dict

    def target_fitness_check(self):
        """Checks if target is fit for the type of analysis"""
        '''replace nan values with nan_class '''
        try:
            self.df[self.target].fillna("nan_class", inplace=True)
            target_val = self.df[self.target]
        except:
            flag = True
            return flag

        if self.method.lower() == "classification":
            if (target_val.nunique()) > 30 or (target_val.nunique()) < 1:
                flag = False
            else:
                flag = True
        else:
            if target_val.nunique() < 10:
                flag = False
            else:
                flag = True
        print("No.Of Target categories: ", target_val.nunique())
        return flag

    def run(self):
        na_values = ["NO CLUE", "no clue", "No Clue", "na", "NA", "N/A", "n/a", "n a", "N A", "not available",
                     "Not Available", "NOT AVAILABLE", "?", "!", "NONE", "None", "none", "null", "-"]
        if type(self.dataframe) == str:
            self.df = pd.read_csv(self.dataframe, encoding=self.find_encoding(), error_bad_lines=False, sep=",",
                                  na_values=na_values)
            self.data_dict['Dataset_name'] = self.dataframe.split('/')[-1]
            self.data_dict['Encoding'] = self.charencode
        else:
            self.df = self.dataframe
        self.data_dict['Column_settings'] = [self.deal_columns(i) for i in self.df.columns]
        self.data_dict['app_type'] = self.method
        self.data_dict["target_fitness_check"] = self.target_fitness_check()
        if self.data_dict["target_fitness_check"] == False:
            print("Target not suitable for ", self.data_dict['app_type'], " analysis. \nExiting.")
#         f = open("dataValidated_dict.pkl","wb")
#         pickle.dump(self.data_dict,f)
#         f.close()
#         self.df.to_csv("dataValidated1.csv",index=False)
