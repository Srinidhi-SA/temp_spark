import operator
import os

import numpy

from bi.narratives import utils as NarrativesUtils


class ChiSquareAnalysis:
    def __init__ (self, chisquare_result, target_dimension, analysed_dimension, significant_variables, num_analysed_variables, appid=None):
        self._chisquare_result = chisquare_result
        self._target_dimension = target_dimension
        self._analysed_dimension = analysed_dimension
        self._significant_variables =  significant_variables
        self._num_analysed_variables = num_analysed_variables
        self.table = []
        self.effect_size = chisquare_result.get_effect_size()
        self.analysis = {}
        self.appid = appid
        # self._base_dir = os.path.dirname(os.path.realpath(__file__))+"/../../templates/chisquare/"
        self._base_dir = os.environ.get('MADVISOR_BI_HOME')+"/templates/chisquare/"
        if self.appid != None:
            if self.appid == "1":
                self._base_dir += "appid1/"
            elif self.appid == "2":
                self._base_dir += "appid2/"
        self._generate_narratives()

    def _get_bin_names (self,splits):
        bin_names = []
        start = splits[0]
        for i in splits[1:]:
            bin_names.append(str(round(start,2)) + ' to ' + str(round(i,2)))
            start = i
        return bin_names

    def _generate_narratives(self):
        chisquare_result = self._chisquare_result
        target_dimension = self._target_dimension
        analysed_dimension = self._analysed_dimension
        significant_variables = self._significant_variables
        num_analysed_variables = self._num_analysed_variables
        #self.narratives[target_dimension][analysed_dimension]['table'] = []
        splits = chisquare_result.get_splits()
        chisquare_result_percentage_table = chisquare_result.get_rounded_percentage_table()
        chisquare_result_contingency_table = chisquare_result.get_contingency_table()
        chisquare_result_percentage_table_by_target = chisquare_result.get_rounded_percentage_table_by_target()

        if splits:
            new_column_2_name = self._get_bin_names(splits)
            # new_column_2_name = NarrativesUtils.get_bin_names(splits)
            chisquare_result_percentage_table.column_two_values = [new_column_2_name[int(float(i))] for i in chisquare_result_percentage_table.column_two_values]
            chisquare_result_contingency_table.column_two_values = [new_column_2_name[int(float(i))] for i in chisquare_result_contingency_table.column_two_values]
            chisquare_result_percentage_table_by_target.column_two_values = [new_column_2_name[int(float(i))] for i in chisquare_result_percentage_table_by_target.column_two_values]
        cumulative_percent = {}

        num_categories = len(chisquare_result_percentage_table.column_two_values)
        chisquare_result_percentage_table.table
        for i in range(0, num_categories):
            column_two_value = chisquare_result_percentage_table.column_two_values[i]
            cumulative_percent[column_two_value] = sum(row_data[i] for row_data in chisquare_result_percentage_table.table)

        cumulative_percent = sorted(cumulative_percent.items(),key=operator.itemgetter(1),reverse=True)

        half_observation_categories = []
        half_observation_percent = 0
        for c,p in cumulative_percent:
            half_observation_percent = half_observation_percent + p
            half_observation_categories.append(c)
            if (half_observation_percent >= 50):
                break

        lowest_contributor = cumulative_percent[-1][0]
        lowest_contributor_percent = cumulative_percent[-1][1]
        #to_exclude = len(chisquare_result_percentage_table[cumulative_percent[0][0]])-1
        to_exclude = len(chisquare_result_percentage_table.column_one_values)
        maximum_percent = 0
        maximum_category = []
        minimum_percent = 100
        minimum_category = []
        maximum_observation = 0
        minimum_observation = 0
        category_list = {}
        observations_by_target_categories = {}
        maximum_std = 0
        maximum_std_category = []
        minimum_std = 1000000000
        minimum_std_category = []

        category_list = chisquare_result_percentage_table.column_one_values

        #rows = [analysed_dimension+'/'+target_dimension] + category_list + ['Distribution by '+analysed_dimension]
        #self.table.append(rows)

        for i in chisquare_result_percentage_table.column_two_values:
            #rows = [i]
            for j in chisquare_result_percentage_table.column_one_values:
                if not observations_by_target_categories.has_key(j):
                    observations_by_target_categories[j] = {}
                else:
                    #rows.append(str(round(chisquare_result_percentage_table.get_value(j, i),2)))
                    observations_by_target_categories[j][i] =chisquare_result_percentage_table.get_value(j, i)
                    if (chisquare_result_percentage_table.get_value(j, i) > maximum_percent):
                        maximum_category = [i,j]
                        maximum_percent = chisquare_result_percentage_table.get_value(j, i)
                        maximum_observation = chisquare_result_contingency_table.get_value(j, i)
                    elif (chisquare_result_percentage_table.get_value(j, i) < minimum_percent):
                        minimum_category = [i,j]
                        minimum_percent = chisquare_result_percentage_table.get_value(j, i)
                        minimum_observation = chisquare_result_contingency_table.get_value(j, i)

        self.table = chisquare_result_percentage_table_by_target
        # self.table = chisquare_result_percentage_table
        for i in observations_by_target_categories.keys():
            if (maximum_std < numpy.std(observations_by_target_categories[i].values())):
                maximum_std = numpy.std(observations_by_target_categories[i].values())
                temp_max = 0
                for j in observations_by_target_categories[i].keys():
                    if temp_max < observations_by_target_categories[i][j]:
                        temp_max = observations_by_target_categories[i][j]

                        maximum_std_category = [i, j, temp_max*100/sum(observations_by_target_categories[i].values())]
            elif (minimum_std > numpy.std(observations_by_target_categories[i].values())):
                minimum_std = numpy.std(observations_by_target_categories[i].values())
                minimum_std_category = [i]

        data_dict = {
                      'num_variables' : num_analysed_variables,
                      'num_significant_variables' : len(significant_variables),
                      'significant_variables' : significant_variables,
                      'target_dimension' : target_dimension,
                      'fifty_percent_categories' : half_observation_categories,
                      'fifty_percent_contribution' : round(half_observation_percent,2),
                      'lowest_contributor' : lowest_contributor,
                      'lowest_contributor_percent' : round(lowest_contributor_percent,2),
                      'maximum_percent' : round(maximum_percent,2),
                      'maximum_category' : maximum_category,
                      'maximum_observation' : maximum_observation,
                      'minimum_percent' : round(minimum_percent,2),
                      'minimum_category' : minimum_category,
                      'num_categories' : num_categories,
                      'analysed_dimension' : analysed_dimension,
                      'max_var' : maximum_std_category,
                      'min_var' : minimum_std_category
        }
        # print "*" * 100
        # print json.dumps(data_dict,indent=2)
        # print "*" * 100
        analysis1 = NarrativesUtils.get_template_output(self._base_dir,'chisquare_template3.temp',data_dict)
        analysis2 = NarrativesUtils.get_template_output(self._base_dir,'chisquare_template4.temp',data_dict)
        title1 = 'Concentration of ' + analysed_dimension
        if analysis2 != '':
            title2 = 'Relationship between '+analysed_dimension+' and '+ target_dimension
        else:
            title2 = ''

        self.analysis = {'title1':title1,
                        'analysis1':analysis1,
                        'title2':title2,
                        'analysis2':analysis2}
        # self.sub_heading = re.split(', whereas',analysis1)[0]
        self.sub_heading = 'Relationship between '+analysed_dimension+' and '+ target_dimension
