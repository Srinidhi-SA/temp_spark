import os

from bi.common import ContextSetter
from bi.common.results import DFChiSquareResult
from bi.common.utils import accepts
from chisquare import ChiSquareAnalysis
from chisquare_app2 import ChiSquareAnalysisApp2


###
### TODO: complete rewrite recommended
###         Ram, 28/Jan/2017
###


class ChiSquareNarratives:
    @accepts(object, int, DFChiSquareResult ,ContextSetter)
    def __init__(self, num_dimension_columns, df_chisquare_result, df_context):
        self._num_dimension_columns = num_dimension_columns
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
        for target_dimension in self._df_chisquare_result.keys():

            target_chisquare_result = self._df_chisquare_result[target_dimension]
            significant_variables = [dim for dim in target_chisquare_result.keys() if target_chisquare_result[dim].get_pvalue()<=0.05]
            effect_sizes = [dim for dim in significant_variables if target_chisquare_result[dim].get_effect_size()]
            significant_variables = [x for (x,y) in sorted(zip(effect_sizes,significant_variables),reverse=True)]
            #insignificant_variables = [i for i in self._df_chisquare_result[target_dimension] if i['pv']>0.05]
            num_analysed_variables = len(target_chisquare_result)
            num_significant_variables = len(significant_variables)
            self.narratives[target_dimension] = {}
            self.narratives[target_dimension]['heading'] = target_dimension + ' Performance Analysis'
            self.narratives[target_dimension]['sub_heading'] = "Relationship with other variables"
            data_dict = {
                          'num_variables' : num_analysed_variables,
                          'num_significant_variables' : num_significant_variables,
                          'significant_variables' : significant_variables,
                          'target_dimension' : target_dimension
            } # for both para 1 and para 2
            summary1 = NarrativesUtils.get_template_output(self._base_dir,'chisquare_template1.temp',data_dict)
            summary2 = NarrativesUtils.get_template_output(self._base_dir,'chisquare_template2.temp',data_dict)
            self.narratives[target_dimension]['summary'] = [summary1,summary2]
            if self._appid=='2' and num_significant_variables>5:
                significant_variables = significant_variables[:5]
            for analysed_dimension in significant_variables:
                chisquare_result = self._df_chisquare.get_chisquare_result(target_dimension,analysed_dimension)
                if self._appid=='2':
                    self.narratives[target_dimension][analysed_dimension] = ChiSquareAnalysisApp2(chisquare_result, target_dimension, analysed_dimension, significant_variables, num_analysed_variables, self._appid)
                else:
                    self.narratives[target_dimension][analysed_dimension] = ChiSquareAnalysis(chisquare_result, target_dimension, analysed_dimension, significant_variables, num_analysed_variables, self._appid)
