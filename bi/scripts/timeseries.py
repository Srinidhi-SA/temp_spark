from bi.common import utils
from bi.common import DataWriter
from bi.narratives.trend import TimeSeriesNarrative


import json

class TrendScript:

    def __init__(self, df_helper, df_context, spark):
        self._dataframe_helper = df_helper
        self._spark = spark
        self._dataframe_context = df_context
        self._dateFormatDetected = False
        self._date_suggestion_cols = df_context.get_date_column_suggestions()
        self._time_dimension_columns = df_helper.get_timestamp_columns()
        self._dateFormatConversionDict = {
            "mm/dd/YYYY":"%m/%d/%Y",
            "dd/mm/YYYY":"%d/%m/%Y",
            "YYYY/mm/dd":"%Y/%m/%d",
            "dd <month> YYYY":"%d %b,%Y",
            "%b-%y":"%b-%y"
        }
        if self._date_suggestion_cols != None:
            self._td_col = self._date_suggestion_cols[0]
            self._measure_col = df_context.get_result_column()
            self._existingDateFormat = None
            dateColumnFormatDict =  df_helper.get_datetime_format(self._td_col)
            if self._td_col in dateColumnFormatDict.keys():
                self._existingDateFormat = dateColumnFormatDict[self._td_col]
                self._dateFormatDetected = True

            if df_context.get_requested_date_format() != None:
                self._requestedDateFormat = df_context.get_requested_date_format()[0]
            else:
                self._requestedDateFormat = None
            if self._requestedDateFormat != None:
                self._requestedDateFormat = self._dateFormatConversionDict[self._requestedDateFormat]
            else:
                self._requestedDateFormat = self._existingDateFormat

    def Run(self):
        if self._date_suggestion_cols != None:
            if self._dateFormatDetected:
                trend_narratives_obj = TimeSeriesNarrative(self._dataframe_helper, self._measure_col, self._td_col, self._existingDateFormat, self._requestedDateFormat)
                trend_narratives = utils.as_dict(trend_narratives_obj)
                # print json.dumps(trend_narratives, indent=2)
                DataWriter.write_dict_as_json(self._spark, {"TREND":json.dumps(trend_narratives)}, self._dataframe_context.get_narratives_file()+'Trend/')
            else:
                print "Trend Analysis Failed"
                print "#"*20+"Trend Analysis Error"+"#"*20
                print "No date format for the date column %s was detected." %(self._td_col)
                print "#"*60
        else:
            if self._time_dimension_columns != None:
                print self._time_dimension_columns
            else:
                print "Trend Analysis Failed"
                print "#"*20+"Trend Analysis Error"+"#"*20
                print "No date column present for Trend Analysis."
                print "#"*60
