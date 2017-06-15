import os
import jinja2
import re
import json
import pandas as pd
import numpy as np
from datetime import datetime

#from nltk import tokenize
from bi.common.utils import accepts
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

        # dataDict["dateLevel"] = "day"
        # if df.shape[0] <= 365:
        #     dataDict["duration"] = df.shape[0]
        #     dataDict["dataLevel"] = "day"
        #     dataDict["durationString"] = str(dataDict["duration"])+" days"
        #
        # elif df.shape[0] > 365 and df.shape[0] <= 1095:
        #     dataDict["duration"] = len(list(set(df["year_month"])))
        #     dataDict["dataLevel"] = "month"
        #     dataDict["durationString"] = str(dataDict["duration"])+" months"
        # else:
        #     dataDict["dataLevel"] = "month"
        #     yr = str(df.shape[0]//365)
        #     mon = str((df.shape[0]%365)//12)
        #     dataDict["durationString"] = yr+" years and "+mon+"months"

        dataDict["dateRange"] = (df["key"].iloc[-1]-df["key"].iloc[0]).days
        dataDict["dateLevel"] = "day"
        if dataDict["dateRange"] <= 365:
            dataDict["duration"] = dataDict["dateRange"]
            dataDict["dataLevel"] = "day"
            dataDict["durationString"] = str(dataDict["duration"])+" days"

        elif dataDict["dateRange"] > 365 and dataDict["dateRange"] <= 1095:
            dataDict["duration"] = len(list(set(df["year_month"])))
            dataDict["dataLevel"] = "month"
            dataDict["durationString"] = str(dataDict["duration"])+" months"
        else:
            dataDict["dataLevel"] = "month"
            yr = str(dataDict["dateRange"]//365)
            mon = str((dataDict["dateRange"]%365)//12)
            dataDict["durationString"] = yr+" years and "+mon+" months"

        df["year_month"] = df["key"].apply(lambda x: self.month_dict[int(x.strftime('%m'))]+"-"+str(x.strftime('%Y')))
        # list(set(zip([x.strftime('%m') for x in df["key"]],[x.strftime('%Y') for x in df["key"]])))


        dataDict["overall_growth"] = round((df["value"].iloc[-1]-df["value"].iloc[0])*100/float(df["value"].iloc[0]),2)
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
        dataDict["lowestTime"] = df["year_month"][low_index]
        k = peak_index
        while df["perChange"][k] >= 0:
            k = k-1
        l = low_index
        while df["perChange"][l] < 0:
            l = l-1
        dataDict["peakStreakDuration"] = k-peak_index
        dataDict["LowStreakDuration"] = l-low_index
        if dataDict["LowStreakDuration"] >=2 :
            dataDict["lowStreakBeginMonth"] = df["year_month"][l]
            dataDict["lowStreakBeginValue"] = df["value"][l]

        max_increase_index = np.argmax(list(df["perChange"]))
        if dataDict["dataLevel"] == "day":
            dataDict["max_increase_time"] = str(df["key"][max_increase_index])
        else:
            dataDict["max_increase_time"] = df["year_month"][max_increase_index]

        dataDict["max_increase_percentage"] = round(df["perChange"][max_increase_index],2)
        dataDict["maxIncreaseValues"] = (df["value"][max_increase_index-1],df["value"][max_increase_index])
        max_decrease_index = np.argmin(list(df["perChange"]))
        if dataDict["dataLevel"] == "day":
            dataDict["max_decrease_time"] = str(df["key"][max_decrease_index])
        else:
            dataDict["max_decrease_time"] = df["year_month"][max_decrease_index]

        dataDict["max_decrease_percentage"] = round(df["perChange"][max_decrease_index],2)
        dataDict["maxDecreaseValues"] = (df["value"][max_decrease_index-1],df["value"][max_decrease_index])

        if dataDict["overall_growth"] > 0:
            dataDict["trend"] = "positive"
            streakList =  NarrativesUtils.continuous_streak(df,direction="increase")
            streak = max(streakList,key=len)
            dataDict["end_streak_value"] = round(streak[-1]["value"],2)
            dataDict["start_streak_value"] = round(streak[0]["value"],2)
            if dataDict["dataLevel"] == "day":
                dataDict["streak_end_month"] = str(streak[-1]["key"])
                dataDict["streak_start_month"] = str(streak[0]["key"])
            else:
                dataDict["streak_end_month"] = streak[-1]["year_month"]
                dataDict["streak_start_month"] = streak[0]["year_month"]

        elif dataDict["overall_growth"] < 0:
            dataDict["trend"] = "negative"
            streakList =  NarrativesUtils.continuous_streak(df,direction="decrease")
            streak = max(streakList,key=len)
            dataDict["end_streak_value"] = round(streak[-1]["value"],2)
            dataDict["start_streak_value"] = round(streak[0]["value"],2)
            if dataDict["dataLevel"] == "day":
                dataDict["streak_end_month"] = str(streak[-1]["key"])
                dataDict["streak_start_month"] = str(streak[0]["key"])
            else:
                dataDict["streak_end_month"] = streak[-1]["year_month"]
                dataDict["streak_start_month"] = streak[0]["year_month"]

        return dataDict

    def generate_sub_heading(self,measure_column):
        sub_heading = "How %s is changing over Time" %(measure_column)
        # sub_heading = "This section provides insights on how %s is performing over time and captures the most significant moments that defined the overall pattern or trend over the observation period." %(measure_column)
        return sub_heading

    def generate_summary(self,dataDict):
        output = NarrativesUtils.get_template_output(self._base_dir,\
                                                        'trend_summary.temp',data_dict)
        return output
