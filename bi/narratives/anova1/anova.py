import os
import jinja2
import re
import pattern.en
import re
from bi.common.utils import accepts
from bi.common.results.two_way_anova import OneWayAnovaResult

from bi.stats.anova.posthoctests import TuckeyHSD


from bi.narratives import utils as NarrativesUtils

class OneWayAnovaNarratives:
    THRESHHOLD_TOTAL = 0.75
    ALPHA = 0.05

    @accepts(object, (str, basestring), (str, basestring), OneWayAnovaResult)
    def __init__(self, measure_column, dimension_column, anova_result):
        self._measure_column = measure_column
        self._measure_column_capitalized = '%s%s' % (measure_column[0].upper(), measure_column[1:])
        self._dimension_column = dimension_column
        self._dimension_column_capitalized = '%s%s' % (dimension_column[0].upper(), dimension_column[1:])
        self._one_way_anova_result = anova_result
        self.effect_size = anova_result.get_effect_size()
        self.title = None
        self.analysis = None
        self.largest_volume = []
        self.largest_average = []

        # self._base_dir = os.path.dirname(os.path.realpath(__file__))+"/../../templates/anova/"
        self._base_dir = os.environ.get('MADVISOR_BI_HOME')+"/templates/anova/"
        self._generate_narratives()
        self.sub_heading = self.get_sub_heading()

    def get_sub_heading(self):
        # return re.split('\. ',self.analysis)[0]
        return None

    def _generate_narratives(self):
        self._generate_title()
        self._generate_analysis()

    def _generate_title(self):
        self.title = 'Impact of %s on %s' % (self._dimension_column_capitalized, self._measure_column_capitalized)

    def _generate_analysis(self):
        dim_table = self._one_way_anova_result.get_dim_table()
        self.group_by_total = {}
        self.group_by_mean = {}
        keys = dim_table['levels']
        totals = dim_table['total']
        means = dim_table['means']
        counts = dim_table['counts']
        for k,t,m in zip(keys,totals,means):
            self.group_by_total[k] = t
            self.group_by_mean[k] = m
        top_group_by_total = keys[totals.index(max(totals))]
        sum_top_group_by_total = max(totals)
        avg_top_group_by_total = means[totals.index(max(totals))]
        self.largest_volume.append(NarrativesUtils.round_number(sum_top_group_by_total,1))
        self.largest_volume.append(top_group_by_total + ' is the largest contributor to ' + self._measure_column)
        top_group_by_mean = keys[means.index(max(means))]
        sum_top_group_by_mean = totals[means.index(max(means))]
        avg_top_group_by_mean = max(means)
        self.largest_average.append(NarrativesUtils.round_number(avg_top_group_by_mean,1))
        self.largest_average.append(top_group_by_mean + ' has the highest average ' + self._measure_column)
        bottom_group_total = min(totals)
        bottom_group_mean = means[totals.index(min(totals))]
        bottom_group_name = keys[totals.index(min(totals))]
        num_groups = len(keys)

        cum_sum = 0
        cat_75_list = []
        groups_by_total = sorted(zip(totals,keys,counts), reverse=True)
        for t,l,c in groups_by_total[:-1]:
            cat_75_list.append(l)
            cum_sum += t
            if len(cat_75_list) == len(keys) - 1 or (float(cum_sum) / sum(totals)) >= 0.75:
                break
        '''suggestion : On the other hand, the top 3 groups by average, accounts for 26% of the total sales,
                        inspite of contributing only 10% of the total observations (--based on TukeyHSD--)'''
        mean_diff_percentage = 0
        msse = self._one_way_anova_result.get_mean_sum_of_squares_error()

        groups_by_mean = sorted(zip(means,keys,counts), reverse=True)
        other_group_names_list = ''
        other_group_names = []
        best_mean,best_level_by_mean,best_level_by_mean_count = groups_by_mean[0]
        num_records = self._one_way_anova_result.get_df_total() + 1
        for i in range(1,len(groups_by_mean)):
            m,k,c = groups_by_mean[i]
            if not TuckeyHSD.studentized_test(msse,num_records, len(keys), best_mean, m, best_level_by_mean_count,c):
                continue
            if m==0:
                mean_diff_percentage = 0
            else:
                mean_diff_percentage = (best_mean-m)*100.00/m
            other_group_names = [key for mean,key,count in groups_by_mean[i:]]
            if len(other_group_names) > 1:
                other_group_names_list = ", and ".join([", ".join(other_group_names[:-1]), other_group_names[-1]])
            else:
                other_group_names_list = other_group_names[0]

        if top_group_by_total == best_level_by_mean:
            cat_bool = 1
        else:
            cat_bool = 0

        data_dict = {
            'cat_bool':cat_bool,
            'cat_75_list' : cat_75_list,
            'n_c_d_75': len(cat_75_list),
            'percent_contr' : NarrativesUtils.round_number(100.0 * cum_sum / sum(totals),2),
            'dimension_name' : self._dimension_column,
            'plural_dimension_name' : pattern.en.pluralize(self._dimension_column),
            'measure_name' : self._measure_column,

            'best_category_by_mean': top_group_by_mean,
            'best_category_by_mean_cont': round(100.0 * sum_top_group_by_mean / sum(totals), 2),
            'best_category_by_mean_avg': NarrativesUtils.round_number(avg_top_group_by_mean,2),

            'best_category_by_total': top_group_by_total,
            'best_category_by_total_cont': round(100.0 * sum_top_group_by_total / sum(totals), 2),
            'best_category_by_total_avg': NarrativesUtils.round_number(avg_top_group_by_total,2),

            'worst_category_name': bottom_group_name,
            'worst_category_percent': round(100.0 * bottom_group_total / sum(totals),2),
            'worst_category_average': NarrativesUtils.round_number(bottom_group_mean,2),

            'measure_name': self._measure_column,
            'top_categories': top_group_by_mean,
            'diff_percent': round(mean_diff_percentage,2),
            'other_categories': other_group_names_list
        }

        templateLoader = jinja2.FileSystemLoader( searchpath=self._base_dir)
        templateEnv = jinja2.Environment( loader=templateLoader )
        template = templateEnv.get_template('anova_template_3.temp')
        output = template.render(data_dict).replace("\n", "")
        output = re.sub(' +',' ',output)
        output = re.sub(' ,',',',output)
        output = re.sub(' \.','.',output)
        output = re.sub('\( ','(',output)
        self.analysis = output
