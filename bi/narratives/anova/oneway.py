import os
import re

import jinja2

from bi.common.results.anova import AnovaResult
from bi.common.utils import accepts
from bi.narratives import utils as NarrativesUtils
from bi.stats.posthoctests import TuckeyHSD


class OneWayAnovaNarratives:
    THRESHHOLD_TOTAL = 0.75
    ALPHA = 0.05

    @accepts(object, (str, basestring), (str, basestring), AnovaResult)
    def __init__(self, measure_column, dimension_column, anova_result):
        self._measure_column = measure_column
        self._measure_column_capitalized = '%s%s' % (measure_column[0].upper(), measure_column[1:])
        self._dimension_column = dimension_column
        self._dimension_column_capitalized = '%s%s' % (dimension_column[0].upper(), dimension_column[1:])
        self._anova_result = anova_result
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
        groups_by_total = self._anova_result.get_anova_column_value_groups_by_total()
        groups_by_mean = self._anova_result.get_anova_column_value_groups_by_mean()
        total = sum([grp_stat.get_descr_stats().get_total() for grp_stat in groups_by_total])
        self.group_by_total = {}
        self.group_by_mean = {}
        for i in groups_by_total:
            key = i.get_column_values()[0]
            sum1 = i.get_descr_stats().get_total()
            mean1 = i.get_descr_stats().get_mean()
            self.group_by_total[key]=sum1
            self.group_by_mean[key]=mean1
        top_group_by_total = groups_by_total[0].get_column_values()[0]
        sum_top_group_by_total = groups_by_total[0].get_descr_stats().get_total()
        self.largest_volume.append(NarrativesUtils.round_number(sum_top_group_by_total,1))
        self.largest_volume.append(top_group_by_total + ' is the largest contributor to ' + self._measure_column)
        avg_top_group_by_total = groups_by_total[0].get_descr_stats().get_mean()
        top_group_by_mean = groups_by_mean[0].get_column_values()[0]
        sum_top_group_by_mean = groups_by_mean[0].get_descr_stats().get_total()
        avg_top_group_by_mean = groups_by_mean[0].get_descr_stats().get_mean()
        self.largest_average.append(NarrativesUtils.round_number(avg_top_group_by_mean,1))
        self.largest_average.append(top_group_by_mean + ' has the highest average ' + self._measure_column)
        bottom_group_total = groups_by_total[-1].get_descr_stats().get_total()
        bottom_group_mean = groups_by_total[-1].get_descr_stats().get_mean()
        bottom_group_name = groups_by_total[-1].get_column_values()[0]
        num_groups = len(groups_by_total)
        top_n_groups = []
        # significant_dimensions = []
        cum_sum = 0
        cat_75_list = []
        cat_75_avg_list = []
        result_obj = self._anova_result
        for grp_stat in groups_by_total:
            cat_total = grp_stat.get_descr_stats().get_total()
            cat_75_list.append(grp_stat.get_column_values()[0])
            cat_75_avg_list.append(grp_stat.get_descr_stats().get_mean())
            cum_sum += grp_stat.get_descr_stats().get_total()
            if len(top_n_groups) == num_groups - 1 or (float(cum_sum) / total) >= 0.75:
                break
        mean_diff_percentage = 0
        other_group_names_list = []
        for idx in range(1, len(groups_by_mean)):
            other_group = groups_by_mean[idx]
            msse = self._anova_result.get_mean_sum_of_squares_error()
            num_records = self._anova_result.get_total_number_of_records()
            group1_mean = groups_by_total[0].get_descr_stats().get_mean()
            group2_mean = other_group.get_descr_stats().get_mean()
            group_size = min(groups_by_mean[0].get_descr_stats().get_n(), other_group.get_descr_stats().get_n())
            if not TuckeyHSD.test(msse, num_records, len(groups_by_mean), group1_mean, group2_mean, group_size):
                continue
            other_group_mean = group2_mean
            if other_group_mean == 0:
                mean_diff_percentage = 0
            else:
                mean_diff_percentage = 100.0 * (avg_top_group_by_mean - other_group_mean) / other_group_mean
            other_group_names = [grp.get_column_values()[0] for grp in groups_by_mean[idx:]]
            other_group_names_list = ""
            if len(other_group_names) > 1:
                other_group_names_list = ", and ".join([", ".join(other_group_names[:-1]), other_group_names[-1]])
            else:
                other_group_names_list = other_group_names[0]
        if top_group_by_total == top_group_by_mean:
            cat_bool = 1
        else:
            cat_bool = 0

        data_dict = {
            'cat_bool':cat_bool,
            'cat_75_list' : cat_75_list,
            'cat_75_avg_list' : cat_75_avg_list,
            'n_c_d_75': len(cat_75_list),
            'percent_contr' : NarrativesUtils.round_number(100.0 * cum_sum / total,2),
            'dimension_name' : self._dimension_column,
            'plural_dimension_name' : NarrativesUtils.pluralize(self._dimension_column),
            'measure_name' : self._measure_column,

            'best_category_by_mean': top_group_by_mean,
            'best_category_by_mean_cont': round(100.0 * sum_top_group_by_mean / total, 2),
            'best_category_by_mean_avg': NarrativesUtils.round_number(avg_top_group_by_mean,2),

            'best_category_by_total': top_group_by_total,
            'best_category_by_total_cont': round(100.0 * sum_top_group_by_total / total, 2),
            'best_category_by_total_avg': NarrativesUtils.round_number(avg_top_group_by_total,2),

            'worst_category_name': bottom_group_name,
            'worst_category_percent': round(100.0 * bottom_group_total / total,2),
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
