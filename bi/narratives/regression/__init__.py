import os
import re
import json
import pandas as pd
from pyspark.sql import functions as FN
from pyspark.sql.functions import sum

from bi.algorithms import LinearRegression
from linear_regression import LinearRegressionNarrative
from bi.narratives import utils as NarrativesUtils
from bi.narratives.trend import TimeSeriesNarrative



class RegressionNarrative:
    def __init__(self, df_helper, df_context, result_setter, spark, df_regression_result, correlations):
        self._result_setter = result_setter
        self._df_regression_result = df_regression_result
        self._correlations = correlations
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context

        self._result_setter.set_trend_section_name("regression")
        self._date_columns = df_context.get_date_column_suggestions()
        # self._dateFormatConversionDict = NarrativesUtils.date_formats_mapping_dict()
        # if self._date_columns != None:
        #     self._primary_date = self._date_columns[0]
        #     self.get_date_conversion_formats(df_context)
        # else:
        #     self._primary_date = None

        self._spark = spark
        self.measures = []
        self.result_column = self._dataframe_helper.resultcolumn

        self.all_coefficients = self._df_regression_result.get_all_coeff()
        all_coeff = [(x,self.all_coefficients[x]) for x in self.all_coefficients.keys()]
        all_coeff = sorted(all_coeff,key = lambda x:abs(x[1]["coefficient"]),reverse = True)
        self._all_coeffs = all_coeff
        self.significant_measures = [x[0] for x in all_coeff[:3]]
        self.narratives = {"heading": self.result_column + "Performance Report",
                           "main_card":{},
                           "cards":[]
                        }
        # self._base_dir = os.path.dirname(os.path.realpath(__file__))+"/../../templates/regression/"
        self._base_dir = os.environ.get('MADVISOR_BI_HOME')+"/templates/regression/"

        self._dim_regression = self.run_regression_for_dimension_levels()
        self.generate_narratives()



    def generate_narratives(self):
        regression_narrative_obj = LinearRegressionNarrative(
                                    self._df_regression_result,
                                    self._correlations,
                                    self._dataframe_helper,
                                    self._dataframe_context,
                                    self._spark
                                    )
        main_card_data = regression_narrative_obj.generate_main_card_data()
        main_card_narrative = NarrativesUtils.get_template_output(self._base_dir,\
                                                        'regression_main_card.temp',main_card_data)
        self.narratives['main_card'] = {}
        self.narratives["main_card"]['paragraphs'] = NarrativesUtils.paragraph_splitter(main_card_narrative)
        self.narratives["main_card"]['header'] = 'Key Measures that affect ' + self.result_column
        self.narratives["main_card"]['chart'] = {}
        self.narratives["main_card"]['chart']['heading'] = ''
        self.narratives["main_card"]['chart']['data'] = [[i for i,j in self._all_coeffs],
                                                         [j['coefficient'] for i,j in self._all_coeffs]]
        self.narratives["main_card"]['chart']['label'] = {'x':'Measure Name',
                                                            'y': 'Change in ' + self.result_column + ' per unit increase'}

        count = 0
        for measure_column in self.significant_measures:
            measure_column_cards = {}
            card0 = {}
            card1data = regression_narrative_obj.generate_card1_data(measure_column)
            card1heading = "Impact of "+measure_column+" on "+self.result_column
            card1narrative = NarrativesUtils.get_template_output(self._base_dir,\
                                                            'regression_card1.temp',card1data)

            card1paragraphs = NarrativesUtils.paragraph_splitter(card1narrative)
            card0 = {"paragraphs":card1paragraphs}
            card0["charts"] = {}
            card0['charts']['chart2']={}
            card0['charts']['chart2']['data']=card1data["chart_data"]
            card0['charts']['chart2']['heading'] = ''
            card0['charts']['chart2']['labels'] = {}
            card0['charts']['chart1']={}
            card0["heading"] = card1heading
            measure_column_cards['card0'] = card0

            card2table, card2data=regression_narrative_obj.generate_card2_data(measure_column,self._dim_regression)
            card2narrative = NarrativesUtils.get_template_output(self._base_dir,\
                                                            'regression_card2.temp',card2data)
            card2paragraphs = NarrativesUtils.paragraph_splitter(card2narrative)
            card1 = {'tables': card2table, 'paragraphs' : card2paragraphs,
                        'heading' : 'Key Areas where ' + measure_column + ' matters'}
            measure_column_cards['card1'] = card1

            self._result_setter.set_trend_section_data({"result_column":self.result_column,
                                                        "measure_column":measure_column,
                                                        "base_dir":self._base_dir
                                                        })
            trend_narratives_obj = TimeSeriesNarrative(self._dataframe_helper, self._dataframe_context, self._result_setter, self._spark)
            card2 =  trend_narratives_obj.get_regression_trend_card_data()
            if card2:
                measure_column_cards['card2'] = card2
            # if self._primary_date != None:
            #
            #     card3heading = 'How '+ self.result_column +' and '+ measure_column + ' changed over time'
            #     agg_data = self._dataframe_helper.get_agg_data_frame(self._primary_date, measure_column,\
            #                 self.result_column,existingDateFormat=self._existingDateFormat,requestedDateFormat=self._requestedDateFormat)
            #     card3data = regression_narrative_obj.generate_card3_data(agg_data, measure_column)
            #     card3narrative = NarrativesUtils.get_template_output(self._base_dir,\
            #                                                     'regression_card3.temp',card3data)
            #
            #     card3chart = {'heading': ''}
            #     card3chart['data']=regression_narrative_obj.generate_card3_chart(agg_data)
            #     card3paragraphs = NarrativesUtils.paragraph_splitter(card3narrative)
            #     card2 = {'charts': card3chart, 'paragraphs': card3paragraphs, 'heading': card3heading}
            #     measure_column_cards['card2'] = card2


            card3 = {}
            card4data = regression_narrative_obj.generate_card4_data(self.result_column,measure_column)
            card4heading = "Sensitivity Analysis: Effect of "+self.result_column+" on Segments of "+measure_column
            card4narrative = NarrativesUtils.get_template_output(self._base_dir,\
                                                                'regression_card4.temp',card4data)
            card4paragraphs = NarrativesUtils.paragraph_splitter(card4narrative)
            card3 = {"paragraphs":card4paragraphs}
            card3["charts"] = card4data["charts"]
            card3["heading"] = card4heading
            measure_column_cards['card3'] = card3

            self.narratives['cards'].append(measure_column_cards)

            if count == 0:
                card4data.pop("charts")
                self._result_setter.update_executive_summary_data(card4data)
            count += 1



    def run_regression_for_dimension_levels(self):

        significant_dimensions = self._dataframe_helper.get_significant_dimension()
        if significant_dimensions != {}:
            sig_dims = [(x,significant_dimensions[x]) for x in significant_dimensions.keys()]
            sig_dims = sorted(sig_dims,key=lambda x:x[1],reverse=True)
            cat_columns = [x[0] for x in sig_dims[:5]]
        else:
            cat_columns = self._dataframe_helper.get_string_columns()[:5]
        if self._date_columns != None:
            if len(self._date_columns) >0 :
                cat_columns = list(set(cat_columns)-set(self._date_columns))

        regression_result_dimension_cols = dict(zip(cat_columns,[{}]*len(cat_columns)))
        for col in cat_columns:
            column_levels = self._dataframe_helper.get_all_levels(col)
            level_regression_result = dict(zip(column_levels,[{}]*len(column_levels)))
            for level in column_levels:
                filtered_df = self._dataframe_helper.filter_dataframe(col,level)
                result = LinearRegression(filtered_df, self._dataframe_helper, self._dataframe_context).fit(self._dataframe_context.get_result_column())
                if result == None:
                    result = {"intercept" : 0.0,
                              "rmse" : 0.0,
                              "rsquare" : 0.0,
                              "coeff" : 0.0
                              }
                else:
                    result = {"intercept" : result.get_intercept(),
                              "rmse" : result.get_root_mean_square_error(),
                              "rsquare" : result.get_rsquare(),
                              "coeff" : result.get_all_coeff()
                              }
                level_regression_result[level] = result
            regression_result_dimension_cols[col] = level_regression_result
        # print json.dumps(regression_result_dimension_cols,indent=2)
        return regression_result_dimension_cols

    # def get_date_conversion_formats(self, df_context):
    #     dateColumnFormatDict =  self._dataframe_helper.get_datetime_format(self._primary_date)
    #     if self._primary_date in dateColumnFormatDict.keys():
    #         self._existingDateFormat = dateColumnFormatDict[self._primary_date]
    #     else:
    #         self._existingDateFormat = None
    #
    #     if df_context.get_requested_date_format() != None:
    #         self._requestedDateFormat = df_context.get_requested_date_format()[0]
    #     else:
    #         self._requestedDateFormat = None
    #
    #     if self._requestedDateFormat != None:
    #         self._requestedDateFormat = self._dateFormatConversionDict[self._requestedDateFormat]
    #     else:
    #         self._requestedDateFormat = self._existingDateFormat


__all__ = [
    'LinearRegressionNarrative',
    'RegressionNarrative'
]
