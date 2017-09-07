
import random
import math
from datetime import datetime
import pandas as pd

from pyspark.ml.feature import Bucketizer
from pyspark.sql.types import DoubleType
from pyspark.sql import functions as FN
from pyspark.sql.functions import udf, col
from pyspark.sql.types import DateType, FloatType
from pyspark.sql.types import StringType

from bi.common import utils as CommonUtils

class MetaDataHelper():

    def __init__(self, data_frame):
        # self._file_name = file_name
        self._data_frame = data_frame
        # if transform==1:
            # self.transform_numeric_column()


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
        displayNameDict = {"count":"Count",
                            "mean":"Mean",
                            "stddev":"Standard Deviation",
                            "min":"Min",
                            "max":"Max",
                            "numberOfNulls":"Null Values",
                            "numberOfUniqueValues":"Unique Values",
                            "numberOfNotNulls":"Not Nulls"
                            }
        for column in measure_columns:
            col_stat = dict(zip(summary_df["summary"],summary_df[column]))
            for k,v in col_stat.items():
                if "." in v:
                    col_stat[k] = round(float(v),2)
                else:
                    col_stat[k] = int(v)
            col_stat["numberOfNulls"] = total_count - int(col_stat["count"])
            col_stat["numberOfNotNulls"] = col_stat["count"]
            col_stat["numberOfUniqueValues"] = df.select(column).distinct().count()
            chart_data[column] = self.get_binned_stat(df,column,col_stat)
            modified_col_stat = []
            for k,v in col_stat.items():
                if k != "numberOfNotNulls":
                    modified_col_stat.append({"name":k,"value":v,"display":True,"displayName":displayNameDict[k]})
                else:
                    modified_col_stat.append({"name":k,"value":v,"display":False,"displayName":displayNameDict[k]})
            output[column] = modified_col_stat
        return output,chart_data

    def calculate_dimension_column_stats(self,df,dimension_columns):
        df = df.select(dimension_columns)
        total_count = df.count()
        output = {}
        chart_data = {}
        summary_df = df.describe().toPandas()
        displayNameDict = {"count":"Count",
                            "mean":"Mean",
                            "stddev":"Standard Deviation",
                            "min":"Min",
                            "max":"Max",
                            "numberOfNulls":"Null Values",
                            "numberOfUniqueValues":"Unique Values",
                            "numberOfNotNulls":"Not Nulls",
                            "MaxLevel":"Max Level",
                            "MinLevel":"Min Level",
                            "LevelCount":"LevelCount"
                            }
        for column in dimension_columns:
            col_stat = {}
            levelCount = df.groupBy(column).count().toPandas().set_index(column).to_dict().values()[0]
            col_stat["LevelCount"] = levelCount
            if None in levelCount.keys():
                col_stat["numberOfNulls"] = levelCount[None]
                col_stat["numberOfNotNulls"] = total_count - col_stat["numberOfNulls"]
            else:
                col_stat["numberOfNulls"] = 0
                col_stat["numberOfNotNulls"] = total_count - col_stat["numberOfNulls"]
            col_stat["numberOfUniqueValues"] = len(levelCount.keys())
            levelCountWithoutNull = levelCount
            dimension_chart_data = [{"name":k,"value":v} if k != None else {"name":"null","value":v} for k,v in levelCount.items()]
            dimension_chart_data_sorted = sorted(dimension_chart_data,key=lambda x:x["value"])
            if None in levelCount:
                levelCountWithoutNull.pop(None)
            if levelCountWithoutNull != {}:
                col_stat["MaxLevel"] = max(levelCountWithoutNull,key=levelCount.get)
                col_stat["MinLevel"] = min(levelCountWithoutNull,key=levelCount.get)
            else:
                col_stat["MaxLevel"] = None
                col_stat["MinLevel"] = None
            modified_col_stat = []
            for k,v in col_stat.items():
                if k not in ["LevelCount","min","max","mean","stddev","numberOfNotNulls"]:
                    modified_col_stat.append({"name":k,"value":v,"display":True,"displayName":displayNameDict[k]})
                else:
                    modified_col_stat.append({"name":k,"value":v,"display":False,"displayName":displayNameDict[k]})
            output[column] = modified_col_stat
            chart_data[column] = dimension_chart_data_sorted
        return output,chart_data


    def get_datetime_suggestions(self,df,col_name):
        output = {}
        date_time_suggestions = {}
        formats = CommonUtils.dateTimeFormatsSupported()["formats"]
        dual_checks = CommonUtils.dateTimeFormatsSupported()["dual_checks"]
        row_vals = df.select(col_name).distinct().na.drop().collect()
        # row_vals = df.select(dims).na.drop().take(int(self.total_rows**0.5 + 1))
        if len(row_vals) > 0:
            x = row_vals[0][col_name]
            for format1 in formats:
                try:
                    t = datetime.strptime(x,format1)
                    # if (format1 in dual_checks):
                    #     for x1 in row_vals:
                    #         x = x1[dims]
                    #         try:
                    #             t = dt.datetime.strptime(x,format1)
                    #         except ValueError as err:
                    #             format1 = '%d'+format1[2]+'%m'+format1[5:]
                    #             break
                    output[col_name] = format1
                    break
                except ValueError as err:
                    pass
        return output

    def get_datetime_format(self,columnVector):
        """
        suggest candidate for datetime column.
        checks against a list of datetime formats

        Arguments:
        columnVector -- an array of strings of any size.

        Return:
        detectedFormat -- datetime format
        """
        detectedFormat = None
        availableDateTimeFormat = CommonUtils.dateTimeFormatsSupported()["formats"]
        x = columnVector[0]
        for dt_format in availableDateTimeFormat:
            try:
                t = datetime.strptime(x,dt_format)
                detectedFormat = dt_format
                break
            except ValueError as err:
                pass
        return detectedFormat


    def get_ignore_column_suggestions(self,df,column_name,dataType,colStat,max_levels=100):
        ignore = False
        reason = None
        total_rows = df.count()
        modifiedColStat = {}
        for obj in colStat:
            modifiedColStat[obj["name"]] = obj["value"]
        colStat = modifiedColStat
        if dataType == "measure":
            if (colStat["numberOfUniqueValues"]==1):
                ignore = True
                reason = "Only one Unique Value"
            if (colStat["numberOfNulls"] == 0):
                if (colStat["numberOfUniqueValues"] == total_rows):
                    ignore = True
                    reason = "Index column (all values are distinct)"
            else:
                if (colStat["numberOfNulls"] > colStat["numberOfNotNulls"]):
                    ignore = True
                    reason = "Count of Nulls More than Count of Not Nulls"
                # handling cases where some ids will be missing
                elif (colStat["numberOfNotNulls"] <= 0.01*colStat["numberOfUniqueValues"]):
                    ignore = True
                    reason = "Index Column(Most of Not Null Values are unique)"

        elif dataType == "dimension":
            if (colStat["numberOfUniqueValues"]==1):
                ignore = True
                reason = "Only one Unique Value"
            if (colStat["numberOfNulls"] == 0):
                if (colStat["numberOfUniqueValues"] == total_rows):
                    ignore = True
                    reason = "All values are distinct"
            else:
                if (colStat["numberOfNulls"] > colStat["numberOfNotNulls"]):
                    ignore = True
                    reason = "Count of Nulls More than Count of Not Nulls"
                elif (colStat["numberOfNotNulls"]==1):
                    ignore = True
                    reason = "Only one Not Null value"
                elif colStat["numberOfUniqueValues"] > max_levels:
                    ignore = True
                    reason = "Number of Levels are more than the defined thershold"
        return ignore,reason


    def get_utf8_suggestions(self,colStat):
        utf8 = False
        modifiedColStat = {}
        for obj in colStat:
            modifiedColStat[obj["name"]] = obj["value"]
        colStat = modifiedColStat
        levels = colStat["LevelCount"].keys()
        for val in levels:
            if val:
                if any([ord(char)>127 for char in val]):
                    utf8 = True
                    break
        return utf8
