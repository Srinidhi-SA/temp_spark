import os
import jinja2
import re
from collections import OrderedDict

from bi.common.utils import accepts
from bi.common.results.regression import RegressionResult
from bi.common.results.correlation import CorrelationStats
from bi.common.results.correlation import ColumnCorrelations


from bi.narratives import utils as NarrativesUtils


class LinearRegressionNarrative:
    STRONG_CORRELATION = 0.7
    MODERATE_CORRELATION = 0.3


    def __init__(self, num_measure_columns, regression_result, column_correlations, df_helper):
        self._dataframe_helper = df_helper
        self._num_measure_columns = num_measure_columns
        self._regression_result = regression_result
        #self._correlation_stats = correlation_stats
        self._measure_columns = self._dataframe_helper.get_numeric_columns()
        self._result_column = self._dataframe_helper.resultcolumn
        self._column_correlations = column_correlations

        self._sample_size = min(int(df_helper.get_num_rows()*0.8),2000)
        self.heading = '%s Performance Analysis'%(self._result_column)
        self.sub_heading = 'Analysis by Measure'
        self.output_column_sample = None
        self.summary = None
        self.key_takeaway = None
        self.narratives = {}
        # self._base_dir = os.path.dirname(os.path.realpath(__file__))+"/../../templates/regression/"
        self._base_dir = os.environ.get('MADVISOR_BI_HOME')+"/templates/regression/"
        self._generate_narratives()

    def _generate_narratives(self):
        self._generate_summary()
        self._generate_analysis()

    def _generate_summary(self):

        all_x_variables = [x for x in self._measure_columns if x != self._regression_result.get_output_column()]
        significant_measures = self._regression_result.get_input_columns()
        non_sig_measures = [x for x in all_x_variables if x not in significant_measures]
        data_dict = {
                    "n_m" : len(self._measure_columns),
                    "n_d" : len(self._dataframe_helper.get_string_columns()),
                    "n_td" : len(self._dataframe_helper.get_timestamp_columns()),
                    "all_measures" : self._measure_columns,
                    "om" : all_x_variables,
                    "n_o_m" : len(all_x_variables),
                    'sm': significant_measures,
                    'n_s_m' : len(significant_measures),
                    'n_ns_m': len(non_sig_measures),
                    'nsm': non_sig_measures,
                    "cm": self._regression_result.get_output_column()
        }
        output = NarrativesUtils.get_template_output(self._base_dir,\
                                                        'regression_template_1.temp',data_dict)
        # print output
        reg_coeffs_present = []
        for cols in self._regression_result.get_input_columns():
            reg_coeffs_present.append(self._regression_result.get_coeff(cols)!=0)
        chart_output=''
        if any(reg_coeffs_present):
            chart_output = NarrativesUtils.get_template_output(self._base_dir,\
                                                            'regression_template_2.temp',data_dict)
        self.summary = [output, chart_output]
        self.key_takeaway = NarrativesUtils.get_template_output(self._base_dir,\
                                                        'regression_takeaway.temp',data_dict)


    def _generate_analysis(self):
        input_columns = self._regression_result.get_input_columns()
        output_column = self._regression_result.get_output_column()
        MVD_analysis = self._regression_result.MVD_analysis
        lines = ''
        # print input_columns
        most_significant_col = ''
        highest_regression_coeff = 0
        input_cols_coeff_list = []
        for cols in input_columns:
            coef = self._regression_result.get_coeff(cols)
            temp = abs(coef)
            input_cols_coeff_list.append((cols,temp))
            if temp > highest_regression_coeff:
                highest_regression_coeff=temp
                most_significant_col = cols
        sorted_input_cols = sorted(input_cols_coeff_list,key=lambda x:x[1],reverse=True)

        for cols,coeff in sorted_input_cols:
            corelation_coeff = round(self._column_correlations.get_correlation(cols).get_correlation(),2)
            regression_coeff = round(self._regression_result.get_coeff(cols),3)
            #mvd_result = MVD_analysis[cols]
            data_dict = {
                "cc" : corelation_coeff,
                "beta" : regression_coeff,
                "hsm" : cols,
                "cm" : output_column,
                "msc" : most_significant_col
                }
            '''
            data_dict = {
                "cc" : corelation_coeff,
                "beta" : regression_coeff,
                "hsm" : cols,
                "cm" : output_column,
                "msc" : most_significant_col,
                "most_significant_dimension" : mvd_result['dimension'],
                "levels" : mvd_result['levels'],
                "coefficients" : mvd_result['coefficients'],
                "num_levels" : len(mvd_result['levels']),
                "abs_coeffs": [abs(l) for l in mvd_result['coefficients']],
                "most_significant_dimension2" : mvd_result['dimension2'],
                "levels2" : mvd_result['levels2'],
                "coefficients2" : mvd_result['coefficients2'],
                "num_levels2" : len(mvd_result['levels2']),
                "abs_coeffs2": [abs(l) for l in mvd_result['coefficients2']]
            }
            '''
            lines=NarrativesUtils.get_template_output(self._base_dir,\
                                                            'regression_template_3.temp',data_dict)
            '''
            lines1 = ''
            if mvd_result['dimension']!='':
                template4 = templateEnv.get_template('regression_template_4.temp')
                output = template4.render(data_dict).replace("\n", "")
                output = re.sub(' +',' ',output)
                output = re.sub(' ,',',',output)
                output = re.sub(' \.','.',output)
                output = re.sub('\( ','()',output)
                lines1 = output

            lines2 = ''
            if mvd_result['dimension2']!='':
                template5 = templateEnv.get_template('regression_template_5.temp')
                output = template4.render(data_dict).replace("\n", "")
                output = re.sub(' +',' ',output)
                output = re.sub(' ,',',',output)
                output = re.sub(' \.','.',output)
                output = re.sub('\( ','()',output)
                lines2 = output
            '''
            # column_narrative = {}
            # column_narrative[cols] = {}
            # column_narrative[cols]['title'] = 'Relationship between ' + cols + ' and ' + output_column
            # column_narrative[cols]['analysis'] = lines
            # temp = re.split('\. ',lines)
            # column_narrative[cols]['sub_heading'] = temp[-2]
            # column_narrative[cols]['data'] = self._dataframe_helper.get_sample_data(cols, output_column, self._sample_size)
            # self.narratives.append(column_narrative)

            self.narratives[cols] = {}
            self.narratives[cols]["coeff"] = coeff
            self.narratives[cols]['title'] = 'Relationship between ' + cols + ' and ' + output_column
            self.narratives[cols]['analysis'] = lines
            '''
            self.narratives[cols]['DVM_analysis'] = lines1
            self.narratives[cols]['DVM_analysis2'] = lines2
            '''
            temp = re.split('\. ',lines)
            self.narratives[cols]['sub_heading'] = temp[-2]
            self.narratives[cols]['data'] = self._dataframe_helper.get_sample_data(cols, output_column, self._sample_size)
            # sample_data = self._dataframe_helper.get_sample_data(cols, output_column, self._sample_size)
            # self.narratives[cols]['sample_data'] = sample_data[cols]
            # self.output_column_sample_data = sample_data[output_column]
