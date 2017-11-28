import pandas as pd
import time
from datetime import datetime
from scipy.stats import f
import __builtin__
from pyspark.sql import functions as FN
from pyspark.sql.functions import mean, sum, min, max, count, udf, col
from pyspark.sql.types import StringType

from bi.common.decorators import accepts
from bi.common.results import DFTwoWayAnovaResult,OneWayAnovaResult
from bi.common.results import MeasureAnovaResult
from bi.common.results import TopDimensionStats, TrendResult,TopLevelDfAnovaStats

from bi.narratives import utils as NarrativesUtils
from bi.common import utils as CommonUtils



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
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context
        self._measure_columns = self._dataframe_helper.get_numeric_columns()
        self._dimension_columns = self._dataframe_helper.get_string_columns()
        self._timestamp_columns = self._dataframe_helper.get_timestamp_columns()
        self._date_column = self._dataframe_context.get_date_columns()
        self._date_column_suggestions = self._dataframe_context.get_datetime_suggestions()
        if self._date_column != None:
            if len(self._date_column) >0 :
                self._dimension_columns = list(set(self._dimension_columns)-set(self._date_column))
        if len(self._date_column_suggestions) > 0:
            if self._date_column_suggestions[0] != {}:
                self._dimension_columns = list(set(self._dimension_columns)-set(self._date_column_suggestions[0].keys()))
        self._df_rows = self._dataframe_helper.get_num_rows()
        self.top_dimension_result = {}
        self._dateFormatConversionDict = NarrativesUtils.date_formats_mapping_dict()
        self._dateFormatDetected = False
        self.trend_result = ''
        self._existingDateFormat=None
        self._requestedDateFormat = '%m-%d-%Y'
        self._trend_on_td_column = False
        self.get_primary_time_dimension(df_context)

        self._completionStatus = self._dataframe_context.get_completion_status()
        self._analysisName = self._dataframe_context.get_analysis_name()
        self._analysisDict = self._dataframe_context.get_analysis_dict()
        self._messageURL = self._dataframe_context.get_message_url()
        self._scriptWeightDict = self._dataframe_context.get_measure_analysis_weight()
        self._scriptStages = {
            "anovaStart":{
                "summary":"Initialized the Anova Scripts",
                "weight":0
                },
            "anovaEnd":{
                "summary":"Anova Calculated",
                "weight":10
                },
            }
        progressMessage = CommonUtils.create_progress_message_object(self._analysisName,\
                                    "anovaStart",\
                                    "info",\
                                    self._scriptStages["anovaStart"]["summary"],\
                                    self._completionStatus,\
                                    self._completionStatus)
        CommonUtils.save_progress_message(self._messageURL,progressMessage)
        self._dataframe_context.update_completion_status(self._completionStatus)



    @accepts(object, measure_columns=(list, tuple), dimension_columns=(list, tuple))
    def test_all(self, measure_columns=None, dimension_columns=None):
        measures = measure_columns
        if measure_columns is None:
            measures = self._measure_columns
        dimensions = dimension_columns
        if dimension_columns is None:
            dimensions = self._dimension_columns
        nColsToUse = self._analysisDict[self._analysisName]["noOfColumnsToUse"]
        if nColsToUse != None:
            dimensions = dimensions[:nColsToUse]
        sqrt_nrows = round(self._dataframe_helper.get_num_rows()**0.5)
        acceptable_level_count = self._dataframe_context.get_anova_max_levels()
        print acceptable_level_count,sqrt_nrows
        max_levels = __builtin__.min([acceptable_level_count,int(sqrt_nrows)])
        df_anova_result = DFTwoWayAnovaResult()
        dimensions_to_test = [dim for dim in dimensions if self._dataframe_helper.get_num_unique_values(dim) <= max_levels]
        self._dimensions_to_test = dimensions_to_test
        print "dimensions to test ",self._dimensions_to_test
        for measure in measures:
            measureColStat = self._data_frame.select([sum(measure).alias("total"),mean(measure).alias("average"),count(measure).alias("count")]).collect()
            measureColMean = measureColStat[0][1]
            measureColCount = measureColStat[0][2]
            measureColSst = self._data_frame.select(sum(pow(col(measure)-measureColMean,2))).collect()[0][0]
            self._anova_result = MeasureAnovaResult(measureColMean=measureColMean,measureColCount=measureColCount, measureColSst=measureColSst)

            for dimension in self._dimensions_to_test:
                anovaResult = self.one_way_anova_test(self._data_frame,measure,dimension,measureColMean=measureColMean,measureColCount=measureColCount, measureColSst=measureColSst)
                dimensionAnovaResult = OneWayAnovaResult()
                dimensionAnovaResult.set_params(df_within=anovaResult["df_within"],
                                                df_between=anovaResult["df_between"],
                                                sum_of_squares_between=anovaResult["ss_between"],
                                                sum_of_squares_within=anovaResult["ss_within"],
                                                mean_sum_of_squares_between=anovaResult["ms_between"],
                                                mean_sum_of_squares_within=anovaResult["ms_within"],
                                                f_value=anovaResult["f_stat"],
                                                p_value=anovaResult["p_value"],
                                                eta_squared=anovaResult["eta_squared"],
                                                f_critical=anovaResult["f_critical"],
                                                total_number_of_records=anovaResult["n_total"],
                                                n_groups=anovaResult["n_groups"],
                                                levelDf=anovaResult["levelDf"]
                                                )
                self._anova_result.set_oneWayAnovaResultDict(dimension,dimensionAnovaResult)
                # for top level
                if anovaResult["p_value"] < 0.05:
                    effect_size = anovaResult["eta_squared"]
                    self._dataframe_helper.add_significant_dimension(dimension,effect_size)
                    topLevelAnova = TopLevelDfAnovaStats()
                    levelDf = anovaResult["levelDf"]
                    toplevelStats = levelDf.ix[levelDf["total"].argmax()]
                    print toplevelStats
                    topLevelAnova.set_top_level_stat(toplevelStats)
                    topLevelDf = self._data_frame.where(col(dimension).isin([toplevelStats.levels]))
                    topLevelDfMeasureColStat = topLevelDf.select([sum(measure).alias("total"),mean(measure).alias("average"),count(measure).alias("count")]).collect()
                    topLevelDfMeasureColMean = measureColStat[0][1]
                    topLevelDfMeasureColCount = measureColStat[0][2]
                    topLevelDfMeasureColSst = self._data_frame.select(sum(pow(col(measure)-measureColMean,2))).collect()[0][0]
                    dimensions_to_test_for_top_level = list(set(self._dimensions_to_test)-set([dimension]))
                    topLevelAnovaDimensions = {}
                    for dimensionlTopLevel in dimensions_to_test_for_top_level:
                        print "top level dimensions",dimensionlTopLevel
                        topLevelDfAnovaResult = self.one_way_anova_test(topLevelDf,measure,dimensionlTopLevel,measureColMean=topLevelDfMeasureColMean,measureColCount=topLevelDfMeasureColCount,measureColSst=topLevelDfMeasureColSst)
                        dimensiontopLevelAnovaResult = OneWayAnovaResult()
                        dimensiontopLevelAnovaResult.set_params(df_within=topLevelDfAnovaResult["df_within"],
                                                        df_between=topLevelDfAnovaResult["df_between"],
                                                        sum_of_squares_between=topLevelDfAnovaResult["ss_between"],
                                                        sum_of_squares_within=topLevelDfAnovaResult["ss_within"],
                                                        mean_sum_of_squares_between=topLevelDfAnovaResult["ms_between"],
                                                        mean_sum_of_squares_within=topLevelDfAnovaResult["ms_within"],
                                                        f_value=topLevelDfAnovaResult["f_stat"],
                                                        p_value=topLevelDfAnovaResult["p_value"],
                                                        eta_squared=topLevelDfAnovaResult["eta_squared"],
                                                        f_critical=topLevelDfAnovaResult["f_critical"],
                                                        total_number_of_records=topLevelDfAnovaResult["n_total"],
                                                        n_groups=topLevelDfAnovaResult["n_groups"],
                                                        levelDf=topLevelDfAnovaResult["levelDf"]
                                                        )
                        topLevelAnova.set_top_level_anova(dimensionlTopLevel,dimensiontopLevelAnovaResult)
                        # contributionDict = self.compute_contributions(topLevelDfAnovaResult["levelDf"])
                        # print contributionDict
                        # topLevelAnova.set_dimension_contributions(dimension,contributionDict)
                    self._anova_result.set_topLevelDfAnovaResult(dimension,topLevelAnova)

            df_anova_result.add_measure_result(measure,self._anova_result)
            print self._anova_result.get_dimensions_analyzed()
            print "checking effect size access",self._anova_result.get_OneWayAnovaEffectSize(self._dimensions_to_test[0])


        self._completionStatus += self._scriptWeightDict[self._analysisName]["script"]
        progressMessage = CommonUtils.create_progress_message_object(self._analysisName,\
                                    "anovaEnd",\
                                    "info",\
                                    self._scriptStages["anovaEnd"]["summary"],\
                                    self._completionStatus,\
                                    self._completionStatus)
        CommonUtils.save_progress_message(self._messageURL,progressMessage)
        self._dataframe_context.update_completion_status(self._completionStatus)
        return df_anova_result



    def one_way_anova_test(self,df,measure,dimension,measureColMean=None,measureColCount=None,measureColSst=None):
        st=time.time()
        print "running anova for :-","measure-",measure,"|***|","dimension-",dimension
        if measureColMean == None:
            measureColStat = df.select([sum(measure).alias("total"),mean(measure).alias("average")]).collect()
            overallMean = measureColStat[0][1]
        else:
            overallMean = measureColMean
        level_aggregate_df = df.na.drop(subset=dimension).groupby(dimension).agg(*[count(col(measure)).alias("count"),mean(col(measure)).alias("average")])
        level_aggregate_df = level_aggregate_df.withColumn("total",col("count")*col("average"))
        level_aggregate_pandasdf = level_aggregate_df.toPandas()
        if measureColCount != None:
            n_total = df.count()
        else:
            n_total = measureColCount
        n_groups = level_aggregate_df.count()
        df_total = n_total-1
        df_within = n_total-n_groups
        df_between = n_groups-1
        if measureColSst == None:
            ss_total = df.select(sum(pow(col(measure)-overallMean,2))).collect()[0][0]
        else:
            ss_total = measureColSst
        ss_between = level_aggregate_df.select(sum(pow(col("average")-overallMean,2))).collect()[0][0]
        ss_within = 0
        for index, row in level_aggregate_pandasdf.iterrows():
            filtered_df = df.filter(col(dimension)==row[dimension])
            group_sse = filtered_df.select(sum(pow(col(measure)-row["average"],2))).collect()[0][0]
            ss_within = ss_within+group_sse

        ms_between = ss_between/df_between
        ms_within = ss_within/df_within
        f_stat = ms_between/ms_within
        f_critical = f.ppf(q=1-0.05, dfn=df_between, dfd=df_within)
        p_value = f.cdf(f_stat, df_between, df_within)
        eta_squared = ss_between/ss_total
        level_aggregate_pandasdf.columns = ["levels"]+list(level_aggregate_pandasdf.columns[1:])
        anovaOutput = {
                       "df_total":df_total,
                       "df_within":df_within,
                       "df_between":df_between,
                       "n_total":n_total,
                       "n_groups":n_groups,
                       "ss_between":ss_between,
                       "ss_within":ss_within,
                       "ss_total":ss_total,
                       "ms_between":ms_between,
                       "ms_within":ms_within,
                       "f_stat":f_stat,
                       "f_critical":f_critical,
                       "p_value":p_value,
                       "eta_squared":eta_squared,
                       "levelDf":level_aggregate_pandasdf
                      }
        # print anovaOutput
        print "finished in :-",time.time()-st
        return anovaOutput

    def get_aggregated_by_dimension(self, measure, dimension, df=None):
        if df==None:
            return self._data_frame.na.drop(subset=dimension).groupby(dimension).agg(*[count(col(measure)),mean(col(measure))]).collect()
        else:
            return df.na.drop(subset=dimension).groupby(dimension).agg(*[count(col(measure)),mean(col(measure))]).collect()

    def test_anova(self,df,measure,dimension):
        print measure,dimension
        level_aggregate_df = df.na.drop(subset=dimension).groupby(dimension).agg(*[count(col(measure)).alias("count"),mean(col(measure)).alias("average")])
        level_aggregate_df = level_aggregate_df.withColumn("total",col("count")*col("average"))
        level_aggregate_pandasdf = level_aggregate_df.toPandas()

        sse = 0
        argmax = level_aggregate_pandasdf["total"].idxmax()
        print "argmax",argmax
        for index, row in level_aggregate_pandasdf.iterrows():
            print index,row[dimension]
            filtered_df = df.filter(col(dimension)==row[dimension])
            group_sse = filtered_df.select(sum(pow(col(measure)-row["average"],2))).collect()[0][0]
            print group_sse
            print "group_sse", row["average"],group_sse
            sse = sse+group_sse
            if i==argmax:
                sst = group_sse[0][0]
        self._anova_result.set_OneWayAnovaResult(dimension,var,sse)
        if self._anova_result.get_OneWayAnovaResult(dimension).is_statistically_significant(alpha = 0.05):
            self.test_anova_top_dimension(var, measure, dimension, sst)
            effect_size = self._anova_result.get_OneWayAnovaEffectSize(dimension)
            self._dataframe_helper.add_significant_dimension(dimension,effect_size)

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
            if self._primary_date in self._timestamp_columns:
                agg_data_frame = self.get_aggregated_by_date(self._primary_date, measure, \
                                                    None, self._requestedDateFormat,True,
                                                    use_timestamp=self._primary_date in self._timestamp_columns)
            else:
                agg_data_frame = self.get_aggregated_by_date(self._primary_date, measure, \
                                                    self._existingDateFormat, self._requestedDateFormat,True,
                                                    use_timestamp=False)
            self.trend_result.add_subset_df(agg_data_frame,agg_dimension, self._top_dimension)
        agg_data_frame_dimension = self.get_aggregated_by_date_and_dimension(self._primary_date, measure, dimension,\
                                                                self._existingDateFormat, self._requestedDateFormat,
                                                                use_timestamp=self._primary_date in self._timestamp_columns)
        self.trend_result.add_trend_result(dimension,agg_data_frame_dimension)

    def test_against(self,df,measure, dimensions):
        for dimension in dimensions:
            self.test_anova(df,measure,dimension)
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

    def get_aggregated_by_date(self, aggregate_column, measure_column, existingDateFormat = None, \
                                requestedDateFormat = None, on_subset = False,use_timestamp=False):
        if on_subset:
            data_frame = self._df_subset.na.drop(subset=aggregate_column)
        else:
            data_frame = self._data_frame.na.drop(subset=aggregate_column)
        if existingDateFormat != None and requestedDateFormat != None:
            # func = udf(lambda x: datetime.strptime(x,existingDateFormat).strftime(requestedDateFormat), StringType())
            # data_frame = data_frame.select(*[func(column).alias(aggregate_column) if column==aggregate_column else column for column in self._data_frame.columns])
            # subset_data = data_frame.select(aggregate_column,measure_column)
            agg_data = data_frame.groupBy(aggregate_column).agg(FN.sum(measure_column)).toPandas()
            if not use_timestamp:
                try:
                    agg_data['date_col'] = pd.to_datetime(agg_data[aggregate_column], format = existingDateFormat)
                except:
                    existingDateFormat = existingDateFormat[3:6]+existingDateFormat[0:3]+existingDateFormat[6:]
                    agg_data['date_col'] = pd.to_datetime(agg_data[aggregate_column], format = existingDateFormat)
            else:
                agg_data['date_col']=agg_data[aggregate_column]
            agg_data = agg_data.sort_values('date_col')
            agg_data[aggregate_column] = agg_data['date_col'].dt.strftime(requestedDateFormat)
            agg_data.columns = ["Date","measure","date_col"]
            agg_data = agg_data[['Date','measure']]
        elif existingDateFormat != None:
            agg_data = data_frame.groupBy(aggregate_column).agg(FN.sum(measure_column)).toPandas()
            if not use_timestamp:
                try:
                    agg_data['date_col'] = pd.to_datetime(agg_data[aggregate_column], format = existingDateFormat)
                except:
                    existingDateFormat = existingDateFormat[3:6]+existingDateFormat[0:3]+existingDateFormat[6:]
                    agg_data['date_col'] = pd.to_datetime(agg_data[aggregate_column], format = existingDateFormat)
            else:
                agg_data['date_col']=agg_data[aggregate_column]
            agg_data = agg_data.sort_values('date_col')
            agg_data.columns = ["Date","measure","date_col"]
            agg_data = agg_data[['Date','measure']]
        else:
            agg_data = data_frame.groupBy(aggregate_column).agg(FN.sum(measure_column)).toPandas()
            agg_data.columns = ["Date","measure"]
            agg_data = agg_data.sort_values('Date')
            agg_data = agg_data[['Date','measure']]
        return agg_data

    def get_aggregated_by_date_and_dimension(self, aggregate_column, measure_column, dimension_column,\
                                existingDateFormat = None, requestedDateFormat = None,use_timestamp=False):
        data_frame = self._data_frame.na.drop(subset=aggregate_column)
        if existingDateFormat != None and requestedDateFormat != None:
            func = udf(lambda x: datetime.strptime(x,existingDateFormat).strftime(requestedDateFormat), StringType())
            # data_frame = data_frame.select(*[func(column).alias(aggregate_column) if column==aggregate_column else column for column in self._data_frame.columns])
            # subset_data = data_frame.select(aggregate_column,measure_column, dimension_column, aggregate_column)
            agg_data = data_frame.groupBy([aggregate_column,dimension_column]).agg(FN.sum(measure_column)).toPandas()
            agg_data.columns = ["Date","dimension","measure"]
            if use_timestamp:
                agg_data['date_col'] = agg_data['Date']
            else:
                try:
                    agg_data['date_col'] = pd.to_datetime(agg_data['Date'], format = existingDateFormat)
                except:
                    existingDateFormat = existingDateFormat[3:6]+existingDateFormat[0:3]+existingDateFormat[6:]
                    agg_data['date_col'] = pd.to_datetime(agg_data['Date'], format = existingDateFormat)
            agg_data = agg_data.sort_values('date_col')
            agg_data['Date'] = agg_data['date_col'].dt.strftime(requestedDateFormat)
            agg_data = agg_data[["Date","dimension","measure"]]
        elif existingDateFormat != None:
            agg_data = data_frame.groupBy([aggregate_column,dimension_column]).agg(FN.sum(measure_column)).toPandas()
            agg_data.columns = ["Date","dimension","measure"]
            if use_timestamp:
                agg_data['date_col'] = agg_data['Date']
            else:
                try:
                    agg_data['date_col'] = pd.to_datetime(agg_data['Date'], format = existingDateFormat)
                except:
                    existingDateFormat = existingDateFormat[3:6]+existingDateFormat[0:3]+existingDateFormat[6:]
                    agg_data['date_col'] = pd.to_datetime(agg_data['Date'], format = existingDateFormat)
            agg_data = agg_data.sort_values('date_col')
            agg_data = agg_data[["Date","dimension","measure"]]
        else:
            agg_data = data_frame.groupBy([aggregate_column,dimension_column]).agg(FN.sum(measure_column)).toPandas()
            agg_data.columns = ["Date","dimension","measure"]
            agg_data = agg_data.sort_values('Date')
        grouped_data = agg_data.groupby('dimension').agg({'measure' : ['first', 'last', 'sum']}).reset_index()
        return grouped_data

    def initialise_trend_object(self, measure, use_timestamp=False):
        if use_timestamp:
            agg_data_frame = self.get_aggregated_by_date(self._timestamp_columns[0], measure, \
                                                        None, self._requestedDateFormat,
                                                        use_timestamp=True)
            self.trend_result = TrendResult(agg_data_frame, self._timestamp_columns[0], measure)
        else:
            agg_data_frame = self.get_aggregated_by_date(self._primary_date, measure, \
                                                    self._existingDateFormat, self._requestedDateFormat)
            self.trend_result = TrendResult(agg_data_frame, self._primary_date, measure)

    def get_primary_time_dimension(self, df_context):
        # timestamp_columns = self._dataframe_helper.get_timestamp_columns()
        date_suggestion_cols = df_context.get_date_columns()
        # if len(timestamp_columns)>0:
        #     self._primary_date = timestamp_columns[0]
        if date_suggestion_cols != None and len(date_suggestion_cols)>0:
            self._primary_date = date_suggestion_cols[0]
            if self._primary_date in self._timestamp_columns:
                self._trend_on_td_column = True
                self._existingDateFormat = "%Y-%m-%d"
                self._dateFormatDetected = True
                if df_context.get_requested_date_format() != None:
                    self._requestedDateFormat = df_context.get_requested_date_format()[0]
                else:
                    self._requestedDateFormat = None
                if self._requestedDateFormat != None:
                    self._requestedDateFormat = self._dateFormatConversionDict[self._requestedDateFormat]
                else:
                    self._requestedDateFormat = self._existingDateFormat
            else:
                self.get_date_conversion_formats(df_context)
        else:
            self._primary_date = None

    def get_date_conversion_formats(self, df_context):
        dateColumnFormatDict =  self._dataframe_helper.get_datetime_format(self._primary_date)
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
