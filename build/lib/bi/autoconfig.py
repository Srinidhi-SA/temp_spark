import pandas as pd
import random
import string
import json
import sys
class ModelParser(object):
    """
    Class used for creating model config
    """
    def __init__(self, target, app_type, train_data, label_level = None):
        self.label_level = label_level
        self.df = train_data
        self.target = target
        self.app_type = app_type
        self.model_name = "Model-" + ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
        self.apiConfig = {}
        self.apiConfig["config"] = {}
        self.apiConfig["config"]["COLUMN_SETTINGS"] = {}

    def run(self):
        """run functions responsible for generating model config"""
        self.apiConfig["config"]["COLUMN_SETTINGS"]['variableSelection'] = []
        self.column_settings()
        self.file_settings()
        self.job_config()
        return self.apiConfig

    def job_config(self):
        """
        Creates job config for model
        """
        if self.app_type == 'classification':
            app_id = 2
        else:
            app_id = 13
        self.apiConfig['job_config'] = {'job_type': 'training',
                                     'job_name': self.model_name,
                                     'app_id': app_id}


    def file_settings(self):
        """
        Creates file settings for model
        """
        if self.app_type == 'classification':
            targetLevel_label = self.label_level
        else:
            targetLevel_label = None
        self.apiConfig["config"]['FILE_SETTINGS'] = {'targetLevel': targetLevel_label,
         'app_type': self.app_type,
         'analysis_type': ['training'],
         'validationTechnique': [{'displayName': 'K Fold Validation',
           'value': 2,
           'name': 'kFold'}],
         'modelpath': [self.model_name]}

    def column_settings(self):
        """
        Generates train data column settings for model
        """
        for i in list(self.df.columns):
            if self.target == i:
                target_flag = True
            else:
                target_flag = False
            if self.df[i].dtype in [float, int]:
                datatype = "measure"
            else:
                datatype = "dimension"

            _dict = {'uidCol': False,
          'selected': True,
          'targetColumn': target_flag,
          'actualColumnType': datatype,
          'targetColSetVarAs': None,
          'polarity': None,
          'setVarAs': None,
          'dateSuggestionFlag': False,
          'columnType': datatype,
          'name': i}
            self.apiConfig["config"]["COLUMN_SETTINGS"]['variableSelection'].append(_dict)


class ScoreParser:
    """Class responsible for generating score config, uses model config and model results"""
    def __init__(self, training_path, prediction_algorithm,test_data):
        self.training_path = training_path
        self.prediction_algorithm = prediction_algorithm
        self.test_data = test_data
        self.classificationalgorithms = {'Logistic Regression': 'Logistic Regression',
                                         'Neural Network (TensorFlow)': 'Neural Network (TensorFlow)',
                                         'XGBoost': 'XGBoost',
                                         'Random Forest': 'Random Forest',
                                         'Naive Bayes': 'Naive Bayes',
                                         'Neural Network (Sklearn)': 'Neural Network (Sklearn)',
                                         'Neural Network (PyTorch)': 'Neural Network (PyTorch)',
                                         'LightGBM':'LightGBM'}
        self.regressionalgorithms = {'Random Forest Regression': 'RF Regression',
                                     'Gradient Boosted Tree Regression': 'GBT Regression',
                                     'Decision Tree Regression': 'DTREE Regression',
                                     'Linear Regression': 'Linear Regression'}
        self.apiConfig = {}
        self.job_name = "Score-" + ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
        self.apiConfig["config"] = {}
        self.apiConfig["config"]["COLUMN_SETTINGS"] = {}
        self.scorepath = self.job_name

    def read_json_file(self, pathfile):
        """
        Used to read json file from local path
        :param pathfile: path to the json file
        :return:
        """
        with open(pathfile, 'r') as json_file:
            file = json.load(json_file)
        return file

    def run(self):
        """run functions responsible for generating score config"""
        self.training_result = self.read_json_file(self.training_path+'/training_result.json')
        self.training_config = self.read_json_file(self.training_path+'/training_config.json')
        self.app_type = self.training_config["config"]["FILE_SETTINGS"]['app_type']
        if self.prediction_algorithm is None:
            if self.app_type == 'classification':
                self.prediction_algorithm = self.classificationalgorithms[self.training_result["Best_ALGO"]]
            else:
                self.prediction_algorithm = self.regressionalgorithms[self.training_result["Best_ALGO"]]

        self.apiConfig['config']['COLUMN_SETTINGS']['modelvariableSelection'] = self.training_config['config']['COLUMN_SETTINGS']['variableSelection']
        self.apiConfig["config"]["COLUMN_SETTINGS"]['variableSelection'] = self.apiConfig['config']['COLUMN_SETTINGS']['modelvariableSelection']
        data_validation_flag, validation_error = self.data_validation()
        if data_validation_flag:
            self.file_settings()
            self.apiConfig["config"]["Targettypecast"] = self.training_config["config"]["Targettypecast"]
            self.apiConfig["config"]['one_click'] = self.training_result['one_click']
            self.job_config()
            return self.apiConfig
        else:
            print(validation_error)
            sys.exit()

    def data_validation(self):
        """data validation module to check the sanity of test data"""
        train_column_settings = self.apiConfig["config"]["COLUMN_SETTINGS"]['variableSelection']
        test_column_type = {}
        for i in list(self.test_data.columns):
            if self.test_data[i].dtype in [float, int]:
                datatype = "measure"
            else:
                datatype = "dimension"
            test_column_type.update({i: datatype})

        train_column_type = {}
        for column in train_column_settings:
            train_column_type.update({column['name']: column['columnType']})
        train_columns = list(train_column_type.keys())
        target_column = [column['name'] for column in train_column_settings if column['targetColumn'] == True][0]
        train_columns.remove(target_column)
        test_columns = list(test_column_type.keys())

        data_validation_flag = True
        validation_error = None
        if set(test_columns) == set(train_columns):
            for column in test_columns:
                if test_column_type[column] != train_column_type[column]:
                    data_validation_flag = False
                    validation_error = "Columns type miss match in test data column {}".format(column)
                    break
        else:
            data_validation_flag = False
            validation_error = "One or more columns are not same in test data"

        return data_validation_flag, validation_error

    def job_config(self):
        """
        creates job config for score
        """
        if self.app_type == 'classification':
            app_id = 2
        else:
            app_id = 13
        self.apiConfig['job_config'] = {'job_type': 'prediction',
                                     'job_name': self.job_name,
                                     'app_id': app_id}

    def file_settings(self):
        """generates file settings for score config"""
        self.apiConfig["config"]['FILE_SETTINGS'] = {}
        self.apiConfig["config"]['FILE_SETTINGS']['selectedModel'] = [i for i in self.training_result['model_dropdown'] if i["name"] == self.prediction_algorithm]
        self.apiConfig["config"]['FILE_SETTINGS']['algorithmslug'] = [self.apiConfig["config"]['FILE_SETTINGS']['selectedModel'][0]['slug']]
        self.apiConfig["config"]['FILE_SETTINGS']['modelfeatures'] = self.training_result['config']['modelFeatures'][self.apiConfig["config"]['FILE_SETTINGS']['algorithmslug'][0]]
        self.apiConfig["config"]['FILE_SETTINGS']['levelcounts'] = self.training_result['config']['targetVariableLevelcount']
        if self.app_type == 'classification':
            self.apiConfig["config"]['FILE_SETTINGS']['labelMappingDict'] = [self.training_result['config']['labelMappingDict'][self.apiConfig["config"]['FILE_SETTINGS']['algorithmslug'][0]]]
        else:
            self.apiConfig["config"]['FILE_SETTINGS']['labelMappingDict'] = [None]
        self.apiConfig["config"]['FILE_SETTINGS']['analysis_type'] = ['score']
        self.apiConfig["config"]['FILE_SETTINGS']['targetLevel'] = self.training_config['config']['FILE_SETTINGS']['targetLevel']
        self.apiConfig["config"]['FILE_SETTINGS']['modelpath'] = self.training_config["config"]['FILE_SETTINGS']['modelpath']
        self.apiConfig["config"]['FILE_SETTINGS']['scorepath'] = [self.scorepath]
