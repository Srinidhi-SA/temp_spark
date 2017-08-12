import json
import random
import datetime as dt

from pyspark.sql import functions as FN
from pyspark.sql.functions import udf, col
from pyspark.sql.types import DateType, FloatType
from pyspark.sql.types import StringType

from bi.common import DataWriter
from bi.common import ColumnType
from bi.common import utils as CommonUtils
from bi.common import MetaDataHelper
from bi.results import DfMetaData,MetaData,ColumnData,ColumnHeader


class MetaDataScript:
    def __init__(self, data_frame, spark):
        self._data_frame = data_frame
        self._spark = spark
        # self._file_name = file_name
        self.total_columns = len([field.name for field in self._data_frame.schema.fields])
        self.total_rows = self._data_frame.count()

        # self._max_levels = min(200, round(self.total_rows**0.5))

        self._numeric_columns = [field.name for field in self._data_frame.schema.fields if
                ColumnType(type(field.dataType)).get_abstract_data_type() == ColumnType.MEASURE]
        self._string_columns = [field.name for field in self._data_frame.schema.fields if
                ColumnType(type(field.dataType)).get_abstract_data_type() == ColumnType.DIMENSION]
        self._timestamp_columns = [field.name for field in self._data_frame.schema.fields if
                ColumnType(type(field.dataType)).get_abstract_data_type() == ColumnType.TIME_DIMENSION]
        self._column_type_dict = dict(\
                                        zip(self._numeric_columns,["Measure"]*len(self._numeric_columns))+\
                                        zip(self._string_columns,["Dimension"]*len(self._string_columns))+\
                                        zip(self._timestamp_columns,["TimeDimension"]*len(self._timestamp_columns))\
                                     )


    def run(self):
        metaData = []
        metaData.append(MetaData(name="measures",value=1,display=True))
        metaData.append(MetaData(name="dimensions",value=2,display=True))
        metaData.append(MetaData(name="timeDimension",value=0,display=True))
        metaData.append(MetaData(name="measureColumns",value = self._numeric_columns,display=False))
        metaData.append(MetaData(name="dimensionColumns",value = self._string_columns,display=False))

        columnData = []
        headers = []
        sampleData = self._data_frame.sample(False, float(100)/self._total_rows, seed=420).toPandas().values.tolist()

        measureColumnStat,measureCharts = MetaDataHelper.calculate_measure_column_stats(self._data_frame,self._numeric_columns)
        dimensionColumnStat,dimensionCharts = MetaDataHelper.calculate_dimension_column_stats(self._data_frame,self._string_columns)

        for column in self._data_frame.columns:
            headers.append(ColumnHeader(name=column,slug=None))
            data = ColumnData()
            data.set_name(column)
            data.set_column_type(self._column_type_dict[column])

            columnStat = []
            columnChartData = None
            if self._column_type_dict[column] == "Measure":
                data.set_column_stats(measureColumnStat[column])
                data.set_column_chart(measureCharts[column])
            elif self._column_type_dict[column] == "Dimension":
                data.set_column_stats(dimensionColumnStat[column])
                data.set_column_chart(dimensionCharts[column])
            columnData.append(data)


        dfMetaData = DfMetaData()
        dfMetaData.set_column_data(columnData)
        dfMetaData.set_header(headers)
        dfMetaData.set_meta_data(metaData)
        dfMetaData.set_sample_data(sampleData)

        return dfMetaData
