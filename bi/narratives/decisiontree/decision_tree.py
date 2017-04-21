import os
import jinja2
import re
import pattern.en
import numpy as np
from bi.common.utils import accepts

from bi.narratives import utils as NarrativesUtils
from bi.common.results import DecisionTreeResult
from bi.common.dataframe import DataFrameHelper
from bi.common.datafilterer import DataFrameFilterer

class DecisionTreeNarrative:
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
        self._get_new_table()
        self._df_helper = df_helper
        self.subheader = None
        #self.table = {}
        self.dropdownComment = None
        self.dropdownValues = None
        # self._base_dir = os.path.dirname(os.path.realpath(__file__))+"/../../templates/decisiontree/"
        self._base_dir = os.environ.get('MADVISOR_BI_HOME')+"/templates/decisiontree/"
        self._generate_narratives()


    def _generate_narratives(self):
        self._generate_summary()

    def _generate_summary(self):
        rules = self._decision_rules_dict
        colname = self._colname
        data_dict = {"dimension_name":self._colname}
        data_dict["plural_colname"] = pattern.en.pluralize(data_dict["dimension_name"])
        data_dict["significant_vars"] = []

        #all_rules = NarrativesUtils.flatten_rules(rules['children'], current_rule_list=None, all_rules=None)
        #rules_dict = NarrativesUtils.generate_leaf_rule_dict(all_rules,separator = ",")
        rules_dict = self.table
        self.condensedTable={}
        #self.succesful_predictions={}
        #self.total_predictions={}
        #self.success_percent= {}
        for target in rules_dict.keys():
            self.condensedTable[target]=[]
            #self.succesful_predictions[target]=[]
            #self.total_predictions[target]=[]
            #self.success_percent[target] = []
            for rule in rules_dict[target]:
                rules1 = self._generate_rules(target,rule)
                #if rules1[2]>0:
                self.condensedTable[target].append(rules1)
                #self.succesful_predictions[target].append(rules1[1])
                #self.total_predictions[target].append(rules1[2])
                #self.success_percent[target].append(rules1[3])

        self.dropdownValues = rules_dict.keys()
        templateLoader = jinja2.FileSystemLoader( searchpath=self._base_dir)
        templateEnv = jinja2.Environment( loader=templateLoader )
        template = templateEnv.get_template('decision_rule_summary.temp')
        output = template.render(data_dict).replace("\n", "")
        output = re.sub(' +',' ',output)
        output = re.sub(' ,',',',output)
        output = re.sub(' \.','.',output)

        template = templateEnv.get_template('decision_tree_summary.temp')
        output1 = template.render(data_dict).replace("\n", "")
        output1 = re.sub(' +',' ',output1)
        output1 = re.sub(' ,',',',output1)
        output1 = re.sub(' \.','.',output1)
        self.dropdownComment = output
        self.subheader = output1

    def _generate_rules(self,target,rules):
        colname = self._colname
        key_dimensions = {}
        key_measures = {}
        rules_list = re.split(r',\s*(?![^()]*\))',rules)
        for rx in rules_list:
            if ' <= ' in rx:
                var,limit = re.split(' <= ',rx)
                if not key_measures.has_key(var):
                    key_measures[var] ={}
                key_measures[var]['upper_limit'] = limit
            elif ' > ' in rx:
                var,limit = re.split(' > ',rx)
                if not key_measures.has_key(var):
                    key_measures[var] = {}
                key_measures[var]['lower_limit'] = limit
            elif ' not in ' in rx:
                var,levels = re.split(' not in ',rx)
                if not key_dimensions.has_key(var):
                    key_dimensions[var]={}
                key_dimensions[var]['not_in'] = levels
            elif ' in ' in rx:
                var,levels = re.split(' in ',rx)
                if not key_dimensions.has_key(var):
                    key_dimensions[var]={}
                key_dimensions[var]['in'] = levels
        temp_narrative = 'If '
        #cols_list = []
        #cols_list_temp = key_measures.keys() + key_dimensions.keys() + [colname]
        #for col in self._df_helper.get_columns():
        #    if col.strip() in cols_list_temp:
        #        cols_list.append(col)

        #df = self._df_helper.get_DataFrame(cols_list)
        #print df.take(10)
        #DFF = DataFrameFilterer(df)
        for var in key_measures.keys():
            if key_measures[var].has_key('upper_limit') and key_measures[var].has_key('lower_limit'):
                temp_narrative = temp_narrative + 'the value of ' + var + ' falls between ' + key_measures[var]['lower_limit'] + ' and ' + key_measures[var]['upper_limit']+', '
                #DFF.values_between(var,key_measures[var]['lower_limit'], key_measures[var]['upper_limit'])
            elif key_measures[var].has_key('upper_limit'):
                temp_narrative = temp_narrative + 'the value of ' + var + ' is less than or equal to ' + key_measures[var]['upper_limit']+', '
                #DFF.values_below(var,key_measures[var]['upper_limit'])
            elif key_measures[var].has_key('lower_limit'):
                temp_narrative = temp_narrative + 'the value of ' + var + ' is greater than ' + key_measures[var]['lower_limit']+', '
                #DFF.values_above(var,key_measures[var]['lower_limit'])
        for var in key_dimensions.keys():
            if key_dimensions[var].has_key('in'):
                temp_narrative = temp_narrative + 'the ' + var + ' falls among ' + key_dimensions[var]['in'] + ', '
                #DFF.values_in(var,key_dimensions[var]['in'])
            elif key_dimensions[var].has_key('not_in'):
                temp_narrative = temp_narrative + 'the ' + var + ' does not fall in ' + key_dimensions[var]['not_in'] + ', '
                #DFF.values_not_in(var,key_dimensions[var]['not_in'])

        if temp_narrative == 'If ':
            temp_narrative = ""
        else:
            temp_narrative = temp_narrative + 'then the ' + colname + ' is most likely to fall under ' + target
            #print DFF.get_aggregated_result(colname,target)
            #success = 0
            #total = 0
            #for rows in DFF.get_aggregated_result(colname,target):
            #    if(rows[0]==target):
            #        success = rows[1]
            #    total = total + rows[1]
            #if total>0:
            #    return [temp_narrative, success, total, round(success*100.0/total, 2)]
            #else:
            #    return [temp_narrative, success, total, 0.0]
            return temp_narrative
