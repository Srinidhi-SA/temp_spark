from pyspark.sql import DataFrame
from pyspark.sql import functions as FN
from pyspark.sql.functions import UserDefinedFunction
from pyspark.sql import SQLContext

from bi.common.decorators import accepts
from bi.common import BIException
from bi.common import DataFrameHelper
from bi.common.datafilterer import DataFrameFilterer
from bi.common.results import DecisionTreeResult
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
import xgboost as xgb
from statistics import mean,median,mode,pstdev

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_extraction import DictVectorizer as DV
from sklearn import datasets, linear_model, cross_validation, grid_search
from sklearn.metrics import roc_curve, auc
from sklearn.feature_selection import RFECV


class RandomForest:
    def __init__(self, data_frame, data_frame_helper, spark):
        # self._spark = spark
        # self.data_frame = data_frame.toPandas()
        # self._measure_columns = data_frame_helper.get_numeric_columns()
        # self._dimension_columns = data_frame_helper.get_string_columns()
        # self.classifier = initiate_forest_classifier(10,5)
        print "RANDOM FOREST INITIALIZATION DONE"

    def initiate_forest_classifier(self,n_estimators,max_features):
        clf = RandomForestClassifier(n_estimators=n_estimators,
                                         max_features = max_features,
        #                                  max_depth=None,
                                         min_samples_split = 10,
        #                                  min_samples_leaf=1,
        #                                  min_weight_fraction_leaf=0,
                                         max_leaf_nodes=None,
                                         warm_start=True,
                                         random_state=0,
                                         n_jobs=-1,
        #                                  oob_score = True,
    #                                      verbose= True
                                    )

        return clf
