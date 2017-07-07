# -*- coding: utf-8 -*-
"""Gathers descriptive stats for all columns in a dataframe"""

from bi.common import DataWriter
from bi.common import utils as CommonUtils
from bi.narratives.executive_summary import ExecutiveSummaryNarrative


class ExecutiveSummaryScript:
    def __init__(self, df_helper, df_context, result_setter, spark):
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context
        self._result_setter = result_setter
        self._spark = spark

    def Run(self):
        print "executive summary script called"
        executive_summary = ExecutiveSummaryNarrative(self._dataframe_helper,self._dataframe_context,self._result_setter,self._spark)
        # descr_stats_obj = DescriptiveStats(self._data_frame, self._dataframe_helper, self._dataframe_context).stats_for_measure_column(self._dataframe_context.get_result_column())
        # descr_stats = utils.as_dict(descr_stats_obj)
        # # print 'RESULT: %s' % (json.dumps(descr_stats, indent=2))
        # DataWriter.write_dict_as_json(self._spark, descr_stats, self._dataframe_context.get_result_file()+'DescrStats/')
        #
        # narratives_obj = MeasureColumnNarrative(self._dataframe_context.get_result_column(), descr_stats_obj, self._dataframe_helper,self._dataframe_context)
        # narratives = utils.as_dict(narratives_obj)
        #
        # # print 'Narratives: %s' % (json.dumps(narratives, indent=2))
        # DataWriter.write_dict_as_json(self._spark, narratives, self._dataframe_context.get_narratives_file()+'DescrStats/')
