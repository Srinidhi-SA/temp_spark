from feature_engineering_helper import FeatureEngineeringHelper


class FeatureEngineering:

    def __init__(self, spark, df, dataframe_context, dataframe_helper, metaParserInstance, featureEngineeringDict):
        self._spark = spark
        self._df = df
        self._dataframe_context = dataframe_context
        self._dataframe_helper = dataframe_helper
        self._metaParserInstance = metaParserInstance
        self._featureEngineeringDict = featureEngineeringDict


    def feature_engineering(self):
        print "Performing Feature Engineering Operations"
        feature_engineering_helper_obj = FeatureEngineeringHelper(self._df,self._dataframe_helper)
        for settings in self._featureEngineeringDict['overall_settings']:
            if settings['name'] == "binning_all_measures" and settings['selected'] == True:
                self._df = feature_engineering_helper_obj.binning_all_measures(settings['number_of_bins'])

        for key in self._featureEngineeringDict['column_wise_settings'].keys():
            if self._featureEngineeringDict['column_wise_settings'][key]['selected']:
                if self._featureEngineeringDict['column_wise_settings'][key]['name'] == "creating_new_bins_or_levels":
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
                if self._featureEngineeringDict['column_wise_settings'][key]['name'] == "transformation_settings":
                    for operation in self._featureEngineeringDict['column_wise_settings'][key]['operations']:
                        if operation['selected']:
                            if operation['name'] == 'replace_values_with':
                                for column in operation['columns']:
                                    self._df = feature_engineering_helper_obj.replace_values_in_column(column["name"], column["replace_values_in_range"], column["replace_by"])
                            if operation['name'] == 'variable_transformation':
                                for column in operation['columns']:
                                    if column["transformation_type"] == "log_transform":
                                        self._df = feature_engineering_helper_obj.logTransform_column(column["name"])
                                    if column["transformation_type"] == "modulus_transform":
                                        self._df = feature_engineering_helper_obj.modulus_transform_column(column["name"])
                                    if column["transformation_type"] == "cube_root_transform":
                                        self._df = feature_engineering_helper_obj.cuberoot_transform_column(column["name"])
                                    if column["transformation_type"] == "square_root_transform":
                                        self._df = feature_engineering_helper_obj.squareroot_transform_column(column["name"])
                            if operation['name'] == 'encoding_dimensions':
                                for column in operation['columns']:
                                    if column["encoding_type"] == "label_encoding":
                                        self._df = feature_engineering_helper_obj.label_encoding_column(column["name"])
                                    if column["encoding_type"] == "one_hot_encoding":
                                        self._df = feature_engineering_helper_obj.onehot_encoding_column(column["name"])
                            if operation['name'] == 'return_character_count':
                                for column in operation['columns']:
                                    self._df = feature_engineering_helper_obj.character_count_string(column["name"])
                            if operation['name'] == 'is_custom_string_in':
                                for column in operation['columns']:
                                    self._df = feature_engineering_helper_obj.contains_word(column["name"], column["user_given_string"])
                            if operation['name'] == 'is_date_weekend':
                                for column in operation['columns']:
                                    self._df = feature_engineering_helper_obj.is_weekend(column["name"])
                            if operation['name'] == 'extract_time_feature':
                                for column in operation['columns']:
                                    self._df = feature_engineering_helper_obj.extract_datetime_info(column["name"], column["time_feature_to_extract"])
                            if operation['name'] == 'time_since':
                                for column in operation['columns']:
                                    self._df = feature_engineering_helper_obj.count_time_since(column["name"], column["time_since"])
                            if operation['name'] == 'perform_standardization':
                                for column in operation['columns']:
                                    if column["standardization_type"] == "standardization":
                                        self._df = feature_engineering_helper_obj.standardize_column(column["name"])
                                for column in operation['columns']:
                                    if column["standardization_type"] == "normalization":
                                        self._df = feature_engineering_helper_obj.normalize_column(column["name"])

        print "Feature Engineering Operations successfully Performed"
        return self._df
