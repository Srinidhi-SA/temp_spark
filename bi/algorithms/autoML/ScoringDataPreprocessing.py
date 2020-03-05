#!/usr/bin/env python
# coding: utf-8

import pickle
import pandas as pd

from bi.algorithms.autoML.Data_Preprocessing import *


class ScorePreprocessing(object):

    def __init__(self, data_dict):
        self.data_dict = data_dict

    def preprocessing(self, dataframe, valid_dict):
        cls = DataPreprocessingAutoMl(valid_dict, dataframe)
        # dataframe=cls.drop_duplicate_rows(dataframe)
        try:
            if valid_dict['Dropped_columns']:
                dataframe.drop(valid_dict['Dropped_columns'], axis=1, inplace=True)
        except:
            print(valid_dict['Dropped_columns'], "does not exits")

        ## TO DO:
        # if valid_dict['MeasureColsToDim']!=[]:
        #     ## TO DO :
        #     mea_dim_df,_=cls.dimension_measure(dataframe,vali_dict['MeasureColsToDim'])
        #     temp=set(dataframe.columns)-set(mea_dim_df.columns)
        #     temp = df[temp]
        #     test_df=pd.merge(temp,mea_dim_df,right_index=True,left_index=True)
        # else:
        #     test_df=dataframe

        if valid_dict['Cap_outlier']:
            outlier_columns, capped_col = cls.handle_outliers(valid_dict['Cap_outlier'])
            ## use _,_ here

        ## TO DO : not necessary as target will never be imputed and valid_dict["Mean_imputeCols"] should not contain target.
        ## Imputation
        var = list(set(valid_dict['Mean_imputeCols']) - set([valid_dict['target']]))
        if var:
            for col in var:
                mean_df = cls.mean_impute(cls.dataframe[col])
                cls.dataframe[col] = mean_df
        var = list(set(valid_dict['Median_imputeCols']) - set([valid_dict['target']]))
        if var:
            for col in var:
                median_df = cls.median_impute(cls.dataframe[col])
                cls.dataframe[col] = median_df
        var = list(set(valid_dict['Mode_imputeCols']) - set([valid_dict['target']]))
        if var:
            for col in var:
                mode_df = cls.mode_impute(cls.dataframe[col])
                cls.dataframe[col] = mode_df

        # works only when there are null values in test data and not in train data
        null_cols = cls.dataframe.columns[cls.dataframe.isna().any()].tolist()

        if len(null_cols) != 0:

            numeric_columns = cls.dataframe[null_cols]._get_numeric_data().columns

            cat_col_names = list(set(null_cols) - set(numeric_columns))

            for col in null_cols:
                if col in cat_col_names:
                    mode_df = cls.mode_impute(cls.dataframe[col])
                    cls.dataframe[col] = mode_df
                else:
                    mean_df = cls.mean_impute(cls.dataframe[col])
                    cls.dataframe[col] = mean_df

        return cls.dataframe

    # def fe_main(self,dataframe,valid_dict):
    #
    #     cls=Data_Preprocessing(valid_dict,dataframe)
    #
    #     if valid_dict['MeasureColsToDim']!=[]:
    #         _=cls.dimension_measure(dataframe,vali_dict['MeasureColsToDim'])
    #         temp=set(dataframe.columns)-set(cls.dataframe.columns)
    #         temp = df[temp]
    #         test_df=pd.merge(temp,cls.dataframe,right_index=True,left_index=True)
    #     else:
    #         test_df=dataframe
    #
    #     if valid_dict['Cap_outlier']!=[]:
    #
    #         test_df,outlier_columns,capped_cols=cls.handle_outliers(test_df,valid_dict['Cap_outlier'])
    #
    #     var = list(set(valid_dict['Mean_imputeCols'])-set([valid_dict['target']]))
    #     if var!=[]:
    #         for col in var:
    #             mean_df=cls.mean_impute(test_df[col])
    #             test_df[col]=mean_df
    #     var = list(set(valid_dict['Median_imputeCols'])-set([valid_dict['target']]))
    #     if var!=[]:
    #         for col in var:
    #             median_df=cls.median_impute(test_df[col])
    #             test_df[col]=median_df
    #     var = list(set(valid_dict['Mode_imputeCols'])-set([valid_dict['target']]))
    #     if var!=[]:
    #         for col in var:
    #             mode_df=cls.mode_impute(test_df[col])
    #             test_df[col]=mode_df
    #
    #     return test_df
