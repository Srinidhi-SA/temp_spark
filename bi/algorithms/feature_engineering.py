from feature_engineering_helper import FeatureEngineeringHelper


class FeatureEngineering:

    def __init__(self, spark, df, dataframe_context, dataframe_helper, metaParserInstance, dataCleansingDict, featureEngineeringDict):
        self._spark = spark
        self._df = df
        self._dataframe_context = dataframe_context
        self._dataframe_helper = dataframe_helper
        self._metaParserInstance = metaParserInstance
        self._dataCleansingDict = dataCleansingDict
        self._featureEngineeringDict = featureEngineeringDict


    def feature_engineering(self):
        print "Performing Feature Engineering Operations"
        feature_engineering_helper_obj = FeatureEngineeringHelper(self._df)
        for settings in self._featureEngineeringDict['overall_settings']:
            if settings['name'] == "binning_all_measures" and settings['selected'] == True:
                self._df = feature_engineering_helper_obj.binning_all_measures()

        for key in self._featureEngineeringDict['column_wise_settings'].keys():
            if self._featureEngineeringDict['column_wise_settings'][key]['selected']:
                if self._featureEngineeringDict['column_wise_settings'][key]['name'] == "Creating_New_Bins_or_Levels":
                    for operation in self._featureEngineeringDict['column_wise_settings'][key]['operations']:
                        if operation['selected']:
                            if operation['name'] == 'create_equal_sized_bins':
                                for column in operation['columns']:
                                    self._df = feature_engineering_helper_obj.create_equal_sized_measure_bins(column["name"], column["number_of_bins"])
                            if operation['name'] == 'create_custom_bins':
                                for column in operation['columns']:
                                    self._df = feature_engineering_helper_obj.create_custom_measure_bins(column["name"], column["list_of_intervals"])
                            if operation['name'] == 'create_new_levels':
                                for column in operation['columns']:
                                    self._df = feature_engineering_helper_obj.create_new_levels_dimension(column["name"], column["mapping_dict"])
                            if operation['name'] == 'create_new_datetime_levels':
                                for column in operation['columns']:
                                    self._df = feature_engineering_helper_obj.create_new_levels_datetimes(column["name"], column["mapping_dict"])

                    #call respective function
                if self._featureEngineeringDict['columns_wise_settings'][key]['name'] == "Transformation_Settings":
                    for operation in self._featureEngineeringDict['columns_wise_settings'][key]['operations']:
                        if operation['selected']:
                            if operation['name'] == 'Replace_Values_With':
                                for column in operation['columns']:
                                    self._df = feature_engineering_helper_obj.replace_values_in_column(column["name"], column["replace_values_in_range"], column["replace_by"])
                            if operation['name'] == 'Variable_Transformation':
                                for column in operation['columns']:
                                    self._df = feature_engineering_helper_obj.logTransform_column(column["name"])
                            if operation['name'] == 'Encoding_Dimensions':
                                for column in operation['columns']:
                                    self._df = feature_engineering_helper_obj.label_encoding_column(column["name"])
                            if operation['name'] == 'return_character_count':
                                for column in operation['columns']:
                                    self._df = feature_engineering_helper_obj.character_count_string(column["name"])
                            if operation['name'] == 'is_custom_string_in':
                                for column in operation['columns']:
                                    self._df = feature_engineering_helper_obj.contains_word(column["name"], column["User_given_character"])
                            if operation['name'] == 'is_date_weekend':
                                for column in operation['columns']:
                                    self._df = feature_engineering_helper_obj.is_weekend(column["name"])
                            if operation['name'] == 'extract_time_feature':
                                for column in operation['columns']:
                                    self._df = feature_engineering_helper_obj.extract_datetime_info(column["name"], column["time_feature_to_extract"])
                            if operation['name'] == 'time_since':
                                for column in operation['columns']:
                                    self._df = feature_engineering_helper_obj.count_time_since(column["name"], column["time_since"])
                            if operation['name'] == 'Perform_Standardization':
                                for column in operation['columns']:
                                    self._df = feature_engineering_helper_obj.standardize_column(column["name"])

        print "Feature Engineering Operations successfully Performed"
        return self._df
