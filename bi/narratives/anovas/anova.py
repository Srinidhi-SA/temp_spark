import os
import jinja2
import re
from bi.common.utils import accepts
from bi.common.results.two_way_anova import OneWayAnovaResult
# from bi.stats import TuckeyHSD
from bi.narratives import utils as NarrativesUtils

class card:
    def __init__(self, heading):
        self.heading = heading
        self.charts = {}
        self.paragraphs = []
        self.bubble_data = []

    def add_chart(self, key, chart):
        self.charts[key]=chart

    def add_paragraph(self, para):
        self.paragraphs.append(para)

    def add_bubble_data(self, bubble_data):
        self.bubble_data.append(bubble_data)


class BubbleData:
    def __init__(self,value, text):
        self.value = value
        self.text = text

class chart:
    def __init__(self, data, labels,  heading = ''):
        self.heading = heading
        self.data = data
        self.labels = labels

    def add_data_c3(self, data_c3):
        self.data_c3 = data_c3

class paragraph:
    def __init__(self, header, content):
        self.header = header
        self.content = [content]

class OneWayAnovaNarratives:
    THRESHHOLD_TOTAL = 0.75
    ALPHA = 0.05

    #@accepts(object, (str, basestring), (str, basestring), OneWayAnovaResult)
    def __init__(self, measure_column, dimension_column, anova_result, trend_result):
        self._measure_column = measure_column
        self._measure_column_capitalized = '%s%s' % (measure_column[0].upper(), measure_column[1:])
        self._dimension_column = dimension_column
        self._dimension_column_capitalized = '%s%s' % (dimension_column[0].upper(), dimension_column[1:])
        self._one_way_anova_result = anova_result
        self._trend_result = trend_result
        # self.effect_size = anova_result.get_effect_size()
        self.card1 = ''
        self.card2 = ''
        self.card3 = ''
        self._base_dir = os.environ.get('MADVISOR_BI_HOME')+"/templates/anovas/"
        self._generate_narratives()

    def _generate_narratives(self):
        self._generate_card1()
        self._generate_card2()
        self._generate_card3()

    def _generate_title(self):
        self.title = 'Impact of %s on %s' % (self._dimension_column_capitalized, self._measure_column_capitalized)

    def _generate_card1(self):
        self.card1 = card('Impact of '+self._dimension_column_capitalized+' on '+self._measure_column_capitalized)
        dim_table = self._one_way_anova_result.get_dim_table()
        keys = dim_table['levels']
        totals = dim_table['total']
        means = dim_table['means']
        counts = dim_table['counts']

        group_by_total = {}
        group_by_mean = {}

        for k,t,m in zip(keys,totals,means):
            group_by_total[k] = t
            group_by_mean[k] = m

        chart1 = chart(data=group_by_total, labels = {self._dimension_column_capitalized:self._measure_column_capitalized})
        chart2 = chart(data=group_by_mean, labels = {self._dimension_column_capitalized:self._measure_column_capitalized})

        self.card1.add_chart('group_by_total',chart1)
        self.card1.add_chart('group_by_mean',chart2)

        top_group_by_total = keys[totals.index(max(totals))]
        sum_top_group_by_total = max(totals)
        avg_top_group_by_total = means[totals.index(max(totals))]
        bubble1 = BubbleData(NarrativesUtils.round_number(sum_top_group_by_total,1),
                            top_group_by_total + ' is the largest contributor to ' + self._measure_column)
        self.card1.add_bubble_data(bubble1)

        top_group_by_mean = keys[means.index(max(means))]
        sum_top_group_by_mean = totals[means.index(max(means))]
        avg_top_group_by_mean = max(means)
        bubble2 = BubbleData(NarrativesUtils.round_number(avg_top_group_by_mean,1),
                            top_group_by_mean + ' has the highest average ' + self._measure_column)
        self.card1.add_bubble_data(bubble2)

        groups_by_total = sorted(zip(totals,keys), reverse=True)
        sum_total = sum(totals)
        uniformly_distributed = True
        five_percent_total = 0.05*sum_total
        fifteen_percent_total = 0.15*sum_total
        sorted_total = sorted(totals, reverse=True)
        if len(groups_by_total)%2 == 0:
            fifty_percent_index = int(len(groups_by_total)/2)
            top_fifty_total = sum(sorted_total[:fifty_percent_index])
            bottom_fifty_total = sum(sorted_total[fifty_percent_index:])
            if top_fifty_total - bottom_fifty_total >= fifteen_percent_total:
                uniformly_distributed = False
        else:
            fifty_percent_index = int(len(groups_by_total)/2)+1
            top_fifty_total = sum(sorted_total[:fifty_percent_index])
            bottom_fifty_total = sum(sorted_total[fifty_percent_index-1:])
            if top_fifty_total - bottom_fifty_total >= fifteen_percent_total:
                uniformly_distributed = False
        top_groups = None
        top_groups_contribution = None
        if (not uniformly_distributed) and len(groups_by_total)>2:
            max_diff = 0
            diffs = [sorted_total[i]-sorted_total[i+1] for i in range(fifty_percent_index)]
            max_diff_index = diffs.index(max(diffs[1:]))
            top_groups = [k for t,k in groups_by_total[:max_diff_index+1]]
            top_groups_contribution = sum(sorted_total[:max_diff_index+1])*100/sum_total
            bottom_groups = []
            bottom_groups_contribution = 0
            for t,k in groups_by_total[::-1]:
                bottom_groups.append(k)
                bottom_groups_contribution = bottom_groups_contribution + t
                if bottom_groups_contribution >= five_percent_total:
                    break
        elif not uniformly_distributed:
            top_groups = [groups_by_total[0][1]]
            top_groups_contribution = groups_by_total[0][0]*100/sum_total
            bottom_groups = [groups_by_total[1][1]]
            bottom_groups_contribution = groups_by_total[1][0]*100/sum_total

        num_groups = len(keys)

        data_dict = {
            'uniformly_distributed' : uniformly_distributed,
            'top_groups' : top_groups,
            'num_top_groups' : len(top_groups),
            'top_groups_percent' : round(100.0 * top_groups_contribution / sum(totals),2),
            'dimension_name' : self._dimension_column,
            'plural_dimension_name' : NarrativesUtils.pluralize(self._dimension_column),
            'measure_name' : self._measure_column,

            'best_category_by_mean': top_group_by_mean,
            'best_category_by_mean_cont': round(100.0 * sum_top_group_by_mean / sum(totals), 2),
            'best_category_by_mean_avg': NarrativesUtils.round_number(avg_top_group_by_mean,2),

            'best_category_by_total': top_group_by_total,
            'best_category_by_total_cont': round(100.0 * sum_top_group_by_total / sum(totals), 2),
            'best_category_by_total_avg': NarrativesUtils.round_number(avg_top_group_by_total,2),
            'best_category_by_total_sum' : NarrativesUtils.round_number(sum_top_group_by_total,2),

            'bottom_groups': bottom_groups,
            'num_bottom_groups' : len(bottom_groups),
            'bottom_groups_percent': round(100.0 * bottom_groups_contribution / sum(totals),2),

            'num_groups' : num_groups
        }
        output = {'header' : 'Overview', 'content': []}
        output['content'].append(NarrativesUtils.get_template_output(self._base_dir,'anova_template_3.temp',data_dict))
        self.card1.add_paragraph(output)
        self.generate_top_dimension_narratives()

    def generate_top_dimension_narratives(self):
        top_dimension_stats = self._one_way_anova_result.contributions
        top_dimension = top_dimension_stats.top_dimension
        self._top_dimension = top_dimension
        significant_dimensions = top_dimension_stats.get_top_3_significant_dimensions()
        top1_contributors, top1_contribution = self.get_contributions_for_dimension(significant_dimensions, 0,top_dimension_stats)
        top2_contributors, top2_contribution = self.get_contributions_for_dimension(significant_dimensions, 1, top_dimension_stats)
        top3_contributors, top3_contribution = self.get_contributions_for_dimension(significant_dimensions, 2, top_dimension_stats)
        data_dict = {
                    'significant_dimensions' : significant_dimensions,
                    'num_significant_dimensions' : len(significant_dimensions),
                    'top1_contributors' : top1_contributors,
                    'top1_contribution' : top1_contribution,
                    'num_top1_contributors' : len(top1_contributors),
                    'top2_contributors' : top2_contributors,
                    'top2_contribution' : top2_contribution,
                    'num_top2_contributors' : len(top2_contributors),
                    'top3_contributors' : top3_contributors,
                    'top3_contribution' : top3_contribution,
                    'num_top3_contributors' : len(top3_contributors),
                    'target' : self._measure_column,
                    'dimension' : self._dimension_column,
                    'top_dimension' : top_dimension
        }
        output = {'header' : 'Key Factors influencing '+self._measure_column+' from '+top_dimension,
                  'content': []}
        output['content'].append(NarrativesUtils.get_template_output(self._base_dir,'anova_template_4.temp',data_dict))
        self.card1.add_paragraph(output)


    def get_contributions_for_dimension(self, significant_dimensions, n, top_dimension_stats):
        if len(significant_dimensions)>n:
            dimension = significant_dimensions[n]
            contributions = top_dimension_stats.get_contributions(dimension)
            contributions = [(v*100,k) for k,v in contributions.items()]
            contributions = sorted(contributions, reverse=True)
            diffs = [contributions[i][0]-contributions[i+1][0] for i in range(len(contributions)-1)]
            cutoff = diffs.index(max(diffs))
            contributions = contributions[:cutoff+1]
            total_contribution = sum([v for v,k in contributions])
            contributions = [(round(v,2),k) for v,k in contributions]
            return contributions, total_contribution
        return '',''

    def _generate_card2(self):
        self.card2 = card(self._top_dimension + "'s " + self._measure_column_capitalized + " Performance over Time")

    def get_category(self, x):
        print '#'*100
        print x['increase']
        print x['increase'][0]
        if x['increase'][0] >= self._increase_limit:
            if x['contribution'][0] >= self._increase_limit:
                return 'Leaders Club'
            else:
                return 'Playing Safe'
        else:
            if x['contribution'][0] >= self._contribution_limit:
                return 'Opportunity Bay'
            else:
                return 'Red Alert'

    def _generate_card3(self):
        self.card3 = card(self._dimension_column_capitalized + '-' + self._measure_column_capitalized + ' Performance Decision Matrix')
        self.card3.add_paragraph({'header': '',
            'content' : 'Based on the absolute '+ self._measure_column+' values and the overall growth rates, mAdvisor presents the decision matrix for '+self._measure_column+' for '+ self._dimension_column +' as displayed below.'})
        grouped_data_frame = self._trend_result.get_grouped_data(self._dimension_column)
        grouped_data_frame['increase'] = (grouped_data_frame['measure']['last'] - grouped_data_frame['measure']['first'])*100/grouped_data_frame['measure']['first']
        grouped_data_frame['contribution'] = grouped_data_frame['measure']['sum']*100/sum(grouped_data_frame['measure']['sum'])
        self._contribution_limit = grouped_data_frame['contribution'].median()
        self._increase_limit = max(0.0, grouped_data_frame['increase'].median())
        print grouped_data_frame
        print self._contribution_limit, self._increase_limit
        grouped_data_frame['category'] = grouped_data_frame.apply(self.get_category, axis=1)
        # grouped_data_frame['category'] = 'Red Alert'
        # grouped_data_frame['category'].ix[(grouped_data_frame['contribution']>=self._contribution_limit) & \
        #                 (grouped_data_frame['increase']>=self._increase_limit)] = 'Leaders Club'
        # grouped_data_frame['category'].ix[(grouped_data_frame['contribution']<self._contribution_limit) & \
        #                 (grouped_data_frame['increase']>=self._increase_limit)] = 'Playing Safe'
        # grouped_data_frame['category'].ix[(grouped_data_frame['contribution']>=self._contribution_limit) & \
        #                 (grouped_data_frame['increase']<self._increase_limit)] = 'Opportunity Bay'
        print grouped_data_frame
        print '*'*120
        data = {
                      'Share of '+self._measure_column : list(grouped_data_frame['contribution']),
                      self._measure_column_capitalized+' growth' : list(grouped_data_frame['increase']),
                      self._dimension_column : list(grouped_data_frame['dimension']),
                      'Category' : list(grouped_data_frame['category']),
        }
        data_c3 = [[self._measure_column_capitalized+' growth'] + list(grouped_data_frame['increase']),
                    ['Share of '+self._measure_column] + list(grouped_data_frame['contribution']),
                    [self._dimension_column] + list(grouped_data_frame['dimension']),
                    ['Category'] + list(grouped_data_frame['category'])]
        print data
        chart_data = chart(data=data, labels={})
        chart_data.add_data_c3(data_c3)
        self.card3.add_chart('decision_matrix', chart_data)
        leaders_club = list(grouped_data_frame['dimension'][grouped_data_frame['category']=='Leaders Club'])
        playing_safe = list(grouped_data_frame['dimension'][grouped_data_frame['category']=='Playing Safe'])
        opportunity_bay = list(grouped_data_frame['dimension'][grouped_data_frame['category']=='Opportunity Bay'])
        red_alert = list(grouped_data_frame['dimension'][grouped_data_frame['category']=='Red Alert'])
        data_dict = {
                    'leaders_club' : leaders_club,
                    'playing_safe' : playing_safe,
                    'opportunity_bay' : opportunity_bay,
                    'red_alert' : red_alert,
                    'num_leaders_club' : len(leaders_club),
                    'num_playing_safe' : len(playing_safe),
                    'num_opportunity_bay' : len(opportunity_bay),
                    'num_red_alert' : len(red_alert),
                    'target' : self._measure_column,
                    'dimension' : self._dimension_column
        }
        output = {'header' : '',
                  'content': []}
        output['content'].append(NarrativesUtils.get_template_output(self._base_dir,'anova_template_5.temp',data_dict))
        self.card3.add_paragraph(output)
