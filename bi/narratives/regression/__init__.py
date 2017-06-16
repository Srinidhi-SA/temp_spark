import os
import re
import json

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

        self.all_coefficients = self._df_regression_result.get_all_coeff()
        all_coeff = [(x,self.all_coefficients[x]) for x in self.all_coefficients.keys()]
        all_coeff = sorted(all_coeff,key = lambda x:abs(x[1]["coefficient"]),reverse = True)
        self.significant_measures = [x[0] for x in all_coeff[:3]]
        cards = dict(zip(self.significant_measures,[{}]*len(self.significant_measures)))
        self.narratives = {"heading": self.result_column + "Performance Report",
                           "main_card":{},
                           "cards":cards
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
        self.narratives["main_card"] = main_card_narrative

        for measure_column in self.significant_measures:
            card1data = regression_narrative_obj.generate_card1_data(measure_column)
            # card1narrative = NarrativesUtils.get_template_output(self._base_dir,\
            #                                                 'regression_card1.temp',card1data)
            card1narrative = "HEEHEEHEE"
            self.narratives["cards"][measure_column]["card1"] = card1narrative

            # card2data = regression_narrative_obj.generate_card2_data(measure_column,self._dim_regression)
            # card2narrative = NarrativesUtils.get_template_output(self._base_dir,\
            #                                                 'regression_card2.temp',card2data)
            card2narrative = "HEEHEEHEE"
            self.narratives["cards"][measure_column]["card2"] = card2narrative

            # card2data = regression_narrative_obj.generate_card2_data(measure_column,self._dim_regression)
            # card2narrative = NarrativesUtils.get_template_output(self._base_dir,\
            #                                                 'regression_card2.temp',card2data)
            card3narrative = "HEEHEEHEE"
            self.narratives["cards"][measure_column]["card3"] = card3narrative

            # card2data = regression_narrative_obj.generate_card2_data(measure_column,self._dim_regression)
            # card2narrative = NarrativesUtils.get_template_output(self._base_dir,\
            #                                                 'regression_card2.temp',card2data)
            card4narrative = "HEEHEEHEE"
            self.narratives["cards"][measure_column]["card4"] = card4narrative

            run_clustering(self.significant_measures)
            print "HAHAH"
            regression_narrative_obj.generate_card2_data(measure_column,self._dim_regression)
            print "DDDD"
            regression_narrative_obj.getQuadrantData(self.result_column,measure_column)

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
        print json.dumps(regression_result_dimension_cols,indent=2)
        return regression_result_dimension_cols


__all__ = [
    'LinearRegressionNarrative',
    'RegressionNarrative'
]
