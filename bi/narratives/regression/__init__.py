from linear_regression import LinearRegressionNarrative


class RegressionNarrative:
    def __init__(self, num_measure_columns, df_regression_result, correlations):
        self._df_regression_result = df_regression_result
        self._num_measure_columns = num_measure_columns
        self._correlations = correlations
        self.measures = []
        self.narratives = {}

        self._generate_narratives()

    def _generate_narratives(self):
        for measure_column in self._df_regression_result.get_measures():
            self.heading = measure_column + ' Performance Analysis'
            self.sub_heading = "Analysis by Measure"
            regression_narrative = LinearRegressionNarrative(
                                        self._num_measure_columns,
                                        self._df_regression_result.get_regression_result(measure_column),
                                        self._correlations.get_correlation_stats(measure_column))

            self.measures.append(measure_column)
            self.narratives[measure_column] = regression_narrative


__all__ = [
    'LinearRegressionNarrative',
    'RegressionNarrative'
]
