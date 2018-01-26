import json

from bi.common import utils as CommonUtils
from bi.common.decorators import accepts
from bi.common.results import FreqDimensionResult

"""
Count Frequency in a Dimension
"""


class FreqDimensions:

    def __init__(self, data_frame, df_helper, df_context, scriptWeight=None, analysisName=None):
        self._data_frame = data_frame
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context

        self._completionStatus = self._dataframe_context.get_completion_status()
        if analysisName == None:
            self._analysisName = self._dataframe_context.get_analysis_name()
        else:
            self._analysisName = analysisName
        self._messageURL = self._dataframe_context.get_message_url()
        if scriptWeight == None:
            self._scriptWeightDict = self._dataframe_context.get_dimension_analysis_weight()
        else:
            self._scriptWeightDict = scriptWeight

        self._scriptStages = {
            "freqinitialization":{
                "summary":"Initialized the Frequency Scripts",
                "weight":4
                },
            "groupby":{
                "summary":"running groupby operations",
                "weight":6
                },
            "completion":{
                "summary":"Frequency Stats Calculated",
                "weight":0
                },
            }

        self._completionStatus += self._scriptWeightDict[self._analysisName]["script"]*self._scriptStages["freqinitialization"]["weight"]/10
        progressMessage = CommonUtils.create_progress_message_object(self._analysisName,\
                                    "freqinitialization",\
                                    "info",\
                                    self._scriptStages["freqinitialization"]["summary"],\
                                    self._completionStatus,\
                                    self._completionStatus)
        CommonUtils.save_progress_message(self._messageURL,progressMessage)
        self._dataframe_context.update_completion_status(self._completionStatus)

    @accepts(object, measure_columns=(list, tuple), dimension_columns=(list, tuple))
    def test_all(self, measure_columns=None, dimension_columns=None):
        freq_dimension_result = FreqDimensionResult()
        dimension = dimension_columns[0]
        frequency_dict = {}
        grouped_dataframe = self._data_frame.groupby(dimension).count().toPandas()
        self._completionStatus += self._scriptWeightDict[self._analysisName]["script"]*self._scriptStages["groupby"]["weight"]/10
        progressMessage = CommonUtils.create_progress_message_object(self._analysisName,\
                                    "groupby",\
                                    "info",\
                                    self._scriptStages["groupby"]["summary"],\
                                    self._completionStatus,\
                                    self._completionStatus)
        CommonUtils.save_progress_message(self._messageURL,progressMessage)
        self._dataframe_context.update_completion_status(self._completionStatus)
        frequency_dict[dimension] = grouped_dataframe.to_dict()
        grouped_dataframe = grouped_dataframe.dropna()
        frequency_dict = json.dumps(frequency_dict)
        freq_dimension_result.set_params(frequency_dict)
        self._completionStatus += self._scriptWeightDict[self._analysisName]["script"]*self._scriptStages["completion"]["weight"]/10
        progressMessage = CommonUtils.create_progress_message_object(self._analysisName,\
                                    "completion",\
                                    "info",\
                                    self._scriptStages["completion"]["summary"],\
                                    self._completionStatus,\
                                    self._completionStatus)
        CommonUtils.save_progress_message(self._messageURL,progressMessage)
        return freq_dimension_result
