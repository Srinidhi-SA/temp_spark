from pandas.api.types import is_datetime64_any_dtype as is_datetime
import numpy as np
import pandas as pd
class DataValidation:
    def __init__(self,data_frame,target,problem_type):
        self.data_frame = data_frame
        data = self.data_frame
        data = data.apply(lambda col: pd.to_datetime(col, errors='ignore') if col.dtypes == object else col, axis=0)
        self.target = target
        self.problem_type = problem_type
        self.numeric_cols = []
        self.dimension_cols = []
        self.datetime_cols = [] #Check it
        self.datetime_cols.extend(data.select_dtypes(include=['datetime']).columns)
        self.data_change_dict = {} #Keeps track of changes done on the dataset

    def find_dataType(self,column):
        Dict = {
            "column_name": column,
            "re_column_name": column,
            "data_type": False,
            "re_name": False,
            "special_char": False,
            "dropped_column_flag": False
        }
        if self.data_frame[column].dtype!= np.object:
            Dict["data_type"] = "{}".format(self.data_frame[column].dtype)
            if column != self.target:
                self.numeric_cols.append(column)
        else:
            Dict["data_type"] = "{}".format(self.data_frame[column].dtype)
            if column != self.target and column not in self.datetime_cols:
                self.dimension_cols.append(column)


        #     try:
        #         self.data_frame[column] = pd.to_datetime(self.data_frame[column], errors='ignore')
        #         Dict["data_type"] = "{}".format(self.data_frame[column].dtype)
        #         if column != self.target:
        #             self.datetime_cols.append(column)
        #     except:
        #         Dict["data_type"] = "{}".format(self.data_frame[column].dtype)
        #         if column != self.target:
        #             self.dimension_cols.append(column)

        return Dict

    def target_fitness_check(self):
        """Checks if target is fit for the type of analysis"""
        '''replace nan values with nan_class '''
        try:
            self.data_frame [self.target].fillna("nan_class", inplace=True)
            target_val = self.data_frame [self.target]
        except:
            flag = True
            return flag
        if self.problem_type.lower() == "classification":
            if (target_val.nunique()) > 30 or (target_val.nunique()) <= 1:
                flag = False
            else:
                flag = True
        else:
            if target_val.nunique() < 10:
                flag = False
            else:
                flag = True
        return flag


    def data_validation_run(self):
        self.data_change_dict['Column_settings'] = [self.find_dataType(i) for i in self.data_frame.columns]
        target_fitness_flag = self.target_fitness_check()
        self.data_change_dict['target_fitness_check']=target_fitness_flag
