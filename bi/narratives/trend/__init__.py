import json
import os
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

from bi.narratives import utils as NarrativesUtils
from bi.common import utils as CommonUtils
from bi.common import NarrativesTree,NormalCard,SummaryCard,HtmlData,C3ChartData
from bi.common import ScatterChartData,NormalChartData,ChartJson



from trend_narratives import TrendNarrative

from pyspark.sql.functions import col, udf, max
from pyspark.sql.types import *
from pyspark.sql.functions import monotonically_increasing_id




class TimeSeriesNarrative:
    def __init__(self, df_helper, df_context, result_setter, spark, story_narrative):
        self._story_narrative = story_narrative
        self._result_setter = result_setter
        self._dataframe_helper = df_helper
        self._data_frame = df_helper.get_data_frame()
        self._spark = spark
        self._dataframe_context = df_context

        self._analysisName = "trend"
        self._messageURL = self._dataframe_context.get_message_url()
        self._dateFormatDetected = False
        self._requestedDateFormat = None
        self._existingDateFormat = None
        self._selected_date_columns = df_context.get_date_columns()
        # self._selected_date_columns = None
        self._dateFormatConversionDict = NarrativesUtils.date_formats_mapping_dict()
        self._td_columns = df_helper.get_timestamp_columns()
        self._string_columns = df_helper.get_string_columns()
        self._result_column = df_context.get_result_column()
        self._analysistype = self._dataframe_context.get_analysis_type()
        self._trendSettings = self._dataframe_context.get_trend_settings()
        self._trendSpecificMeasure = False
        if self._trendSettings != None:
            if self._analysistype == "dimension" and self._trendSettings["name"] != "Count":
                self._trendSpecificMeasure = True
                self._analysistype = "measure"
                self._result_column = self._trendSettings["selectedMeasure"]
            elif self._analysistype == "measure" and self._trendSettings["name"] != "Count":
                self._result_column = self._trendSettings["selectedMeasure"]

        self._trend_subsection = self._result_setter.get_trend_section_name()
        self._regression_trend_card = None
        self._num_significant_digits = NarrativesUtils.get_significant_digit_settings("trend")
        self._blockSplitter = "|~NEWBLOCK~|"
        self._trend_on_td_column = False
        self._number_of_dimensions_to_consider = 10

        self._completionStatus = self._dataframe_context.get_completion_status()
        self._analysisName = self._dataframe_context.get_analysis_name()
        self._messageURL = self._dataframe_context.get_message_url()
        if self._analysistype == "dimension":
            self._scriptWeightDict = self._dataframe_context.get_dimension_analysis_weight()
            self._scriptStages = {
                "initialization":{
                    "summary":"Initialized the Frequency Narratives",
                    "weight":0
                    },
                "summarygeneration":{
                    "summary":"summary generation finished",
                    "weight":10
                    },
                "completion":{
                    "summary":"Frequency Stats Narratives done",
                    "weight":0
                    },
                }
        elif self._analysistype == "measure":
            if self._trendSpecificMeasure:
                self._scriptWeightDict = self._dataframe_context.get_dimension_analysis_weight()
            else:
                self._scriptWeightDict = self._dataframe_context.get_measure_analysis_weight()
            self._scriptStages = {
                "trendNarrativeStart":{
                    "summary":"Started the Descriptive Stats Narratives",
                    "weight":1
                    },
                "trendNarrativeEnd":{
                    "summary":"Narratives for descriptive Stats Finished",
                    "weight":0
                    },
                }

        if self._selected_date_columns != None and len(self._selected_date_columns) > 0:
            suggested_date_column = self._selected_date_columns[0]
            existingDateFormat = None
            if suggested_date_column not in self._td_columns:
                dateColumnFormatDict =  df_context.get_datetime_suggestions()[0]
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
            else:
                self._trend_on_td_column = True
                existingDateFormat = "%Y-%m-%d"
                self._dateFormatDetected = True
                if df_context.get_requested_date_format() != None:
                    requestedDateFormat = df_context.get_requested_date_format()[0]
                else:
                    requestedDateFormat = None
                if requestedDateFormat != None:
                    requestedDateFormat = self._dateFormatConversionDict[requestedDateFormat]
                else:
                    requestedDateFormat = existingDateFormat
        else:
            if self._td_columns != None:
                if len(self._td_columns) > 0:
                    self._trend_on_td_column = True
                    suggested_date_column = self._td_columns[0]
                    existingDateFormat = "%Y-%m-%d"
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
            if self._selected_date_columns != None and self._trend_on_td_column == False:
                date_format = self._existingDateFormat
                string_to_date = udf(lambda x: datetime.strptime(x,date_format), DateType())
                date_to_month_year = udf(lambda x: datetime.strptime(x,date_format).strftime("%b-%y"), StringType())
                self._data_frame = self._data_frame.withColumn("suggestedDate", string_to_date(self._date_column_suggested))
                self._data_frame = self._data_frame.withColumn("year_month", date_to_month_year(self._date_column_suggested))
                self._data_frame = self._data_frame.orderBy(["suggestedDate"],ascending=[True])
                self._data_frame = self._data_frame.withColumn("_id_", monotonically_increasing_id())
            else:
                self._data_frame = self._data_frame.withColumn("suggestedDate", udf(lambda x:x.date(),DateType())(self._date_column_suggested))
                self._data_frame = self._data_frame.withColumn("year_month", udf(lambda x:x.date().strftime("%b-%y"),StringType())(self._date_column_suggested))
                self._data_frame = self._data_frame.orderBy(["suggestedDate"],ascending=[True])
                self._data_frame = self._data_frame.withColumn("_id_", monotonically_increasing_id())
            id_max = self._data_frame.select(max("_id_")).first()[0]
            first_date = self._data_frame.select("suggestedDate").first()[0]
            #####  This is a Temporary fix
            try:
                print "TRY BLOCK STARTED"
                last_date = self._data_frame.where(col("_id_") == id_max).select("suggestedDate").first()[0]
            except:
                print "ENTERING EXCEPT BLOCK"
                pandas_df = self._data_frame.select(["_id_","suggestedDate"]).toPandas()
                pandas_df.sort_values(by="suggestedDate",ascending=True,inplace=True)
                last_date = pandas_df["suggestedDate"].iloc[-1]
            if last_date == None:
                print "IF Last date none:-"
                pandas_df = self._data_frame.toPandas()
                pandas_df.sort_values(by="suggestedDate",ascending=True,inplace=True)
                last_date = pandas_df["suggestedDate"].iloc[-1]

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
                mon = str((self._dataRange%365)//30)
                if mon == "12":
                    yr = str(int(yr)+1)
                    mon = None
                if mon != None:
                    self._durationString = yr+" years and "+mon+" months"
                else:
                    self._durationString = yr+" years"

            if self._td_columns != None:
                if self._selected_date_columns == None:
                    self._selected_date_columns = self._td_columns
                else:
                    self._selected_date_columns += self._td_columns
            print self._durationString
            print self._dataLevel
            print self._existingDateFormat
        if self._trend_subsection=="regression":
            if self._selected_date_columns != None:
                if self._dateFormatDetected:
                    trend_subsection_data = self._result_setter.get_trend_section_data()
                    measure_column = trend_subsection_data["measure_column"]
                    result_column = trend_subsection_data["result_column"]
                    base_dir = trend_subsection_data["base_dir"]

                    card3heading = 'How '+ result_column +' and '+ measure_column + ' changed over time'
                    if self._dataLevel == "day":
                        grouped_data = self._data_frame.groupBy("suggestedDate").agg({measure_column : 'sum', result_column : 'sum'})
                        grouped_data = grouped_data.withColumnRenamed(grouped_data.columns[-1],result_column)
                        grouped_data = grouped_data.withColumnRenamed(grouped_data.columns[-2],measure_column)

                        grouped_data = grouped_data.withColumn("year_month",udf(lambda x:x.strftime("%b-%y"))("suggestedDate"))
                        grouped_data = grouped_data.orderBy("suggestedDate",ascending=True)
                        grouped_data = grouped_data.withColumnRenamed(grouped_data.columns[0],"key")
                        grouped_data = grouped_data.toPandas()
                    elif self._dataLevel == "month":
                        grouped_data = self._data_frame.groupBy("year_month").agg({measure_column : 'sum', result_column : 'sum'})
                        grouped_data = grouped_data.withColumnRenamed(grouped_data.columns[-1],result_column)
                        grouped_data = grouped_data.withColumnRenamed(grouped_data.columns[-2],measure_column)

                        grouped_data = grouped_data.withColumn("suggestedDate",udf(lambda x:datetime.strptime(x,"%b-%y"))("year_month"))
                        grouped_data = grouped_data.orderBy("suggestedDate",ascending=True)
                        grouped_data = grouped_data.withColumnRenamed("suggestedDate","key")
                        grouped_data = grouped_data.select(["key",measure_column,result_column,"year_month"]).toPandas()
                        grouped_data["key"] = grouped_data["year_month"].apply(lambda x: datetime.strptime(x,"%b-%y").date())

                    trend_narrative_obj = TrendNarrative(self._result_column,self._date_column_suggested,grouped_data,self._existingDateFormat,self._requestedDateFormat)

                    card3data = trend_narrative_obj.generate_regression_trend_data(grouped_data,measure_column,result_column,self._dataLevel,self._durationString)

                    card3narrative = NarrativesUtils.get_template_output(base_dir,\
                                                                    'regression_card3.temp',card3data)


                    card3chart =trend_narrative_obj.generate_regression_trend_chart(grouped_data,self._dataLevel)
                    card3paragraphs = NarrativesUtils.paragraph_splitter(card3narrative)
                    card2 = {'charts': card3chart, 'paragraphs': card3paragraphs, 'heading': card3heading}
                    self.set_regression_trend_card_data(card2)
                else:
                    print "NO DATE FORMAT DETECTED"
            else:
                print "NO DATE COLUMNS PRESENT"


        if self._analysistype=="measure":
            self._completionStatus += self._scriptWeightDict[self._analysisName]["total"]*self._scriptStages["trendNarrativeStart"]["weight"]/10
            progressMessage = CommonUtils.create_progress_message_object(self._analysisName,\
                                        "trendNarrativeStart",\
                                        "info",\
                                        self._scriptStages["trendNarrativeStart"]["summary"],\
                                        self._completionStatus,\
                                        self._completionStatus)
            CommonUtils.save_progress_message(self._messageURL,progressMessage)
            self._dataframe_context.update_completion_status(self._completionStatus)
            # self._startMeasureTrend = self._result_setter.get_trend_section_completion_status()
            self._startMeasureTrend = True

            if self._startMeasureTrend == True:
                self.narratives = {"SectionHeading":"",
                                   "card1":{},
                                   "card2":{},
                                   "card3":{}
                                }
                if self._selected_date_columns != None:

                    if self._dateFormatDetected:

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

                        significant_dimensions = []
                        significant_dimension_dict = df_helper.get_significant_dimension()
                        if significant_dimension_dict != {} and significant_dimension_dict != None:
                            significant_dimension_tuple = tuple(significant_dimension_dict.items())
                            significant_dimension_tuple = sorted(significant_dimension_tuple,key=lambda x: x[1],reverse=True)
                            significant_dimensions = [x[0] for x in significant_dimension_tuple[:self._number_of_dimensions_to_consider]]
                        else:
                            significant_dimensions = self._string_columns[:self._number_of_dimensions_to_consider]
                        print "significant_dimensions",significant_dimensions
                        trend_narrative_obj = TrendNarrative(self._result_column,self._date_column_suggested,grouped_data,self._existingDateFormat,self._requestedDateFormat)
                        dataDict = trend_narrative_obj.generateDataDict(grouped_data,self._dataLevel,self._durationString)
                        # # update reference time with max value
                        reference_time = dataDict["reference_time"]
                        dataDict["duration"] = self._duration
                        dataDict["dataLevel"] = self._dataLevel
                        dataDict["durationString"] = self._durationString
                        dataDict["significant_dimensions"] = significant_dimensions
                        if len(significant_dimensions) > 0:
                            xtraData = trend_narrative_obj.get_xtra_calculations(pandasDf,grouped_data,significant_dimensions,self._date_column_suggested,self._result_column,self._existingDateFormat,reference_time,self._dataLevel)
                            if xtraData != None:
                                dataDict.update(xtraData)
                        # print 'Trend dataDict:  %s' %(json.dumps(dataDict, indent=2))
                        self._result_setter.update_executive_summary_data(dataDict)
                        dataDict.update({"blockSplitter":self._blockSplitter})
                        summary1 = NarrativesUtils.get_template_output(self._base_dir,\
                                                                        'trend_narrative_card1.temp',dataDict)
                        summary2 = NarrativesUtils.get_template_output(self._base_dir,\
                                                                        'trend_narrative_card2.temp',dataDict)
                        measureTrendCard = NormalCard()
                        measureTrendcard1Data = NarrativesUtils.block_splitter(summary1,self._blockSplitter)
                        measureTrendcard2Data = NarrativesUtils.block_splitter(summary2,self._blockSplitter)
                        # print measureTrendcard1Data

                        bubbledata = dataDict["bubbleData"]
                        print bubbledata
                        card1BubbleData = "<div class='col-md-6 col-xs-12 xs-p-20'><h2 class='text-center'><span>{}</span><br/><small>{}</small></h2></div><div class='col-md-6 col-xs-12 xs-p-20'><h2 class='text-center'><span>{}</span><br/><small>{}</small></h2></div>".format(bubbledata[0]["value"],bubbledata[0]["text"],bubbledata[1]["value"],bubbledata[1]["text"])
                        # print card1BubbleData

                        trend_chart_data = grouped_data[["key","value"]].T.to_dict().values()
                        trend_chart_data = sorted(trend_chart_data,key=lambda x:x["key"])
                        card1chartdata = {"actual":[],"predicted":[]}

                        if self._dataLevel == "day":
                            card1chartdata["actual"] = [{"key":str(val["key"]),"value":val["value"]} for val in trend_chart_data]
                        elif self._dataLevel == "month":
                            card1chartdata["actual"] = [{"key":val["key"].strftime("%b-%y"),"value":val["value"]} for val in trend_chart_data]

                        if self._duration<365:
                            prediction_window = 3
                        else:
                            prediction_window = 6
                        predicted_values = trend_narrative_obj.get_forecast_values(grouped_data["value"],prediction_window)[len(grouped_data["value"]):]
                        predicted_values = [round(x,self._num_significant_digits) for x in predicted_values]

                        forecasted_data = []
                        forecasted_data.append(card1chartdata["actual"][-1])
                        forecasted_dates = []
                        # forecast_start_time = datetime.strptime(card1chartdata["actual"][-1]["key"],"%b-%y")
                        if self._dataLevel == "month":
                            forecast_start_time = datetime.strptime(card1chartdata["actual"][-1]["key"],"%b-%y")
                        elif self._dataLevel == "day":
                            forecast_start_time = datetime.strptime(card1chartdata["actual"][-1]["key"],"%Y-%m-%d")
                        for val in range(prediction_window):
                            if self._dataLevel == "month":
                                key = forecast_start_time+relativedelta(months=1+val)
                                forecasted_dates.append(key)
                            elif self._dataLevel == "day":
                                key = forecast_start_time+relativedelta(days=1+val)
                                forecasted_dates.append(key)
                        forecasted_list = zip(forecasted_dates,predicted_values)
                        if self._dataLevel == "month":
                            forecasted_list = [{"key":val[0].strftime("%b-%y"),"value":val[1]} for val in forecasted_list]
                        elif self._dataLevel == "day":
                            forecasted_list = [{"key":val[0].strftime("%Y-%m-%d"),"value":val[1]} for val in forecasted_list]
                        forecasted_data += forecasted_list
                        card1chartdata["predicted"] = forecasted_data
                        print json.dumps(card1chartdata,indent=2)
                        card1chartdata = ScatterChartData(data=card1chartdata)
                        chartJson = ChartJson()
                        chartJson.set_data(card1chartdata.get_data())
                        # chartJson.set_label_text()
                        chartJson.set_legend({"actual":"Observed","predicted":"Forecast"})
                        chartJson.set_chart_type("scatter_line")
                        chartJson.set_axes({"x":"key","y":"value"})
                        chartJson.set_yaxis_number_format(".2f")
                        measureTrendcard1Data.insert(1,C3ChartData(data=chartJson))
                        measureTrendcard1Data.append(HtmlData(data=card1BubbleData))
                        cardData = measureTrendcard1Data+measureTrendcard2Data
                        measureTrendCard.set_card_data(cardData)
                        measureTrendCard.set_card_name("Trend Analysis")
                        trendStoryNode = NarrativesTree("Trend",None,[],[measureTrendCard])
                        self._story_narrative.add_a_node(trendStoryNode)
                        self._result_setter.set_trend_node(trendStoryNode)

                        # prediction_data = [{"key":x["key"],"value":x["value"]} for x in trend_chart_data]
                        # last_val = prediction_data[-1]
                        # last_val.update({"predicted_value":last_val["value"]})
                        # prediction_data[-1] = last_val
                        #
                        # for val in range(prediction_window):
                        #     dataLevel = dataDict["dataLevel"]
                        #     if self._dataLevel == "month":
                        #         last_key = prediction_data[-1]["key"]
                        #         key = last_key+relativedelta(months=1)
                        #         prediction_data.append({"key":key,"predicted_value":predicted_values[val]})
                        #         forecasted_data.append({"key":key,"value":predicted_values[val]})
                        #     elif self._dataLevel == "day":
                        #         last_key = prediction_data[-1]["key"]
                        #         key = last_key+relativedelta(days=1)
                        #         prediction_data.append({"key":key,"predicted_value":predicted_values[val]})
                        # prediction_data_copy = prediction_data
                        # prediction_data = []
                        # for val in prediction_data_copy:
                        #     val["key"] = val["key"].strftime("%b-%y")
                        #     prediction_data.append(val)

                        # forecastDataDict = {"startForecast":predicted_values[0],
                        #                     "endForecast":predicted_values[prediction_window-1],
                        #                     "measure":dataDict["measure"],
                        #                     "forecast":True,
                        #                     "forecast_percentage": round((predicted_values[prediction_window-1]-predicted_values[0])/predicted_values[0],self._num_significant_digits),
                        #                     "prediction_window_text": str(prediction_window) + " months"
                        #                     }
                        #
                        # self._result_setter.update_executive_summary_data(forecastDataDict)
                        # summary3 = NarrativesUtils.get_template_output(self._base_dir,\
                                                                        # 'trend_narrative_card3.temp',forecastDataDict)
                        self._completionStatus += self._scriptWeightDict[self._analysisName]["total"]*self._scriptStages["trendNarrativeEnd"]["weight"]/10
                        progressMessage = CommonUtils.create_progress_message_object(self._analysisName,\
                                                    "trendNarrativeEnd",\
                                                    "info",\
                                                    self._scriptStages["trendNarrativeEnd"]["summary"],\
                                                    self._completionStatus,\
                                                    self._completionStatus)
                        CommonUtils.save_progress_message(self._messageURL,progressMessage)
                        self._dataframe_context.update_completion_status(self._completionStatus)
                    else:
                        # self._result_setter.update_executive_summary_data({"trend_present":False})
                        print "Trend Analysis for Measure Failed"
                        print "#"*20+"Trend Analysis Error"+"#"*20
                        print "No date format for the date column %s was detected." %(self._date_column_suggested)
                        print "#"*60
                        self._completionStatus += self._scriptWeightDict[self._analysisName]["total"]
                        self._dataframe_context.update_completion_status(completionStatus)
                        progressMessage = CommonUtils.create_progress_message_object("Trend","failedState","error",\
                                        "Trend failed as "+"No date format for the date column %s was detected." %(self._date_column_suggested),\
                                        completionStatus,completionStatus)
                        CommonUtils.save_progress_message(messageURL,progressMessage)
                        self._dataframe_context.update_completion_status(self._completionStatus)
                else:
                    # self._result_setter.update_executive_summary_data({"trend_present":False})
                    print "Trend Analysis for Measure Failed"
                    print "#"*20+"Trend Analysis Error"+"#"*20
                    print "No date column present for Trend Analysis."
                    print "#"*60
                    self._completionStatus += self._scriptWeightDict[self._analysisName]["total"]
                    self._dataframe_context.update_completion_status(completionStatus)
                    progressMessage = CommonUtils.create_progress_message_object("Trend","failedState","error",\
                                    "No Date Column Present",\
                                    completionStatus,completionStatus)
                    CommonUtils.save_progress_message(messageURL,progressMessage)
                    self._dataframe_context.update_completion_status(self._completionStatus)
            else:
                print "overall Trend not Started YET"

        elif self._analysistype == "dimension":
            print "Dimension Trend Started"
            self._completionStatus += self._scriptWeightDict[self._analysisName]["total"]*self._scriptStages["initialization"]["weight"]/10
            progressMessage = CommonUtils.create_progress_message_object(self._analysisName,\
                                        "initialization",\
                                        "info",\
                                        self._scriptStages["initialization"]["summary"],\
                                        self._completionStatus,\
                                        self._completionStatus)
            CommonUtils.save_progress_message(self._messageURL,progressMessage)
            self._dataframe_context.update_completion_status(self._completionStatus)



            self.narratives = {
                               "card0":{}
                               }
            if self._selected_date_columns != None:
                if self._dateFormatDetected:
                    result_column_levels = [x[0] for x in self._data_frame.select(self._result_column).distinct().collect()]
                    level_count_df = self._data_frame.groupBy(self._result_column).count().orderBy("count",ascending=False)
                    level_count_df_rows =  level_count_df.collect()
                    top2levels = [level_count_df_rows[0][0],level_count_df_rows[1][0]]
                    cardData = []
                    chart_data = {}
                    cardData1 = []
                    c3_chart = {"dataType":"c3Chart","data":{}}
                    if self._dataLevel == "day":
                        overall_count = self._data_frame.groupBy("suggestedDate").agg({ self._result_column : 'count'})
                        overall_count = overall_count.withColumnRenamed(overall_count.columns[-1],"totalCount")
                        overall_count = overall_count.orderBy("suggestedDate",ascending=True)
                        overall_count = overall_count.withColumnRenamed("suggestedDate","key")
                        overall_count = overall_count.toPandas()
                    elif self._dataLevel == "month":
                        overall_count = self._data_frame.groupBy("year_month").agg({ self._result_column : 'count'})
                        overall_count = overall_count.withColumnRenamed(overall_count.columns[-1],"totalCount")
                        overall_count = overall_count.withColumn("suggestedDate",udf(lambda x:datetime.strptime(x,"%b-%y"))("year_month"))
                        overall_count = overall_count.orderBy("suggestedDate",ascending=True)
                        overall_count = overall_count.withColumnRenamed("suggestedDate","key")
                        overall_count = overall_count.select(["key","totalCount","year_month"]).toPandas()
                        overall_count["key"] = overall_count["year_month"].apply(lambda x: datetime.strptime(x,"%b-%y").date())
                        overall_count = overall_count.loc[:,[c for c in overall_count.columns if c != "year_month"]]

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

                        grouped_data.rename(columns={"value":"value_count"},inplace=True)
                        grouped_data = pd.merge(grouped_data, overall_count, on='key', how='left')
                        # grouped_data["value"] = grouped_data["value_count"].apply(lambda x:round(x*100/float(self._data_frame.count()),self._num_significant_digits))
                        grouped_data["value"] = grouped_data["value_count"]/grouped_data["totalCount"]
                        grouped_data["value"] = grouped_data["value"].apply(lambda x:round(x*100,self._num_significant_digits))
                        pandasDf = leveldf.toPandas()
                        pandasDf.drop(self._date_column_suggested,axis=1,inplace=True)
                        pandasDf.rename(columns={'year_month': self._date_column_suggested}, inplace=True)
                        pandasDf["value_col"] = [1]*pandasDf.shape[0]


                        trend_narrative_obj = TrendNarrative(self._result_column,self._date_column_suggested,grouped_data,self._existingDateFormat,self._requestedDateFormat)
                        dataDict = trend_narrative_obj.generateDataDict(grouped_data,self._dataLevel,self._durationString)
                        dataDict["target_column"] = dataDict["measure"]
                        dataDict["measure"] = level
                        dataDict["duration"] = self._duration
                        dataDict["dataLevel"] = self._dataLevel
                        dataDict["durationString"] = self._durationString
                        # grouped_data.to_csv("/home/gulshan/marlabs/datasets/grouped_data"+str(idx))
                        # print json.dumps(dataDict,indent=2)
                        significant_dimensions = []
                        significant_dimension_dict = df_helper.get_chisquare_significant_dimension()
                        if significant_dimension_dict != {} and significant_dimension_dict != None:
                            significant_dimension_tuple = tuple(significant_dimension_dict.items())
                            significant_dimension_tuple = sorted(significant_dimension_tuple,key=lambda x: x[1],reverse=True)
                            significant_dimensions = [x[0] for x in significant_dimension_tuple[:self._number_of_dimensions_to_consider]]
                        else:
                            significant_dimensions = self._string_columns[:self._number_of_dimensions_to_consider]
                        print "significant_dimensions",significant_dimensions
                        reference_time = dataDict["reference_time"]
                        dataDict["significant_dimensions"] = significant_dimensions
                        if len(significant_dimensions) > 0:
                            xtraData = trend_narrative_obj.get_xtra_calculations(pandasDf,grouped_data,significant_dimensions,self._date_column_suggested,"value_col",self._existingDateFormat,reference_time,self._dataLevel)
                            if xtraData != None:
                                dataDict.update(xtraData)
                        dimensionCount = trend_narrative_obj.generate_dimension_extra_narrative(grouped_data,dataDict,self._dataLevel)
                        if dimensionCount != None:
                            dataDict.update(dimensionCount)

                        dataDict.update({"level_index":idx,"blockSplitter":self._blockSplitter})


                        self._result_setter.update_executive_summary_data(dataDict)
                        trendStory = NarrativesUtils.get_template_output(self._base_dir,\
                                                                        'dimension_trend_new.temp',dataDict)
                        blocks = NarrativesUtils.block_splitter(trendStory,self._blockSplitter)

                        if idx != 0:
                            cardData1 += blocks[2:]
                        else:
                            cardData1 += blocks

                        trend_chart_data = grouped_data[["key","value"]].T.to_dict().values()
                        trend_chart_data = sorted(trend_chart_data,key=lambda x:x["key"])
                        card1chartdata = trend_chart_data
                        if self._dataLevel == "day":
                                card1chartdata = [{"key":str(val["key"]),"value":val["value"]} for val in card1chartdata]
                        elif self._dataLevel == "month":
                            card1chartdata = [{"key":val["key"].strftime("%b-%y"),"value":val["value"]} for val in card1chartdata]
                        chart_data[level] = card1chartdata

                    labels = {"x":"key","y":chart_data.keys()[0],"y2":chart_data.keys()[1]}
                    c3Chart = {
                               "data":chart_data,
                               "format":"%b-%y",
                               "label":labels,
                               "label_text":{
                                             "x":"Time",
                                             "y":"Percentage of "+labels["y"],
                                             "y2":"Percentage of "+labels["y2"]
                                             }
                               }


                    c3_chart["data"] = c3Chart
                    multiLineData = []
                    for idx in range(len(chart_data[top2levels[0]])):
                        key = chart_data[top2levels[0]][idx]["key"]
                        value = chart_data[top2levels[0]][idx]["value"]
                        try:
                            value1 = chart_data[top2levels[1]][idx]["value"]
                        except:
                            value1 = 0
                        multiLineData.append({"key":key,top2levels[0]:value,top2levels[1]:value1})
                    chartData = NormalChartData(multiLineData)
                    chartJson = ChartJson()
                    chartJson.set_data(chartData.get_data())
                    chartJson.set_label_text(c3Chart["label_text"])
                    chartJson.set_legend(c3Chart["label"])
                    chartJson.set_chart_type("line")
                    chartJson.set_yaxis_number_format(".2f")
                    chartJson.set_axes(labels)
                    cardData1.insert(1,C3ChartData(data=chartJson))
                    trendCard = NormalCard(name="Trend Analysis",slug=None,cardData = cardData1)
                    trendStoryNode = NarrativesTree("Trend",None,[],[trendCard])
                    self._story_narrative.add_a_node(trendStoryNode)
                    self._result_setter.set_trend_node(trendStoryNode)
                    self._completionStatus += self._scriptWeightDict[self._analysisName]["total"]*self._scriptStages["summarygeneration"]["weight"]/10
                    progressMessage = CommonUtils.create_progress_message_object(self._analysisName,\
                                                "summarygeneration",\
                                                "info",\
                                                self._scriptStages["summarygeneration"]["summary"],\
                                                self._completionStatus,\
                                                self._completionStatus)
                    CommonUtils.save_progress_message(self._messageURL,progressMessage)
                    self._dataframe_context.update_completion_status(self._completionStatus)

                    self._completionStatus += self._scriptWeightDict[self._analysisName]["total"]*self._scriptStages["completion"]["weight"]/10
                    progressMessage = CommonUtils.create_progress_message_object(self._analysisName,\
                                                "completion",\
                                                "info",\
                                                self._scriptStages["completion"]["summary"],\
                                                self._completionStatus,\
                                                self._completionStatus)
                    CommonUtils.save_progress_message(self._messageURL,progressMessage)
                    self._dataframe_context.update_completion_status(self._completionStatus)
                else:
                    self._result_setter.update_executive_summary_data({"trend_present":False})
                    print "Trend Analysis for Dimension Failed"
                    print "#"*20+"Trend Analysis Error"+"#"*20
                    if self._date_column_suggested:
                        print "No date format for the date column %s was detected." %(self._date_column_suggested)
                    print "#"*60
                    self._completionStatus += self._scriptWeightDict[self._analysisName]["total"]
                    self._dataframe_context.update_completion_status(self._completionStatus)
                    progressMessage = CommonUtils.create_progress_message_object("Trend","failedState","error",\
                                    "Trend failed as "+"No date format for the date column %s was detected." %(self._date_column_suggested),\
                                    self._completionStatus,self._completionStatus)
                    CommonUtils.save_progress_message(messageURL,progressMessage)
                    self._dataframe_context.update_completion_status(self._completionStatus)

            else:
                self._result_setter.update_executive_summary_data({"trend_present":False})
                print "Trend Analysis for Dimension Failed"
                print "#"*20+"Trend Analysis Error"+"#"*20
                print "No date column present for Trend Analysis."
                print "#"*60
                self._completionStatus += self._scriptWeightDict[self._analysisName]["total"]
                self._dataframe_context.update_completion_status(self._completionStatus)
                progressMessage = CommonUtils.create_progress_message_object("Trend","failedState","error",\
                                "No date column present",\
                                self._completionStatus,self._completionStatus)
                CommonUtils.save_progress_message(messageURL,progressMessage)
                self._dataframe_context.update_completion_status(self._completionStatus)

    def set_regression_trend_card_data(self,data):
        self._regression_trend_card = data

    def get_regression_trend_card_data(self):
        return self._regression_trend_card

    def get_story_narrative(self):
        return self._story_narrative

__all__ = [
    'TrendNarrative',
    'TimeSeriesCalculations'
]
