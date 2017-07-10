import os

from anova_drilldown import AnovaDrilldownNarratives
from bi.narratives import utils as NarrativesUtils
from bi.narratives.anovas.anova import OneWayAnovaNarratives


class AnovaNarratives:
    ALPHA = 0.05

    KEY_SUMMARY = 'summary'
    KEY_NARRATIVES = 'narratives'
    KEY_TAKEAWAY = 'key_takeaway'
    DRILL_DOWN = 'drill_down_narrative'
    KEY_CARD = 'card'
    KEY_HEADING = 'heading'
    KEY_SUBHEADING = 'header'
    KEY_CHART = 'charts'
    KEY_PARAGRAPH = 'paragraphs'
    KEY_PARA_HEADER = 'header'
    KEY_PARA_CONTENT = 'content'
    KEY_BUBBLE = 'bubble_data'

    # @accepts(object, DFAnovaResult, DataFrameHelper)
    def __init__(self, df_anova_result, df_helper, result_setter):
        self._result_setter = result_setter
        self._df_anova_result = df_anova_result
        self._df_helper = df_helper
        self.narratives = {}
        self.narratives['variables'] = ''
        #self._base_dir = os.path.dirname(os.path.realpath(__file__))+"/../../templates/anova/"
        self._base_dir = os.environ.get('MADVISOR_BI_HOME')+"/templates/anovas/"
        self._generate_narratives()
        #self._generate_take_away()


    def _generate_narratives(self):
        for measure_column in self._df_anova_result.get_measure_columns():
            measure_anova_result = self._df_anova_result.result[measure_column]
            significant_dimensions_dict, insignificant_dimensions = measure_anova_result.get_OneWayAnovaSignificantDimensions()
            significant_dimensions = [k for k,v in sorted(significant_dimensions_dict.items(), key=lambda x: -x[1])]
            num_significant_dimensions = len(significant_dimensions)
            num_insignificant_dimensions = len(insignificant_dimensions)
            self.narratives = {}
            self.narratives[AnovaNarratives.KEY_HEADING] = "%s Performance Analysis" % (measure_column,)
            self.narratives['main_card'] = {}
            self.narratives['cards'] = []
            self.narratives['main_card'][AnovaNarratives.KEY_SUBHEADING] = "Relationship between %s and other Dimensions" % (measure_column)
            self.narratives['main_card'][AnovaNarratives.KEY_PARAGRAPH] = []
            data_dict = { \
                            'significant_dimensions' : significant_dimensions,
                            'insignificant_dimensions' : insignificant_dimensions,
                            'num_significant_dimensions' : num_significant_dimensions,
                            'num_insignificant_dimensions' : num_insignificant_dimensions,
                            'num_dimensions' : num_significant_dimensions+num_insignificant_dimensions,
                            'target' : measure_column \
                        }
            output = {'header' : ''}
            output['content'] = NarrativesUtils.get_template_output(self._base_dir,'anova_template_1.temp',data_dict)
            self.narratives['main_card'][AnovaNarratives.KEY_PARAGRAPH].append(output)
            output1 = {'header' : ''}
            output1['content'] = NarrativesUtils.get_template_output(self._base_dir,'anova_template_2.temp',data_dict)
            self.narratives['main_card'][AnovaNarratives.KEY_PARAGRAPH].append(output1)
            self.narratives['main_card'][AnovaNarratives.KEY_CHART] = {}
            effect_size_chart = { 'heading' : '',
                                  'labels' : {'Dimension':'Effect Size'},
                                  'data' : significant_dimensions_dict}
            self.narratives['main_card'][AnovaNarratives.KEY_CHART]['effect_size'] = effect_size_chart
            self._generate_dimension_narratives(significant_dimensions, measure_anova_result, measure_column)

    def _generate_dimension_narratives(self, significant_dimensions, measure_anova_result, measure):
        self.narratives['cards'] = []
        anova_trend_result = measure_anova_result.get_TrendResult()
        if len(significant_dimensions) == 0:
            self.narratives['cards'].append({'card1':'', 'card2':'', 'card3':''})
        self.narratives['variables'] = significant_dimensions
        for dimension in significant_dimensions:
            anova_dimension_result = measure_anova_result.get_anova_result(dimension)
            narratives = OneWayAnovaNarratives(measure, dimension, anova_dimension_result, anova_trend_result,self._result_setter)
            self.narratives['cards'].append(narratives)
