import json
import random
import uuid
import datetime as dt

from pyspark.sql import functions as FN
from pyspark.sql.functions import udf, col
from pyspark.sql.types import DateType, FloatType
from pyspark.sql.types import StringType

from bi.common import DataWriter
from bi.common import ColumnType
from bi.common import utils as CommonUtils
from bi.common import MetaDataHelper
from bi.common.results import DfMetaData,MetaData,ColumnData,ColumnHeader


class MetaDataScript:
    def __init__(self, data_frame, spark):
        self._data_frame = data_frame
        self._spark = spark
        # self._file_name = file_name
        self.total_columns = len([field.name for field in self._data_frame.schema.fields])
        self._total_rows = self._data_frame.count()
        self._max_levels = min(200, round(self._total_rows**0.5))

        self._numeric_columns = [field.name for field in self._data_frame.schema.fields if
                ColumnType(type(field.dataType)).get_abstract_data_type() == ColumnType.MEASURE]
        self._string_columns = [field.name for field in self._data_frame.schema.fields if
                ColumnType(type(field.dataType)).get_abstract_data_type() == ColumnType.DIMENSION]
        self._timestamp_columns = [field.name for field in self._data_frame.schema.fields if
                ColumnType(type(field.dataType)).get_abstract_data_type() == ColumnType.TIME_DIMENSION]
        self._boolean_columns = [field.name for field in self._data_frame.schema.fields if
                ColumnType(type(field.dataType)).get_abstract_data_type() == ColumnType.BOOLEAN]
        self._column_type_dict = dict(\
                                        zip(self._numeric_columns,["measure"]*len(self._numeric_columns))+\
                                        zip(self._string_columns,["dimension"]*len(self._string_columns))+\
                                        zip(self._timestamp_columns,["datetime"]*len(self._timestamp_columns))+\
                                        zip(self._boolean_columns,["boolean"]*len(self._boolean_columns))\
                                     )
        print self._column_type_dict

    def run(self):
        metaData = []
        metaData.append(MetaData(name="noOfRows",value=self._total_rows,display=True,displayName="Rows"))
        metaData.append(MetaData(name="noOfColumns",value=self.total_columns,display=True,displayName="Columns"))
        if len(self._numeric_columns) > 1:
            metaData.append(MetaData(name="measures",value=len(self._numeric_columns),display=True,displayName="Measures"))
        else:
            metaData.append(MetaData(name="measures",value=len(self._numeric_columns),display=True,displayName="Measure"))
        if len(self._string_columns) > 1:
            metaData.append(MetaData(name="dimensions",value=len(self._string_columns),display=True,displayName="Dimensions"))
        else:
            metaData.append(MetaData(name="dimensions",value=len(self._string_columns),display=True,displayName="Dimension"))
        if len(self._timestamp_columns) > 1:
            metaData.append(MetaData(name="timeDimension",value=len(self._timestamp_columns),display=True,displayName="Time Dimensions"))
        else:
            metaData.append(MetaData(name="timeDimension",value=len(self._timestamp_columns),display=True,displayName="Time Dimension"))


        metaData.append(MetaData(name="measureColumns",value = self._numeric_columns,display=False))
        metaData.append(MetaData(name="dimensionColumns",value = self._string_columns,display=False))
        metaData.append(MetaData(name="timeDimensionColumns",value = self._timestamp_columns,display=False))

        columnData = []
        headers = []
        if self._data_frame.count() > 100:
            sampleData = self._data_frame.sample(False, float(100)/self._total_rows, seed=420)
            if len(self._timestamp_columns) > 0:
                for colname in self._timestamp_columns:
                    print colname
                    sampleData = sampleData.withColumn(colname, sampleData[colname].cast(StringType()))
                    sampleData = sampleData.toPandas().values.tolist()
            else:
                sampleData = sampleData.toPandas().values.tolist()
        else:
            sampleData = self._data_frame.toPandas().values.tolist()

        helper_instance = MetaDataHelper(self._data_frame)
        measureColumnStat,measureCharts = helper_instance.calculate_measure_column_stats(self._data_frame,self._numeric_columns)
        dimensionColumnStat,dimensionCharts = helper_instance.calculate_dimension_column_stats(self._data_frame,self._string_columns)

        ignoreColumnSuggestions = []
        utf8ColumnSuggestion = []
        dateTimeSuggestions = {}
        for column in self._data_frame.columns:
            random_slug = uuid.uuid4().hex
            headers.append(ColumnHeader(name=column,slug=random_slug))
            data = ColumnData()
            data.set_slug(random_slug)
            data.set_name(column)
            data.set_column_type(self._column_type_dict[column])

            columnStat = []
            columnChartData = None
            if self._column_type_dict[column] == "measure":
                data.set_column_stats(measureColumnStat[column])
                data.set_column_chart(measureCharts[column])
            elif self._column_type_dict[column] == "dimension":
                data.set_column_stats(dimensionColumnStat[column])
                data.set_column_chart(dimensionCharts[column])
            if self._column_type_dict[column] == "measure":
                ignoreSuggestion = helper_instance.get_ignore_column_suggestions(self._data_frame,column,"measure",measureColumnStat[column],max_levels=self._max_levels)
                if ignoreSuggestion:
                    ignoreColumnSuggestions.append(column)
            elif self._column_type_dict[column] == "dimension":
                utf8Suggestion = helper_instance.get_utf8_suggestions(dimensionColumnStat[column])
                dateColumn = helper_instance.get_datetime_suggestions(self._data_frame,column)
                if dateColumn != {}:
                    dateTimeSuggestions.update(dateColumn)
                    data.set_level_count_to_null()
                    data.set_chart_data_to_null()
                if utf8Suggestion:
                    utf8ColumnSuggestion.append(column)
                ignoreSuggestion = helper_instance.get_ignore_column_suggestions(self._data_frame,column,"dimension",dimensionColumnStat[column],max_levels=self._max_levels)
                if ignoreSuggestion:
                    ignoreColumnSuggestions.append(column)
            columnData.append(data)

        ignoreColumnSuggestions = list(set(ignoreColumnSuggestions)-set(dateTimeSuggestions.keys()))+utf8ColumnSuggestion
        print ignoreColumnSuggestions
        metaData.append(MetaData(name="ignoreColumnSuggestions",value = ignoreColumnSuggestions,display=False))
        metaData.append(MetaData(name="utf8ColumnSuggestion",value = utf8ColumnSuggestion,display=False))
        metaData.append(MetaData(name="dateTimeSuggestions",value = dateTimeSuggestions,display=False))

        dfMetaData = DfMetaData()
        dfMetaData.set_column_data(columnData)
        dfMetaData.set_header(headers)
        dfMetaData.set_meta_data(metaData)
        dfMetaData.set_sample_data(sampleData)

        return dfMetaData
