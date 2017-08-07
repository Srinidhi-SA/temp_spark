# -*- coding: utf-8 -*-
"""Gathers descriptive stats for all columns in a dataframe"""
import json
from bi.common import DataWriter
from bi.common import utils as CommonUtils
# from bi.narratives.descr import DescriptiveStatsNarrative
from bi.narratives.descr.measure import MeasureColumnNarrative
from bi.stats.descr import DescriptiveStats


class DescriptiveStatsScript:
    def __init__(self, data_frame, df_helper, df_context, result_setter, spark):
        self._result_setter = result_setter
        self._data_frame = data_frame
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context
        self._spark = spark

    def Run(self):
        descr_stats_obj = DescriptiveStats(self._data_frame, self._dataframe_helper, self._dataframe_context).stats_for_measure_column(self._dataframe_context.get_result_column())
        descr_stats = CommonUtils.as_dict(descr_stats_obj)
        # print 'RESULT: %s' % (json.dumps(descr_stats, indent=2))
        DataWriter.write_dict_as_json(self._spark, descr_stats, self._dataframe_context.get_result_file()+'DescrStats/')

        narratives_obj = MeasureColumnNarrative(self._dataframe_context.get_result_column(), descr_stats_obj, self._dataframe_helper,self._dataframe_context,self._result_setter)
        narratives = CommonUtils.as_dict(narratives_obj)

        # print 'Narratives: %s' % (json.dumps(narratives, indent=2))
        DataWriter.write_dict_as_json(self._spark, narratives, self._dataframe_context.get_narratives_file()+'DescrStats/')
