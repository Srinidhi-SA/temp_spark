
import random

import datetime as dt
from pyspark.sql import functions as FN
from pyspark.sql.functions import udf, col
from pyspark.sql.types import DateType, FloatType
from pyspark.sql.types import StringType

from bi.common import utils as CommonUtils
from column import ColumnType


class MetaDataHelperNew():

    def __init__(self, data_frame, file_name=None, transform = 0):
        self._file_name = file_name
        self._data_frame = data_frame
        if transform==1:
            self.transform_numeric_column()
        self.total_columns = len([field.name for field in self._data_frame.schema.fields])
        self.total_rows = self._data_frame.count()
        #self._max_levels = max(40,round(self.total_rows**0.34))
        self._max_levels = min(200, round(self.total_rows**0.5))
        self.ignore_column_suggestions = {MetaDataHelper.MEASURE_COLUMNS:[],
                                            MetaDataHelper.DIMENSION_COLUMNS:[]}
        self.utf8_columns = []
        #self.dimension_filter = {}
        self._levels_count = {}
        self.levels_count = {}
        self._numeric_columns = [field.name for field in self._data_frame.schema.fields if
                ColumnType(type(field.dataType)).get_abstract_data_type() == ColumnType.MEASURE]
        self._string_columns = [field.name for field in self._data_frame.schema.fields if
                ColumnType(type(field.dataType)).get_abstract_data_type() == ColumnType.DIMENSION]
        self._timestamp_columns = [field.name for field in self._data_frame.schema.fields if
                ColumnType(type(field.dataType)).get_abstract_data_type() == ColumnType.TIME_DIMENSION]
        self.columns = {
            MetaDataHelper.MEASURE_COLUMNS: {},
            MetaDataHelper.DIMENSION_COLUMNS: {},
            MetaDataHelper.TIME_DIMENSION_COLUMNS: {}
            }
        self.get_datetime_suggestions()
        self._dimensions_to_consider = []
        self._populate_data()
        self._numeric_columns = [x.split('||')[0] for x in self._numeric_columns]

        #self.get_sample_data_frame()

    
