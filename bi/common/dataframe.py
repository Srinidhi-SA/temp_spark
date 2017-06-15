from functools import reduce

import datetime as dt
from datetime import datetime
from pyspark.sql import DataFrame
from pyspark.sql import functions as FN
from pyspark.sql.functions import udf, col
from pyspark.sql.types import *
from pyspark.sql.types import StringType
from sklearn.model_selection import train_test_split

from bi.common import utils as CommonUtils
from column import ColumnType
from decorators import accepts
from exception import BIException


class DataFrameHelper:
    """
    Provides helper method to query properties of a dataframe
    """

    MEASURE_COLUMNS = "measure_columns"
    DIMENSION_COLUMNS = "dimension_columns"
    TIME_DIMENSION_COLUMNS = "time_dimension_columns"
    NULL_VALUES = 'num_nulls'
    NON_NULL_VALUES = 'num_non_nulls'

    def __init__(self, data_frame, df_context):
        self._data_frame = data_frame
        # stripping spaces from column names
        self._data_frame = self._data_frame.select(*[col(c.name).alias(c.name.strip()) for c in self._data_frame.schema.fields])

        self._sample_data_frame = None

        self.column_data_types = {}
        self.columns = []
        self.numeric_columns = []
        self.string_columns = []
        self.timestamp_columns = []
        self.num_rows = 0
        self.num_columns = 0
        self.column_details = {
            DataFrameHelper.MEASURE_COLUMNS: {},
            DataFrameHelper.DIMENSION_COLUMNS: {},
            DataFrameHelper.TIME_DIMENSION_COLUMNS: {}
        }
        self.ignorecolumns = ""
        self.consider_columns = ""
        self._df_context = df_context
        self.measure_suggestions = []
        self.train_test_data = {"x_train":None,"x_test":None,"y_train":None,"y_test":None}
        self._date_formats = {}
        self.significant_dimensions = {}

    def set_params(self):

        self.columns = [field.name for field in self._data_frame.schema.fields]
        self.ignorecolumns = self._df_context.get_ignore_column_suggestions()
        self.utf8columns = self._df_context.get_utf8_columns()
        self.resultcolumn = self._df_context.get_result_column()
        self.consider_columns = self._df_context.get_consider_columns()
        self.considercolumnstype = self._df_context.get_consider_columns_type()

        if self.considercolumnstype[0] == "including":
            if self.consider_columns != None:
                if self.utf8columns != None:
                    self.consider_columns = list(set(self.consider_columns)-set(self.utf8columns))
                for colname in self.consider_columns:
                    if colname in self.ignorecolumns:
                        self.ignorecolumns.remove(colname)
        if self.ignorecolumns != None:
            if self.resultcolumn in self.ignorecolumns:
                self.ignorecolumns.remove(self.resultcolumn)
            if self.utf8columns != None:
                self.ignorecolumns += self.utf8columns
        else:
            if self.utf8columns != None:
                self.ignorecolumns = self.utf8columns

        self.subset_data()
        #self.df_filterer = DataFrameFilterer(self._data_frame)
        #self.dimension_filter = self._df_context.get_dimension_filters()
        self.__subset_data()

        self.measure_suggestions = self._df_context.get_measure_suggestions()

        if self.measure_suggestions != None:
            if self.ignorecolumns != None:
                self.measure_suggestions = list(set(self.measure_suggestions)-set(self.ignorecolumns))
            elif self.ignorecolumns == None:
                self.measure_suggestions = list(set(self.measure_suggestions))

            self.measure_suggestions = [m for m in self.measure_suggestions if m in self.columns]
            if len(self.measure_suggestions)>0:
                    self.clean_data_frame()
        # for colmn in self.dimension_filter.keys():
        #     self.df_filterer.values_in(colmn, self.dimension_filter[colmn])
        #
        # self.measure_filter = self._df_context.get_measure_filters()
        # print self.measure_filter
        # for colmn in self.measure_filter.keys():
        #     self.df_filterer.values_between(colmn, self.measure_filter[colmn][0],self.measure_filter[colmn][1],1,1)

        # self._data_frame = self.df_filterer.get_filtered_data_frame()
        self.date_settings = self._df_context.get_date_settings()
        self.columns = [field.name for field in self._data_frame.schema.fields]
        for colmn in self.date_settings.keys():
            if colmn in self.columns:
                self.change_to_date(colmn, self.date_settings[colmn][0])
                # print self.date_settings[colmn][0]
        #self.date_filter = self._df_context.get_date_filters()
        #for colmn in self.date_filter.keys():
        #    self.df_filterer.dates_between(colmn, dt.date(int(self.date_filter[colmn][2]),int(self.date_filter[colmn][1]),int(self.date_filter[colmn][0])),
        #                                        dt.date(int(self.date_filter[colmn][5]),int(self.date_filter[colmn][4]),int(self.date_filter[colmn][3])))
        self.__update_meta()
        self.__populate_data()

        if self._data_frame.count() > 5000:
            self._sample_data_frame = self._data_frame.sample(False, 4000/float(self._data_frame.count()), seed=0)
        else:
            self._sample_data_frame = self._data_frame

    def set_train_test_data(self,df):
        # from bi.algorithms import utils as MLUtils
        df = df
        result_column = self._df_context.get_result_column()
        train_test_ratio = float(self._df_context.get_train_test_split())
        print train_test_ratio
        if train_test_ratio == None:
            train_test_ratio = 0.7
        x_train,x_test,y_train,y_test = train_test_split(df[[col for col in df.columns if col != result_column]], df[result_column], train_size=train_test_ratio, random_state=42, stratify=df[result_column])
        # x_train,x_test,y_train,y_test = MLUtils.generate_train_test_split(df,train_test_ratio,result_column,drop_column_list)
        self.train_test_data = {"x_train":x_train,"x_test":x_test,"y_train":y_train,"y_test":y_test}

    def remove_nulls(self, col):
        self._data_frame = self._data_frame.na.drop(subset=col)
        self.num_rows = self._data_frame.count()

    def clean_data_frame(self):
        """
        used to convert dimension columns to measures takes input from config (measure suggestions).
        """
        try:
            func = udf(lambda x: CommonUtils.tryconvert(x), FloatType())
            self._data_frame = self._data_frame.select(*[func(c).alias(c) if c in self.measure_suggestions else c for c in self.columns])
            self._data_frame.schema.fields
        except:
            pass

    def __update_meta(self):
        self.columns = [field.name for field in self._data_frame.schema.fields]
        self.column_data_types = {field.name: field.dataType for field in self._data_frame.schema.fields}
        self.numeric_columns = [field.name for field in self._data_frame.schema.fields if
                ColumnType(type(field.dataType)).get_abstract_data_type() == ColumnType.MEASURE]
        self.string_columns = [field.name for field in self._data_frame.schema.fields if
                ColumnType(type(field.dataType)).get_abstract_data_type() == ColumnType.DIMENSION]

        self.timestamp_columns = [field.name for field in self._data_frame.schema.fields if
                ColumnType(type(field.dataType)).get_abstract_data_type() == ColumnType.TIME_DIMENSION]
        self.num_rows = self._data_frame.count()
        self.num_columns = len(self._data_frame.columns)

    def get_column_data_types(self):
        return self.column_data_types

    def get_columns(self):
        return self.columns

    @accepts(object, basestring)
    def has_column(self, column_name):
        return column_name in self.get_columns()

    def get_numeric_columns(self):
        return self.numeric_columns

    @accepts(object, basestring)
    def is_numeric_column(self, column_name):
        return column_name in self.get_numeric_columns()

    def get_string_columns(self):
        return self.string_columns

    def get_all_levels(self,column_name):
        return [levels[0] for levels in self._data_frame.select(column_name).distinct().collect()]

    def get_num_unique_values(self,column_name):
        return self._data_frame.select(column_name).distinct().count()

    @accepts(object, basestring)
    def is_string_column(self, column_name):
        return column_name in self.get_string_columns()

    def get_timestamp_columns(self):
        return self.timestamp_columns

    @accepts(object, basestring)
    def is_timestamp_column(self, column_name):
        return column_name in self.get_timestamp_columns()

    def get_num_rows(self):
        return self.num_rows

    def get_num_columns(self):
        return self.num_columns

    def get_data_frame(self):
        return self._data_frame

    def subset_data_frame(self, columns):
        return self._data_frame.select(*columns)

    def add_significant_dimension(self, dimension, effect_size):
        self.significant_dimensions[dimension] = effect_size

    def get_significant_dimension(self):
        return self.significant_dimensions

    def filter_dataframe(self, colname, values):
        if type(values) == str:
            values = values[1:-1]
            values = values.split(',')
        df = self._data_frame.where(col(colname).isin(values))
        return df

    def get_splits_of_numerical_column(self,colname):
        min_max = self._data_frame.agg(FN.min(column_name).alias('min'), FN.max(column_name).alias('max')).collect()
        min_value = min_max[0]['min']
        max_value = min_max[0]['max']
        splits = CommonUtils.frange(min_value, max_value, num_bins)
        return splits

    def get_num_null_values(self, column_name):
        if not self.has_column(column_name):
          raise BIException('No such column exists: %s' %(column_name,))

        column = FN.col(column_name)
        rows = self._data_frame.select(column).groupBy(FN.isnull(column)).agg({'*': 'count'}).collect()
        for row in rows:
            if row[0] == True:
                return row[1]
        return 0

    def __populate_data(self):
        for measure_column in self.numeric_columns:
            null_values = self.get_num_null_values(measure_column)
            non_null_values = self.num_rows - null_values
            self.column_details[DataFrameHelper.MEASURE_COLUMNS][measure_column] = {
                DataFrameHelper.NULL_VALUES: null_values,
                DataFrameHelper.NON_NULL_VALUES: non_null_values
            }

        for dimension_column in self.string_columns:
            null_values = self.get_num_null_values(dimension_column)
            non_null_values = self.num_rows - null_values
            self.column_details[DataFrameHelper.DIMENSION_COLUMNS][dimension_column] = {
                DataFrameHelper.NULL_VALUES: null_values,
                DataFrameHelper.NON_NULL_VALUES: non_null_values
            }

        for time_dimension_column in self.timestamp_columns:
            null_values = self.get_num_null_values(time_dimension_column)
            non_null_values = self.num_rows - null_values
            self.column_details[DataFrameHelper.TIME_DIMENSION_COLUMNS][time_dimension_column] = {
                DataFrameHelper.NULL_VALUES: null_values,
                DataFrameHelper.NON_NULL_VALUES: non_null_values
            }

    def __subset_data(self):
        """
        dropping or keeping columns based on consider column input coming from users.
        """
        if self.considercolumnstype[0] == 'excluding':
            if self.consider_columns != None:
                self.consider_columns = list(set(self.consider_columns)-set([self.resultcolumn]))
                self._data_frame = reduce(DataFrame.drop, self.consider_columns, self._data_frame)
                self.columns = [field.name for field in self._data_frame.schema.fields]
            else:
                self._data_frame = self._data_frame
        elif self.considercolumnstype[0] == 'including':
            if self.consider_columns != None:
                self.consider_columns = self.consider_columns + [self.resultcolumn]
                self.consider_columns = list(set(self.columns) - set(self.consider_columns))
                self._data_frame = reduce(DataFrame.drop, self.consider_columns, self._data_frame)
                self.columns = [field.name for field in self._data_frame.schema.fields]
        self.__update_meta()


    def subset_data(self):
        """
        drops columns from ignore_column_suggestions coming from config.
        """
        if self.ignorecolumns != None:
            #self._data_frame = reduce(DataFrame.drop, *self.ignorecolumns, self._data_frame)
            self._data_frame = self._data_frame.select(*[c for c in self.columns if c not in self.ignorecolumns ])
            self.__update_meta()
        else:
            self._data_frame = self._data_frame

    def get_sample_data(self, column_name1, column_name2, outputLength):
        rowCount = self._sample_data_frame.count()
        if rowCount <= outputLength:
            newDf = self._sample_data_frame.select(column_name1,column_name2).toPandas()
            newDF = newDF[[column_name1, column_name2]]
        else:
            newDf = self._sample_data_frame.select(column_name1,column_name2).toPandas()[:outputLength]

        output = {column_name1:None,column_name2:None}
        output[column_name1] = [float(x) for x in newDf[column_name1]]
        output[column_name2] = [float(x) for x in newDf[column_name2]]
        return output

    def get_aggregate_data(self, aggregate_column, measure_column, existingDateFormat = None, requestedDateFormat = None):
        self._data_frame = self._data_frame.na.drop(subset=aggregate_column)
        if existingDateFormat != None and requestedDateFormat != None:
            print existingDateFormat,requestedDateFormat
            # def date(s):
            #   return str(s.date())
            # date_udf = udf(date, StringType())
            # Below line is just for testing a special scenario
            # func = udf(lambda x: datetime.strptime(x.strip("*"),existingDateFormat).strftime(requestedDateFormat), StringType())
            func = udf(lambda x: datetime.strptime(x,existingDateFormat).strftime(requestedDateFormat), StringType())

            self._data_frame = self._data_frame.select(*[func(column).alias(aggregate_column) if column==aggregate_column else column for column in self._data_frame.columns])
            # subset_data = self._data_frame.select(aggregate_column,measure_column, date_udf(aggregate_column).alias("dateString"))
            subset_data = self._data_frame.select(aggregate_column,measure_column, aggregate_column)
            agg_data = subset_data.groupBy(aggregate_column).agg(FN.sum(measure_column)).toPandas()
            agg_data.columns = ["key","value"]
        else:
            agg_data = self._data_frame.groupBy(aggregate_column).agg(FN.sum(measure_column)).toPandas()
            agg_data.columns = ["key","value"]
        return agg_data

    def fill_na_measure_mean(self):
        stats = self._data_frame.agg(*(avg(c).alias(c) for c in self.numeric_columns))
        self._data_frame = self._data_frame.na.fill(stats.first().asDict())
        #return self._data_frame.na.fill(stats.first().asDict())

    def fill_na_dimension_nulls(self):
        self._data_frame = self._data_frame.na.fill(value='nulls',subset=self.string_columns)

    def fill_na_zero(self):
        self._data_frame = self._data_frame.na.fill(0)

    def get_datetime_suggestions(self):
        self.date_time_suggestions = {}
        formats = CommonUtils.dateTimeFormatsSupported()["formats"]
        dual_checks = CommonUtils.dateTimeFormatsSupported()["dual_checks"]

        for dims in self.string_columns:
            row_vals = self._data_frame.select(dims).na.drop().take(int(self.total_rows**0.5 + 1))
            x = row_vals[0][dims]
            for format1 in formats:
                try:
                    t = dt.datetime.strptime(x,format1)
                    if (format1 in dual_checks):
                        for x1 in row_vals:
                            x = x1[dims]
                            try:
                                t = dt.datetime.strptime(x,format1)
                            except ValueError as err:
                                format1 = '%d'+format1[2]+'%m'+format1[5:]
                                break
                    self.date_time_suggestions[dims] = format1
                    break
                except ValueError as err:
                    pass

    def has_date_suggestions(self):
        if len(self.date_time_suggestions)>0:
            return True
        return False

    def get_formats(self):
        self.formats_to_convert = ["mm/dd/YYYY","dd/mm/YYYY","YYYY/mm/dd", "dd <month>, YYYY"]

    ###### An alternative is present in datacleansing. Can fix after final product plan
    def change_format(self,colname,frmt1,frmt2):
        # below line is just for testing a specific type.
        # func = udf(lambda x: datetime.strptime(x.strip("*"),frmt1).strftime(frmt2), StringType())
        func = udf(lambda x: datetime.strptime(x,frmt1).strftime(frmt2), StringType())
        self._data_frame = self._data_frame.select(*[func(column).alias(colname) if column==colname else column for column in self._data_frame.columns])
        return self._data_frame.collect()

    def change_to_date(self, colname, format1):
        func = udf(lambda x: datetime.strptime(x, format1), DateType())
        #self._data_frame = self._data_frame.withColumn(colname, func(col(colname)))
        self._data_frame = self._data_frame.select(*[func(column).alias(colname) if column==colname else column for column in self._data_frame.columns])
        #return self._data_frame.collect()

    def get_datetime_format(self,colname):
        if self._date_formats.has_key(colname):
            return self._date_formats[colname]
        else:
            date_time_suggestions = {}
            formats = CommonUtils.dateTimeFormatsSupported()["formats"]
            dual_checks = CommonUtils.dateTimeFormatsSupported()["dual_checks"]

            row_vals = self._data_frame.select(colname).na.drop().take(int(self._data_frame.count()**0.5 + 1))
            x = row_vals[0][colname]
            for format1 in formats:
                try:
                    t = datetime.strptime(x,format1)
                    date_time_suggestions[colname] = format1
                    self._date_formats[colname] = format1
                    break
                except ValueError as err:
                    pass
            return date_time_suggestions

    def get_train_test_data(self):
        train_test_data = self.train_test_data
        x_train = train_test_data["x_train"]
        x_test = train_test_data["x_test"]
        y_train = train_test_data["y_train"]
        y_test = train_test_data["y_test"]
        return (x_train,x_test,y_train,y_test)

class DataFrameColumnMetadata:
    @accepts(object, basestring, type(ColumnType.MEASURE), type(ColumnType.INTEGER))
    def __init__(self, column_name, abstract_data_type, actual_data_type):
        self._column_name = column_name
        self._abstract_data_type = abstract_data_type
        self._actual_data_type = actual_data_type

    def get_column_name(self):
        return self._column_name

    def get_abstract_data_type(self):
        return self._abstract_data_type

    def get_actual_data_type(self):
        return self._actual_data_type

    def as_dict(self):
        ''' Utility function return object as a dict for persisting as a JSON object
        :return:
        '''
        return {
            self._column_name: self._column_type,
            'actual_data_type': self._actual_data_type,
            'abstract_data_type': self._abstract_data_type
        }
