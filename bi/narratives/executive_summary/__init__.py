import os
import re
import json
import pandas as pd
from pyspark.sql import functions as FN
from pyspark.sql.functions import sum

from bi.narratives import utils as NarrativesUtils



class ExecutiveSummaryNarrative:
    def __init__(self, df_helper, df_context, result_setter, spark):
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context
        self._result_setter = result_setter
        print self._result_setter.get_executive_summary_data()


__all__ = [
    'ExecutiveSummaryNarrative'
]
