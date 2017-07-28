import os
import re
import time

import jinja2

from anova_drilldown import AnovaDrilldownNarratives
from bi.common import DataFrameHelper
from bi.common.results.anova import DFAnovaResult
from bi.common.utils import accepts
from oneway import OneWayAnovaNarratives


class AnovaNarratives:
    ALPHA = 0.05

    KEY_SUMMARY = 'summary'
    KEY_NARRATIVES = 'narratives'
    KEY_TAKEAWAY = 'key_takeaway'
    DRILL_DOWN = 'drill_down_narrative'

    @accepts(object, int, DFAnovaResult, DataFrameHelper)
    def __init__(self, num_dimension_columns, df_anova_result, df_helper):
        self.df_helper = df_helper
        self._num_dimension_columns = num_dimension_columns
        self._df_anova_result = df_anova_result
        self.measures = []
        self.narratives = {}
        #self._base_dir = os.path.dirname(os.path.realpath(__file__))+"/../../templates/anova/"
        self._base_dir = os.environ.get('MADVISOR_BI_HOME')+"/templates/anova/"
        self._generate_narratives()


    def _generate_narratives(self):
        for measure_column in self._df_anova_result.get_measure_columns():
            self.narratives[measure_column] = {}
            self.narratives[measure_column]['heading'] = "%s Performance Analysis" % (measure_column,)
            self.narratives[measure_column]['sub_heading1'] = "Analysis by Dimension"
            num_significant_dimensions = 0
            num_insignificant_dimensions = 0
            significant_dimensions = []
            insignificant_dimensions = []
            effect_sizes = {}
            self.narratives[measure_column][AnovaNarratives.KEY_NARRATIVES]={}
            #self.narratives[measure_column]['sub_heading'] = {}
            for dimension_column in self._df_anova_result.get_dimensions_analyzed(measure_column):
                anova_result = self._df_anova_result.get_anova_result(measure_column, dimension_column)
                if not anova_result.is_statistically_significant(AnovaNarratives.ALPHA):
                    insignificant_dimensions.append(dimension_column)
                    num_insignificant_dimensions+=1
                    continue
                significant_dimensions.append(dimension_column)
                effect_sizes[dimension_column] = anova_result.get_effect_size()
                num_significant_dimensions += 1
                if measure_column not in self.measures:
                    self.measures.append(measure_column)
                if not self.narratives.has_key(measure_column):
                    self.narratives[measure_column] = {AnovaNarratives.KEY_SUMMARY: '',
                                                       AnovaNarratives.KEY_NARRATIVES: {}}
                narrative = OneWayAnovaNarratives(measure_column, dimension_column, anova_result)
                self.narratives[measure_column][AnovaNarratives.KEY_NARRATIVES][dimension_column] = narrative
            fs = time.time()
            try:
                anova_narrative = self.narratives[measure_column][AnovaNarratives.KEY_NARRATIVES]
                drill_down_narrative = AnovaDrilldownNarratives(measure_column, significant_dimensions, self.df_helper, anova_narrative)
                self.narratives[measure_column][AnovaNarratives.DRILL_DOWN] = drill_down_narrative.analysis
                print "Drill Down Narrative Success"
            except Exception as e:
                print "Drill Down Narrative Failed"
                self.narratives[measure_column][AnovaNarratives.DRILL_DOWN] = {}
                print "ERROR"*5
                print e
                print "ERROR"*5
            print "Drill Down Analysis Done in ", time.time() - fs,  " seconds."

            #self.narratives[measure_column]['sub_heading'][dimension_column] = narrative.get_sub_heading()
            #self.ordered_narratives = OrderedDict(sorted(self.narratives[measure_column][AnovaNarratives.KEY_NARRATIVES][dimension_column].items(),
            #                            key = lambda kv: kv[1]['effect_size'], reverse=True))

            sorted_dim=[]
            for key,value in sorted(effect_sizes.iteritems(),key = lambda (k,v):(v,k)):
                sorted_dim.append(key)
            data_dict = {
                'n_d': num_significant_dimensions+num_insignificant_dimensions,
                'n_s_d': num_significant_dimensions,
                'n_ns_d': num_insignificant_dimensions,
                'sd': significant_dimensions,
                'nsd': insignificant_dimensions,
                'cm': measure_column,
                'd' : significant_dimensions+insignificant_dimensions,
                'dims' : sorted_dim
            }

            templateLoader = jinja2.FileSystemLoader( searchpath=self._base_dir)
            templateEnv = jinja2.Environment( loader=templateLoader )
            template = templateEnv.get_template('anova_template_1.temp')
            output = template.render(data_dict).replace("\n", "")
            output = re.sub(' +',' ',output)

            chart_template = templateEnv.get_template('anova_template_2.temp')
            output_chart = chart_template.render(data_dict).replace("\n", "")
            output_chart = re.sub(' +',' ',output_chart)

            #anova_1_and_2 = output +"\n"+ output_chart
            #print anova_1_and_2
            self.narratives[measure_column][AnovaNarratives.KEY_SUMMARY] = [output,output_chart]

            takeaway = ''
            templateLoader = jinja2.FileSystemLoader( searchpath=self._base_dir)
            templateEnv = jinja2.Environment( loader=templateLoader )
            template = templateEnv.get_template('anova_takeaway.temp')
            takeaway = template.render(data_dict).replace("\n", " ")
            takeaway = re.sub(' +',' ',takeaway)
            self.narratives[measure_column][AnovaNarratives.KEY_TAKEAWAY] = takeaway
