from pyspark.sql import DataFrame
from pyspark.ml.feature import QuantileDiscretizer
from pyspark.sql import functions as FN

from bi.common import BIException
from bi.common.decorators import accepts
from bi.common.results import FivePointSummary


class Quantizer:
    QUANTIZATION_OUTPUT_COLUMN = '__quant'
    QUANTIZATION_RELATIVE_ERROR = 0.0001

    @staticmethod
    def quantize(data_frame, measure_column, data_frame_helper):
        if not data_frame_helper.is_numeric_column(measure_column):
            raise BIException.non_numeric_column(measure_column)

        quantile_discretizer = QuantileDiscretizer(numBuckets=4, inputCol=measure_column,
                                                   outputCol=Quantizer.QUANTIZATION_OUTPUT_COLUMN,
                                                   relativeError=Quantizer.QUANTIZATION_RELATIVE_ERROR)
        bucketizer = quantile_discretizer.fit(data_frame)
        # splits have these values [-Inf, Q1, Median, Q3, Inf]
        splits = bucketizer.getSplits()
        if len(splits) < 5:
            q1 = splits[1]
            median = splits[1]
            q3 = splits[1]
            iqr = (q3 - q1)
            left_hinge = (q1 - 1.5 * iqr)
            right_hinge = (q3 + 1.5 * iqr)
        else:
            q1 = splits[1]
            median = splits[2]
            q3 = splits[3]
            iqr = (q3 - q1)
            left_hinge = (q1 - 1.5 * iqr)
            right_hinge = (q3 + 1.5 * iqr)

        mean = data_frame.select(FN.mean(measure_column)).collect()[0][0]
        column = FN.column(measure_column)
        num_left_outliers = data_frame.filter(column < left_hinge).count()
        num_right_outliers = data_frame.filter(column > right_hinge).count()
        q1_freq = data_frame.filter(column < q1).count()
        q2_freq = data_frame.filter(column >= q1).filter(column < median).count()
        q3_freq = data_frame.filter(column >= median).filter(column < q3).count()
        q4_freq = data_frame.filter(column >= q3).count()

        return FivePointSummary(left_hinge_value=left_hinge, q1_value=q1, median=median, q3_value=q3,
                                right_hinge_value=right_hinge, num_left_outliers=num_left_outliers,
                                num_right_outliers=num_right_outliers, q1_freq=q1_freq, q2_freq=q2_freq,
                                q3_freq=q3_freq, q4_freq=q4_freq)
