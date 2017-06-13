import os
import re
import json
from dateutil.relativedelta import relativedelta
from datetime import datetime
from bi.common.utils import accepts
from trend_narratives import TrendNarrative
from datetime import datetime
from bi.narratives import utils as NarrativesUtils



class TimeSeriesNarrative:
    def __init__(self, df_helper, measure_column, time_dimension_column, existingDateFormat, requestedDateFormat):
        # self._base_dir = os.path.dirname(os.path.realpath(__file__))+"/../../templates/trend/"
        self._base_dir = os.environ.get('MADVISOR_BI_HOME')+"/templates/trend/"
        self.narratives = {"SectionHeading":"",
                           "card1":{},
                           "card2":{},
                           "card3":{}
                        }
        month_dict = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}

        #grouped_data needs to be sorted by date
        grouped_data = df_helper.get_aggregate_data(time_dimension_column,measure_column,
                                                        existingDateFormat=existingDateFormat,
                                                        requestedDateFormat=requestedDateFormat)
        significant_dimensions = df_helper.get_significant_dimension()
        trend_narrative_obj = TrendNarrative(measure_column,time_dimension_column,grouped_data,existingDateFormat,requestedDateFormat)
        grouped_data = trend_narrative_obj.formatDateColumn(grouped_data,requestedDateFormat)
        grouped_data = grouped_data.sort_values(by='key', ascending=True)
        grouped_data["value"] = grouped_data["value"].apply(lambda x: round(x,2))
        dataDict = trend_narrative_obj.generateDataDict(grouped_data)
        pandasDf = df_helper.get_data_frame().toPandas()
        pandasDf[time_dimension_column] = pandasDf[time_dimension_column].apply(lambda x:datetime.strptime(x,existingDateFormat))
        pandasDf[time_dimension_column] = pandasDf[time_dimension_column].apply(lambda x: month_dict[x.month]+"-"+str(x.year))
        # update reference time with max value
        reference_time = dataDict["reference_time"]
        print reference_time
        print significant_dimensions

        xtraData = trend_narrative_obj.get_xtra_calculations(pandasDf,significant_dimensions.keys(),time_dimension_column,measure_column,existingDateFormat,reference_time)
        dataDict.update(xtraData)

        print 'Trend dataDict:  %s' %(json.dumps(dataDict, indent=2))

        self.narratives["SectionHeading"] = measure_column+" Performance Report"
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

        grouped_data["key1"] = grouped_data["key"].apply(lambda x: month_dict[x.month]+"-"+str(x.year))
        grouped_data["key"] = grouped_data["key"].apply(lambda x: str(x))
        trend_data = grouped_data[["key","key1","value"]].T.to_dict().values()
        trend_data = sorted(trend_data,key=lambda x :datetime.strptime(x['key'],"%Y-%m-%d"))
        self.narratives["card1"]["chart"] = trend_data

        prediction_window = 6
        predicted_values = trend_narrative_obj.get_forecast_values(grouped_data["value"],prediction_window)
        predicted_values = predicted_values[len(grouped_data["value"]):]
        predicted_values = [round(x,2) for x in predicted_values]

        prediction_data = [{"key":datetime.strftime(datetime.strptime(x["key"],"%Y-%m-%d"),existingDateFormat),"value":x["value"]} for x in trend_data]
        prediction_data[-1]["predicted_value"] = prediction_data[-1]["value"]

        for val in range(prediction_window):
            dataLevel = dataDict["dataLevel"]
            if dataLevel == "month":
                last_key = datetime.strptime(prediction_data[-1]["key"],existingDateFormat)
                key = datetime.strftime(last_key+relativedelta(months=val+1),existingDateFormat)
                prediction_data.append({"key":key,"predicted_value":predicted_values[val]})

        forecastDataDict = {"startForecast":predicted_values[0],
                            "endForecast":predicted_values[1],
                            "measure":dataDict["measure"],
                            "prediction_window_text":"6 months"
                            }
        summary3 = NarrativesUtils.get_template_output(self._base_dir,\
                                                        'trend_narrative_card3.temp',forecastDataDict)
        self.narratives["card3"]["paragraphs"] = NarrativesUtils.paragraph_splitter(summary3)
        self.narratives["card3"]["chart"] = prediction_data

__all__ = [
    'TrendNarrative'
]
