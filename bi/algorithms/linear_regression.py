from pyspark.ml.regression import LinearRegression as LR
from pyspark.ml.linalg import DenseVector

from bi.common.utils import accepts
from bi.common.exception import BIException
from bi.common.results.regression import DFRegressionResult
from bi.common.results.regression import RegressionResult


class LinearRegression:
    LABEL_COLUMN_NAME = '_1'
    FEATURES_COLUMN_NAME = '_2'

    MAX_ITERATIONS = 100
    REGULARIZATION_PARAM = 0.1

    def __init__(self, data_frame, df_helper, df_context):
        self._data_frame = data_frame
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context
        self._sample_size = min(round(df_helper.get_num_rows()*0.8),2000)

    def fit_all(self):
        """
        Performs one vs all-other measures regression fit
        :return:
        """
        if len(self._measure_columns) <= 1:
            return None

        df_regression_result = DFRegressionResult()
        measure_columns = set(self._measure_columns)
        for output_column in measure_columns:
            input_columns = list(measure_columns - set([output_column]))
            regression_result = self.fit(output_column, input_columns)
            if regression_result != None:
                df_regression_result.add_regression_result(regression_result)

        return df_regression_result

    def fit(self, output_column, input_columns=None):
        if output_column not in self._dataframe_helper.get_numeric_columns():
            raise BIException('Output column: %s is not a measure column' % (output_column,))

        if input_columns == None:
            input_columns = list(set(self._dataframe_helper.get_numeric_columns())-set([output_column]))

        if len(set(input_columns) - set(self._dataframe_helper.get_numeric_columns())) != 0:
            raise BIException('At least one of the input columns %r is not a measure column' % (input_columns,))

        # TODO: ensure no duplicates are present in input_columns
        regression_result = RegressionResult(output_column, input_columns)
        training_df = self._data_frame.rdd.map(lambda row: \
                                                   (float(row[output_column]),
                                                    DenseVector([float(row[col]) for col in input_columns]))).toDF()
        lr = LR(maxIter=LinearRegression.MAX_ITERATIONS, regParam=LinearRegression.REGULARIZATION_PARAM,
                elasticNetParam=1.0, labelCol=LinearRegression.LABEL_COLUMN_NAME,
                featuresCol=LinearRegression.FEATURES_COLUMN_NAME)
        lr_model = lr.fit(training_df)
        lr_summary = lr_model.evaluate(training_df)
        #regression_result.set_params(intercept=lr_model.intercept, coefficients=lr_model.coefficients,
        #                              rmse=lr_summary.rootMeanSquaredError, r2=lr_summary.r2,
        #                              t_values=lr_summary.tValues, p_values=lr_summary.pValues)

        # TODO: pass t_values and p_values
        coefficients = [float(i) for i in lr_model.coefficients.values]
        if not any([coeff != 0 for coeff in coefficients]):
            return None
        sample_data_dict = {}
        for col in input_columns:
            # sample_data_dict[col] = self._dataframe_helper.get_sample_data(col, output_column, self._sample_size)
            sample_data_dict[col] = None

        regression_result.set_params(intercept=float(lr_model.intercept), coefficients=coefficients,
                                      rmse=float(lr_summary.rootMeanSquaredError), r2=float(lr_summary.r2),sample_data_dict=sample_data_dict)

        return regression_result
