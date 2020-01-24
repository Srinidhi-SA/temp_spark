#!/usr/bin/env python
# coding: utf-8

import pickle
import pandas as pd


from bi.algorithms.autoML.Data_Preprocessing import *

class Score_Preprocessing(object):

    def __init__ (self,data_dict):
        self.data_dict=data_dict

    def preprocessing(self,dataframe,valid_dict):
        cls=Data_Preprocessing(valid_dict)
        #dataframe=cls.drop_duplicate_rows(dataframe)
        try:
            if valid_dict['Dropped_columns']!=[]:
                dataframe.drop(valid_dict['Dropped_columns'],axis= 1,inplace = True)
        except:
            print(valid_dict['Dropped_columns'], "does not exits")

        if valid_dict['MeasureColsToDim']!=[]:
            mea_dim_df,_=cls.Dimension_Measure(dataframe,vali_dict['MeasureColsToDim'])
            temp=set(dataframe.columns)-set(mea_dim_df.columns)
            temp = df[temp]
            test_df=pd.merge(temp,mea_dim_df,right_index=True,left_index=True)
        else:
            test_df=dataframe

        if valid_dict['Cap_outlier']!=[]:

            test_df,outlier_columns,capped_cols=cls.handle_outliers(test_df,valid_dict['Cap_outlier'])

        var = list(set(valid_dict['Mean_imputeCols'])-set([valid_dict['target']]))
        if var!=[]:
            for col in var:
                mean_df=cls.mean_impute(test_df[col])
                test_df[col]=mean_df
        var = list(set(valid_dict['Median_imputeCols'])-set([valid_dict['target']]))
        if var!=[]:
            for col in var:
                median_df=cls.median_impute(test_df[col])
                test_df[col]=median_df
        var = list(set(valid_dict['Mode_imputeCols'])-set([valid_dict['target']]))
        if var!=[]:
            for col in var:
                mode_df=cls.mode_impute(test_df[col])
                test_df[col]=mode_df

        # works only when there are null values in test data and not in train data
        null_cols = test_df.columns[test_df.isna().any()].tolist()

        if len(null_cols) != 0:

            numeric_columns = test_df[null_cols]._get_numeric_data().columns

            cat_col_names = list(set(null_cols) - set(numeric_columns))

            for col in null_cols:
                if col in cat_col_names:
                    mode_df=cls.mode_impute(test_df[col])
                    test_df[col]=mode_df
                else:
                    mean_df=cls.mean_impute(test_df[col])
                    test_df[col]=mean_df

        return test_df


    def fe_main(self,dataframe,valid_dict):

        cls=Data_Preprocessing(valid_dict)

        if valid_dict['MeasureColsToDim']!=[]:
            mea_dim_df,_=cls.Dimension_Measure(dataframe,vali_dict['MeasureColsToDim'])
            temp=set(dataframe.columns)-set(mea_dim_df.columns)
            temp = df[temp]
            test_df=pd.merge(temp,mea_dim_df,right_index=True,left_index=True)
        else:
            test_df=dataframe

        if valid_dict['Cap_outlier']!=[]:

            test_df,outlier_columns,capped_cols=cls.handle_outliers(test_df,valid_dict['Cap_outlier'])

        var = list(set(valid_dict['Mean_imputeCols'])-set([valid_dict['target']]))
        if var!=[]:
            for col in var:
                mean_df=cls.mean_impute(test_df[col])
                test_df[col]=mean_df
        var = list(set(valid_dict['Median_imputeCols'])-set([valid_dict['target']]))
        if var!=[]:
            for col in var:
                median_df=cls.median_impute(test_df[col])
                test_df[col]=median_df
        var = list(set(valid_dict['Mode_imputeCols'])-set([valid_dict['target']]))
        if var!=[]:
            for col in var:
                mode_df=cls.mode_impute(test_df[col])
                test_df[col]=mode_df

        return test_df
