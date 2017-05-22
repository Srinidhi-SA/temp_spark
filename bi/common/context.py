
from pyspark.sql.dataframe import DataFrame
from bi.parser import configparser

# from bi.common.decorators import accepts
# from bi.common.dataframe import DataFrameHelper

class ContextSetter:

    MEASUREC_COLUMNS = "measure_columns"
    DIMENSION_COLUMNS = "dimension_columns"
    TIME_DIMENSION_COLUMNS = "time_dimension_columns"
    NULL_VALUES = 'num_nulls'
    NON_NULL_VALUES = 'num_non_nulls'

    def __init__(self, config_obj):
        self._config_obj = config_obj
        self._column_separator = "|~|"
        self.CSV_FILE = ""
        self.RESULT_FILE = ""
        self.NARRATIVES_FILE = ""
        self.resultcolumn = ""
        self.MONITOR_API = ""
        self.analysistype = ""
        self.ignorecolumns = []
        self.MODELFEATURES = []

    def set_params(self):
        self.FILE_SETTING_KEYS = self._config_obj.get_file_settings()
        file_setting_keys = self.FILE_SETTING_KEYS.keys()
        self.CSV_FILE = self._config_obj.get_file_settings()['inputfile'][0]
        if "narratives_file" in file_setting_keys:
            self.NARRATIVES_FILE = self._config_obj.get_file_settings()['narratives_file'][0]
        if "result_file" in file_setting_keys:
            self.RESULT_FILE = self._config_obj.get_file_settings()['result_file'][0]
        if "monitor_api" in file_setting_keys:
            self.MONITOR_API = self._config_obj.get_file_settings()['monitor_api'][0]
        if "train_test_split" in file_setting_keys:
            self.train_test_split = self._config_obj.get_file_settings()['train_test_split'][0]
        if "modelpath" in file_setting_keys:
            self.MODEL_PATH = self._config_obj.get_file_settings()['modelpath'][0]
        if "scorepath" in file_setting_keys:
            self.SCORE_PATH = self._config_obj.get_file_settings()['scorepath'][0]
        if "foldername" in file_setting_keys:
            self.FOLDERS = self._config_obj.get_file_settings()['foldername'][0]
        if "modelname" in file_setting_keys:
            self.MODELS = self._config_obj.get_file_settings()['modelname'][0]
        if "modelfeatures" in file_setting_keys:
            self.MODELFEATURES = self._config_obj.get_file_settings()['modelfeatures'][0].split(self._column_separator)

        self.resultcolumn = self._config_obj.get_column_settings()['result_column'][0].strip()
        self.analysistype = self._config_obj.get_column_settings()['analysis_type'][0].strip()
        self.ignorecolumns = self._config_obj.get_column_settings().get('ignore_column_suggestions')
        self.utf8columns = self._config_obj.get_column_settings().get('utf8_columns')

        if self.ignorecolumns!=None:
            self.ignorecolumns = list(set(self.ignorecolumns)-set([self.resultcolumn]))
        self.considercolumns = self._config_obj.get_column_settings().get('consider_columns')
        if not self.considercolumns == None:
            if not self.resultcolumn == None:
                self.considercolumns.append(self.resultcolumn)
                self.considercolumns = list(set(self.considercolumns))

        self.dimension_filter = self._config_obj.get_dimension_filters()
        self.measure_filter = self._config_obj.get_measure_filters()
        self.date_filter = self._config_obj.get_date_filters()
        self.string_to_date_columns = self._config_obj.get_date_settings()
        self.considercolumnstype = self._config_obj.get_column_settings().get('consider_columns_type')
        self.scripts_to_run = self._config_obj.get_file_settings().get('script_to_run')
        self.date_columns = self._config_obj.get_column_settings().get('date_columns')
        self.date_format = self._config_obj.get_column_settings().get('date_format')
        self.measure_suggestions = self._config_obj.get_column_settings().get('measure_suggestions')

    def get_measure_suggestions(self):
        return self.measure_suggestions

    def get_scripts_to_run(self):
        return self.scripts_to_run

    def get_consider_columns_type(self):
        return self.considercolumnstype

    def get_input_file(self):
        return self.CSV_FILE

    def get_narratives_file(self):
        return self.NARRATIVES_FILE

    def get_result_file(self):
        return self.RESULT_FILE

    def get_result_column(self):
        return self.resultcolumn

    def get_monitor_api(self):
        return self.MONITOR_API

    def get_analysis_type(self):
        return self.analysistype

    def get_consider_columns(self):
        return self.considercolumns

    def get_ignore_column_suggestions(self):
        return self.ignorecolumns

    def get_utf8_columns(self):
        return self.utf8columns

    def get_dimension_filters(self):
        return self.dimension_filter

    def get_measure_filters(self):
        return self.measure_filter

    def get_date_settings(self):
        return self.string_to_date_columns

    def get_column_subset(self):
        return self.considercolumns

    def get_date_filters(self):
        return self.date_filter

    def get_date_column_suggestions(self):
        return self.date_columns

    def get_requested_date_format(self):
        return self.date_format

    def get_train_test_split(self):
        return self.train_test_split

    def get_model_path(self):
        return self.MODEL_PATH

    def get_score_path(self):
        return self.SCORE_PATH

    def get_model_features(self):
        return self.MODELFEATURES
