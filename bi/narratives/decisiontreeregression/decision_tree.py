import os
import random

from bi.common.dataframe import DataFrameHelper
from bi.common.results import DecisionTreeResult
from bi.common.utils import accepts
from bi.common import ResultSetter
from bi.narratives import utils as NarrativesUtils
from bi.common import utils as CommonUtils
from bi.common import NarrativesTree
from bi.common import NormalCard,SummaryCard,NarrativesTree,HtmlData,C3ChartData,TableData,TreeData
from bi.common import ScatterChartData,NormalChartData,ChartJson


class DecisionTreeRegNarrative:
    MAX_FRACTION_DIGITS = 2

    def _get_new_table(self):
        self.card1Table = [["PREDICTION","RULES","PERCENTAGE"]]
        for keys in self.table.keys():
            self.new_table[keys]={}
            self.new_table[keys]['rules'] = self.table[keys]
            self.new_table[keys]['probability'] = [round(i,2) for i in self.success_percent[keys]]
            keyTable = [keys,self.new_table[keys]['rules'],self.new_table[keys]['probability']]
            self.card1Table.append(keyTable)

    # @accepts(object, (str, basestring), DecisionTreeResult,DataFrameHelper,ResultSetter)
    def __init__(self, column_name, decision_tree_rules,df_helper,df_context,result_setter,story_narrative):
        self._story_narrative = story_narrative
        self._blockSplitter = "|~NEWBLOCK~|"
        self._result_setter = result_setter
        self._dataframe_context = df_context
        self._column_name = column_name.lower()
        self._colname = column_name
        self._capitalized_column_name = "%s%s" % (column_name[0].upper(), column_name[1:])
        self._decision_rules_dict = decision_tree_rules.get_decision_rules()
        self.table = decision_tree_rules.get_table()
        self.new_table={}
        self.succesful_predictions=decision_tree_rules.get_success()
        self.total_predictions=decision_tree_rules.get_total()
        self.success_percent= decision_tree_rules.get_success_percent()
        self._important_vars = decision_tree_rules.get_significant_vars()
        self._target_distribution = decision_tree_rules.get_target_contributions()
        self._get_new_table()
        self._df_helper = df_helper
        self.subheader = None
        self.dropdownComment = None
        self.dropdownValues = None
        self._base_dir = os.environ.get('MADVISOR_BI_HOME')+"/templates/decisiontree/"
        self._decisionTreeNode = NarrativesTree(name='Prediction')
        # self._decisionTreeNode.set_name("Decision Tree Regression")

        self._completionStatus = self._dataframe_context.get_completion_status()
        self._analysisName = self._dataframe_context.get_analysis_name()
        self._messageURL = self._dataframe_context.get_message_url()
        self._scriptWeightDict = self._dataframe_context.get_measure_analysis_weight()
        self._scriptStages = {
            "dtreeNarrativeStart":{
                "summary":"Started the Decision Tree Regression Narratives",
                "weight":0
                },
            "dtreeNarrativeEnd":{
                "summary":"Narratives for Decision Tree Regression Finished",
                "weight":10
                },
            }
        self._completionStatus += self._scriptWeightDict[self._analysisName]["narratives"]*self._scriptStages["dtreeNarrativeStart"]["weight"]/10
        progressMessage = CommonUtils.create_progress_message_object(self._analysisName,\
                                    "dtreeNarrativeStart",\
                                    "info",\
                                    self._scriptStages["dtreeNarrativeStart"]["summary"],\
                                    self._completionStatus,\
                                    self._completionStatus)
        CommonUtils.save_progress_message(self._messageURL,progressMessage)
        self._dataframe_context.update_completion_status(self._completionStatus)


        self._generate_narratives()
        self._story_narrative.add_a_node(self._decisionTreeNode)
        self._result_setter.set_decision_tree_node(self._decisionTreeNode)

        self._completionStatus += self._scriptWeightDict[self._analysisName]["narratives"]*self._scriptStages["dtreeNarrativeEnd"]["weight"]/10
        progressMessage = CommonUtils.create_progress_message_object(self._analysisName,\
                                    "dtreeNarrativeEnd",\
                                    "info",\
                                    self._scriptStages["dtreeNarrativeEnd"]["summary"],\
                                    self._completionStatus,\
                                    self._completionStatus)
        CommonUtils.save_progress_message(self._messageURL,progressMessage)
        self._dataframe_context.update_completion_status(self._completionStatus)



    def _generate_narratives(self):
        self._decisionTreeCard1 = NormalCard(name = 'Predicting key drivers of '+self._capitalized_column_name)
        self._decisionTreeCard2 = NormalCard(name = 'Decision Rules of '+self._capitalized_column_name)
        self._generate_summary()
        self._decisionTreeNode.add_cards([self._decisionTreeCard1,self._decisionTreeCard2])

    def _generate_summary(self):
        rules = self._decision_rules_dict
        colname = self._colname
        data_dict = {"dimension_name":self._colname}
        data_dict["plural_colname"] = NarrativesUtils.pluralize(data_dict["dimension_name"])
        data_dict["significant_vars"] = []
        if "High" in self._important_vars:
            data_dict['significant_vars_high'] = self._important_vars['High']
        if "Low" in self._important_vars:
            data_dict['significant_vars_low'] = self._important_vars['Low']
        rules_dict = self.table
        self.condensedTable={}
        for target in rules_dict.keys():
            self.condensedTable[target]=[]
            total = self.total_predictions[target]
            success = self.succesful_predictions[target]
            success_percent = self.success_percent[target]
            for idx,rule in enumerate(rules_dict[target]):
                rules1 = self._generate_rules(target,rule, total[idx], success[idx], success_percent[idx])
                self.condensedTable[target].append(rules1)
        self.dropdownValues = rules_dict.keys()
        lines2 = []
        lines2 += NarrativesUtils.block_splitter('Most Significant Rules for Price :',self._blockSplitter)
        lines2 += [TreeData(data=self.condensedTable,datatype='dropdown')]
        self._decisionTreeCard2.add_card_data(lines2)
        if "High" in self.condensedTable:
            data_dict['rules_list_high'] = self.condensedTable['High']
        if "Low" in self.condensedTable:
            data_dict['rules_list_low'] = self.condensedTable['Low']
        print self._target_distribution.keys()
        if "High" in self._target_distribution:
            data_dict['count_percent_high'] = NarrativesUtils.round_number(self._target_distribution['High']['count_percent'],2)
            data_dict['sum_percent_high'] =  NarrativesUtils.round_number(self._target_distribution['High']['sum_percent'],2)
            data_dict['sum_high'] =  NarrativesUtils.round_number(self._target_distribution['High']['sum'],2)
            data_dict['average_high_group'] = self._target_distribution['High']['sum']*1.0/self._target_distribution['High']['count']
        if "Low" in self._target_distribution:
            data_dict['count_percent_low'] =  NarrativesUtils.round_number(self._target_distribution['Low']['count_percent'],2)
            data_dict['sum_percent_low'] =  NarrativesUtils.round_number(self._target_distribution['Low']['sum_percent'],2)
        data_dict['average_overall'] = sum([self._target_distribution[i]['sum'] for i in self._target_distribution])*1.0/sum([self._target_distribution[i]['count'] for i in self._target_distribution])
        data_dict['high_vs_overall'] = data_dict['average_high_group']*100.0/data_dict['average_high_group'] - 100
        self.card2_data = NarrativesUtils.paragraph_splitter(NarrativesUtils.get_template_output(self._base_dir,\
                                                    'decision_reg_card2.html',data_dict))
        self.card2_chart = {'sum' : dict([(k,v['sum']) for k,v in self._target_distribution.items()]),
                            'mean': dict([(k,v['sum']*1.0/v['count']) for k,v in self._target_distribution.items()]),
                            'legends': {'sum': self._capitalized_column_name+' Total',
                                        'mean': self._capitalized_column_name+' Avg'}}
        self.subheader = NarrativesUtils.get_template_output(self._base_dir,\
                                        'decision_tree_summary.html',data_dict)
        lines = []
        lines += NarrativesUtils.block_splitter(self.subheader,self._blockSplitter)
        tableData = TableData(data={"tableType" : "decisionTreeTable",'tableData':self.card1Table})
        lines += [TreeData(data=self._decision_rules_dict),tableData]
        self._decisionTreeCard1.add_card_data(lines)
        # executive_summary_data = {"rules_list_high":data_dict['rules_list_high'],
        #                           "average_high_group" : data_dict["average_high_group"],
        #                           "average_overall" : data_dict["average_overall"],
        #                           "high_vs_overall" : data_dict["high_vs_overall"]
        #                          }
        # self._result_setter.update_executive_summary_data(executive_summary_data)

    def _generate_rules(self,target,rules, total, success, success_percent):
        colname = self._colname
        key_dimensions,key_measures=NarrativesUtils.get_rules_dictionary(rules)
        temp_narrative = ''
        for var in key_measures.keys():
            if key_measures[var].has_key('upper_limit') and key_measures[var].has_key('lower_limit'):
                temp_narrative = temp_narrative + 'the value of ' + var + ' falls between ' + key_measures[var]['lower_limit'] + ' and ' + key_measures[var]['upper_limit']+', '
            elif key_measures[var].has_key('upper_limit'):
                temp_narrative = temp_narrative + 'the value of ' + var + ' is less than or equal to ' + key_measures[var]['upper_limit']+', '
            elif key_measures[var].has_key('lower_limit'):
                temp_narrative = temp_narrative + 'the value of ' + var + ' is greater than ' + key_measures[var]['lower_limit']+', '
        for var in key_dimensions.keys():
            if key_dimensions[var].has_key('in'):
                temp_narrative = temp_narrative + 'the ' + var + ' falls among ' + key_dimensions[var]['in'] + ', '
            elif key_dimensions[var].has_key('not_in'):
                temp_narrative = temp_narrative + 'the ' + var + ' does not fall in ' + key_dimensions[var]['not_in'] + ', '

        if temp_narrative == '':
            temp_narrative = ""
        else:
            r = random.randint(0,99)%5
            if r == 0:
                narrative = 'Nearly <b>' + NarrativesUtils.round_number(success_percent)+ '%' + \
                            '</b> of observations that have ' + temp_narrative + ' result in '+ \
                            target + ' '+ self._column_name + ' values.'
            elif r == 1:
                narrative = 'If ' + temp_narrative +' it is <b>' + NarrativesUtils.round_number(success_percent)+ '%' + \
                            '</b> likely that the observations are ' + target + ' segment.'
            elif r == 2:
                narrative = 'When ' +  temp_narrative + ' the probability of ' + target + \
                            ' is <b>' + NarrativesUtils.round_number(success_percent)+ '%' + '</b>.'
            elif r == 3:
                narrative = 'If ' + temp_narrative +' then there is <b>' + NarrativesUtils.round_number(success_percent)+ '%' + \
                            '</b> probability that the ' + self._column_name + ' observations would be ' + target + ' valued.'
            else:
                narrative = 'There is a very high chance(<b>' + NarrativesUtils.round_number(success_percent)+ '%' + \
                            '</b>) that ' +  self._column_name + ' would be relatively ' + target + ' when, ' + \
                            temp_narrative[:-2] + '.'
            return narrative
