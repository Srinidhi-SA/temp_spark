# -*- coding: utf-8 -*-
"""This module contains result object for ChiSquare test"""

import random
import json
from humanize import intcomma

from pyspark.mllib.stat.test import ChiSqTestResult

from bi.common.exception import BIException
from bi.common.decorators import accepts


class ContingencyTable:
    '''
    Represents a two dimensional contingency table of M x N dimension.
        M rows      - one for each unique value of column one
        N columns   - one for each unique value of column two
    '''
    @accepts(object, (list, tuple), (list, tuple))
    def __init__(self, column_one_values, column_two_values):
        self.column_one_values = column_one_values
        self.column_two_values = column_two_values
        self.table = [[0 for j in range(0,len(column_two_values))] \
                        for i in range(0,len(column_one_values))]
        self.table_percent = [[0 for j in range(0,len(column_two_values))] \
                        for i in range(0,len(column_one_values))]
        self.table_percent_by_row = [[0 for j in range(0,len(column_two_values))] \
                        for i in range(0,len(column_one_values))]
        self.table_percent_by_column = [[0 for j in range(0,len(column_two_values))] \
                        for i in range(0,len(column_one_values))]

    def get_column_two_levels(self):
        return self.column_two_values

    def get_column_one_levels(self):
        return self.column_one_values

    def update_splits(self,splits):
        splits = [intcomma(int(i)) if int(i)==i else intcomma(round(i,2)) for i in splits]
        return  splits

    def get_bin_names (self,splits):
        bin_names = []
        splits = self.update_splits(list(splits))
        start = splits[0]
        for i in splits[1:]:
            bin_names.append(str(start) + ' to ' + str(i))
            start = i
        return bin_names

    def update_col2_names(self, splits):
        bin_names = self.get_bin_names(splits)
        print '*'*145
        print bin_names
        self.column_two_values = [bin_names[int(float(i))] for i in self.column_two_values]

    def get_row_total(self):
        return [sum(row_data) for row_data in self.table]

    def get_column_total(self):
        return [sum(row_data) for row_data in zip(*self.table)]

    def set_tables(self):
        total = self.get_total()
        row_total = self.get_row_total()
        column_total = self.get_column_total()
        column_one_values = self.column_one_values
        column_two_values = self.column_two_values
        self.table_percent = [[round(self.table[i][j]*100.0/total,2) for j in range(0,len(column_two_values))] \
                        for i in range(0,len(column_one_values))]
        self.table_percent_by_row = [[round(self.table[i][j]*100.0/row_total[i],2) for j in range(0,len(column_two_values))] \
                        for i in range(0,len(column_one_values))]
        self.table_percent_by_column = [[round(self.table[i][j]*100.0/column_total[j],2) for j in range(0,len(column_two_values))] \
                        for i in range(0,len(column_one_values))]

    @accepts(object, (str, basestring), (list, tuple))
    def add_row(self, column_one_value, row_data):
        if column_one_value not in self.column_one_values:
            raise BIException('Unknown value: "%s" for column' %(column_one_value,))
        if len(row_data) != len(self.column_two_values):
            raise BIException('Row for: "%s" should have %d values, but has %d values only', \
                              column_one_value, len(self.column_two_values), len(row_data))
        index = self.column_one_values.index(column_one_value)
        self.table[index] = row_data

    def get_total(self):
        return sum([sum(row_data) for row_data in self.table])


    @accepts(object, (str, basestring), (str, basestring))
    def get_value(self, column_one_value, column_two_value):
        if column_one_value not in self.column_one_values:
            raise BIException('Unknown column one value: %s' %(column_one_value,))
        if column_two_value not in self.column_two_values:
            raise BIException('Unknown column two value: %s' %(column_two_value,))

        column_one_index = self.column_one_values.index(column_one_value)
        column_two_index = self.column_two_values.index(column_two_value)
        return self.table[column_one_index][column_two_index]

    def get_value_column_percent(self, column_one_value, column_two_value):
        if column_one_value not in self.column_one_values:
            raise BIException('Unknown column one value: %s' %(column_one_value,))
        if column_two_value not in self.column_two_values:
            raise BIException('Unknown column two value: %s' %(column_two_value,))

        column_one_index = self.column_one_values.index(column_one_value)
        column_two_index = self.column_two_values.index(column_two_value)
        return self.table_percent_by_column[column_one_index][column_two_index]

class ChiSquareResult:
    """
    Encapsulates results of ChiSquare test
    """

    def __init__(self):
        self.method = ""
        self.dof = 0
        self.nh = ""
        self.pv = 0.0
        self.stat = 0.0
        self.contingency_table = {}
        self.percentage_table = {}
        self.cramers_v = 0.0
        self.splits  = None


    @accepts(object, ChiSqTestResult)
    def set_params(self, chi_square_result):
        ### TODO: refactor this method into 5 different methods,
        ###     one each for setting method, dof, nh, pv, and stat values.
        ###
        ###     Results should be plain objects with zero knowledge about any external objects.
        ###
        self.method = chi_square_result.method
        self.dof = chi_square_result.degreesOfFreedom
        self.nh = chi_square_result.nullHypothesis
        self.pv = chi_square_result.pValue
        self.stat = chi_square_result.statistic

    def get_pvalue(self):
        return self.pv

    def get_contingency_table(self):
        return self.contingency_table

    def get_effect_size(self):
        return self.cramers_v

    @accepts(object, ContingencyTable)
    def set_table_result(self, c_table):
        self.contingency_table = c_table

    def set_v_value(self, v):
        self.cramers_v = v

    def set_split_values(self,splits):
        self.splits = splits

    def get_splits(self):
        if self.splits:
            return self.splits
        else:
            return None

    # def set_buckeddata(self.bucketedData):
    #     self._bucketedData = bucketedData



class DFChiSquareResult:
    """
    Result object for all ChiSquare tests in a dataframe
    """

    def __init__(self):
        self.dimensions = []
        self.results = {}

    @accepts(object, (str, basestring), (str, basestring), ChiSquareResult)
    def add_chisquare_result(self, dimension_column_input, dimension_column, chisquare_result):
        if dimension_column_input not in self.dimensions:
            self.dimensions.append(dimension_column)
        if not self.results.has_key(dimension_column_input):
            self.results[dimension_column_input] = {}
        self.results.get(dimension_column_input)[dimension_column] = chisquare_result

    def get_result(self):
        return self.results

    def get_measure_columns(self):
        return self.measures

    def get_dimensions_analyzed(self, measure_column):
        if not self.results.has_key(measure_column):
            return []
        return self.results.get(measure_column).keys()

    def get_chisquare_result(self, target_dimension, input_dimension):
        if not self.results.has_key(target_dimension) or not self.results.get(target_dimension).has_key(input_dimension):
            return None
        return self.results.get(target_dimension).get(input_dimension)
