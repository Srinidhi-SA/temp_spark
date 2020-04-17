import pandas as pd
import json
from bi.algorithms.autoML.data_validation import DataValidation
from bi.algorithms.autoML.data_preprocessing_auto_ml import DataPreprocessingAutoML
from bi.algorithms.autoML.feature_engineering_auto_ml import FeatureEngineeringAutoML
from bi.algorithms.autoML.feature_selection import FeatureSelection
from bi.algorithms import utils as MLUtils
class Scoring(object):

    def __init__(self, df, train_json):
        print ("Auto ML score Running "*10)
        self.data_frame = df
        self.train_json = train_json


    def run(self):
        if len(self.train_json['MeasureColsToDim']) > 0:
            DataPreprocessingAutoML_obj = DataPreprocessingAutoML(self.data_frame, None, {}, [], [], [], None)
            DataPreprocessingAutoML_obj.dimension_measure_test(self.train_json['MeasureColsToDim'])
            self.data_frame = DataPreprocessingAutoML_obj.data_frame
        if len(self.train_json['MeanImputeCols']) > 0:
            DataPreprocessingAutoML_obj = DataPreprocessingAutoML(self.data_frame, None, {}, [], [], [], None)
            DataPreprocessingAutoML_obj.measure_col_imputation(self.train_json['MeasureColsToDim'])
            self.data_frame = DataPreprocessingAutoML_obj.data_frame
        if len(self.train_json['ModeImputeCols']) > 0:
            DataPreprocessingAutoML_obj = DataPreprocessingAutoML(self.data_frame, None, {}, [], [], [], None)
            DataPreprocessingAutoML_obj.dim_col_imputation(self.train_json['MeasureColsToDim'])
            DataPreprocessingAutoML_obj.test_data_imputation()
            self.data_frame = DataPreprocessingAutoML_obj.data_frame
        if len(self.train_json['date_column_split']) > 0:
            FeatureEngineeringAutoML_obj = FeatureEngineeringAutoML(self.data_frame, None, {}, [], [], [], None)
            FeatureEngineeringAutoML_obj.date_column_split(self.train_json['date_column_split'])
            self.data_frame = FeatureEngineeringAutoML_obj.data_frame
        if len(self.train_json['one_hot_encoded']) > 0:
            FeatureEngineeringAutoML_obj = FeatureEngineeringAutoML(self.data_frame, None, {}, [], [], [], None)
            FeatureEngineeringAutoML_obj.sk_one_hot_encoding(self.train_json['one_hot_encoded'])
            self.data_frame = FeatureEngineeringAutoML_obj.data_frame
        #score_df = self.data_frame[list(set(self.train_json['SelectedColsTree'])-set(self.train_json['target']))]
        final_list_linear=self.train_json['SelectedColsLinear']
        final_list_tree=self.train_json['SelectedColsTree']
        final_list_linear.remove(self.train_json['target'])
        final_list_tree.remove(self.train_json['target'])
        score_df_linear = MLUtils.fill_missing_columns(self.data_frame,final_list_linear,self.train_json['target'])
        score_df_tree = MLUtils.fill_missing_columns(self.data_frame,final_list_tree,self.train_json['target'])
        return score_df_linear, score_df_tree
