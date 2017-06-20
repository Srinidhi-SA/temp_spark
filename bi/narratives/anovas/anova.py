import os
import jinja2
import math
import numpy as np
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
    def __init__(self, data, labels='',  heading = ''):
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
        if self._trend_result != '':
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
        elif uniformly_distributed:
            top_groups = []
            top_groups_contribution = 0
            bottom_groups = []
            bottom_groups_contribution = 0

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
        subset_data_frame = self._trend_result.get_subset_data(self._dimension_column)
        agg_data_frame = self._trend_result.get_data_frame()
        total_measure = 'Total '+ self._measure_column_capitalized
        if len(agg_data_frame.columns)==2:
            agg_data_frame.columns = ['Date',total_measure]
        subset_measure = self._trend_result.get_top_dimension(self._dimension_column) + ' ' + self._measure_column_capitalized
        subset_data_frame.columns = ['Date', subset_measure]
        outer_join = agg_data_frame.merge(subset_data_frame, how='left', on = 'Date')
        inner_join = agg_data_frame.merge(subset_data_frame, how='inner', on = 'Date')
        correlation = inner_join[[total_measure,subset_measure]].corr()[total_measure][subset_measure]
        data = {
                'Time Period' : list(inner_join['Date']),
                total_measure : list(inner_join[total_measure]),
                subset_measure : list(inner_join[subset_measure])
        }
        data_c3 = [['Time Period'] + list(inner_join['Date']),
                [total_measure] + list(inner_join[total_measure]),
                [subset_measure] + list(inner_join[subset_measure])]
        chart1 = chart(data = data)
        chart1.add_data_c3(data_c3)
        self.card2.add_chart('trend_chart',chart1)

        overall_increase_percent = (agg_data_frame[total_measure].iloc[-1]*100/agg_data_frame[total_measure].iloc[0]) - 100
        subset_increase_percent = (subset_data_frame[subset_measure].iloc[-1]*100/subset_data_frame[subset_measure].iloc[0]) - 100

        overall_peak_index = agg_data_frame[total_measure].argmax()
        overall_peak_value = agg_data_frame[total_measure].ix[overall_peak_index]
        overall_peak_date = agg_data_frame['Date'].ix[overall_peak_index]

        subset_peak_index = subset_data_frame[subset_measure].argmax()
        subset_peak_value = subset_data_frame[subset_measure].ix[subset_peak_index]
        subset_peak_date = subset_data_frame['Date'].ix[subset_peak_index]

        agg_data_frame['prev'] = agg_data_frame[total_measure].shift(1)
        subset_data_frame['prev'] = subset_data_frame[subset_measure].shift(1)
        if math.isnan(agg_data_frame['prev'].ix[overall_peak_index]):
            overall_peak_increase = 0
        else:
            overall_peak_increase = (subset_data_frame[subset_measure].ix[subset_peak_index]/subset_data_frame['prev'].ix[subset_peak_index])*100 - 100
        if math.isnan(subset_data_frame['prev'].ix[subset_peak_index]):
            subset_peak_increase = 0
        else:
            subset_peak_increase = (subset_data_frame[subset_measure].ix[subset_peak_index]/subset_data_frame['prev'].ix[subset_peak_index])*100 - 100

        agg_data_frame['avg_diff'] = agg_data_frame[total_measure] - agg_data_frame[total_measure].mean()
        subset_data_frame['avg_diff'] = subset_data_frame[subset_measure] - subset_data_frame[subset_measure].mean()

        agg_data_frame = self.streaks(agg_data_frame,'avg_diff')
        subset_data_frame = self.streaks(subset_data_frame, 'avg_diff')

        overall_longest_streak_end_index = agg_data_frame['u_streak'].argmax()
        overall_longest_streak_contribution = agg_data_frame[total_measure].ix[overall_longest_streak_end_index]
        overall_streak_length = int(agg_data_frame['u_streak'].ix[overall_longest_streak_end_index])
        for i in range(1,int(overall_streak_length)):
            overall_longest_streak_contribution = agg_data_frame[total_measure].shift(i).ix[overall_longest_streak_end_index]
        overall_longest_streak_contribution = overall_longest_streak_contribution*100/agg_data_frame[total_measure].sum()
        overall_longest_streak_end_date = agg_data_frame['Date'].ix[overall_longest_streak_end_index]
        overall_longest_streak_start_date = agg_data_frame['Date'].shift(overall_streak_length-1).ix[overall_longest_streak_end_index]

        subset_longest_streak_end_index = subset_data_frame['u_streak'].argmax()
        subset_longest_streak_contribution = subset_data_frame[subset_measure].ix[subset_longest_streak_end_index]
        subset_streak_length = int(subset_data_frame['u_streak'].ix[subset_longest_streak_end_index])
        for i in range(1,int(subset_streak_length)):
            subset_longest_streak_contribution = subset_data_frame[subset_measure].shift(i).ix[subset_longest_streak_end_index]
        subset_longest_streak_contribution = subset_longest_streak_contribution*100/subset_data_frame[subset_measure].sum()
        subset_longest_streak_end_date = subset_data_frame['Date'].ix[subset_longest_streak_end_index]
        subset_longest_streak_start_date = subset_data_frame['Date'].shift(subset_streak_length-1).ix[subset_longest_streak_end_index]

        data_dict = {
                    'correlation' : correlation,
                    'overall_increase_percent' : round(overall_increase_percent,2),
                    'subset_increase_percent' : round(subset_increase_percent,2),
                    'overall_peak_value' : overall_peak_value,
                    'overall_peak_date' : overall_peak_date,
                    'overall_peak_increase' : round(overall_peak_increase,2),
                    'overall_streak_length' : overall_streak_length,
                    'overall_streak_start_date' : overall_longest_streak_start_date,
                    'overall_streak_end_date' : overall_longest_streak_end_date,
                    'overall_streak_contribution' : round(overall_longest_streak_contribution,2),
                    'subset_peak_value' : subset_peak_value,
                    'subset_peak_date' : subset_peak_date,
                    'subset_peak_increase' : round(subset_peak_increase,2),
                    'subset_streak_length' : subset_streak_length,
                    'subset_streak_start_date' : subset_longest_streak_start_date,
                    'subset_streak_end_date' : subset_longest_streak_end_date,
                    'subset_streak_contribution' : round(subset_longest_streak_contribution,2),
                    'target' : self._measure_column,
                    'top_dimension' : self._trend_result.get_top_dimension(self._dimension_column),
                    'dimension' : self._dimension_column,
        }
        output = {}
        output['header'] = ''
        output['content'] = []
        output['content'].append(NarrativesUtils.get_template_output(self._base_dir,'anova_template_6.temp',data_dict))
        self.card2.add_paragraph(output)
        self.generate_trending_comments()

    def generate_trending_comments(self):
        grouped_data_frame = self._trend_result.get_grouped_data(self._dimension_column)
        grouped_data_frame['increase'] = (grouped_data_frame['measure']['last'] - grouped_data_frame['measure']['first'])*100/grouped_data_frame['measure']['first']
        positive_growth_dimensions = grouped_data_frame['dimension'].ix[grouped_data_frame['increase']>3]
        negative_growth_dimensions = grouped_data_frame['dimension'].ix[grouped_data_frame['increase']<-2]
        stable_growth_dimensions = grouped_data_frame['dimension'].ix[(grouped_data_frame['increase']>=-2) & (grouped_data_frame['increase']<=3)]
        positive_growth_values = grouped_data_frame['increase'].ix[grouped_data_frame['increase']>3]
        negative_growth_values = grouped_data_frame['increase'].ix[grouped_data_frame['increase']<-2]
        # stable_growth_values = grouped_data_frame['increase'].ix[(grouped_data_frame['increase']>=-2) & (grouped_data_frame['increase']<=3)]

        positive_growth_dimensions = [i for j,i in sorted(zip(positive_growth_values,positive_growth_dimensions), reverse=True)]
        negative_growth_dimensions = [i for j,i in sorted(zip(negative_growth_values,negative_growth_dimensions))]
        positive_growth_values = sorted(positive_growth_values, reverse=True)
        negative_growth_values = sorted(negative_growth_values)

        overall_growth_rate = self._trend_result.get_overall_growth_percent()

        data_dict = {
                    'positive_growth_dimensions' : positive_growth_dimensions,
                    'negative_growth_dimensions' : negative_growth_dimensions,
                    'stable_growth_dimensions' : stable_growth_dimensions,
                    'positive_growth_values' : positive_growth_values,
                    'negative_growth_values' : negative_growth_values,
                    'num_positive_growth_dimensions' : len(positive_growth_dimensions),
                    'num_negative_growth_dimensions' : len(negative_growth_dimensions),
                    'num_stable_growth_dimensions' : len(stable_growth_dimensions),
                    'target' : self._measure_column,
                    'dimension' : self._dimension_column,
                    'overall_growth_rate' : overall_growth_rate,
        }
        output = {'header' : '',
                  'content': []}
        output['content'].append(NarrativesUtils.get_template_output(self._base_dir,'anova_template_7.temp',data_dict))
        self.card2.add_paragraph(output)

    def streaks(self, df, col):
        sign = np.sign(df[col])
        s = sign.groupby((sign!=sign.shift()).cumsum()).cumsum()
        return df.assign(u_streak=s.where(s>0, 0.0), d_streak=s.where(s<0, 0.0).abs())

    def get_category(self, x):
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
        grouped_data_frame['category'] = grouped_data_frame.apply(self.get_category, axis=1)
        data = {
                      'Share of '+self._measure_column : list(grouped_data_frame['contribution']),
                      self._measure_column_capitalized+' growth' : list(grouped_data_frame['increase']),
                      self._dimension_column : list(grouped_data_frame['dimension']),
                      'Category' : list(grouped_data_frame['category']),
        }
        # data_c3 = [[self._measure_column_capitalized+' growth'] + list(grouped_data_frame['increase']),
        #             ['Share of '+self._measure_column] + list(grouped_data_frame['contribution']),
        #             [self._dimension_column] + list(grouped_data_frame['dimension']),
        #             ['Category'] + list(grouped_data_frame['category'])]
        data_c3 = [['Growth'] + list(grouped_data_frame['increase']),
                    ['Share'] + list(grouped_data_frame['contribution']),
                    [self._dimension_column] + list(grouped_data_frame['dimension']),
                    ['Category'] + list(grouped_data_frame['category'])]
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
