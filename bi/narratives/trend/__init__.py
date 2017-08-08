import json
import os
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

from bi.narratives import utils as NarrativesUtils
from bi.common import NarrativesTree,NormalCard,SummaryCard,HtmlData,C3ChartData

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

        self._dateFormatDetected = False
        self._requestedDateFormat = None
        self._existingDateFormat = None
        self._date_suggestion_columns = df_context.get_date_column_suggestions()
        # self._date_suggestion_columns = None
        self._dateFormatConversionDict = NarrativesUtils.date_formats_mapping_dict()
        self._td_columns = df_helper.get_timestamp_columns()
        self._result_column = df_context.get_result_column()
        self._analysistype = self._dataframe_context.get_analysis_type()
        self._trend_subsection = self._result_setter.get_trend_section_name()
        self._regression_trend_card = None
        self._num_significant_digits = NarrativesUtils.get_significant_digit_settings("trend")
        self._blockSplitter = "|~NEWBLOCK~|"


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
        else:
            if self._td_columns != None:
                if len(self._td_columns) > 0:
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

            if self._date_suggestion_columns != None:
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
                mon = str((self._dataRange%365)//30)
                if mon == "12":
                    yr = str(int(yr)+1)
                    mon = None
                if mon != None:
                    self._durationString = yr+" years and "+mon+" months"
                else:
                    self._durationString = yr+" years"

            print self._duration
            print self._dataLevel
            print self._durationString
            print self._existingDateFormat

            if self._td_columns != None:
                if self._date_suggestion_columns == None:
                    self._date_suggestion_columns = self._td_columns
                else:
                    self._date_suggestion_columns += self._td_columns

        if self._trend_subsection=="regression":
            if self._date_suggestion_columns != None:
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

                    card3chart = {'heading': ''}
                    card3chart['data']=trend_narrative_obj.generate_regression_trend_chart(grouped_data,self._dataLevel)
                    card3paragraphs = NarrativesUtils.paragraph_splitter(card3narrative)
                    card2 = {'charts': card3chart, 'paragraphs': card3paragraphs, 'heading': card3heading}
                    self.set_regression_trend_card_data(card2)
                else:
                    print "NO DATE FORMAT DETECTED"
            else:
                print "NO DATE COLUMNS PRESENT"


        if self._analysistype=="Measure":
            self._startMeasureTrend = self._result_setter.get_trend_section_completion_status()
            if self._startMeasureTrend == True:
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
                        # grouped_data["value"] = grouped_data["value"].apply(lambda x: round(x,self._num_significant_digits))
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
                        self.narratives["card1"]["paragraphs"]=self.narratives["card1"]["paragraphs"]+summary2[:2]
                        # self.narratives["card2"]["paragraphs"] = NarrativesUtils.paragraph_splitter(summary2)
                        # self.narratives["card2"]["table1"] = dataDict["table_data"]["increase"]
                        # self.narratives["card2"]["table2"] = dataDict["table_data"]["decrease"]

                        # grouped_data["key"] = grouped_data["key"].apply(lambda x: month_dict[x.month]+"-"+str(x.year))
                        # trend_chart_data = grouped_data[["key","value"]].groupby("key").agg(sum).reset_index()
                        trend_chart_data = grouped_data[["key","value"]].T.to_dict().values()
                        trend_chart_data = sorted(trend_chart_data,key=lambda x:x["key"])
                        card1chartdata = trend_chart_data
                        card1chartdata = [{"key":val["key"].strftime("%b-%y"),"value":val["value"]} for val in card1chartdata]
                        self.narratives["card1"]["chart"] = {"data":card1chartdata,"format":"%b-%y"}
                        if self._duration<365:
                            prediction_window = 3
                        else:
                            prediction_window = 6
                        predicted_values = trend_narrative_obj.get_forecast_values(grouped_data["value"],prediction_window)[len(grouped_data["value"]):]
                        predicted_values = [round(x,self._num_significant_digits) for x in predicted_values]
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
                                            "forecast_percentage": round((predicted_values[prediction_window-1]-predicted_values[0])/predicted_values[0],self._num_significant_digits),
                                            "prediction_window_text": str(prediction_window) + " months"
                                            }

                        self._result_setter.update_executive_summary_data(forecastDataDict)
                        summary3 = NarrativesUtils.get_template_output(self._base_dir,\
                                                                        'trend_narrative_card3.temp',forecastDataDict)
                        # self.narratives["card3"]["paragraphs"] = NarrativesUtils.paragraph_splitter(summary3)
                        # self.narratives["card3"]["chart"] = {"data":prediction_data,"format":"%b-%y"}
                        print json.dumps(self.narratives,indent=2)

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
            else:
                print "overall Trend not Started YET"

        elif self._analysistype == "Dimension":
            self.narratives = {
                               "card0":{}
                               }
            if self._date_suggestion_columns != None:
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
                        significant_dimensions = df_helper.get_chisquare_significant_dimension()
                        reference_time = dataDict["reference_time"]
                        if len(significant_dimensions.keys()) > 0:
                            xtraData = trend_narrative_obj.get_xtra_calculations(pandasDf,grouped_data,significant_dimensions.keys(),self._date_column_suggested,"value_col",self._existingDateFormat,reference_time,self._dataLevel)
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
                            cardData1 += blocks[1:]
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

                    labels = {"y":chart_data.keys()[0],"y2":chart_data.keys()[1]}
                    c3Chart = {
                               "data":chart_data,
                               "format":"%b-%y",
                               "label":labels,
                               "label_text":{
                                             "x":"Time Duration",
                                             "y":"Percentage of "+labels["y"],
                                             "y2":"Percentage of "+labels["y2"]
                                             }
                               }


                    c3_chart["data"] = c3Chart
                    cardData1.insert(1,c3_chart)
                    trendCard = NormalCard(name="Trend",slug=None,cardData = cardData1)
                    trendStoryNode = NarrativesTree("Trend",None,[],[trendCard])
                    self._story_narrative.add_a_node(trendStoryNode)
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
