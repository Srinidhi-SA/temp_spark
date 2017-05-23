from pyspark.sql import DataFrame
from pyspark.sql import functions as FN
from pyspark.sql.functions import UserDefinedFunction
from pyspark.sql import SQLContext

from bi.common.decorators import accepts
from bi.common import BIException
from bi.common import DataFrameHelper
from bi.common.datafilterer import DataFrameFilterer
from bi.common import utils

import time
import math
import random
import itertools
from datetime import datetime
from datetime import timedelta
from collections import Counter

import numpy as np
import pandas as pd

from sklearn.linear_model import LogisticRegression as Logit
from sklearn.feature_extraction import DictVectorizer as DV
from sklearn import linear_model, cross_validation, grid_search
from sklearn.metrics import roc_curve, auc
from sklearn.feature_selection import RFECV
from bi.algorithms import utils as MLUtils


class LogisticRegression:
    def __init__(self, data_frame, data_frame_helper, spark):
        # self._spark = spark
        # self.data_frame = data_frame.toPandas()
        # self._measure_columns = data_frame_helper.get_numeric_columns()
        # self._dimension_columns = data_frame_helper.get_string_columns()
        # self.classifier = initiate_forest_classifier(10,5)
        print "LOGSTIC REGRESSION INITIALIZATION DONE"
        self._levels = None

    def set_number_of_levels(self,levels):
        self._levels = levels

    def initiate_logistic_regression_classifier(self):
        if len(self._levels) > 2:
            clf = Logit(multi_class = 'multinomial', solver = 'newton-cg')
        else:
            clf = Logit()
        return clf

    def train_and_predict(self,x_train, x_test, y_train, y_test,clf,drop_cols):
        """
        Output is a dictionary
        y_prob => Array probability values for prediction
        feature_importance => features ranked by their Importance
        feature_Weight => weight of features
        """
        if len(drop_cols) > 0:
            x_train = drop_columns(x_train,drop_cols)
            x_test = drop_columns(x_test,drop_cols)
        clf.fit(x_train, y_train)
        y_score = clf.predict(x_test)
        y_prob = clf.predict_proba(x_test)
        y_prob = [0]*len(y_score)

        # importances = clf.feature_importances_
        # feature_importance = clf.feature_importances_.argsort()[::-1]
        # imp_cols = [x_train.columns[x] for x in feature_importance]
        # feature_importance = dict(zip(imp_cols,importances))
        feature_importance = {}

        return {"trained_model":clf,"actual":y_test,"predicted":y_score,"probability":y_prob,"feature_importance":feature_importance}

    def predict(self,x_test,trained_model,drop_cols):
        """
        """
        if len(drop_cols) > 0:
            x_test = MLUtils.drop_columns(x_test,drop_cols)
        y_score = trained_model.predict(x_test)
        y_prob = trained_model.predict_proba(x_test)
        y_prob = MLUtils.calculate_predicted_probability(y_prob)
        x_test['responded'] = y_score
        return {"predicted_class":y_score,"predicted_probability":y_prob}
