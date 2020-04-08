import pandas as pd
from bi.algorithms.autoML.data_validation import DataValidation
from bi.algorithms.autoML.data_preprocessing_auto_ml import DataPreprocessingAutoML
from bi.algorithms.autoML.feature_engineering_auto_ml import FeatureEngineeringAutoML
from bi.algorithms.autoML.feature_selection import FeatureSelection
import time as time
import json
from bi.common import utils as CommonUtils

class AutoMl:

    def __init__(self, df, dataframe_context, app_type):
        print ("Auto ML train Running "*10)

        self.df = df
        self.target = dataframe_context.get_result_column()
        self.app_type = app_type
        self.final_json = {}
        self.tree_df = None
        self.linear_df = None
        self.LOGGER = dataframe_context.get_logger()
        self.errorURL = dataframe_context.get_error_url()
        self.ignoreMsg = dataframe_context.get_message_ignore()

    def run(self):
        try:
            DataValidation_obj = DataValidation(self.df, self.target, self.app_type)
            DataValidation_obj.data_validation_run()
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(self.LOGGER, "datavalidation", e)
            CommonUtils.save_error_messages(self.errorURL, self.app_type, e, ignore=self.ignoreMsg)
        try:
            DataPreprocessingAutoML_obj = DataPreprocessingAutoML(DataValidation_obj.data_frame, DataValidation_obj.target, DataValidation_obj.data_change_dict, DataValidation_obj.numeric_cols, DataValidation_obj.dimension_cols, DataValidation_obj.datetime_cols,DataValidation_obj.problem_type)
            DataPreprocessingAutoML_obj.data_preprocessing_run()
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(self.LOGGER, "dataPreprocessing", e)
            CommonUtils.save_error_messages(self.errorURL, self.app_type, e, ignore=self.ignoreMsg)
        try:
            FeatureEngineeringAutoML_obj = FeatureEngineeringAutoML(DataPreprocessingAutoML_obj.data_frame, DataPreprocessingAutoML_obj.target, DataPreprocessingAutoML_obj.data_change_dict, DataPreprocessingAutoML_obj.numeric_cols, DataPreprocessingAutoML_obj.dimension_cols, DataPreprocessingAutoML_obj.datetime_cols, DataPreprocessingAutoML_obj.problem_type)
            FeatureEngineeringAutoML_obj.feature_engineering_run()
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(self.LOGGER, "Feature Engineering", e)
            CommonUtils.save_error_messages(self.errorURL, self.app_type, e, ignore=self.ignoreMsg)
        try:
            FeatureSelection_obj = FeatureSelection(FeatureEngineeringAutoML_obj.data_frame, FeatureEngineeringAutoML_obj.target, FeatureEngineeringAutoML_obj.data_change_dict, FeatureEngineeringAutoML_obj.numeric_cols, FeatureEngineeringAutoML_obj.dimension_cols, FeatureEngineeringAutoML_obj.datetime_cols, FeatureEngineeringAutoML_obj.problem_type)
            cols_considered_linear = FeatureSelection_obj.feat_importance_linear()
            cols_considered_tree = FeatureSelection_obj.feat_importance_tree()
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(self.LOGGER, "Feature Selection", e)
            CommonUtils.save_error_messages(self.errorURL, self.app_type, e, ignore=self.ignoreMsg)
        self.df = FeatureEngineeringAutoML_obj.data_frame
        self.linear_df = self.df[cols_considered_linear]
        self.tree_df=self.df[cols_considered_tree]
        self.final_json = json.dumps(FeatureSelection_obj.data_change_dict)
        return self.final_json, self.linear_df, self.tree_df
