# from bi.common.decorators import accepts
# from bi.common.dataframe import DataFrameHelper
import ast
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
        self.utf8columns = []
        self.considercolumns = []
        self.considercolumnstype = []
        self.measure_suggestions = []
        self.date_columns = []
        self.string_to_date_columns = {}
        self.MODELFEATURES = []
        self.appid = None
        self.considercolumnstype = None
        self.algorithmslug = []

    def set_model_path(self,data):
        self.MODEL_PATH = data

    def set_score_path(self,data):
        self.SCORE_PATH = data

    def set_params(self):
        self.FILE_SETTINGS = self._config_obj.get_file_settings()
        self.COLUMN_SETTINGS = self._config_obj.get_column_settings()
        fileSettingKeys = self.FILE_SETTINGS.keys()
        columnSettingKeys = self.COLUMN_SETTINGS.keys()
        # return {"file":self.FILE_SETTINGS,"column":self.COLUMN_SETTINGS}

        self.CSV_FILE =self.FILE_SETTINGS['inputfile'][0]
        if "narratives_file" in fileSettingKeys:
            self.NARRATIVES_FILE =self.FILE_SETTINGS['narratives_file'][0]
        if "result_file" in fileSettingKeys:
            self.RESULT_FILE =self.FILE_SETTINGS['result_file'][0]
        if "monitor_api" in fileSettingKeys:
            self.MONITOR_API =self.FILE_SETTINGS['monitor_api'][0]
        if "train_test_split" in fileSettingKeys:
            self.train_test_split =self.FILE_SETTINGS['train_test_split'][0]
        if "modelpath" in fileSettingKeys:
            self.MODEL_PATH =self.FILE_SETTINGS['modelpath'][0]
        if "scorepath" in fileSettingKeys:
            self.SCORE_PATH =self.FILE_SETTINGS['scorepath'][0]
        if "foldername" in fileSettingKeys:
            self.FOLDERS =self.FILE_SETTINGS['foldername'][0]
        if "modelname" in fileSettingKeys:
            self.MODELS =self.FILE_SETTINGS['modelname'][0]
        if "modelfeatures" in fileSettingKeys:
            self.MODELFEATURES =self.FILE_SETTINGS['modelfeatures'][0].split(self._column_separator)
        if "levelcounts" in fileSettingKeys:
            self.levelcounts =self.FILE_SETTINGS['levelcounts'][0].split(self._column_separator)
            self.levelcount_dict = dict([(self.levelcounts[i*2],self.levelcounts[i*2+1]) for i in range(len(self.levelcounts)/2)])
        if "script_to_run" in fileSettingKeys:
            self.scripts_to_run =self.FILE_SETTINGS.get('script_to_run')
        else:
            self.scripts_to_run = []
        if "algorithmslug" in fileSettingKeys:
            self.algorithmslug = self.FILE_SETTINGS.get('algorithmslug')
        if "app_id" in columnSettingKeys:
            self.appid = self.COLUMN_SETTINGS['app_id'][0].strip()
        if "result_column" in columnSettingKeys:
            self.resultcolumn = "{}".format(self.COLUMN_SETTINGS['result_column'][0].strip())
        if "analysis_type" in columnSettingKeys:
            self.analysistype = self.COLUMN_SETTINGS['analysis_type'][0].strip()
        if "ignore_column_suggestions" in columnSettingKeys:
            self.ignorecolumns = ["{}".format(col) for col in self.COLUMN_SETTINGS.get('ignore_column_suggestions')]
        if "utf8_columns" in columnSettingKeys:
            self.utf8columns = self.COLUMN_SETTINGS.get('utf8_columns')
        if self.ignorecolumns!=None:
            self.ignorecolumns = ["{}".format(col) for col in list(set(self.ignorecolumns)-set([self.resultcolumn]))]
        if "consider_columns" in columnSettingKeys:
            self.considercolumns = ["{}".format(col) for col in self.COLUMN_SETTINGS.get('consider_columns')]
        if "score_consider_columns" in columnSettingKeys:
            self.scoreconsidercolumns = self.COLUMN_SETTINGS.get('score_consider_columns')
        if "consider_columns_type" in columnSettingKeys:
            self.considercolumnstype = self.COLUMN_SETTINGS.get('consider_columns_type')

        if self.considercolumnstype == ["including"]:
            if self.resultcolumn != None and self.considercolumns != None:
                self.considercolumns.append(self.resultcolumn)
                self.considercolumns = list(set(self.considercolumns))


        if "date_columns" in columnSettingKeys:
            self.date_columns = ["{}".format(col) for col in self.COLUMN_SETTINGS.get('date_columns')]
        if "date_format" in columnSettingKeys:
            self.date_format = self.COLUMN_SETTINGS.get('date_format')
        if "measure_suggestions" in columnSettingKeys:
            self.measure_suggestions = self.COLUMN_SETTINGS.get('measure_suggestions')
        if "score_consider_columns_type" in columnSettingKeys:
            self.scoreconsidercolumnstype = self.COLUMN_SETTINGS.get('score_consider_columns_type')

        # self.dimension_filter = self._config_obj.get_dimension_filters()
        # self.measure_filter = self._config_obj.get_measure_filters()
        # self.date_filter = self._config_obj.get_date_filters()
        # self.string_to_date_columns = self._config_obj.get_date_settings()
    def get_algorithm_slug(self):
        return self.algorithmslug

    def get_column_separator(self):
        return self._column_separator

    def get_level_count_dict(self):
        return self.levelcount_dict

    def get_measure_suggestions(self):
        return self.measure_suggestions

    def get_scripts_to_run(self):
        return self.scripts_to_run

    def get_consider_columns_type(self):
        return self.considercolumnstype

    def get_score_consider_columns_type(self):
        return self.scoreconsidercolumnstype

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

    def get_score_consider_columns(self):
        return self.scoreconsidercolumns

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

    def get_app_id(self):
        return self.appid
