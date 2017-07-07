import os
import random

from bi.common.dataframe import DataFrameHelper
from bi.common.results import DecisionTreeResult
from bi.common.utils import accepts
from bi.narratives import utils as NarrativesUtils


class DecisionTreeRegNarrative:
    MAX_FRACTION_DIGITS = 2

    def _get_new_table(self):
        for keys in self.table.keys():
            self.new_table[keys]={}
            self.new_table[keys]['rules'] = self.table[keys]
            self.new_table[keys]['probability'] = [round(i,2) for i in self.success_percent[keys]]

    @accepts(object, (str, basestring), DecisionTreeResult,DataFrameHelper)
    def __init__(self, column_name, decision_tree_rules,df_helper):
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
        print '$'*300
        print self._target_distribution
        self._get_new_table()
        self._df_helper = df_helper
        self.subheader = None
        self.dropdownComment = None
        self.dropdownValues = None
        self._base_dir = os.environ.get('MADVISOR_BI_HOME')+"/templates/decisiontree/"
        self._generate_narratives()


    def _generate_narratives(self):
        self._generate_summary()

    def _generate_summary(self):
        rules = self._decision_rules_dict
        colname = self._colname
        data_dict = {"dimension_name":self._colname}
        data_dict["plural_colname"] = NarrativesUtils.pluralize(data_dict["dimension_name"])
        data_dict["significant_vars"] = []
        data_dict['significant_vars_high'] = self._important_vars['High']
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
        data_dict['rules_list_high'] = self.condensedTable['High']
        data_dict['rules_list_low'] = self.condensedTable['Low']
        data_dict['count_percent_high'] = NarrativesUtils.round_number(self._target_distribution['High']['count_percent'],2)
        data_dict['sum_percent_high'] =  NarrativesUtils.round_number(self._target_distribution['High']['sum_percent'],2)
        data_dict['sum_high'] =  NarrativesUtils.round_number(self._target_distribution['High']['sum'],2)
        data_dict['count_percent_low'] =  NarrativesUtils.round_number(self._target_distribution['Low']['count_percent'],2)
        data_dict['sum_percent_low'] =  NarrativesUtils.round_number(self._target_distribution['Low']['sum_percent'],2)

        self.card2_data = NarrativesUtils.paragraph_splitter(NarrativesUtils.get_template_output(self._base_dir,\
                                                    'decision_reg_card2.temp',data_dict))
        self.card2_chart = {'sum' : dict([(k,v['sum']) for k,v in self._target_distribution.items()]),
                            'mean': dict([(k,v['sum']*1.0/v['count']) for k,v in self._target_distribution.items()])}
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
                            '</b> of observations that have <i><u>' + temp_narrative + '</u></i> result in '+ \
                            target + ' '+ self._column_name + ' values.'
            elif r == 1:
                narrative = 'If <i><u>' + temp_narrative +'</u></i> it is <b>' + NarrativesUtils.round_number(success_percent)+ '%' + \
                            '</b> likely that the observations are ' + target + ' segment.'
            elif r == 2:
                narrative = 'When <i><u>' +  temp_narrative + '</u></i> the probability of ' + target + \
                            ' is <b>' + NarrativesUtils.round_number(success_percent)+ '%' + '</b>.'
            elif r == 3:
                narrative = 'If <i><u>' + temp_narrative +'</u></i> then there is <b>' + NarrativesUtils.round_number(success_percent)+ '%' + \
                            '</b> probability that the ' + self._column_name + ' observations would be ' + target + ' valued.'
            else:
                narrative = 'There is a very high chance(<b>' + NarrativesUtils.round_number(success_percent)+ '%' + \
                            '</b>) that ' +  self._column_name + ' would be relatively ' + target + ' when, <i><u>' + \
                            temp_narrative[:-1] + '</u></i>.'
            return narrative
