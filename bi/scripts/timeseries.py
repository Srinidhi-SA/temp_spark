import json

from bi.common import DataWriter
from bi.common import utils as CommonUtils
from bi.narratives import utils as NarrativesUtils
from bi.narratives.trend import TimeSeriesNarrative


class TrendScript:

    def __init__(self, df_helper, df_context, result_setter, spark, story_narrative):
        self._story_narrative = story_narrative
        self._result_setter = result_setter
        self._dataframe_helper = df_helper
        self._spark = spark
        self._dataframe_context = df_context


    def Run(self):
        analysisName = self._dataframe_context.get_analysis_name()
        scriptWeightDict = self._dataframe_context.get_measure_analysis_weight()
        completionStatus = self._dataframe_context.get_completion_status()

        trend_narratives_obj = TimeSeriesNarrative(self._dataframe_helper, self._dataframe_context, self._result_setter, self._spark, self._story_narrative)
        trend_narratives = CommonUtils.as_dict(trend_narratives_obj)
        # print json.dumps(trend_narratives, indent=2)
        # DataWriter.write_dict_as_json(self._spark, {"TREND":json.dumps(trend_narratives)}, self._dataframe_context.get_narratives_file()+'Trend/')
        completionStatus += scriptWeightDict[analysisName]["total"]
        self._dataframe_context.update_completion_status(completionStatus)
