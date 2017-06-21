import os
import re
import json
import pandas as pd
from pyspark.sql import functions as FN
from pyspark.sql.functions import sum

from bi.algorithms import LinearRegression
from linear_regression import LinearRegressionNarrative
from bi.narratives import utils as NarrativesUtils



class RegressionNarrative:
    def __init__(self, df_helper, df_context, spark, df_regression_result, correlations):
        self._df_regression_result = df_regression_result
        self._correlations = correlations
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context
        self._spark = spark
        self.measures = []
        self.result_column = self._dataframe_helper.resultcolumn
        self._dateFormatConversionDict = {
            "mm/dd/YYYY":"%m/%d/%Y",
            "dd/mm/YYYY":"%d/%m/%Y",
            "YYYY/mm/dd":"%Y/%m/%d",
            "dd <month> YYYY":"%d %b,%Y"
        }
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
        self.get_primary_time_dimension(df_context)
        self.generate_narratives()

    def get_primary_time_dimension(self, df_context):
        date_suggestion_cols = df_context.get_date_column_suggestions()
        if date_suggestion_cols != None:
            self._primary_date = date_suggestion_cols[0]
            self.get_date_conversion_formats(df_context)
        else:
            self._primary_date = None

    def get_agg_data_frame(self, measure_column, result_column):
        aggregate_column = self._primary_date
        data_frame = self._dataframe_helper.get_data_frame()
        existingDateFormat = self._existingDateFormat
        requestedDateFormat = self._requestedDateFormat
        if existingDateFormat != None and requestedDateFormat != None:
            agg_data = data_frame.groupBy(aggregate_column).agg({measure_column : 'sum', result_column : 'sum'}).toPandas()
            try:
                agg_data['date_col'] = pd.to_datetime(agg_data[aggregate_column], format = existingDateFormat)
            except Exception as e:
                print e
                print '----  ABOVE EXCEPTION  ----' * 10
                existingDateFormat = existingDateFormat[3:6]+existingDateFormat[0:3]+existingDateFormat[6:]
                agg_data['date_col'] = pd.to_datetime(agg_data[aggregate_column], format = existingDateFormat)
            agg_data = agg_data.sort_values('date_col')
            agg_data[aggregate_column] = agg_data['date_col'].dt.strftime(requestedDateFormat)
            agg_data.columns = [aggregate_column,measure_column,result_column,"date_col"]
            agg_data = agg_data[[aggregate_column,measure_column, result_column]]
        elif existingDateFormat != None:
            agg_data = data_frame.groupBy(aggregate_column).agg({measure_column : 'sum', result_column : 'sum'}).toPandas()
            try:
                agg_data['date_col'] = pd.to_datetime(agg_data[aggregate_column], format = existingDateFormat)
            except Exception as e:
                print e
                print '----  ABOVE EXCEPTION  ----' * 10
                existingDateFormat = existingDateFormat[3:6]+existingDateFormat[0:3]+existingDateFormat[6:]
                agg_data['date_col'] = pd.to_datetime(agg_data[aggregate_column], format = existingDateFormat)
            agg_data = agg_data.sort_values('date_col')
            agg_data.columns = [aggregate_column,measure_column,result_column,"date_col"]
            agg_data = agg_data[['Date','measure']]
        else:
            agg_data = data_frame.groupBy(aggregate_column).agg({measure_column : 'sum', result_column : 'sum'}).toPandas()
            agg_data.columns = [aggregate_column,measure_column,result_column]
        return agg_data

    def get_date_conversion_formats(self, df_context):
        dateColumnFormatDict =  self._dataframe_helper.get_datetime_format(self._primary_date)
        if self._primary_date in dateColumnFormatDict.keys():
            self._existingDateFormat = dateColumnFormatDict[self._primary_date]
        else:
            self._existingDateFormat = None

        if df_context.get_requested_date_format() != None:
            self._requestedDateFormat = df_context.get_requested_date_format()[0]
        else:
            self._requestedDateFormat = None

        if self._requestedDateFormat != None:
            self._requestedDateFormat = self._dateFormatConversionDict[self._requestedDateFormat]
        else:
            self._requestedDateFormat = self._existingDateFormat

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


        for measure_column in self.significant_measures:
            temp_cards = {}
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
            # self.narratives["cards"].append({"card0":card0})
            temp_cards['card0'] = card0


            # card2data = regression_narrative_obj.generate_card2_data(measure_column,self._dim_regression)
            card2table, card2data=regression_narrative_obj.generate_card2_data(measure_column,self._dim_regression)
            card2narrative = NarrativesUtils.get_template_output(self._base_dir,\
                                                            'regression_card2.temp',card2data)
            card2paragraphs = NarrativesUtils.paragraph_splitter(card2narrative)
            card1 = {'tables': card2table, 'paragraphs' : card2paragraphs,
                        'heading' : 'Key Areas where ' + measure_column + ' matters'}
            # self.narratives['cards'].append({'card1':card1})
            temp_cards['card1'] = card1

            # card2data = regression_narrative_obj.generate_card2_data(measure_column,self._dim_regression)
            # card2narrative = NarrativesUtils.get_template_output(self._base_dir,\
            #                                                 'regression_card2.temp',card2data)
            if self._primary_date != None:
                card3heading = 'How '+ self.result_column +' and '+ measure_column + ' changed over time'
                agg_data = self.get_agg_data_frame(measure_column, result_column= self.result_column)
                card3data = regression_narrative_obj.generate_card3_data(agg_data, measure_column)
                card3narrative = NarrativesUtils.get_template_output(self._base_dir,\
                                                                'regression_card3.temp',card3data)
                card3chart = {'heading': ''}
                card3chart['data']=regression_narrative_obj.generate_card3_chart(agg_data)
                card3paragraphs = NarrativesUtils.paragraph_splitter(card3narrative)
                card2 = {'charts': card3chart, 'paragraphs': card3paragraphs, 'heading': card3heading}
                # self.narratives["cards"].append({"card2":card2})
                temp_cards['card2'] = card2


            card3 = {}
            card4data = regression_narrative_obj.generate_card4_data(self.result_column,measure_column)
            card4heading = "Sensitivity Analysis: Effect of "+self.result_column+" on Segments of "+measure_column
            card4narrative = NarrativesUtils.get_template_output(self._base_dir,\
                                                                'regression_card4.temp',card4data)
            card4paragraphs = NarrativesUtils.paragraph_splitter(card4narrative)
            card3 = {"paragraphs":card4paragraphs}
            card3["charts"] = card4data["charts"]
            card3["heading"] = card4heading
            # self.narratives["cards"].append({"card3":card3})
            temp_cards['card3'] = card3

            self.narratives['cards'].append(temp_cards)

    def run_regression_for_dimension_levels(self):

        significant_dimensions = self._dataframe_helper.get_significant_dimension()
        if significant_dimensions != {}:
            sig_dims = [(x,significant_dimensions[x]) for x in significant_dimensions.keys()]
            sig_dims = sorted(sig_dims,key=lambda x:x[1],reverse=True)
            cat_columns = [x[0] for x in sig_dims[:5]]
        else:
            cat_columns = self._dataframe_helper.get_string_columns()[:5]

        regression_result_dimension_cols = dict(zip(cat_columns,[{}]*len(cat_columns)))
        for col in cat_columns:
            column_levels = self._dataframe_helper.get_all_levels(col)
            level_regression_result = dict(zip(column_levels,[{}]*len(column_levels)))
            for level in column_levels:
                filtered_df = self._dataframe_helper.filter_dataframe(col,level)
                result = LinearRegression(filtered_df, self._dataframe_helper, self._dataframe_context).fit(self._dataframe_context.get_result_column())
                result = {"intercept" : result.get_intercept(),
                          "rmse" : result.get_root_mean_square_error(),
                          "rsquare" : result.get_rsquare(),
                          "coeff" : result.get_all_coeff()
                          }
                level_regression_result[level] = result
            regression_result_dimension_cols[col] = level_regression_result
        # print json.dumps(regression_result_dimension_cols,indent=2)
        return regression_result_dimension_cols


__all__ = [
    'LinearRegressionNarrative',
    'RegressionNarrative'
]
