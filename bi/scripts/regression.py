
from bi.common import utils
from bi.common import DataWriter
from bi.algorithms import LinearRegression
from bi.narratives.regression import RegressionNarrative
from bi.narratives.regression import LinearRegressionNarrative
import json

import json
# from bi.stats import Correlation

class RegressionScript:
    def __init__(self, data_frame, df_helper, df_context, spark, correlations):
        self._data_frame = data_frame
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context
        self._spark = spark
        self._correlations = correlations

    def Run(self):
        regression_result_obj = LinearRegression(self._data_frame, self._dataframe_helper, self._dataframe_context).fit(self._dataframe_context.get_result_column())
        regression_result = utils.as_dict(regression_result_obj)

        #print 'Regression result: %s' % (json.dumps(regression_result, indent=2))
        DataWriter.write_dict_as_json(self._spark, regression_result, self._dataframe_context.get_result_file()+'Regression/')

        overall_regression_result = {"intercept" : regression_result_obj.get_intercept(),
                                     "rmse" : regression_result_obj.get_root_mean_square_error(),
                                     "rsquare" : regression_result_obj.get_rsquare(),
                                     "coeff" : regression_result_obj.get_all_coeff()
                                    }
        print "##################################"
        print "Running Regression for all Levels:"
        print "##################################"

        # significant_dimensions = self._dataframe_helper.get_significant_dimension()
        # cat_columns = top 5 from significant_dimensions
        cat_columns = self._dataframe_helper.get_string_columns()[:5]
        regression_result_cat_columns = dict(zip(cat_columns,[{}]*len(cat_columns)))
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
            regression_result_cat_columns[col] = level_regression_result
        print json.dumps(regression_result_cat_columns,indent=2)




        regression_narratives_obj = LinearRegressionNarrative(len(self._dataframe_helper.get_numeric_columns()),regression_result_obj, self._correlations,self._dataframe_helper)
        regression_narratives = utils.as_dict(regression_narratives_obj)

        #print 'Regression narratives:  %s' %(json.dumps(regression_narratives, indent=2))
        DataWriter.write_dict_as_json(self._spark, regression_narratives, self._dataframe_context.get_narratives_file()+'Regression/')
