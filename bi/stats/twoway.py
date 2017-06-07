from pyspark.sql import DataFrame
from pyspark.sql import functions as FN
from pyspark.sql.functions import mean, sum, col, count
import math

from bi.common.decorators import accepts
from bi.common import BIException
from bi.common import DataFrameHelper
import pandas as pd

from bi.common.results import DFTwoWayAnovaResult
from bi.common.results import MeasureAnovaResult
from bi.common.results import TwoWayAnovaResult
from bi.common.results import OneWayAnovaResult, TopDimensionStats

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
            self.test_against(m, dimensions_to_test)
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

    def test_anova_top_dimension(self, var, measure, dimension, sst):
        top_dimension = var.ix[var.total.argmax()]
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
