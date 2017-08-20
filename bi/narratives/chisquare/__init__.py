import os

from bi.common import ContextSetter
from bi.common.results import DFChiSquareResult
from bi.common.utils import accepts
from chisquare import ChiSquareAnalysis
from chisquare_app2 import ChiSquareAnalysisApp2
from bi.narratives import utils as NarrativesUtils
from bi.common import NormalCard,SummaryCard,NarrativesTree,HtmlData,C3ChartData
from bi.common import ScatterChartData,NormalChartData,ChartJson


class ChiSquareNarratives:
    print "Starting Narratives"
    #@accepts(object, int, DFChiSquareResult ,ContextSetter)
    def __init__(self, df_helper, df_chisquare_result, df_context, data_frame, story_narrative):
        self._story_narrative = story_narrative
        self._blockSplitter = "|~NEWBLOCK~|"
        self._data_frame = data_frame
        self._df_helper = df_helper
        self._measure_columns = df_helper.get_numeric_columns()
        self._df_chisquare = df_chisquare_result
        self._df_chisquare_result = df_chisquare_result.get_result()
        self.narratives = {}
        self._appid = df_context.get_app_id()
        # self._base_dir = os.path.dirname(os.path.realpath(__file__))+"/../../templates/chisquare/"
        self._base_dir = os.environ.get('MADVISOR_BI_HOME')+"/templates/chisquare/"
        if self._appid != None:
            if self._appid == "1":
                self._base_dir += "appid1/"
            elif self._appid == "2":
                self._base_dir += "appid2/"
        self._generate_narratives()

    def _generate_narratives(self):
        chiSquareNode = NarrativesTree()
        chiSquareNode.set_name("Chi-Square")
        for target_dimension in self._df_chisquare_result.keys():

            target_chisquare_result = self._df_chisquare_result[target_dimension]
            analysed_variables = target_chisquare_result.keys()
            significant_variables = [dim for dim in target_chisquare_result.keys() if target_chisquare_result[dim].get_pvalue()<=0.05]
            effect_sizes = [target_chisquare_result[dim].get_effect_size() for dim in significant_variables]
            effect_size_dict = dict(zip(significant_variables,effect_sizes))
            significant_variables = [y for (x,y) in sorted(zip(effect_sizes,significant_variables),reverse=True)]
            #insignificant_variables = [i for i in self._df_chisquare_result[target_dimension] if i['pv']>0.05]
            num_analysed_variables = len(analysed_variables)
            num_significant_variables = len(significant_variables)
            self.narratives['main_card']= {}
            self.narratives['main_card']['heading'] = 'Relationship between '+target_dimension+' and other factors'
            self.narratives['main_card']['paragraphs'] = {}
            data_dict = {
                          'num_variables' : num_analysed_variables,
                          'num_significant_variables' : num_significant_variables,
                          'significant_variables' : significant_variables,
                          'target' : target_dimension,
                          'analysed_dimensions': analysed_variables,
                          'blockSplitter':self._blockSplitter
            } # for both para 1 and para 2
            paragraph={}
            paragraph['header'] = ''

            paragraph['content'] = NarrativesUtils.get_template_output(self._base_dir,'main_card.temp',data_dict)
            self.narratives['main_card']['paragraphs']=[paragraph]
            self.narratives['cards'] = []
            chart = {'header':'Strength of association between '+target_dimension+' and other dimensions'}
            chart['data'] = effect_size_dict
            chart['label_text']={'x':'Dimensions',
                                'y':'Effect Size (Cramers-V)'}

            chart_data = []
            for k,v in effect_size_dict.items():
                chart_data.append({"key":k,"value":v})
            chart_data = sorted(chart_data,key=lambda x:x["value"],reverse=True)
            chart_json = ChartJson()
            chart_json.set_data(chart_data)
            chart_json.set_chart_type("bar")
            chart_json.set_label_text({'x':'Dimensions','y':'Effect Size (Cramers-V)'})
            chart_json.set_axis_rotation(True)
            chart_json.set_axes({"x":"key","y":"value"})
            self.narratives['main_card']['chart']=chart


            main_card = NormalCard()
            header = "Strength of association between "+target_dimension+" and other dimensions"
            main_card_data = [HtmlData(data=header)]
            main_card_data.append(C3ChartData(data=chart_json))
            main_card_narrative = NarrativesUtils.get_template_output(self._base_dir,'main_card.temp',data_dict)
            main_card_narrative = NarrativesUtils.block_splitter(main_card_narrative,self._blockSplitter)
            main_card_data += main_card_narrative
            main_card.set_card_data(main_card_data)
            main_card.set_card_name("Chi-Square-Main-Card")
            chiSquareNode.add_a_card(main_card)

            print "target_dimension",target_dimension
            if self._appid=='2' and num_significant_variables>5:
                significant_variables = significant_variables[:5]
            for analysed_dimension in significant_variables:
                print analysed_dimension
                dimensionNode = NarrativesTree()
                dimensionNode.set_name(target_dimension)
                chisquare_result = self._df_chisquare.get_chisquare_result(target_dimension,analysed_dimension)
                if self._appid=='2':
                    # print "APPID 2 is used"
                    # self.narratives[target_dimension][analysed_dimension] = ChiSquareAnalysisApp2(chisquare_result, target_dimension, analysed_dimension, significant_variables, num_analysed_variables, self._appid)
                    card = ChiSquareAnalysis(chisquare_result, target_dimension, analysed_dimension, significant_variables, num_analysed_variables, self._data_frame, self._measure_columns, None,target_chisquare_result)
                    self.narratives['cards'].append(card)

                else:
                    card = ChiSquareAnalysis(chisquare_result, target_dimension, analysed_dimension, significant_variables, num_analysed_variables, self._data_frame, self._measure_columns, None,target_chisquare_result,dimensionNode)
                    self.narratives['cards'].append(card)
                    chiSquareNode.add_a_node(card.get_dimension_node())
        self._story_narrative.add_a_node(chiSquareNode)
