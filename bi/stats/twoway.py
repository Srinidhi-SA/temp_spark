import pandas as pd
from datetime import datetime
from pyspark.sql import functions as FN
from pyspark.sql.functions import mean, sum, col, count, udf
from pyspark.sql.types import StringType

from bi.common.decorators import accepts
from bi.common.results import DFTwoWayAnovaResult
from bi.common.results import MeasureAnovaResult
from bi.common.results import TopDimensionStats, TrendResult

from bi.narratives import utils as NarrativesUtils

#from bi.stats.descr import DescriptiveStats

"""
Two way ANOVA test
"""


class TwoWayAnova:

    '''
        var1 = n*mean2
        var2 = sum(x2)
        var5 = n*mean2 for each group(a,b)
        var3 = n*mean2 for each group a

    '''

    def __init__(self, data_frame, df_helper, df_context):
        self._data_frame = data_frame
        self._data_frame_helper = df_helper
        self._measure_columns = self._data_frame_helper.get_numeric_columns()
        self._dimension_columns = self._data_frame_helper.get_string_columns()
        self._df_rows = self._data_frame_helper.get_num_rows()
        self.top_dimension_result = {}
        self._dateFormatConversionDict = NarrativesUtils.date_formats_mapping_dict()
        self._dateFormatDetected = False
        self.trend_result = ''
        self.get_primary_time_dimension(df_context)

    def get_aggregated_by_date(self, aggregate_column, measure_column, existingDateFormat = None, \
                                requestedDateFormat = None, on_subset = False):
        if on_subset:
            data_frame = self._df_subset.na.drop(subset=aggregate_column)
        else:
            data_frame = self._data_frame.na.drop(subset=aggregate_column)
        if existingDateFormat != None and requestedDateFormat != None:
            # func = udf(lambda x: datetime.strptime(x,existingDateFormat).strftime(requestedDateFormat), StringType())
            # data_frame = data_frame.select(*[func(column).alias(aggregate_column) if column==aggregate_column else column for column in self._data_frame.columns])
            # subset_data = data_frame.select(aggregate_column,measure_column)
            agg_data = data_frame.groupBy(aggregate_column).agg(FN.sum(measure_column)).toPandas()
            try:
                agg_data['date_col'] = pd.to_datetime(agg_data[aggregate_column], format = existingDateFormat)
            except:
                existingDateFormat = existingDateFormat[3:6]+existingDateFormat[0:3]+existingDateFormat[6:]
                agg_data['date_col'] = pd.to_datetime(agg_data[aggregate_column], format = existingDateFormat)
            agg_data = agg_data.sort_values('date_col')
            agg_data[aggregate_column] = agg_data['date_col'].dt.strftime(requestedDateFormat)
            agg_data.columns = ["Date","measure","date_col"]
            agg_data = agg_data[['Date','measure']]
        elif existingDateFormat != None:
            agg_data = data_frame.groupBy(aggregate_column).agg(FN.sum(measure_column)).toPandas()
            try:
                agg_data['date_col'] = pd.to_datetime(agg_data[aggregate_column], format = existingDateFormat)
            except:
                existingDateFormat = existingDateFormat[3:6]+existingDateFormat[0:3]+existingDateFormat[6:]
                agg_data['date_col'] = pd.to_datetime(agg_data[aggregate_column], format = existingDateFormat)
            agg_data = agg_data.sort_values('date_col')
            agg_data.columns = ["Date","measure","date_col"]
            agg_data = agg_data[['Date','measure']]
        else:
            agg_data = data_frame.groupBy(aggregate_column).agg(FN.sum(measure_column)).toPandas()
            agg_data.columns = ["Date","measure"]
        return agg_data

    def get_aggregated_by_date_and_dimension(self, aggregate_column, measure_column, dimension_column,\
                                existingDateFormat = None, requestedDateFormat = None):
        data_frame = self._data_frame.na.drop(subset=aggregate_column)
        if existingDateFormat != None and requestedDateFormat != None:
            func = udf(lambda x: datetime.strptime(x,existingDateFormat).strftime(requestedDateFormat), StringType())
            # data_frame = data_frame.select(*[func(column).alias(aggregate_column) if column==aggregate_column else column for column in self._data_frame.columns])
            # subset_data = data_frame.select(aggregate_column,measure_column, dimension_column, aggregate_column)
            agg_data = data_frame.groupBy([aggregate_column,dimension_column]).agg(FN.sum(measure_column)).toPandas()
            agg_data.columns = ["Date","dimension","measure"]
            try:
                agg_data['date_col'] = pd.to_datetime(agg_data['Date'], format = existingDateFormat)
            except:
                existingDateFormat = existingDateFormat[3:6]+existingDateFormat[0:3]+existingDateFormat[6:]
                agg_data['date_col'] = pd.to_datetime(agg_data['Date'], format = existingDateFormat)
            agg_data = agg_data.sort_values('date_col')
            agg_data['Date'] = agg_data['date_col'].dt.strftime(requestedDateFormat)
            agg_data = agg_data[["Date","dimension","measure"]]
        else:
            agg_data = data_frame.groupBy([aggregate_column,dimension_column]).agg(FN.sum(measure_column)).toPandas()
            agg_data.columns = ["Date","dimension","measure"]
            try:
                agg_data['date_col'] = pd.to_datetime(agg_data['Date'], format = existingDateFormat)
            except:
                existingDateFormat = existingDateFormat[3:6]+existingDateFormat[0:3]+existingDateFormat[6:]
                agg_data['date_col'] = pd.to_datetime(agg_data['Date'], format = existingDateFormat)
            agg_data = agg_data.sort_values('date_col')
            agg_data = agg_data[["Date","dimension","measure"]]
        grouped_data = agg_data.groupby('dimension').agg({'measure' : ['first', 'last', 'sum']}).reset_index()
        return grouped_data

    def initialise_trend_object(self, measure):
        agg_data_frame = self.get_aggregated_by_date(self._primary_date, measure, \
                                                    self._existingDateFormat, self._requestedDateFormat)
        self.trend_result = TrendResult(agg_data_frame, self._primary_date, measure)

    def get_primary_time_dimension(self, df_context):
        # timestamp_columns = self._data_frame_helper.get_timestamp_columns()
        date_suggestion_cols = df_context.get_date_column_suggestions()
        # if len(timestamp_columns)>0:
        #     self._primary_date = timestamp_columns[0]
        if date_suggestion_cols != None:
            self._primary_date = date_suggestion_cols[0]
            self.get_date_conversion_formats(df_context)
        else:
            self._primary_date = None

    def get_date_conversion_formats(self, df_context):
        dateColumnFormatDict =  self._data_frame_helper.get_datetime_format(self._primary_date)
        if self._primary_date in dateColumnFormatDict.keys():
            self._existingDateFormat = dateColumnFormatDict[self._primary_date]
            self._dateFormatDetected = True

        if df_context.get_requested_date_format() != None:
            self._requestedDateFormat = df_context.get_requested_date_format()[0]
        else:
            self._requestedDateFormat = None

        if self._requestedDateFormat != None:
            self._requestedDateFormat = self._dateFormatConversionDict[self._requestedDateFormat]
        else:
            self._requestedDateFormat = self._existingDateFormat

    @accepts(object, measure_columns=(list, tuple), dimension_columns=(list, tuple), max_num_levels=int)
    def test_all(self, measure_columns=None, dimension_columns=None, max_num_levels=200):
        measures = measure_columns
        if measure_columns is None:
            measures = self._measure_columns
        dimensions = dimension_columns
        if dimension_columns is None:
            dimensions = self._dimension_columns
        max_num_levels = min(max_num_levels, round(self._data_frame_helper.get_num_rows()**0.5))
        DF_Anova_Result = DFTwoWayAnovaResult()
        dimensions_to_test = [dim for dim in dimensions if self._data_frame_helper.get_num_unique_values(dim) <= max_num_levels]
        self._dimensions_to_test = dimensions_to_test
        for m in measures:
            #var = self._data_frame.select(col(m).alias('x'),(col(m)**2).alias('x2')).agg({'x':'count','x':'mean','x2':'sum'}).collect()
            var = self._data_frame.select(col(m).alias('x'),(col(m)**2).alias('x2')).agg(*[count(col('x')),mean(col('x')),sum(col('x2'))]).collect()
            global_mean = var[0][1]
            sst = self._data_frame.select((col(m)-global_mean)*(col(m)-global_mean)).agg({'*':'sum'}).collect()[0][0]
            self._anova_result = MeasureAnovaResult(var[0],sst)
            if self._dateFormatDetected:
                self.initialise_trend_object(m)
            self.test_against(m, dimensions_to_test)
            self._anova_result.set_TrendResult(self.trend_result)
            DF_Anova_Result.add_measure_result(m,self._anova_result)
        return DF_Anova_Result

    def get_aggregated_by_dimension(self, measure, dimension, df=None):
        if df==None:
            return self._data_frame.na.drop(subset=dimension).groupby(dimension).agg(*[count(col(measure)),mean(col(measure))]).collect()
        else:
            return df.na.drop(subset=dimension).groupby(dimension).agg(*[count(col(measure)),mean(col(measure))]).collect()

    def test_anova(self,measure,dimension):
        #var = self._data_frame.na.drop(subset=dimension).groupby(dimension).agg(*[count(col(measure)),mean(col(measure))]).collect()
        var = self.get_aggregated_by_dimension(measure, dimension)
        var = pd.DataFrame(var,columns=['levels', 'counts', 'means'])
        var['total'] = var.means*var.counts
        #var['var3'] = var.counts*var.means*var.means
        sse = 0
        argmax = var.total.argmax()
        for i in range(len(var)):
            group_sse = self._data_frame.filter(col(dimension)==var.levels[i]).\
                        select((col(measure)-var.means[i])*(col(measure)-var.means[i])).\
                        agg({'*':'sum'}).collect()
            sse = sse+group_sse[0][0]
            if i==argmax:
                sst = group_sse[0][0]
        self._anova_result.set_OneWayAnovaResult(dimension,var,sse)
        if self._anova_result.get_OneWayAnovaResult(dimension).is_statistically_significant(alpha = 0.05):
            self.test_anova_top_dimension(var, measure, dimension, sst)
            effect_size = self._anova_result.get_OneWayAnovaEffectSize(dimension)
            self._data_frame_helper.add_significant_dimension(dimension,effect_size)

    def test_anova_top_dimension(self, var, measure, dimension, sst):
        top_dimension = var.ix[var.total.argmax()]
        self._top_dimension = top_dimension
        self._df_subset = self._data_frame.where(col(dimension).isin([top_dimension.levels]))
        dimensions_to_test_for_top_dimension = set(self._dimensions_to_test)-set([dimension])
        self.top_dimension_result[dimension] = TopDimensionStats(top_dimension.levels,top_dimension.total, top_dimension.counts, top_dimension.means, sst)
        for dim in dimensions_to_test_for_top_dimension:
            self.set_top_dimension_result(measure, dim, dimension)

    def set_top_dimension_result(self, measure, dimension, agg_dimension):
        var = self.get_aggregated_by_dimension(measure, dimension, self._df_subset)
        var = pd.DataFrame(var,columns=['levels', 'counts', 'means'])
        var['total'] = var.means*var.counts
        #var['var3'] = var.counts*var.means*var.means
        sse = 0
        for i in range(len(var)):
            group_sse = self._df_subset.filter(col(dimension)==var.levels[i]).\
                        select((col(measure)-var.means[i])*(col(measure)-var.means[i])).\
                        agg({'*':'sum'}).collect()
            sse = sse+group_sse[0][0]
        self.top_dimension_result[agg_dimension].set_p_value(var, sse, dimension)
        # TODO: check for significant dimension and add trend result only if significant
        # if self.top_dimension_result[agg_dimension].get_p_value(dimension)<=0.05:
        if self._dateFormatDetected:
                self.set_trend_result(measure, dimension, agg_dimension)

    def set_trend_result(self, measure, dimension, agg_dimension):
        if not self.trend_result.subset_df.has_key(agg_dimension):
            agg_data_frame = self.get_aggregated_by_date(self._primary_date, measure, \
                                                    self._existingDateFormat, self._requestedDateFormat,True)
            self.trend_result.add_subset_df(agg_data_frame,agg_dimension, self._top_dimension)
        agg_data_frame_dimension = self.get_aggregated_by_date_and_dimension(self._primary_date, measure, dimension,\
                                                                self._existingDateFormat, self._requestedDateFormat)
        self.trend_result.add_trend_result(dimension,agg_data_frame_dimension)

    def test_against(self,measure, dimensions):
        for dimension in dimensions:
            self.test_anova(measure,dimension)
        self._anova_result.set_OneWayAnova_Contributions(self.top_dimension_result)
        '''for i in range(0,len(dimensions)-1):
            for j in range(i+1,len(dimensions)):
                self.test_anova_interaction(measure,dimensions[i],dimensions[j])'''

    def test_anova_interaction(self,measure,dimension1,dimension2):
        var = self._data_frame.groupby(dimension1,dimension2).agg(*[count(col(measure)),mean(col(measure))]).collect()
        var = pd.DataFrame(var,columns=['level1','level2', 'counts', 'means'])
        var['total'] = var.means*var.counts
        #var['var5'] = var.counts*var.means*var.means
        sse = 0
        for i in range(len(var)):
            group_sse = self._data_frame.filter((col(dimension1)==var.level1[i]) & (col(dimension2)==var.level2[i])).\
                        select((col(measure)-var.means[i])*(col(measure)-var.means[i])).\
                        agg({'*':'sum'}).collect()
            sse = sse+group_sse[0][0]
        self._anova_result.set_TwoWayAnovaResult(dimension1,dimension2,var,sse)
