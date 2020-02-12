#!/usr/bin/env python
# coding: utf-8

# # Scoring


from Feature_Engineering import Feature_Engineering

from ScoringDataPreprocessing import Score_Preprocessing

from Data_Preprocessing import Data_Preprocessing

from Feature_Selection import Utils

import chardet

import pandas as pd


class Scoring(object):

    def __init__(self,path,data_dict):

        self.path = path

        self.data_dict = data_dict

    def find_encoding(self):

        r_file = open(self.path, 'rb').read()

        result = chardet.detect(r_file)

        charencode = result['encoding']

        return charencode

    def read_df(self):

        na_values = ["NO CLUE","no clue", "No Clue","na","NA","N/A", "n/a","n a","N A", "not available",
             "Not Available", "NOT AVAILABLE","?","!","NONE","None","none","null","-"]

        df = pd.read_csv(self.path,encoding=self.find_encoding(),error_bad_lines=False,
                                  sep=",",na_values=na_values)
        return df


    def validation(self,data,data_dict):

        for idx in range(len(data_dict["Column_settings"])):

            re_column = data_dict["Column_settings"][idx]['re_column_name']

            column = data_dict["Column_settings"][idx]['column_name']

            if data_dict['target'] != re_column:

                if data_dict["Column_settings"][idx]['droped_column'] == False:

                    data.rename(columns = {column:re_column}, inplace = True)

                else:

                    data.drop([column], axis = 1,inplace = True)


                if data_dict["Column_settings"][idx]['data_type'] == 'datetime64[ns]':
                    data[re_column] = pd.to_datetime(data[re_column], infer_datetime_format=True) #data[re_column].astype['datetime64[ns]']

        return data

    def null_handling(self,df):

        cls=Data_Preprocessing(self.data_dict,df)

        measureCol,dim = [],[]

        for i in df.columns:

            if df[i].dtypes != "object" and df[i].dtypes != "datetime64[ns]":

                measureCol.append(i)

            else :

                dim.append(i)

        outlier_columns,capped_cols=cls.handle_outliers(measureCol)

        measureColImpu = [i for i in measureCol if cls.dataframe[i].isna().sum()>0 ]

        dimColImpu = [i for i in dim if cls.dataframe[i].isna().sum()>0 ]

        mean_impute_cols,median_impute_cols = cls.measureCol_imputation(measureColImpu,outlier_columns)

        cls.dimCol_imputation(dimColImpu)

        return cls.dataframe


    def score_feature_eng(self,df,data_dict):
        fe_obj=Feature_Engineering(df,data_dict)

        if len(data_dict['created_feature'])>0:

            fe_obj.test_main(data_dict['normalize_column'],data_dict['train_final_cols'])

            return fe_obj.original_df,fe_obj.only_created_df
        print("fe_obj: ", fe_obj.original_df)
        print("created only: ",fe_obj.only_created_df)


    def Scoring_feature_selection(self,Dataframe,data_dict):
        linear_dataframe = Dataframe[data_dict['linear_features']]

        tree_dataframe = Dataframe[data_dict['tree_features']]

        obj = Utils()

        """ Label encoding transform"""

        if data_dict['labelencoder']['tree'] != []:

            tree_dataframe = obj.label_en(tree_dataframe,data_dict['labelencoder']['tree'])

        if data_dict['labelencoder']['linear'] != []:

            linear_dataframe = obj.label_en(linear_dataframe,data_dict['labelencoder']['linear'])

        """ Dummy transform"""

        if data_dict['dummy']['tree'] != []:

            for col in data_dict['dummy']['tree']:

                tree_dataframe = obj.Onehotencoder(tree_dataframe,col)

        if data_dict['dummy']['linear'] != []:

            for col in data_dict['dummy']['linear']:

                linear_dataframe = obj.Onehotencoder(linear_dataframe,col)

        """ Saving the Dataframe as CSV file """

#         linear_dataframe.to_csv('linear_test.csv')

#         tree_dataframe.to_csv('tree_test.csv')

        return linear_dataframe,tree_dataframe


    def validate(self,Dataframe,data_dict,linear_dataframe,tree_dataframe):

        if data_dict['dummified_columns']['linear'] != []:

            for i in data_dict['dummified_columns']['linear']:

                labels = list(Dataframe[i].value_counts().index)

                labels.sort()

                labels.pop(0)

                if len(labels)<len(data_dict['dummified_columns']['linear'][i]):


                    missing_labels =  set(data_dict['dummified_columns']['linear'][i]) - set(labels)

                    for i in missing_labels:

                        linear_dataframe[i] = 0

                elif len(labels) > len(data_dict['dummified_columns']['linear'][i]) :

                    excess_labels =  set(data_dict['dummified_columns']['linear'][i]) - set(labels)

                    for i in excess_labels:

                        linear_dataframe.drop(i, inplace = True)

        if data_dict['dummified_columns']['tree'] != []:

            for i in data_dict['dummified_columns']['tree']:

                labels = list(Dataframe[i].value_counts().index)

                labels.sort()

                labels.pop(0)

                if len(labels)<len(data_dict['dummified_columns']['tree'][i]):


                    missing_labels =  set(data_dict['dummified_columns']['tree'][i]) - set(labels)

                    for i in missing_labels:

                        tree_dataframe[i] = 0

                elif len(labels) > len(data_dict['dummified_columns']['tree'][i]) :

                    excess_labels =  set(data_dict['dummified_columns']['tree'][i]) - set(labels)

                    for i in excess_labels:

                        tree_dataframe.drop(i, inplace = True)

        return linear_dataframe,tree_dataframe


    def scoring_data_distribution(self,data,data_dict):
        print(len(data.columns))
        l=data[data_dict['linear_features']]
        t=data[data_dict['tree_features']]
        return l,t


    def run(self):

        """pass_1 """

        """DataValidation"""

        data = self.read_df()

        data = self.validation(data,self.data_dict)

        """preprocessing"""

        obj = Score_Preprocessing(self.data_dict)

        data = obj.preprocessing(data,self.data_dict)

        """FeatureEngineering"""
        o,c = self.score_feature_eng(data,self.data_dict)

        try:
#             result = o.merge(c)
            result = pd.concat([o,c], axis=1)

        except:
            result = o.merge(c, left_on=o.index,right_on=c.index,copy=False)

        print("Result Shape: ", result.shape)

        """Feature_selection"""
        l1,t1 = self.Scoring_feature_selection(result,self.data_dict)
        l,t = self.validate(data,self.data_dict,l1,t1)

        return l,t
