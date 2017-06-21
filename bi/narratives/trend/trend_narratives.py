import os

import numpy as np
from datetime import datetime

from bi.algorithms import TimeSeriesAnalysis
# from nltk import tokenize
from bi.narratives import utils as NarrativesUtils


class TrendNarrative:

    def __init__(self, measure_column, time_dimension_column, grouped_data, existingDateFormat,requestedDateFormat):
        self._measure_column = measure_column
        self._td_column = time_dimension_column
        self._grouped_data = grouped_data
        self._requestedDateFormat = requestedDateFormat

        self._heading = 'Trend Analysis'
        self._sub_heading = 'Analysis by Measure'
        self.output_column_sample = None
        self.summary = None
        self.key_takeaway = None
        self.narratives = {}
        # self._base_dir = os.path.dirname(os.path.realpath(__file__))+"/../../templates/trend/"
        self._base_dir = os.environ.get('MADVISOR_BI_HOME')+"/templates/trend/"

        self.month_dict = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}


    def formatDateColumn(self,df,requestedDateFormat):
        df_copy = df
        date_series = df_copy["key"]
        date_series = date_series.apply(lambda x: datetime.strptime(x ,requestedDateFormat).date())
        df_copy["key"] = date_series
        return df_copy

    def generateDataDict(self,df):
        dataDict = {}
        # df["perChange"] = [round((y-x)*100/float(x),2) for x,y in zip(df["value"],df["value"].iloc[1:])]+[round((df["value"].iloc[-1]-df["value"].iloc[-2])*100/float(df["value"].iloc[-2]),2)]
        df["perChange"] = [0]+[round((x-y)*100/float(y),2) for x,y in zip(df["value"].iloc[1:],df["value"])]
        dataDict["measure"] = self._measure_column
        df["year_month"] = df["key"].apply(lambda x: self.month_dict[int(x.strftime('%m'))]+"-"+str(x.strftime('%Y')))
        df["trendDirection"] = df["perChange"].apply(lambda x: "P" if x>=0 else "N")
        trendString = "".join(df["trendDirection"])
        maxRuns = NarrativesUtils.longestRun(trendString)

        dataDict["dateRange"] = (df["key"].iloc[-1]-df["key"].iloc[0]).days
        dataDict["dateLevel"] = "month"
        if dataDict["dateRange"] <= 180:
            dataDict["duration"] = dataDict["dateRange"]
            dataDict["dataLevel"] = "day"
            dataDict["durationString"] = str(dataDict["duration"])+" days"

        elif dataDict["dateRange"] > 180 and dataDict["dateRange"] <= 1095:
            dataDict["duration"] = len(list(set(df["year_month"])))
            dataDict["dataLevel"] = "month"
            dataDict["durationString"] = str(dataDict["duration"])+" months"
        else:
            dataDict["dataLevel"] = "month"
            yr = str(dataDict["dateRange"]//365)
            mon = str((dataDict["dateRange"]%365)//12)
            dataDict["durationString"] = yr+" years and "+mon+" months"

        # list(set(zip([x.strftime('%m') for x in df["key"]],[x.strftime('%Y') for x in df["key"]])))
        dataDict["bubbleData"] = [{"value":"","text":""},{"value":"","text":""}]
        dataDict["overall_growth"] = round((df["value"].iloc[-1]-df["value"].iloc[0])*100/float(df["value"].iloc[0]),2)
        dataDict["bubbleData"][0]["value"] = str(dataDict["overall_growth"])+"%"
        dataDict["bubbleData"][0]["text"] = "Overall growth in %s over the last %s"%(self._measure_column ,dataDict["durationString"])
        max_growth_index = np.argmax(df["perChange"])
        dataDict["bubbleData"][1]["value"] = str(round(list(df["perChange"])[max_growth_index],2))+"%"
        dataDict["bubbleData"][1]["text"] = "Largest growth in %s happened in %s"%(self._measure_column ,list(df["key"])[max_growth_index])
        dataDict["start_value"] = round(df["value"].iloc[0],2)
        dataDict["end_value"] = round(df["value"].iloc[-1],2)
        dataDict["average_value"] = round(df["value"].mean(),2)
        dataDict["total"] = round(df["value"].sum(),2)
        if dataDict["dataLevel"] == "day":
            dataDict["start_time"] = str(df["key"].iloc[0])
            dataDict["end_time"] = str(df["key"].iloc[-1])
        else:
            dataDict["start_time"] = df["year_month"].iloc[0]
            dataDict["end_time"] = df["year_month"].iloc[-1]

        if dataDict["overall_growth"] < 0:
            dataDict["overall_growth_text"] = "negative growth"
        else:
            dataDict["overall_growth_text"] = "positive growth"
        peak_index = np.argmax(df["value"])
        low_index = np.argmin(df["value"])
        dataDict["peakValue"] = df["value"][peak_index]
        dataDict["lowestValue"] = df["value"][low_index]
        dataDict["peakTime"] = df["year_month"][peak_index]
        dataDict["reference_time"] = dataDict["peakTime"]
        dataDict["lowestTime"] = df["year_month"][low_index]

        k = peak_index
        while k != -1 and df["perChange"][k] >= 0:
            k = k-1
        l = low_index
        while l != -1 and df["perChange"][l] < 0:
            l = l-1
        if peak_index - k > 0:
            dataDict["peakStreakDuration"] = peak_index - k
        else:
            dataDict["peakStreakDuration"] = 0
        if low_index - l > 0:
            dataDict["lowStreakDuration"] = low_index - l
        else:
            dataDict["lowStreakDuration"] = 0
        if dataDict["lowStreakDuration"] >=2 :
            dataDict["lowStreakBeginMonth"] = df["year_month"][l]
            dataDict["lowStreakBeginValue"] = df["value"][l]

        table_data = {"increase":[],"decrease":[]}

        percent_stats = NarrativesUtils.get_max_min_stats(df,dataDict["dataLevel"],trend = "positive", stat_type = "percentage")
        abs_stats = NarrativesUtils.get_max_min_stats(df,dataDict["dataLevel"],trend = "positive", stat_type = "absolute")
        streak = NarrativesUtils.get_streak_data(df,trendString,maxRuns,"positive",dataDict["dataLevel"])
        table_data["increase"].append(percent_stats)
        table_data["increase"].append(abs_stats)
        table_data["increase"].append(streak)

        percent_stats = NarrativesUtils.get_max_min_stats(df,dataDict["dataLevel"],trend = "negative", stat_type = "percentage")
        abs_stats = NarrativesUtils.get_max_min_stats(df,dataDict["dataLevel"],trend = "negative", stat_type = "absolute")
        streak = NarrativesUtils.get_streak_data(df,trendString,maxRuns,"negative",dataDict["dataLevel"])
        table_data["decrease"].append(percent_stats)
        table_data["decrease"].append(abs_stats)
        table_data["decrease"].append(streak)

        dataDict["table_data"] = table_data
        return dataDict

    def get_xtra_calculations(self,df,significant_columns,index_col,value_col,datetime_pattern,reference_time):
        datetime_pattern = "%b-%Y"
        level_cont = NarrativesUtils.calculate_level_contribution(df,significant_columns,index_col,datetime_pattern,value_col,reference_time)
        level_cont_dict = NarrativesUtils.get_level_cont_dict(level_cont)

        bucket_dict = NarrativesUtils.calculate_bucket_data(level_cont)
        bucket_data = NarrativesUtils.get_bucket_data_dict(bucket_dict,level_cont)
        dim_data = NarrativesUtils.calculate_dimension_contribution(level_cont)
        if level_cont_dict != None:
            if bucket_data != None:
                level_cont_dict.update(bucket_data)
            if dim_data != None:
                level_cont_dict.update(dim_data)
        return level_cont_dict

    def get_forecast_values(self,series,prediction_window):
        if len(series) > 12:
            slen = 12
        else:
            slen = 1
        alpha, beta, gamma = 0.716, 0.029, 0.993
        time_series_object = TimeSeriesAnalysis()
        prediction = time_series_object.triple_exponential_smoothing(series, slen, alpha, beta, gamma, prediction_window)
        return prediction

    def generate_sub_heading(self,measure_column):
        sub_heading = "How %s is changing over Time" %(measure_column)
        # sub_heading = "This section provides insights on how %s is performing over time and captures the most significant moments that defined the overall pattern or trend over the observation period." %(measure_column)
        return sub_heading

    def generate_summary(self,dataDict):
        output = NarrativesUtils.get_template_output(self._base_dir,\
                                                        'trend_summary.temp',data_dict)
        return output
