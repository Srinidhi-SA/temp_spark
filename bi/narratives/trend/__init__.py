import os
import json
from bi.common.utils import accepts
from trend_narratives import TrendNarrative
from datetime import datetime


class TimeSeriesNarrative:
    def __init__(self, df_helper, measure_column, time_dimension_column, existingDateFormat, requestedDateFormat):

        self.narratives = {}
        #grouped_data needs to be sorted by date
        grouped_data = df_helper.get_aggregate_data(time_dimension_column,measure_column,
                                                        existingDateFormat=existingDateFormat,
                                                        requestedDateFormat=requestedDateFormat)
        trend_narrative_obj = TrendNarrative(measure_column,time_dimension_column,grouped_data,existingDateFormat,requestedDateFormat)
        grouped_data = trend_narrative_obj.formatDateColumn(grouped_data,requestedDateFormat)
        grouped_data = grouped_data.sort_values(by='key', ascending=True)
        grouped_data["value"] = grouped_data["value"].apply(lambda x: round(x,2))
        dataDict = trend_narrative_obj.generateDataDict(grouped_data)
        # print 'Trend dataDict:  %s' %(json.dumps(dataDict, indent=2))

        self.narratives["heading"] = "Trend Analysis"
        self.narratives["summary"] = trend_narrative_obj.generate_summary(dataDict).split("#LINESEPARATOR#")
        self.narratives["sub_heading"] = trend_narrative_obj.generate_sub_heading(measure_column)

        month_dict = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
        grouped_data["key1"] = grouped_data["key"].apply(lambda x: month_dict[x.month]+"-"+str(x.year))
        grouped_data["key"] = grouped_data["key"].apply(lambda x: str(x))
        self.trend_data = grouped_data[["key","key1","value"]].T.to_dict().values()
        # print existingDateFormat,requestedDateFormat
        self.trend_data = sorted(self.trend_data,key=lambda x :datetime.strptime(x['key'],"%Y-%m-%d"))



__all__ = [
    'TrendNarrative'
]
