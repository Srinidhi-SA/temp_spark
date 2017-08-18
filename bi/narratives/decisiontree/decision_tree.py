import os
import random
import json
import itertools
from bi.common.dataframe import DataFrameHelper
from bi.common.results import DecisionTreeResult
from bi.common.utils import accepts
from bi.narratives import utils as NarrativesUtils
from bi.common import utils as CommonUtils
from bi.common import NarrativesTree
from bi.common import NormalCard,SummaryCard,NarrativesTree,HtmlData,C3ChartData,TableData
from bi.common import ScatterChartData,NormalChartData,ChartJson




class DecisionTreeNarrative:
    MAX_FRACTION_DIGITS = 2

    def _get_new_table(self):
        self.card1Table = []
        for keys in self.table.keys():
            self.new_table[keys]={}
            self.new_table[keys]['rules'] = self.table[keys]
            self.new_table[keys]['probability'] = [round(i,2) for i in self.success_percent[keys]]
            first_col = [""]*len(self.new_table[keys]['rules'])
            first_col[0] = keys
            keyTable = zip(first_col,self.new_table[keys]['rules'],self.new_table[keys]['probability'])
            keyTable = [list(obj) for obj in keyTable]
            self.card1Table += keyTable

    @accepts(object, (str, basestring), DecisionTreeResult,DataFrameHelper,NarrativesTree)
    def __init__(self, column_name, decision_tree_rules,df_helper ,story_narrative):
        self._story_narrative = story_narrative
        self._blockSplitter = "|~NEWBLOCK~|"
        self._column_name = column_name.lower()
        self._colname = column_name
        self._capitalized_column_name = "%s%s" % (column_name[0].upper(), column_name[1:])
        self._decision_rules_dict = decision_tree_rules.get_decision_rules()
        self._decision_tree_json = CommonUtils.as_dict(decision_tree_rules)
        self._decision_tree_raw = {"tree":{"children":None}}
        self._decision_tree_raw['tree']["children"] = self._decision_tree_json['tree']["children"]
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
        self.decisionTreeNode = NarrativesTree()
        self.decisionTreeNode.set_name("Decision-Tree")
        self._generate_narratives()
        self._story_narrative.add_a_node(self.decisionTreeNode)


    def _generate_narratives(self):
        self._generate_summary()

    def _generate_summary(self):
        rules = self._decision_rules_dict
        colname = self._colname
        data_dict = {"dimension_name":self._colname}
        data_dict["plural_colname"] = NarrativesUtils.pluralize(data_dict["dimension_name"])
        data_dict["significant_vars"] = []
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
        data_dict["blockSplitter"] = self._blockSplitter
        data_dict['rules'] = self.condensedTable
        data_dict['success'] = self.success_percent
        data_dict['significant_vars'] = list(set(itertools.chain.from_iterable(self._important_vars.values())))
        data_dict['significant_vars'] = self._important_vars
        # print '*'*16
        # print data_dict['rules']
        # print self.new_table
        self.card2_data = NarrativesUtils.paragraph_splitter(NarrativesUtils.get_template_output(self._base_dir,\
                                                    'decision_tree_card2.temp',data_dict))
        self.card2_chart = self._target_distribution

        self.dropdownComment = NarrativesUtils.get_template_output(self._base_dir,\
                                                    'decision_rule_summary.temp',data_dict)
        main_card = NormalCard()
        main_card_data = []
        main_card_narrative = NarrativesUtils.block_splitter(self.dropdownComment,self._blockSplitter)
        main_card_narrative = [HtmlData(data=main_card_narrative)]
        main_card_data += main_card_narrative
        main_card_data.append(HtmlData(data=self._decision_tree_raw))
        main_card_table = TableData()
        main_card_table.set_table_data(self.card1Table)
        main_card_table.set_table_type("normal")
        main_card_data.append(main_card_table)
        main_card.set_card_data(main_card_data)
        main_card.set_card_name("main_card")
        card2 = NormalCard()
        card2Data = NarrativesUtils.block_splitter(NarrativesUtils.get_template_output(self._base_dir,\
                                                    'decision_tree_card2.temp',data_dict),self._blockSplitter)
        card2ChartData = []
        for k,v in self._target_distribution.items():
            card2ChartData.append({"key":k,"value":v})
        card2ChartData = NormalChartData(data=card2ChartData)
        card2ChartJson = ChartJson()
        card2ChartJson.set_data(card2ChartData.get_data())
        card2ChartJson.set_chart_type("bar")
        card2Data.insert(1,C3ChartData(data=card2ChartJson))
        card2.set_card_data(card2Data)
        card2.set_card_name("card2")
        self.decisionTreeNode.add_a_card(main_card)
        self.decisionTreeNode.add_a_card(card2)
        self.subheader = NarrativesUtils.get_template_output(self._base_dir,\
                                        'decision_tree_summary.temp',data_dict)

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
