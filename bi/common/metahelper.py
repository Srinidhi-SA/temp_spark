
import random

import datetime as dt
from pyspark.sql import functions as FN
from pyspark.sql.functions import udf, col
from pyspark.sql.types import DateType, FloatType
from pyspark.sql.types import StringType

from bi.common import utils
from column import ColumnType


class MetaDataHelper():
    MEASURE_COLUMNS = "measure_columns"
    DIMENSION_COLUMNS = "dimension_columns"
    TIME_DIMENSION_COLUMNS = "time_dimension_columns"
    NULL_VALUES = 'num_nulls'
    NON_NULL_VALUES = 'num_non_nulls'
    UNIQUE_VALUES = 'unique_values'
    MINIMUM = 'minimum'
    MAXIMUM = 'maximum'
    LEVELS = 'levels'

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

    def transform_numeric_column(self):
        sample_rows = min(500.0, float(self._data_frame.count()*0.8))
        sample_df = self._data_frame.sample(False, sample_rows/self._data_frame.count(), seed = random.randint(1,1000))
        sample_df = sample_df.toPandas()
        updated_col_names = utils.get_updated_colnames(sample_df)
        changed_columns = updated_col_names['c']
        self.measure_suggestions = changed_columns
        try:
            func = udf(lambda x: utils.tryconvert(x), FloatType())
            self._data_frame = self._data_frame.select(*[func(c).alias(c) if c in changed_columns else c for c in sample_df.columns])
        except :
            pass

    def get_num_unique_values(self,column_name):
        return self._data_frame.select(column_name).distinct().count()

    def get_all_levels(self,column_name):
        return [levels[0] for levels in self._data_frame.select(column_name).distinct().collect()]

    def get_num_null_values(self, column_name):
        column = FN.col(column_name)
        rows = self._data_frame.select(column).groupBy(FN.isnull(column)).agg({'*': 'count'}).collect()
        for row in rows:
            if row[0] == True:
                return row[1]
        return 0

    def get_min(self, measure_column_name):
        #return self._data_frame.na.drop(subset=measure_column_name).select(FN.min(measure_column_name)).collect()[0][0]
        return self._data_frame.filter(col(measure_column_name).isNotNull()).select(FN.min(measure_column_name)).collect()[0][0]

    def get_max(self, measure_column_name):
        #return self._data_frame.na.drop(subset=measure_column_name).filter(col(measure_column_name).isNotNull()).select(FN.max(measure_column_name)).collect()[0][0]
        return self._data_frame.filter(col(measure_column_name).isNotNull()).select(FN.max(measure_column_name)).collect()[0][0]

    def get_level_count(self, column_name):
        levels = self._data_frame.groupby(column_name).count().toPandas().to_dict()
        levels_fin = {}
        for i in levels[column_name].keys():
            if i == None or i == '':
                levels_fin[levels[column_name]['null values']]= int(levels['count'][i])
            else:
                levels_fin[levels[column_name][i]]= int(levels['count'][i])
        return levels_fin

    def _populate_data(self):
        #self._data_frame.show()
        for measure_column in self._numeric_columns:
            measure_column_name = measure_column.split('||')[0]
            null_values = self.get_num_null_values(measure_column)
            non_null_values = self.total_rows - null_values
            unique_values = self.get_num_unique_values(measure_column)
            if non_null_values > 0:
                min_val = self.get_min(measure_column)
                max_val = self.get_max(measure_column)

            else:
                min_val = 0
                max_val = 0
            self.columns[MetaDataHelper.MEASURE_COLUMNS][measure_column_name] = {
                MetaDataHelper.NULL_VALUES: null_values,
                MetaDataHelper.NON_NULL_VALUES: non_null_values,
                MetaDataHelper.UNIQUE_VALUES: unique_values,
                MetaDataHelper.MINIMUM: min_val,
                MetaDataHelper.MAXIMUM: max_val
            }
            if (null_values>non_null_values) or (unique_values==1):
                self.ignore_column_suggestions[MetaDataHelper.MEASURE_COLUMNS].append(measure_column)
            elif min_val==int(min_val) and max_val==int(max_val):
                if abs(non_null_values-unique_values) <= 0.01*non_null_values:
                    if abs(non_null_values-max_val+min_val)<= 0.01*non_null_values or abs(self.total_rows-max_val+min_val)<= 0.01*self.total_rows:
                        self.ignore_column_suggestions[MetaDataHelper.MEASURE_COLUMNS].append(measure_column)
                        
        for dimension_column in self._string_columns:
            null_values = self.get_num_null_values(dimension_column)
            non_null_values = self.total_rows - null_values
            unique_values = self.get_num_unique_values(dimension_column)
            self.columns[MetaDataHelper.DIMENSION_COLUMNS][dimension_column] = {
                MetaDataHelper.NULL_VALUES: null_values,
                MetaDataHelper.NON_NULL_VALUES: non_null_values,
                MetaDataHelper.UNIQUE_VALUES: unique_values
            }

            ## IGNORE SUGGESTIONS - Initial
            if null_values>non_null_values or unique_values<=1 or (null_values>0 and unique_values==2):
                self.ignore_column_suggestions[MetaDataHelper.DIMENSION_COLUMNS].append(dimension_column)
            elif dimension_column in self.date_time_suggestions.keys():
                pass
            elif unique_values>1 and unique_values<=self._max_levels:
                flag = 0
                self.levels_count[dimension_column] = self.get_level_count(dimension_column)
                levels = self.levels_count[dimension_column].keys()
                for val in levels:
                    if val:
                        if any([ord(char)>127 for char in val]):
                            # self.ignore_column_suggestions[MetaDataHelper.DIMENSION_COLUMNS].append(dimension_column)
                            self.utf8_columns.append(dimension_column)
                            flag = 1
                            break
                if flag == 0:
                    self._dimensions_to_consider.append((unique_values,dimension_column))
            else:
                self.ignore_column_suggestions[MetaDataHelper.DIMENSION_COLUMNS].append(dimension_column)
            # removing utf8_columns from validation page
            if self.utf8_columns != None:
                for colname in self.utf8_columns:
                    self.columns[MetaDataHelper.DIMENSION_COLUMNS].pop(colname)


            # if ((unique_values > self._max_levels) and (dimension_column not in self.date_time_suggestions.keys())) or (null_values>non_null_values):
            #     if(not self.ignore_column_suggestions.has_key(MetaDataHelper.DIMENSION_COLUMNS)):
            #         self.ignore_column_suggestions[MetaDataHelper.DIMENSION_COLUMNS] = []
            #     self.ignore_column_suggestions[MetaDataHelper.DIMENSION_COLUMNS].append(dimension_column)
            # elif unique_values==1:
            #     if(not self.ignore_column_suggestions.has_key(MetaDataHelper.DIMENSION_COLUMNS)):
            #         self.ignore_column_suggestions[MetaDataHelper.DIMENSION_COLUMNS] = []
            #     self.ignore_column_suggestions[MetaDataHelper.DIMENSION_COLUMNS].append(dimension_column)
            # elif dimension_column not in self.date_time_suggestions.keys():
            #     '''self._levels_count[dimension_column] = self.get_level_count(dimension_column)
            #     self.levels_count[dimension_column] = {}
            #     for key in self._levels_count[dimension_column][dimension_column].keys():
            #         k = self._levels_count[dimension_column][dimension_column][key]
            #         self.levels_count[dimension_column][k] = int(self._levels_count[dimension_column]['count'][key])
            #     #self.dimension_filter[dimension_column] = self.get_all_levels(dimension_column)'''
            #     self.levels_count[dimension_column] = self.get_level_count(dimension_column)
            #     levels = self.levels_count[dimension_column].keys()
            #     for val in levels:
            #         if val:
            #             ord_list =  [ord(char) for char in val if ord(char) > 127]
            #             if len(ord_list) > 0:
            #                 self.ignore_column_suggestions["dimension_columns"].append(dimension_column)
            #                 break

        # at this point dimensions_to_consider has >=2 and self._max_levels
        self._dimensions_to_consider = sorted(self._dimensions_to_consider, key=lambda x: x[0])

        if len(self._dimensions_to_consider)>10:
            ignore_suggestions = [x[1] for x in self._dimensions_to_consider]
            ignore_suggestions = ignore_suggestions[10:]
            self.ignore_column_suggestions[MetaDataHelper.DIMENSION_COLUMNS] += ignore_suggestions

        for time_dimension_column in self._timestamp_columns:
            null_values = self.get_num_null_values(time_dimension_column)
            non_null_values = self.total_rows - null_values
            unique_values = self.get_num_unique_values(time_dimension_column)
            self.columns[MetaDataHelper.TIME_DIMENSION_COLUMNS][time_dimension_column] = {
                MetaDataHelper.NULL_VALUES: null_values,
                MetaDataHelper.NON_NULL_VALUES: non_null_values,
                MetaDataHelper.UNIQUE_VALUES: unique_values
            }

    def get_datetime_suggestions(self):
        self.date_time_suggestions = {}
        formats = utils.dateTimeFormatsSupported()["formats"]
        dual_checks = utils.dateTimeFormatsSupported()["dual_checks"]

        for dims in self._string_columns:
            row_vals = self._data_frame.select(dims).na.drop().take(int(self.total_rows**0.5 + 1))
            x = row_vals[0][dims]
            for format1 in formats:
                try:
                    t = dt.datetime.strptime(x,format1)
                    # if (format1 in dual_checks):
                    #     for x1 in row_vals:
                    #         x = x1[dims]
                    #         try:
                    #             t = dt.datetime.strptime(x,format1)
                    #         except ValueError as err:
                    #             format1 = '%d'+format1[2]+'%m'+format1[5:]
                    #             break
                    self.date_time_suggestions[dims] = format1
                    break
                except ValueError as err:
                    pass

    def has_date_suggestions(self):
        if len(self.date_time_suggestions)>0:
            return True
        return False

    def get_formats(self):
        self.formats_to_convert = ["mm/dd/YYYY","dd/mm/YYYY","YYYY/mm/dd", "dd <month> YYYY"]

    ###### An alternative is present in datacleansing. Can fix after final product plan
    def change_format(self,colname,frmt1,frmt2):
        func = udf(lambda x: dt.datetime.strptime(x,frmt1).strftime(frmt2), StringType())
        #func = udf(lambda x: dt.datetime.strptime(x,'%d-%m-%Y'), DateType())
        self._data_frame = self._data_frame.select(*[func(column).alias(colname) if column==colname else column for column in self._data_frame.columns]).collect()
        return self._data_frame.collect()

    def change_to_date(self, colname, format):
        func = udf(lambda x: datetime.strptime(x, format), DateType())
        self._data_frame = self._data_frame.select(*[func(column).alias(colname) if column==colname else column for column in self._data_frame.columns])
        return self._data_frame.collect()

    def get_sample_data_frame(self,num_rows = 100):
        print self._data_frame.sample(False, 100/self.num_rows, 140).toPandas()
