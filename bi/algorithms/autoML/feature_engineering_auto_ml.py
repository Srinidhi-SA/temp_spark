import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import OneHotEncoder
class FeatureEngineeringAutoML():

    def __init__(self, data_frame, target, data_change_dict, numeric_cols, dimension_cols, datetime_cols,problem_type):
        self.data_frame = data_frame
        self.target = target
        self.problem_type = problem_type
        self.numeric_cols = numeric_cols
        self.dimension_cols = dimension_cols
        self.datetime_cols = datetime_cols
        self.data_change_dict = data_change_dict
        self.data_change_dict['date_column_split'] = []
        self.data_change_dict['one_hot_encoded'] = []

    def date_column_split(self,col_list):
        """Splitting date column"""
        self.data_frame = self.data_frame.apply(lambda col: pd.to_datetime(col, errors='ignore') if col.dtypes == object else col, axis=0)
        for col_name in col_list:
            column = str(col_name)
            self.data_frame[column + '_day'] = self.data_frame[column].dt.day
            self.data_frame[column + '_month'] = self.data_frame[column].dt.month
            self.data_frame[column + '_year'] = self.data_frame[column].dt.year
            self.data_frame[column + '_quarter'] = self.data_frame[column].dt.quarter
            self.data_frame[column + '_semester'] = np.where(self.data_frame[column + '_quarter'].isin([1, 2]), 1, 2)
            self.data_frame[column + '_day_of_the_week'] = self.data_frame[column].dt.dayofweek
            self.data_frame[column + '_time'] = self.data_frame[column].dt.time
            self.data_frame[column + '_day_of_the_year'] = self.data_frame[column].dt.dayofyear
            self.data_frame[column + '_week_of_the_year'] = self.data_frame[column].dt.weekofyear
            self.data_change_dict['date_column_split'].append(column)

    def one_hot_encoding(self, col_list):
        for col in col_list:
            dummy = enc.fit_transform(col)
            self.data_frame = pd.concat([self.data_frame,dummy], axis = 1)
            self.data_change_dict['one_hot_encoded'].append(col)
        #print(self.data_frame)
    def sk_one_hot_encoding(self,col_list):
        oh_enc = OneHotEncoder(sparse=False)
        new_df  = oh_enc.fit_transform(self.data_frame[col_list])
        uniq_vals = self.data_frame[col_list].apply(lambda x: x.value_counts()).unstack()
        uniq_vals = uniq_vals[~uniq_vals.isnull()]
        enc_cols = list(uniq_vals.index.map('{0[0]}_{0[1]}'.format))
        encoded_df=pd.DataFrame(new_df,columns=enc_cols,index=self.data_frame.index,dtype='int64')
        encoded_df.columns = [re.sub('\W+', '_', col.strip()) for col in encoded_df.columns]
        self.data_frame=self.data_frame[self.data_frame.columns.difference(col_list)]
        self.data_frame.reset_index(drop=True, inplace=True)
        encoded_df.reset_index(drop=True, inplace=True)
        self.data_frame = pd.concat([self.data_frame,encoded_df], axis = 1)
        self.data_change_dict['one_hot_encoded']=col_list
        #print(self.data_frame)

    def feature_engineering_run(self):
        self.date_column_split(self.datetime_cols)
        self.data_frame = self.data_frame.apply(lambda x: x.mask(x.map(x.value_counts()/x.count())<0.01, 'other') if x.name in self.dimension_cols else x)
        self.sk_one_hot_encoding(self.dimension_cols)
