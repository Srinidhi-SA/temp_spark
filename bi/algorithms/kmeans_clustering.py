from pyspark.sql import DataFrame
from pyspark.sql import functions as FN
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark.ml.feature import StringIndexer, VectorIndexer, VectorAssembler, SQLTransformer
from pyspark.ml.feature import MinMaxScaler,StandardScaler
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.linalg import Vectors
from pyspark.ml.clustering import KMeans

from bi.common import DataFrameHelper
from bi.common import utils as CommonUtils
from bi.algorithms import utils as MLUtils

import time
import math
import random
import itertools
from datetime import datetime
from datetime import timedelta
from collections import Counter



class KmeansClustering:
    def __init__(self, data_frame, df_helper, df_context, spark):
        # self._spark = spark
        self._data_frame = data_frame
        print "KMEANS INITIALIZATION DONE"
        self._kmeans_result = {}
        self._max_cluster = 5
        self._predictedData = None

    def kmeans_pipeline(self,inputCols,cluster_count=None,max_cluster=None):
        if max_cluster != None:
            self._max_cluster = max_cluster

        assembler = VectorAssembler(inputCols = inputCols, outputCol = "features")
        assembled = assembler.transform(self._data_frame)
        mmScaler = StandardScaler(inputCol="features", outputCol="featuresCol",withStd=True, withMean=False)
        scale_model = mmScaler.fit(assembled)
        vectorized_data = scale_model.transform(assembled)

        if cluster_count == None:
            cluster_count_array = range(2,self._max_cluster)
            wssse_output = []
            for n_cluster in cluster_count_array:
                kmeans = KMeans().setK(n_cluster).setSeed(1)
                kmeans_model = kmeans.fit(vectorized_data)
                wssse = kmeans_model.computeCost(vectorized_data)
                wssse_output.append(wssse)
            wssse_dict = dict(zip(cluster_count_array,wssse_output))

            cluster_count = min(wssse_dict,key = wssse_dict.get)
            kmeans = KMeans().setK(cluster_count).setSeed(1)
            kmeans_model = kmeans.fit(vectorized_data)
            wssse = kmeans_model.computeCost(vectorized_data)
            centers = kmeans_model.clusterCenters()
            cluster_prediction = kmeans_model.transform(vectorized_data)
        else:
            wssse_dict = {}
            kmeans = KMeans().setK(cluster_count).setSeed(1)
            kmeans_model = kmeans.fit(vectorized_data)
            wssse = kmeans_model.computeCost(vectorized_data)
            centers = kmeans_model.clusterCenters()
            cluster_prediction = kmeans_model.transform(vectorized_data)

        self._kmeans_result["cluster_count"] = cluster_count
        self._kmeans_result["wssse"] = wssse
        self._kmeans_result["wssse_dict"] = wssse_dict
        self._kmeans_result["centers"] = centers
        self._kmeans_result["cluster_count"] = cluster_count
        self._kmeans_result["inputCols"] = inputCols
        self._predictedData = cluster_prediction

    def get_kmeans_result(self):
        return self._kmeans_result

    def get_prediction_data(self):
        return self._predictedData
