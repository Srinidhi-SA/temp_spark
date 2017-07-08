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

        # self._base_dir = os.path.dirname(os.path.realpath(__file__))+"/../../templates/executiveSummary/"
        self._base_dir = os.environ.get('MADVISOR_BI_HOME')+"/templates/executiveSummary/"

        self.generate_narratives()

    def generate_narratives(self):
        narrative_data_dict = self._result_setter.get_executive_summary_data()

        sig_dimension_dict = self._dataframe_helper.get_significant_dimension()
        sig_dimension_dict = sorted(sig_dimension_dict,key=lambda x:abs(sig_dimension_dict[x]),reverse=True)
        sig_dims = []
        anova_data = []
        for val in sig_dimension_dict:
            sig_dims.append(val)
            anova_data.append(narrative_data_dict[val])
        narrative_data_dict["sig_dims"] = sig_dims
        narrative_data_dict["anova_data"] = anova_data
        # print json.dumps(narrative_data_dict,indent=2)
        executive_summary = NarrativesUtils.get_template_output(self._base_dir,\
                                                        'executive_summary.temp',narrative_data_dict)
        executive_summary_paragraphs = NarrativesUtils.paragraph_splitter(executive_summary)
        print executive_summary_paragraphs


__all__ = [
    'ExecutiveSummaryNarrative'
]
