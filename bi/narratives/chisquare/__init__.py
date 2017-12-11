import os
import json
from bi.common import ContextSetter
from bi.common.results import DFChiSquareResult
from bi.common.utils import accepts
from chisquare import ChiSquareAnalysis
from bi.narratives import utils as NarrativesUtils
from bi.common import NormalCard,SummaryCard,NarrativesTree,HtmlData,C3ChartData
from bi.common import ScatterChartData,NormalChartData,ChartJson
from bi.common import utils as CommonUtils


class ChiSquareNarratives:
    print "Starting Narratives"
    #@accepts(object, int, DFChiSquareResult ,ContextSetter)
    def __init__(self, df_helper, df_chisquare_result, df_context, data_frame, story_narrative,result_setter,scriptWeight=None, analysisName=None):
        self._story_narrative = story_narrative
        self._result_setter = result_setter
        self._blockSplitter = "|~NEWBLOCK~|"
        self._data_frame = data_frame
        self._dataframe_context = df_context
        self._df_helper = df_helper
        self._measure_columns = df_helper.get_numeric_columns()
        self._df_chisquare = df_chisquare_result
        self._df_chisquare_result = df_chisquare_result.get_result()
        self.narratives = {}
        self._appid = df_context.get_app_id()
        self._chiSquareNode = NarrativesTree()
        self._chiSquareNode.set_name("Association")
        self._base_dir = self._dataframe_context.get_base_directory()+"/templates/chisquare/"
        if self._appid != None:
            if self._appid == "1":
                self._base_dir += "appid1/"
            elif self._appid == "2":
                self._base_dir += "appid2/"

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
        self._analysisDict = self._dataframe_context.get_analysis_dict()
        if self._analysisDict != {}:
            self._nColsToUse = self._analysisDict[self._analysisName]["noOfColumnsToUse"]
        else:
            self._nColsToUse = None



        self._scriptStages = {
            "initialization":{
                "summary":"Initialized the Frequency Narratives",
                "weight":0
                },
            "summarygeneration":{
                "summary":"summary generation finished",
                "weight":10
                },
            "completion":{
                "summary":"Frequency Stats Narratives done",
                "weight":0
                },
            }
        self._completionStatus += self._scriptWeightDict[self._analysisName]["narratives"]*self._scriptStages["initialization"]["weight"]/10
        progressMessage = CommonUtils.create_progress_message_object(self._analysisName,\
                                    "initialization",\
                                    "info",\
                                    self._scriptStages["initialization"]["summary"],\
                                    self._completionStatus,\
                                    self._completionStatus)
        CommonUtils.save_progress_message(self._messageURL,progressMessage)
        self._dataframe_context.update_completion_status(self._completionStatus)


        self._generate_narratives()
        self._completionStatus += self._scriptWeightDict[self._analysisName]["narratives"]*self._scriptStages["summarygeneration"]["weight"]/10
        progressMessage = CommonUtils.create_progress_message_object(self._analysisName,\
                                    "summarygeneration",\
                                    "info",\
                                    self._scriptStages["summarygeneration"]["summary"],\
                                    self._completionStatus,\
                                    self._completionStatus)
        CommonUtils.save_progress_message(self._messageURL,progressMessage)
        self._dataframe_context.update_completion_status(self._completionStatus)

        self._completionStatus += self._scriptWeightDict[self._analysisName]["narratives"]*self._scriptStages["completion"]["weight"]/10
        progressMessage = CommonUtils.create_progress_message_object(self._analysisName,\
                                    "completion",\
                                    "info",\
                                    self._scriptStages["completion"]["summary"],\
                                    self._completionStatus,\
                                    self._completionStatus)
        CommonUtils.save_progress_message(self._messageURL,progressMessage)
        self._dataframe_context.update_completion_status(self._completionStatus)

    def _generate_narratives(self):
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

            paragraph['content'] = NarrativesUtils.get_template_output(self._base_dir,'main_card.html',data_dict)
            self.narratives['main_card']['paragraphs']=[paragraph]
            self.narratives['cards'] = []
            chart = {'header':'Strength of association between '+target_dimension+' and other dimensions'}
            chart['data'] = effect_size_dict
            chart['label_text']={'x':'Dimensions',
                                'y':'Effect Size (Cramers-V)'}

            chart_data = []
            for k,v in effect_size_dict.items():
                chart_data.append({"key":k,"value":float(v)})
            chart_data = sorted(chart_data,key=lambda x:x["value"],reverse=True)
            chart_json = ChartJson()
            chart_json.set_data(chart_data)
            chart_json.set_chart_type("bar")
            # chart_json.set_label_text({'x':'Dimensions','y':'Effect Size (Cramers-V)'})
            chart_json.set_label_text({'x':'  ','y':'Effect Size (Cramers-V)'})
            chart_json.set_axis_rotation(True)
            chart_json.set_axes({"x":"key","y":"value"})
            chart_json.set_yaxis_number_format(".2f")
            self.narratives['main_card']['chart']=chart


            main_card = NormalCard()
            header = "<h3>Strength of association between "+target_dimension+" and other dimensions</h3>"
            main_card_data = [HtmlData(data=header)]
            main_card_narrative = NarrativesUtils.get_template_output(self._base_dir,'main_card.html',data_dict)
            main_card_narrative = NarrativesUtils.block_splitter(main_card_narrative,self._blockSplitter)
            main_card_data += main_card_narrative
            main_card_data.append(C3ChartData(data=chart_json))
            main_card.set_card_data(main_card_data)
            main_card.set_card_name("Key Influencers")
            self._chiSquareNode.add_a_card(main_card)
            self._result_setter.add_a_score_chi_card(main_card)

            print "target_dimension",target_dimension
            if self._appid=='2' and num_significant_variables>5:
                significant_variables = significant_variables[:5]
            else:
                if self._nColsToUse != None:
                    significant_variables = significant_variables[:self._nColsToUse]
            for analysed_dimension in significant_variables:
                chisquare_result = self._df_chisquare.get_chisquare_result(target_dimension,analysed_dimension)
                if self._appid=='2':
                    print "APPID 2 is used"
                    card = ChiSquareAnalysis(chisquare_result, target_dimension, analysed_dimension, significant_variables, num_analysed_variables, self._data_frame, self._measure_columns, self._base_dir,None,target_chisquare_result)
                    # self.narratives['cards'].append(card)
                    self._result_setter.add_a_score_chi_card(json.loads(CommonUtils.convert_python_object_to_json(card.get_dimension_card1())))

                elif self._appid=='1':
                    print "APPID 1 is used"
                    card = ChiSquareAnalysis(chisquare_result, target_dimension, analysed_dimension, significant_variables, num_analysed_variables, self._data_frame, self._measure_columns,self._base_dir, None,target_chisquare_result)
                    # self.narratives['cards'].append(card)
                    self._result_setter.add_a_score_chi_card(json.loads(CommonUtils.convert_python_object_to_json(card.get_dimension_card1())))
                else:
                    target_dimension_card = ChiSquareAnalysis(chisquare_result, target_dimension, analysed_dimension, significant_variables, num_analysed_variables, self._data_frame, self._measure_columns,self._base_dir, None,target_chisquare_result)
                    self.narratives['cards'].append(target_dimension_card)
                    self._chiSquareNode.add_a_node(target_dimension_card.get_dimension_node())
        self._story_narrative.add_a_node(self._chiSquareNode)
        self._result_setter.set_chisquare_node(self._chiSquareNode)
