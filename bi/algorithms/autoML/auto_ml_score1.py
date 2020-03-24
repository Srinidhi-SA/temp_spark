import pandas as pd
import json
from bi.algorithms.autoML.data_validation import DataValidation
from bi.algorithms.autoML.data_preprocessing_auto_ml import DataPreprocessingAutoML
from bi.algorithms.autoML.feature_engineering_auto_ml import FeatureEngineeringAutoML
from bi.algorithms.autoML.feature_selection import FeatureSelection

class Scoring(object):

    def __init__(self, path, train_json):
        print ("Auto ML score Running "*10)
        self.data_frame = df
        self.train_json = train_json


    def run(self):
        if len(self.train_json['MeasureColsToDim']) > 0:
            DataPreprocessingAutoML_obj = DataPreprocessingAutoML(self.data_frame, None, {}, [], [], [], None)
            DataPreprocessingAutoML_obj.dimension_measure(self.train_json['MeasureColsToDim'])
            self.data_frame = DataPreprocessingAutoML_obj.self.data_frame
        if len(self.train_json['MeanImputeCols']) > 0:
            DataPreprocessingAutoML_obj = DataPreprocessingAutoML(self.data_frame, None, {}, [], [], [], None)
            DataPreprocessingAutoML_obj.measure_col_imputation(self.train_json['MeasureColsToDim'])
            self.data_frame = DataPreprocessingAutoML_obj.self.data_frame
        if len(self.train_json['ModeImputeCols']) > 0:
            DataPreprocessingAutoML_obj = DataPreprocessingAutoML(self.data_frame, None, {}, [], [], [], None)
            DataPreprocessingAutoML_obj.dim_col_imputation(self.train_json['MeasureColsToDim'])
            self.data_frame = DataPreprocessingAutoML_obj.self.data_frame
        if len(self.train_json['date_column_split']) > 0:
            FeatureEngineeringAutoML_obj = FeatureEngineeringAutoML(self.data_frame, None, {}, [], [], [], None)
            FeatureEngineeringAutoML_obj.date_column_split(self.train_json['date_column_split'])
            self.data_frame = FeatureEngineeringAutoML_obj.self.data_frame
        if len(self.train_json['one_hot_encoded']) > 0:
            FeatureEngineeringAutoML_obj = FeatureEngineeringAutoML(self.data_frame, None, {}, [], [], [], None)
            FeatureEngineeringAutoML_obj.one_hot_encoding(self.train_json['one_hot_encoded'])
            self.data_frame = FeatureEngineeringAutoML_obj.self.data_frame
        score_df = self.data_frame[self.train_json['SelectedColsTree']]
        return score_df, score_df
