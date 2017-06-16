import os
import re
import json
from collections import OrderedDict

from bi.common.utils import accepts
from bi.common.results.regression import RegressionResult
from bi.common.results.correlation import CorrelationStats
from bi.common.results.correlation import ColumnCorrelations
from bi.algorithms import KmeansClustering
from bi.narratives import utils as NarrativesUtils
from bi.stats.util import Stats
from bi.common import utils as CommonUtils

import pyspark.sql.functions as FN
from pyspark.sql.functions import avg
from pyspark.ml.feature import Bucketizer
from pyspark.sql.types import DoubleType

class LinearRegressionNarrative:
    STRONG_CORRELATION = 0.7
    MODERATE_CORRELATION = 0.3


    def __init__(self, regression_result, column_correlations, df_helper,df_context,spark):
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context
        self._regression_result = regression_result
        self._data_frame = self._dataframe_helper.get_data_frame()
        self._spark = spark
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

    def generate_main_card_data(self):
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

        return data_dict

    def getQuadrantData(self,col1,col2):
        print "YELLOS"
        col1_mean = Stats.mean(self._data_frame,col1)
        col2_mean = Stats.mean(self._data_frame,col2)
        low1low2 = self._data_frame.filter(FN.col(col1) < col1_mean & FN.col(col2) < col2_mean)
        low1high2 = self._data_frame.filter(FN.col(col1) < col1_mean & FN.col(col2) >= col2_mean)
        high1high2 = self._data_frame.filter(FN.col(col1) >= col1_mean & FN.col(col2) >= col2_mean)
        high1low2 = self._data_frame.filter(FN.col(col1) >= col1_mean & FN.col(col2) < col2_mean)
        print "AAAA"

    def keyAreasDict(self,dim_col_regression,measure_col):
        data = dim_col_regression
        dimension_data_dict = {}
        dims = data.keys()
        dimension_level_coeff_dict = {}
        all_coeff_list = []
        highest_coeff = {}
        lowest_coeff = {}
        for dim in dims:
            levels = data[dim].keys()
            coeff_list = [(x,data[dim][x]["coeff"][measure_col]["coefficient"]) for x in levels if data[dim][x]["coeff"].has_key(measure_col)]
            coeff_list = sorted(coeff_list,key=lambda x:abs(x[1]),reverse=True)
            highest_coeff[dim] = coeff_list[0]
            lowest_coeff[dim] = coeff_list[-1]
            all_coeff_list.append([coeff_list[0],dim])
        all_coeff_list = sorted(all_coeff_list,key=lambda x:abs(x[0][1]),reverse=True)
        top2_dims = [x[1] for x in all_coeff_list[:2]]
        dimension_data_dict = dict(zip(top2_dims,[{}]*len(top2_dims)))
        for val in top2_dims:
            temp_dict = {}
            temp_dict["levels"] = data[val].keys()
            temp_dict["highest_impact_level"] = highest_coeff[val]
            temp_dict["lowest_impact_level"] = lowest_coeff[val]
            dimension_data_dict[val] = temp_dict
        dimension_data_dict[top2_dims[0]]["rank"] = 1
        dimension_data_dict[top2_dims[1]]["rank"] = 2
        return dimension_data_dict

    def generateGroupedMeasureDataDict(self,measure_column):
        splits_data = self.get_measure_column_splits(self._data_frame,measure_column)
        splits = splits_data["splits"]
        double_df = self._data_frame.withColumn(measure_column, self._data_frame[measure_column].cast(DoubleType()))
        bucketizer = Bucketizer(inputCol=measure_column,
                        outputCol="BINNED_INDEX")
        bucketizer.setSplits(splits)
        binned_df = bucketizer.transform(double_df)
        unique_bins = binned_df.select("BINNED_INDEX").distinct().collect()
        unique_bins = [int(x[0]) for x in unique_bins]
        binned_index_dict = dict(zip(unique_bins,splits_data["splits_range"]))
        output = {"bins":binned_index_dict,"data":binned_df}
        return output

    def generate_card1_data(self,measure_column):
        data_dict = {}
        input_cols = [self._result_column,measure_column]
        df = self._data_frame
        kmeans_obj = KmeansClustering(df, self._dataframe_helper, self._dataframe_context, self._spark)
        kmeans_obj.kmeans_pipeline(input_cols,cluster_count=None,max_cluster=5)
        kmeans_result = {"stats":kmeans_obj.get_kmeans_result(),"data":kmeans_obj.get_prediction_data()}
        data_dict = self.generateClusterDataDict(kmeans_result)
        # print json.dumps(data_dict,indent=2)
        return data_dict

    def generate_card2_data(self,measure_column,dim_col_regression):
        dimension_data_dict = self.keyAreasDict(dim_col_regression,measure_column)
        grouped_output = self.generateGroupedMeasureDataDict(measure_column)
        df = grouped_output["data"]
        bins = grouped_output["bins"]
        # print json.dumps(dimension_data_dict,indent=2)
        category_dict = dict(zip(bins.keys(),[str(bins[x][0])+" to "+str(bins[x][1]) for x in bins.keys()]))
        table_data = {}
        for val in dimension_data_dict.keys():
            data = df.groupby(df["BINNED_INDEX"]).pivot(val).avg(self._result_column).toPandas()
            data = data.fillna(0)
            print data
            print "GGGGGGGGGGG"*3
            data = data.sort_values(by="BINNED_INDEX", axis=0, ascending=True, inplace=True)
            print data
            # print category_dict[data["BINNED_INDEX"][0]]
            # data["BINNED_INDEX"] = data["BINNED_INDEX"].apply(lambda x:category_dict[x])
            table_data[val] = data

    def get_measure_column_splits(self,df,colname,n_split = 4):
        """
        n_split = number of splits required -1
        splits = [0.0, 23.0, 46.0, 69.0, 92.0, 115.0]
        splits_range = [(0.0, 23.0), (23.0, 46.0), (46.0, 69.0), (69.0, 92.0), (92.0, 115.0)]
        """
        minimum_val = Stats.min(df,colname)
        maximum_val = Stats.max(df,colname)
        splits  = CommonUtils.frange(minimum_val,maximum_val,num_steps=n_split)
        splits = sorted(splits)
        splits_range = [(splits[idx],splits[idx+1]) for idx in range(len(splits)-1)]
        output = {"splits":splits,"splits_range":splits_range}
        return output


    def generateClusterDataDict(self,kmeans_result):
        kmeans_stats = kmeans_result["stats"]
        input_columns = kmeans_stats["inputCols"]
        kmeans_df = kmeans_result["data"]
        cluster_data_dict = {"chart_data":None,"grp_data":None}
        grp_df = kmeans_df.groupBy("prediction").count().toPandas()
        grp_counts = zip(grp_df["prediction"], grp_df["count"])
        grp_counts = sorted(grp_counts,key=lambda x:x[1],reverse=True)
        grp_dict = dict(grp_counts)
        chart_data = {}
        for idx in grp_df["prediction"]:
            chart_data[idx] = []
        grp_data = {}
        total = float(sum(grp_dict.values()))
        for grp_id in list(grp_df["prediction"]):
            data = {}
            data["count"] = grp_dict[grp_id]
            data["contribution"] = round(grp_dict[grp_id]*100/total,2)
            df = kmeans_df.filter(FN.col("prediction") == grp_id)
            data["columns"] = dict(zip(input_columns,[{}]*len(input_columns)))
            for val in input_columns:
                data["columns"][val]["avg"] = Stats.mean(df,val)
            grp_data[grp_id] = data
            chart_data[grp_id] = df.select(input_columns).toPandas().T.to_dict()
        cluster_data_dict["chart_data"] = chart_data
        cluster_data_dict["grp_data"] = grp_data
        return cluster_data_dict

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
