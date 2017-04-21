import math

from bi.common.decorators import accepts
from ..util import Stats

"""
Tuckey Range test (Ref: https://en.wikipedia.org/wiki/Tukey%27s_range_test)

    Note: Aapplicable only when all groups have same number of observations
"""


class TuckeyHSD:

    @staticmethod
    @accepts((int, long, float), (int, long), (int, long), (int, long, float), (int, long, float), (int, long), alpha_level=float)
    def test(mean_sum_of_squares_error, num_records, num_groups, group1_mean, group2_mean, group_size, alpha_level=0.05):
        """
        Tests if difference between mean of two groups is significant, using TukeyHSD test
        :param mean_sum_of_squares_error:
        :param num_records:
        :param num_groups:
        :param group1_mean:
        :param group2_mean:
        :param group_size:
        :param alpha_level:
        :return:
        """
        std_err = math.sqrt(float(mean_sum_of_squares_error) / group_size)
        critical_value = math.fabs(group1_mean-group2_mean)/std_err
        df = num_records - num_groups
        if critical_value <= Stats.studentized_range(alpha=alpha_level, samples=num_groups, df=df):
            return True
        return False
