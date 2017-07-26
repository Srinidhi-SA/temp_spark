import json
import os

from datetime import datetime
from dateutil.relativedelta import relativedelta

from bi.narratives import utils as NarrativesUtils
from trend_narratives import TrendNarrative

from pyspark.sql.functions import col, udf, max
from pyspark.sql.types import *
from pyspark.sql.functions import monotonically_increasing_id




class TimeSeriesNarrative:
    def __init__(self, df_helper, df_context, result_setter, spark):
        self._result_setter = result_setter
        self._dataframe_helper = df_helper
        self._data_frame = df_helper.get_data_frame()
        self._spark = spark
        self._dataframe_context = df_context

        self._dateFormatDetected = False
        self._requestedDateFormat = None
        self._existingDateFormat = None
        self._date_suggestion_columns = df_context.get_date_column_suggestions()
        self._dateFormatConversionDict = NarrativesUtils.date_formats_mapping_dict()
        self._td_columns = df_helper.get_timestamp_columns()
        self._result_column = df_context.get_result_column()
        self._analysistype = self._dataframe_context.get_analysis_type()

        # requestedDateFormat = None
        # existingDateFormat = None
        if self._date_suggestion_columns != None:
            suggested_date_column = self._date_suggestion_columns[0]
            existingDateFormat = None
            dateColumnFormatDict =  df_helper.get_datetime_format(suggested_date_column)
            if suggested_date_column in dateColumnFormatDict:
                existingDateFormat = dateColumnFormatDict[suggested_date_column]
                self._dateFormatDetected = True
            if df_context.get_requested_date_format() != None:
                requestedDateFormat = df_context.get_requested_date_format()[0]
            else:
                requestedDateFormat = None
            if requestedDateFormat != None:
                requestedDateFormat = self._dateFormatConversionDict[requestedDateFormat]
            else:
                requestedDateFormat = existingDateFormat

        # self._base_dir = os.path.dirname(os.path.realpath(__file__))+"/../../templates/trend/"
        self._base_dir = os.environ.get('MADVISOR_BI_HOME')+"/templates/trend/"
        if self._dateFormatDetected:
            self._requestedDateFormat = requestedDateFormat
            self._existingDateFormat = existingDateFormat
            self._date_column_suggested = suggested_date_column

        if self._existingDateFormat:
            date_format = self._existingDateFormat
            string_to_date = udf(lambda x: datetime.strptime(x,date_format), DateType())
            date_to_month_year = udf(lambda x: datetime.strptime(x,date_format).strftime("%b-%y"), StringType())
            self._data_frame = self._data_frame.withColumn("suggestedDate", string_to_date(self._date_column_suggested))
            self._data_frame = self._data_frame.withColumn("year_month", date_to_month_year(self._date_column_suggested))
            self._data_frame = self._data_frame.orderBy(["suggestedDate"],ascending=[True])
            self._data_frame = self._data_frame.withColumn("_id_", monotonically_increasing_id())
            id_max = self._data_frame.select(max("_id_")).first()[0]
            first_date = self._data_frame.select("suggestedDate").first()[0]
            last_date = self._data_frame.where(col("_id_") == id_max).select("suggestedDate").first()[0]
            self._dataRange = (last_date-first_date).days

            if self._dataRange <= 180:
                self._duration = self._dataRange
                self._dataLevel = "day"
                self._durationString = str(self._duration)+" days"
            elif self._dataRange > 180 and self._dataRange <= 1095:
                self._duration = self._data_frame.select("year_month").distinct().count()
                self._dataLevel = "month"
                self._durationString = str(self._duration)+" months"
            else:
                self._dataLevel = "month"
                self._duration = self._data_frame.select("year_month").distinct().count()
                yr = str(self._dataRange//365)
                mon = str((self._dataRange%365)//12)
                self._durationString = yr+" years and "+mon+" months"
            print self._duration
            print self._dataLevel
            print self._durationString



        if self._analysistype=="Measure":
            self.narratives = {"SectionHeading":"",
                               "card1":{},
                               "card2":{},
                               "card3":{}
                            }
            if self._date_suggestion_columns != None:
                if self._dateFormatDetected:
                    # grouped_data = self._data_frame .groupBy("suggestedDate").agg({ self._result_column : 'sum'})
                    # grouped_data = grouped_data.withColumnRenamed(grouped_data.columns[-1],"value")
                    # grouped_data = grouped_data.withColumn("year_month",udf(lambda x:x.strftime("%b-%y"))("suggestedDate"))
                    # grouped_data = grouped_data.orderBy("suggestedDate",ascending=True)
                    # grouped_data = grouped_data.withColumnRenamed(grouped_data.columns[0],"key")
                    # grouped_data = grouped_data.toPandas()

                    if self._dataLevel == "day":
                        grouped_data = self._data_frame .groupBy("suggestedDate").agg({ self._result_column : 'sum'})
                        grouped_data = grouped_data.withColumnRenamed(grouped_data.columns[-1],"value")
                        grouped_data = grouped_data.withColumn("year_month",udf(lambda x:x.strftime("%b-%y"))("suggestedDate"))
                        grouped_data = grouped_data.orderBy("suggestedDate",ascending=True)
                        grouped_data = grouped_data.withColumnRenamed(grouped_data.columns[0],"key")
                        grouped_data = grouped_data.toPandas()
                    elif self._dataLevel == "month":
                        grouped_data = self._data_frame .groupBy("year_month").agg({ self._result_column : 'sum'})
                        grouped_data = grouped_data.withColumnRenamed(grouped_data.columns[-1],"value")
                        grouped_data = grouped_data.withColumn("suggestedDate",udf(lambda x:datetime.strptime(x,"%b-%y"))("year_month"))
                        grouped_data = grouped_data.orderBy("suggestedDate",ascending=True)
                        grouped_data = grouped_data.withColumnRenamed("suggestedDate","key")
                        grouped_data = grouped_data.select(["key","value","year_month"]).toPandas()
                        grouped_data["key"] = grouped_data["year_month"].apply(lambda x: datetime.strptime(x,"%b-%y").date())


                    pandasDf = self._data_frame.toPandas()
                    pandasDf.drop(self._date_column_suggested,axis=1,inplace=True)
                    pandasDf.rename(columns={'year_month': self._date_column_suggested}, inplace=True)

                    # pandasDf = df_helper.get_data_frame().toPandas()
                    # pandasDf[self._date_column_suggested] = pandasDf[self._date_column_suggested].apply(lambda x:datetime.strptime(x,self._existingDateFormat))
                    # pandasDf[self._date_column_suggested] = pandasDf[self._date_column_suggested].apply(lambda x: month_dict[x.month]+"-"+str(x.year))

                    # grouped_data = df_helper.get_aggregate_data(self._date_column_suggested,self._result_column,
                    #                                                 existingDateFormat=self._existingDateFormat,
                    #                                                 requestedDateFormat=self._requestedDateFormat)
                    significant_dimensions = df_helper.get_significant_dimension()
                    trend_narrative_obj = TrendNarrative(self._result_column,self._date_column_suggested,grouped_data,self._existingDateFormat,self._requestedDateFormat)
                    # grouped_data = trend_narrative_obj.formatDateColumn(grouped_data,self._requestedDateFormat)
                    # grouped_data = grouped_data.sort_values(by='key', ascending=True)
                    # grouped_data["value"] = grouped_data["value"].apply(lambda x: round(x,2))
                    dataDict = trend_narrative_obj.generateDataDict(grouped_data,self._dataLevel,self._durationString)
                    # # update reference time with max value
                    reference_time = dataDict["reference_time"]
                    dataDict["duration"] = self._duration
                    dataDict["dataLevel"] = self._dataLevel
                    dataDict["durationString"] = self._durationString
                    if len(significant_dimensions.keys()) > 0:
                        xtraData = trend_narrative_obj.get_xtra_calculations(pandasDf,grouped_data,significant_dimensions.keys(),self._date_column_suggested,self._result_column,self._existingDateFormat,reference_time,self._dataLevel)
                        if xtraData != None:
                            dataDict.update(xtraData)
                    # print 'Trend dataDict:  %s' %(json.dumps(dataDict, indent=2))
                    self._result_setter.update_executive_summary_data(dataDict)
                    self.narratives["SectionHeading"] = self._result_column+" Performance Report"
                    summary1 = NarrativesUtils.get_template_output(self._base_dir,\
                                                                    'trend_narrative_card1.temp',dataDict)
                    summary2 = NarrativesUtils.get_template_output(self._base_dir,\
                                                                    'trend_narrative_card2.temp',dataDict)

                    self.narratives["card1"]["paragraphs"] = NarrativesUtils.paragraph_splitter(summary1)
                    self.narratives["card1"]["bubbleData"] = dataDict["bubbleData"]
                    self.narratives["card1"]["chart"] = ""
                    self.narratives["card2"]["paragraphs"] = NarrativesUtils.paragraph_splitter(summary2)
                    self.narratives["card2"]["table1"] = dataDict["table_data"]["increase"]
                    self.narratives["card2"]["table2"] = dataDict["table_data"]["decrease"]

                    # grouped_data["key"] = grouped_data["key"].apply(lambda x: month_dict[x.month]+"-"+str(x.year))
                    # trend_chart_data = grouped_data[["key","value"]].groupby("key").agg(sum).reset_index()
                    trend_chart_data = grouped_data[["key","value"]].T.to_dict().values()
                    trend_chart_data = sorted(trend_chart_data,key=lambda x:x["key"])
                    card1chartdata = trend_chart_data
                    card1chartdata = [{"key":val["key"].strftime("%b-%y"),"value":val["value"]} for val in card1chartdata]
                    self.narratives["card1"]["chart"] = {"data":card1chartdata,"format":"%b-%y"}
                    if dataDict["dateRange"]<365:
                        prediction_window = 3
                    else:
                        prediction_window = 6
                    predicted_values = trend_narrative_obj.get_forecast_values(grouped_data["value"],prediction_window)[len(grouped_data["value"]):]
                    predicted_values = [round(x,2) for x in predicted_values]
                    prediction_data = [{"key":x["key"],"value":x["value"]} for x in trend_chart_data]
                    last_val = prediction_data[-1]
                    last_val.update({"predicted_value":last_val["value"]})
                    prediction_data[-1] = last_val
                    for val in range(prediction_window):
                        dataLevel = dataDict["dataLevel"]
                        if dataLevel == "month":
                            last_key = prediction_data[-1]["key"]
                            key = last_key+relativedelta(months=1)
                            prediction_data.append({"key":key,"predicted_value":predicted_values[val]})
                        else:
                            last_key = prediction_data[-1]["key"]
                            key = last_key+relativedelta(days=1)
                            prediction_data.append({"key":key,"predicted_value":predicted_values[val]})
                    prediction_data_copy = prediction_data
                    prediction_data = []
                    for val in prediction_data_copy:
                        val["key"] = val["key"].strftime("%b-%y")
                        prediction_data.append(val)

                    forecastDataDict = {"startForecast":predicted_values[0],
                                        "endForecast":predicted_values[prediction_window-1],
                                        "measure":dataDict["measure"],
                                        "forecast":True,
                                        "forecast_percentage": round((predicted_values[prediction_window-1]-predicted_values[0])/predicted_values[0],2),
                                        "prediction_window_text": str(prediction_window) + " months"
                                        }

                    self._result_setter.update_executive_summary_data(forecastDataDict)
                    summary3 = NarrativesUtils.get_template_output(self._base_dir,\
                                                                    'trend_narrative_card3.temp',forecastDataDict)
                    self.narratives["card3"]["paragraphs"] = NarrativesUtils.paragraph_splitter(summary3)
                    self.narratives["card3"]["chart"] = {"data":prediction_data,"format":"%b-%y"}
                else:
                    self._result_setter.update_executive_summary_data({"trend_present":False})
                    print "Trend Analysis for Measure Failed"
                    print "#"*20+"Trend Analysis Error"+"#"*20
                    print "No date format for the date column %s was detected." %(self._date_column_suggested)
                    print "#"*60
            else:
                self._result_setter.update_executive_summary_data({"trend_present":False})
                print "Trend Analysis for Measure Failed"
                print "#"*20+"Trend Analysis Error"+"#"*20
                print "No date column present for Trend Analysis."
                print "#"*60

        elif self._analysistype == "Dimension":
            self.narratives = {
                               "card0":{},
                               "card1":{}
                               }
            if self._date_suggestion_columns != None:
                if self._dateFormatDetected:
                    result_column_levels = [x[0] for x in self._data_frame.select(self._result_column).distinct().collect()]
                    level_count_df = self._data_frame.groupBy(self._result_column).count().orderBy("count",ascending=False)
                    level_count_df_rows =  level_count_df.collect()
                    top2levels = [level_count_df_rows[0][0],level_count_df_rows[1][0]]
                    all_paragraphs = []
                    chart_data = {}
                    for idx,level in  enumerate(top2levels):
                        leveldf = self._data_frame.filter(col(self._result_column) == level)
                        if self._dataLevel == "day":
                            grouped_data = leveldf.groupBy("suggestedDate").agg({ self._result_column : 'count'})
                            grouped_data = grouped_data.withColumnRenamed(grouped_data.columns[-1],"value")
                            grouped_data = grouped_data.withColumn("year_month",udf(lambda x:x.strftime("%b-%y"))("suggestedDate"))
                            grouped_data = grouped_data.orderBy("suggestedDate",ascending=True)
                            grouped_data = grouped_data.withColumnRenamed(grouped_data.columns[0],"key")
                            grouped_data = grouped_data.toPandas()
                        elif self._dataLevel == "month":
                            grouped_data = leveldf.groupBy("year_month").agg({ self._result_column : 'count'})
                            grouped_data = grouped_data.withColumnRenamed(grouped_data.columns[-1],"value")
                            grouped_data = grouped_data.withColumn("suggestedDate",udf(lambda x:datetime.strptime(x,"%b-%y"))("year_month"))
                            grouped_data = grouped_data.orderBy("suggestedDate",ascending=True)
                            grouped_data = grouped_data.withColumnRenamed("suggestedDate","key")
                            grouped_data = grouped_data.select(["key","value","year_month"]).toPandas()
                            grouped_data["key"] = grouped_data["year_month"].apply(lambda x: datetime.strptime(x,"%b-%y").date())

                        pandasDf = leveldf.toPandas()
                        pandasDf.drop(self._date_column_suggested,axis=1,inplace=True)
                        pandasDf.rename(columns={'year_month': self._date_column_suggested}, inplace=True)
                        pandasDf["value_col"] = [1]*pandasDf.shape[0]


                        trend_narrative_obj = TrendNarrative(self._result_column,self._date_column_suggested,grouped_data,self._existingDateFormat,self._requestedDateFormat)
                        dataDict = trend_narrative_obj.generateDataDict(grouped_data,self._dataLevel,self._durationString)
                        dataDict["measure"] = level
                        dataDict["duration"] = self._duration
                        dataDict["dataLevel"] = self._dataLevel
                        dataDict["durationString"] = self._durationString
                        # grouped_data.to_csv("/home/gulshan/marlabs/datasets/grouped_data"+str(idx))
                        # print json.dumps(dataDict,indent=2)
                        significant_dimensions = df_helper.get_chisquare_significant_dimension()
                        reference_time = dataDict["reference_time"]
                        if len(significant_dimensions.keys()) > 0:
                            xtraData = trend_narrative_obj.get_xtra_calculations(pandasDf,grouped_data,significant_dimensions.keys(),self._date_column_suggested,"value_col",self._existingDateFormat,reference_time,self._dataLevel)
                            if xtraData != None:
                                print xtraData
                                dataDict.update(xtraData)

                        # print 'Trend dataDict:  %s' %(json.dumps(dataDict, indent=2))

                        dataDict.update({"level_index":idx})
                        self._result_setter.update_executive_summary_data(dataDict)
                        summary1 = NarrativesUtils.get_template_output(self._base_dir,\
                                                                        'dimension_trend.temp',dataDict)


                        all_paragraphs += NarrativesUtils.paragraph_splitter(summary1)

                        trend_chart_data = grouped_data[["key","value"]].T.to_dict().values()
                        trend_chart_data = sorted(trend_chart_data,key=lambda x:x["key"])
                        card1chartdata = trend_chart_data
                        if self._dataLevel == "day":
                                card1chartdata = [{"key":str(val["key"]),"value":val["value"]} for val in card1chartdata]
                        elif self._dataLevel == "month":
                            card1chartdata = [{"key":val["key"].strftime("%b-%y"),"value":val["value"]} for val in card1chartdata]
                        chart_data[level] = card1chartdata
                        # self.narratives["card0"]["chart"] = {"data":card1chartdata,"format":"%b-%y"}
                    self.narratives["card0"]["paragraphs"] = all_paragraphs
                    labels = {"y":chart_data.keys()[0],"y2":chart_data.keys()[1]}
                    self.narratives["card0"]["chart"] = {"data":chart_data,"format":"%b-%y",
                                                        "label":labels,
                                                        "label_text":{"x":"Time Duration","y":"Count of "+labels["y"],"y2":"Count of "+labels["y2"]}}
                    # print json.dumps(self.narratives,indent=2)
                else:
                    self._result_setter.update_executive_summary_data({"trend_present":False})
                    print "Trend Analysis for Measure Failed"
                    print "#"*20+"Trend Analysis Error"+"#"*20
                    print "No date format for the date column %s was detected." %(self._date_column_suggested)
                    print "#"*60
            else:
                self._result_setter.update_executive_summary_data({"trend_present":False})
                print "Trend Analysis for Measure Failed"
                print "#"*20+"Trend Analysis Error"+"#"*20
                print "No date column present for Trend Analysis."
                print "#"*60


__all__ = [
    'TrendNarrative',
    'TimeSeriesCalculations'
]
