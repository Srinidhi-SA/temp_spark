from bi.algorithms.autoML_score.Feature_Engineering import Feature_Engineering

from bi.algorithms.autoML_score.Data_Validation import Data_Validation

from bi.algorithms.autoML_score.ScoringDataPreprocessing import Score_Preprocessing

from bi.algorithms.autoML_score.Data_Preprocessing import Data_Preprocessing

from bi.algorithms.autoML_score.Feature_Selection import Utils

import chardet

import pandas as pd

import ast

import re

class Scoring(object):

    def __init__(self,path,data_dict):

        self.path = path

        self.data_dict = ast.literal_eval(data_dict)

        # path = self.path
        #
        # obj =  Data_Validation(path,target =self.target,method = self.app_type)
        # obj.run()


    def find_encoding(self):

        r_file = open(self.path, 'rb').read()

        result = chardet.detect(r_file)

        charencode = result['encoding']

        return charencode

    def read_df(self):

        na_values = ["NO CLUE","no clue", "No Clue","na","NA","N/A", "n/a","n a","N A", "not available",
             "Not Available", "NOT AVAILABLE","?","!","NONE","None","none","null","-"]

        # df = pd.read_csv(self.path,encoding=self.find_encoding(),error_bad_lines=False,
        #                           sep=",",na_values=na_values)
        df = pd.read_csv(self.path,error_bad_lines=False,
                                  sep=",",na_values=na_values)
        return df


    def validation(self,data,data_dict):

        for idx in range(len(data_dict["Column_settings"])):

            re_column = data_dict["Column_settings"][idx]['re_column_name']

            column = data_dict["Column_settings"][idx]['column_name']
            print ("\n\n\n")
            print (column)

            if data_dict['target'] != re_column:

                if data_dict["Column_settings"][idx]['droped_column'] == False:

                    data.rename(columns = {column:re_column}, inplace = True)

                else:

                    data.drop([column], axis = 1,inplace = True)


                if data_dict["Column_settings"][idx]['data_type'] == 'datetime64[ns]':
                    data[re_column] = pd.to_datetime(data[re_column], infer_datetime_format=True) #data[re_column].astype['datetime64[ns]']

        return data

    def null_handling(self,df):

        cls=Data_Preprocessing(self.data_dict)

        measureCol,dim = [],[]

        for i in df.columns:

            if df[i].dtypes != "object" and df[i].dtypes != "datetime64[ns]":

                measureCol.append(i)

            else :

                dim.append(i)

        df,outlier_columns,capped_cols=cls.handle_outliers(df,measureCol)

        measureColImpu = [i for i in measureCol if df[i].isna().sum()>0 ]

        dimColImpu = [i for i in dim if df[i].isna().sum()>0 ]

        df,mean_impute_cols,median_impute_cols = cls.measureCol_imputation(df,measureColImpu,outlier_columns)

        df = cls.dimCol_imputation(df,dimColImpu)

        return df


    def score_feature_eng(self,df,data_dict):
        fe_obj=Feature_Engineering(df,data_dict)

        if len(data_dict['created_feature'])>0:
            print ("\n\n\n\n\n\n\n\n\n\n")
            print(data_dict['train_final_cols'], "\n\n\n\n\n\n\n\n\n\n\n")

            fe_obj.test_main(data_dict['normalize_column'],data_dict['train_final_cols'])
#             print("fe_obj: ", fe_obj.original_df)
#             print("created only: ",fe_obj.only_created_df)
            return fe_obj.original_df,fe_obj.only_created_df, fe_obj.date_time_columns



    def Scoring_feature_selection(self,Dataframe,data_dict):

        print("linear features: ",data_dict['linear_features'])
        print("tree features: ",data_dict['tree_features'])

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

        # data = self.read_df()
        data = self.path

        data = self.validation(data,self.data_dict)
        print(data.shape)

        """preprocessing"""

        obj = Score_Preprocessing(self.data_dict)

        data = obj.preprocessing(data,self.data_dict)
        print(data.shape)

        """FeatureEngineering"""
        o,c,date_col = self.score_feature_eng(data,self.data_dict)
        print(o.columns, c.columns)
        cols = list(set(o)-set(date_col))
        o = o[cols]

        try:
#             result = o.merge(c)
            result = pd.concat([o,c], axis=1)
        except:
            result = o.merge(c, left_on=o.index,right_on=c.index,copy=False)

        print('result: ',result.shape)

        """Feature_selection"""
        l1,t1 = self.Scoring_feature_selection(result,self.data_dict)
        l,t = self.validate(data,self.data_dict,l1,t1)
        linear_df_cols = [re.sub('\W+','_', col) for col in l.columns]
        l.columns = linear_df_cols
        tree_df_cols = [re.sub('\W+','_', col) for col in t.columns]
        t.columns = tree_df_cols
        return l,t


# directory = 'D:/mAdvisor/AutoML/SCORING+TRAINING/OneClick_AutoML (copy)/soccer_train/'
# path = directory + 'test.csv'
#
# import pickle
#
# pickle_in = open(directory+"dict4.pickle","rb")
#
# data_dict = pickle.load(pickle_in)
#
#
# obj = Scoring(path,data_dict)
#
# l,t = obj.run()
# l.to_csv(directory+'linear_score.csv')
# t.to_csv(directory+'tree_score.csv')
#
#
# from Scoring import *
# obj = Scoring(path,data_dict)
#
# linear,tree =  obj.run()
