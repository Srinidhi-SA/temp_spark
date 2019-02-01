from data_preprocessing_helper import DataPreprocessingHelper


class DataPreprocessing:

    def __init__(self,spark,df,dataframe_context,dataframe_helper,metaParserInstance,dataCleansingDict,featureEngineeringDict):
        self._spark = spark
        self._df = df
        self._dataframe_context = dataframe_context
        self._dataframe_helper = dataframe_helper
        self._metaParserInstance = metaParserInstance
        self._dataCleansingDict = dataCleansingDict
        self._featureEngineeringDict = featureEngineeringDict

    def data_cleansing(self):
        print "Cleaning The Data"
        data_preprocessing_helper_obj = DataPreprocessingHelper(self._df)
        for settings in self._dataCleansingDict['overall_settings']:
            if settings['name'] == "duplicate_row" and settings['selected'] == True:
                self._df = data_preprocessing_helper_obj.drop_duplicate_rows()
            if settings['name'] == "duplicate_column" and settings['selected'] == True:
                self._df = data_preprocessing_helper_obj.drop_duplicate_cols()

        for key in self._dataCleansingDict['columns_wise_settings'].keys():
            if self._dataCleansingDict['columns_wise_settings'][key]['selected']:
                if self._dataCleansingDict['columns_wise_settings'][key]['name'] == "missing_value_treatment":
                    for operation in self._dataCleansingDict['columns_wise_settings'][key]['operations']:
                        if operation['selected']:
                            if operation['name'] == 'remove_observations':
                                for column in operation['columns']:
                                    self._df = data_preprocessing_helper_obj.remove_missing_values(column["name"])
                            if operation['name'] == 'mean_imputation':
                                for column in operation['columns']:
                                    self._df = data_preprocessing_helper_obj.mean_impute_missing_values(column["name"])
                            if operation['name'] == 'median_imputation':
                                for column in operation['columns']:
                                    self._df = data_preprocessing_helper_obj.median_impute_missing_values(column["name"])
                            if operation['name'] == 'mode_imputation':
                                for column in operation['columns']:
                                    self._df = data_preprocessing_helper_obj.mode_impute_missing_values(column["name"])
                            if operation['name'] == 'user_imputation':
                                for column in operation['columns']:
                                    self._df = data_preprocessing_helper_obj.user_impute_missing_values(column["name"], column["mvt_value"])


                    #call respective function
                if self._dataCleansingDict['columns_wise_settings'][key]['name'] == "outlier_treatment":
                    for operation in self._dataCleansingDict['columns_wise_settings'][key]['operations']:
                        if operation['selected']:
                            if operation['name'] == 'remove_outliers':
                                for column in operation['columns']:
                                    self._df = data_preprocessing_helper_obj.remove_outliers(column["name"], column['ol_lower_range'], column['ol_upper_range'])
                            if operation['name'] == 'replace_with_mean':
                                for column in operation['columns']:
                                    self._df = data_preprocessing_helper_obj.mean_impute_outliers(column["name"], column['ol_lower_range'], column['ol_upper_range'])
                            if operation['name'] == 'replace_with_median':
                                for column in operation['columns']:
                                    self._df = data_preprocessing_helper_obj.median_impute_outliers(column["name"], column['ol_lower_range'], column['ol_upper_range'])
                            if operation['name'] == 'replace_with_mode':
                                for column in operation['columns']:
                                    self._df = data_preprocessing_helper_obj.mode_impute_outliers(column["name"], column['ol_lower_range'], column['ol_upper_range'])

        print "Data Cleaning Completed"
        return self._df
