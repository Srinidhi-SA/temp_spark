import time
from pyspark.ml.feature import Bucketizer
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import col, expr, when, udf
from pyspark.sql.types import DoubleType,StringType,StructType
from bi.common.utils import accepts
from bi.common import DataFilterHelper
from bi.common import utils as CommonUtils
#import bi.common.dataframe

class DataFrameTransformer:
    # @accepts(object,DataFrame,DataFrameHelper,ContextSetter)
    def __init__(self, dataframe, df_helper, df_context):
        self._data_frame = dataframe
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context
        self._completionStatus = 0
        self._start_time = time.time()
        self._analysisName = "transformation"
        self._messageURL = self._dataframe_context.get_message_url()
        self._replaceTypeList = ["equals","contains","startsWith","endsWith"]
        self._scriptStages = {
            "initialization":{
                "summary":"initialized the filter parameters",
                "weight":3
                },
            "dimensionfilters":{
                "summary":"dimensionfilters is Run",
                "weight":3
                },
            "measurefilters":{
                "summary":"measurefilters is run",
                "weight":6
                },
            "datetimefilters":{
                "summary":"Datetimefilter is run",
                "weight":3
                }
            }

    def applyTransformations(self):
        """
        here all the filter settings will come from the df_context
        """
        existingColTransforms = self._dataframe_context.get_existing_column_transform_settings()
        newColTransforms = self._dataframe_context.get_new_column_transform_settings()
        if len(existingColTransforms) > 0:
            for transformObj in existingColTransforms:
                transformActionList = [obj["actionName"]  for obj in transformObj["columnSetting"]]
                print transformActionList
                if "delete" in transformActionList:
                    self.delete_column(transformObj["name"])
                else:
                    for obj in transformObj["columnSetting"]:
                        if obj["actionName"] == "replace":
                            self.update_column_data(transformObj["name"],obj["replacementValues"])
                        if obj["actionName"] == "rename":
                            self.update_column_name(transformObj["name"],obj["newName"])
                        if obj["actionName"] == "data_type":
                            castDataType = [x["name"] for x in obj["listOfActions"] if x["status"] == True][0]
                            if castDataType == "numeric":
                                newDataType = 'int'
                            elif castDataType == "string":
                                newDataType = "string"
                            elif castDataType == "datetime":
                                newDataType = "timestamp"
                            self.update_column_datatype(transformObj["name"],newDataType)
                            print self._data_frame.printSchema()




    def add_new_columns(self,df,new_col_name,old_col_list,operator):
        print "hi adding new column"
        col_dtype_list=[] #will take dtype of all the merger column to see unique value
        ncol_dtype=False
        col_dtype_map={}
        col_dtype_setlist=df.dtypes
        for col_dtype_set in col_dtype_setlist:
            col_dtype_map[col_dtype_set[0]]=col_dtype_set[1]
        #will check data type of each column,if all of them are same then only we will merge different col dataset to create new col
        print col_dtype_map
        dtype_col_map={}
        for old_col in old_col_list:
            dtype=col_dtype_map[old_col]
            col_dtype_list.append(dtype)
            if dtype in dtype_col_map:
                dtype_col_map[dtype]=dtype_col_map[dtype].append(old_col)
            else:
                dtype_col_map[dtype]=[old_col]
        print col_dtype_list
        uniq_dtype_list=list(set(col_dtype_list))
        newdf=df
        if uniq_dtype_list and len(uniq_dtype_list)==1:
            #newdf = df.withColumn('total', sum(df[col] for col in df.columns))
            print new_col_name
            newdf=df.withColumn(new_col_name,lit(10))
            #TODO here actual operation is not happening,need to change according to the passed operator
            #newdf=     df.withColumn(new_col_name,sum(df[col] for col in old_col_list))
            #all the data type of merger columns are same so we can create new column adding different fields data
            print "all data type is same"
        else:
            print "data type of merger column are different so cant concatnate different data types"
            for dtype in dtype_col_map.keys():
                print dtype_col_map[dtype]
        return newdf

    def delete_column(self,column):
        self._data_frame = self._data_frame.drop(column)

    def update_column_data(self,column_name,replace_obj_list):
        for replace_obj in replace_obj_list:
            if replace_obj["valueToReplace"] == "" and replace_obj["replacedValue"] == "":
                pass
            else:
                key = replace_obj["valueToReplace"]
                value = replace_obj["replacedValue"]
                replace_type = replace_obj["replaceType"]
                if replace_type in self._replaceTypeList:
                    if replace_type == "contains":
                        replace_values = udf(lambda x: x.replace(key,value),StringType())
                        self._data_frame = self._data_frame.withColumn(column_name,replace_values(col(column_name)))
                    if replace_type == "startsWith":
                        print replace_obj
                        replace_values = udf(lambda x: replace_obj["replacedValue"]+x[len(replace_obj["valueToReplace"]):] if x.startswith(replace_obj["valueToReplace"]) else x,StringType())
                        self._data_frame = self._data_frame.withColumn(column_name,replace_values(col(column_name)))
                    if replace_type == "endsWith":
                        print replace_obj
                        replace_values = udf(lambda x: x[:-len(replace_obj["valueToReplace"])]+replace_obj["replacedValue"] if x.endswith(replace_obj["valueToReplace"]) else x,StringType())
                        self._data_frame = self._data_frame.withColumn(column_name,replace_values(col(column_name)))
                    if replace_type == "equals":
                        replace_values = udf(lambda x: x.replace(key,value) if x==replace_obj["valueToReplace"] else x,StringType())
                        self._data_frame = self._data_frame.withColumn(column_name,replace_values(col(column_name)))

    def update_column_datatype(self,column_name,data_type):
        print "hi udating column data type"
        self._data_frame = self._data_frame.withColumn(column_name, self._data_frame[column_name].cast(data_type))
        print self._data_frame.printSchema()
        #TODO update data type as measure or dimension

    def update_column_name(self,old_column_name,new_column_name):
        if new_column_name:
            self._data_frame = self._data_frame.withColumnRenamed(old_column_name,new_column_name)

    def get_transformed_data_frame(self):
        return self._data_frame
