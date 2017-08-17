from pyspark.ml.linalg import DenseVector
from pyspark.ml.regression import LinearRegression as LR
from pyspark.sql.functions import  col, udf, count
from pyspark.ml.linalg import Vectors, VectorUDT

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

        all_measures = input_columns+[output_column]

        # TODO: ensure no duplicates are present in input_columns
        p_values = []
        coefficients = []
        intercepts = []
        rmses = []
        r2s = []
        sample_data_dict={}
        func = udf(lambda x: DenseVector([x]),VectorUDT())
        regression_result = RegressionResult(output_column, input_columns)
        training_df = self._data_frame.select(*(func(c).alias(c) if c!=output_column else col(c) for c in all_measures))
        for input_col in input_columns:
            if training_df.select(input_col).distinct().count() < 2:
                p_values.append(1.0)
                coefficients.append(0.0)
                intercepts.append(0.0)
                r2s.append(0.0)
                sample_data_dict[input_col]=None
                continue
            lr = LR(maxIter=LinearRegression.MAX_ITERATIONS, regParam=LinearRegression.REGULARIZATION_PARAM,
                    labelCol=output_column,featuresCol=input_col,fitIntercept=True, solver='normal')
            lr_model = lr.fit(training_df)
            lr_summary = lr_model.evaluate(training_df)
            try:
                p_values.append(lr_model.summary.pValues[0])
            except:
                print '|'*140
                p_values.append(1.0)
            coefficients.append(float(lr_model.coefficients[0]))
            intercepts.append(float(lr_model.intercept))
            rmses.append(float(lr_summary.rootMeanSquaredError))
            r2s.append(float(lr_summary.r2))
            sample_data_dict[input_col] = None
        regression_result.set_params(intercept=intercepts, coefficients=coefficients,p_values = p_values,
                                      rmse=rmses, r2=r2s,sample_data_dict=sample_data_dict)

        return regression_result
