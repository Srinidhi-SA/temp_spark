from bi.common.utils import accepts
from bi.common.results.regression import DFRegressionResult
from bi.common.results.correlation import Correlations

from linear_regression import LinearRegressionNarrative


class RegressionNarrative:
    def __init__(self, df_helper, df_regression_result, correlations,kmeans_result):
        self._df_regression_result = df_regression_result
        self._kmeans_result = kmeans_result
        self._correlations = correlations
        self._datafram_helper = df_helper
        self.measures = []
        self.narratives = {"SectionHeading":"",
                           "card1":{},
                           "card2":{},
                           "card3":{}
                        }

        # self._generate_narratives()
        self.generate_narratives()

    def generate_narratives(self):
        regression_narrative_obj = LinearRegressionNarrative(
                                    self._df_regression_result,
                                    self._correlations,
                                    self._kmeans_result,
                                    self._datafram_helper)
        # self.heading = measure_column + ' Performance Analysis'
        regression_narrative_obj.generateClusterDataDict()
        regression_narrative_obj.generateGroupedMeasureDataDict()
        regression_narrative_obj.getQuadrantData("Sales","Marketing_Cost")



    def _generate_narratives(self):
        print self._df_regression_result.get_measures()
        for measure_column in self._df_regression_result.get_measures():
            self.heading = measure_column + ' Performance Analysis'
            self.sub_heading = "Analysis by Measure"
            regression_narrative_obj = LinearRegressionNarrative(
                                        self._df_regression_result.get_regression_result(measure_column),
                                        self._correlations.get_correlation_stats(measure_column),
                                        self._kmeans_result,
                                        self._datafram_helper)

            self.measures.append(measure_column)
            self.narratives[measure_column] = regression_narrative

__all__ = [
    'LinearRegressionNarrative',
    'RegressionNarrative'
]
