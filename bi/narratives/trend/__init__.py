import os
import json
from bi.common.utils import accepts
from trend_narratives import TrendNarrative
from datetime import datetime
from bi.narratives import utils as NarrativesUtils



class TimeSeriesNarrative:
    def __init__(self, df_helper, measure_column, time_dimension_column, existingDateFormat, requestedDateFormat):
        # self._base_dir = os.path.dirname(os.path.realpath(__file__))+"/../../templates/trend/"
        self._base_dir = os.environ.get('MADVISOR_BI_HOME')+"/templates/trend/"

        self.narratives = {}
        #grouped_data needs to be sorted by date
        grouped_data = df_helper.get_aggregate_data(time_dimension_column,measure_column,
                                                        existingDateFormat=existingDateFormat,
                                                        requestedDateFormat=requestedDateFormat)
        trend_narrative_obj = TrendNarrative(measure_column,time_dimension_column,grouped_data,existingDateFormat,requestedDateFormat)
        grouped_data = trend_narrative_obj.formatDateColumn(grouped_data,requestedDateFormat)
        grouped_data = grouped_data.sort_values(by='key', ascending=True)
        grouped_data["value"] = grouped_data["value"].apply(lambda x: round(x,2))
        # dataDict = trend_narrative_obj.generateDataDict(grouped_data)
        # print 'Trend dataDict:  %s' %(json.dumps(dataDict, indent=2))

        # self.narratives["heading"] = measure_column+" Performance Report"
        # self.narratives["summary"] = trend_narrative_obj.generate_summary(dataDict).split("#LINESEPARATOR#")
        # self.narratives["sub_heading"] = trend_narrative_obj.generate_sub_heading(measure_column)

        self.narratives["SectionHeading"] = measure_column+" Performance Report"
        summary = NarrativesUtils.get_template_output(self._base_dir,\
                                                        'trend_narrative_dummy.temp',{})
        output = []
        paragraphs = summary.split("PARASEPARATOR")
        for val in paragraphs:
            temp = {"header":"","content":[""]}
            if "PARAHEADER" in val:
                parts = val.split("PARAHEADER")
                temp["header"] = parts[0]
                if "LINESEPARATOR" in parts[1]:
                    lines = parts[1].split("LINESEPARATOR")
                    temp["content"] = lines
                    if "BULLETSEPARATOR" in lines[1]:
                        temp["content"][1] = lines[1].split("BULLETSEPARATOR")
                else:
                    temp["content"] = [parts[1]]
            else:
                temp["content"] = [val]
            output.append(temp)

        self.narratives["summary"] = output



        month_dict = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
        grouped_data["key1"] = grouped_data["key"].apply(lambda x: month_dict[x.month]+"-"+str(x.year))
        grouped_data["key"] = grouped_data["key"].apply(lambda x: str(x))
        self.trend_data = grouped_data[["key","key1","value"]].T.to_dict().values()
        # print existingDateFormat,requestedDateFormat
        self.trend_data = sorted(self.trend_data,key=lambda x :datetime.strptime(x['key'],"%Y-%m-%d"))




__all__ = [
    'TrendNarrative'
]
