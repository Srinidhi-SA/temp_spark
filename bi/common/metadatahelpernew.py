
import random
import math
import datetime as dt
import pandas as pd

from pyspark.ml.feature import Bucketizer
from pyspark.sql.types import DoubleType
from pyspark.sql import functions as FN
from pyspark.sql.functions import udf, col
from pyspark.sql.types import DateType, FloatType
from pyspark.sql.types import StringType

from bi.common import utils as CommonUtils

class MetaDataHelper():

    def __init__(self, data_frame, transform = 0):
        self._file_name = file_name
        self._data_frame = data_frame
        if transform==1:
            self.transform_numeric_column()


    def get_binned_stat(self,df,colname,col_stat,n_split = 10):

        splits  = CommonUtils.frange(col_stat["min"],col_stat["max"],num_steps=n_split)
        splits = sorted(splits)
        splits_range = [(splits[idx],splits[idx+1]) for idx in range(len(splits)-1)]

        splits_data = {"splits":splits,"splits_range":splits_range}
        splits = splits_data["splits"]
        double_df = df.withColumn(colname, df[colname].cast(DoubleType()))
        bucketizer = Bucketizer(inputCol=colname,outputCol="BINNED_INDEX")
        bucketizer.setSplits(splits)
        binned_df = bucketizer.transform(double_df)
        histogram_df = binned_df.groupBy("BINNED_INDEX").count().toPandas()

        str_splits_range = [" to ".join([str(x[0]),str(x[1])]) for x in splits_range]
        bin_name_dict = dict(zip(range(len(splits_range)),str_splits_range))
        bin_name_dict[n_split] = "null"
        histogram_df["orderIndex"] = histogram_df["BINNED_INDEX"].apply(lambda x: n_split if pd.isnull(x) else x)
        histogram_df["bins"] = histogram_df["orderIndex"].apply(lambda x:bin_name_dict[int(x)])
        relevant_df = histogram_df[["bins","count","orderIndex"]]
        histogram_dict = relevant_df.T.to_dict().values()
        histogram_dict = sorted(histogram_dict,key=lambda x:x["orderIndex"])
        output = []
        for val in histogram_dict:
            output.append({"name":val["bins"],"value":val["count"]})
        return output

    def calculate_measure_column_stats(self,df,measure_columns):
        df = df.select(measure_columns)
        total_count = df.count()
        output = {}
        chart_data = {}
        summary_df = df.describe().toPandas()
        for column in measure_columns:
            col_stat = dict(zip(summary_df["summary"],summary_df[column]))
            for k,v in col_stat.items():
                if "." in v:
                    col_stat[k] = float(v)
                else:
                    col_stat[k] = int(v)
            col_stat["numberOfNulls"] = total_count - int(col_stat["count"])
            col_stat["numberOfNotNulls"] = col_stat["count"]
            col_stat["numberOfUniqueValues"] = df.select(column).distinct().count()
            chart_data[column] = self.get_binned_stat(df,column,col_stat)
            output[column] = col_stat
        return output,chart_data

    def calculate_dimension_column_stats(self,df,dimension_columns):
        df = df.select(dimension_columns)
        total_count = df.count()
        output = {}
        chart_data = {}
        summary_df = df.describe().toPandas()
        for column in dimension_columns:
            col_stat = {}
            col_stat["LevelCount"] = df.groupBy(column).count().toPandas().set_index(column).to_dict().values()[0]

            if None in col_stat["LevelCount"].keys():
                col_stat["numberOfNulls"] = col_stat["LevelCount"][None]
                col_stat["numberOfNotNulls"] = total_count - col_stat["numberOfNulls"]
            else:
                col_stat["numberOfNulls"] = 0
                col_stat["numberOfNotNulls"] = total_count - col_stat["numberOfNulls"]
            col_stat["numberOfUniqueValues"] = len(col_stat["LevelCount"].keys())
            levelCountWithoutNull = col_stat["LevelCount"]
            dimension_chart_data = [{"name":k,"value":v} if k != None else {"name":"null","value":v} for k,v in col_stat["LevelCount"].items()]
            dimension_chart_data_sorted = sorted(dimension_chart_data,key=lambda x:x["value"])
            if None in col_stat["LevelCount"]:
                levelCountWithoutNull.pop(None)
            col_stat["MaxLevel"] = max(levelCountWithoutNull,key=col_stat["LevelCount"].get)
            col_stat["MinLevel"] = min(levelCountWithoutNull,key=col_stat["LevelCount"].get)
            output[column] = col_stat
            chart_data[column] = dimension_chart_data_sorted
        return output,chart_data
