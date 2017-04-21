
from bi.common import utils
from bi.common import DataWriter
#from bi.stats.regression.new_regression import LinearRegression
from bi.stats.regression import LinearRegression
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

        regression_narratives_obj = LinearRegressionNarrative(len(self._dataframe_helper.get_numeric_columns()),regression_result_obj, self._correlations,self._dataframe_helper)
        regression_narratives = utils.as_dict(regression_narratives_obj)

        #print 'Regression narratives:  %s' %(json.dumps(regression_narratives, indent=2))
        DataWriter.write_dict_as_json(self._spark, regression_narratives, self._dataframe_context.get_narratives_file()+'Regression/')
