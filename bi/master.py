import sys
import time
import json
# from pyhocon.tool import HOCONConverter

reload(sys)
sys.setdefaultencoding('utf-8')
import ConfigParser

from bi.common import utils as CommonUtils
from bi.common import DataLoader
from bi.common import DataWriter
from bi.common import DataFrameHelper
from bi.common import ContextSetter
from bi.common import ResultSetter

from bi.scripts.frequency_dimensions import FreqDimensionsScript
from bi.scripts.chisquare import ChiSquareScript
from bi.scripts.decision_tree import DecisionTreeScript
from bi.scripts.correlation import CorrelationScript
from bi.scripts.descr_stats import DescriptiveStatsScript
from bi.scripts.density_histogram import DensityHistogramsScript
from bi.scripts.histogram import HistogramsScript
from bi.scripts.two_way_anova import TwoWayAnovaScript
from bi.scripts.regression import RegressionScript
from bi.scripts.timeseries import TrendScript
from bi.scripts.random_forest import RandomForestScript
from bi.scripts.xgboost_classification import XgboostScript
from bi.scripts.logistic_regression import LogisticRegressionScript
from bi.scripts.decision_tree_regression import DecisionTreeRegressionScript
from bi.scripts.executive_summary import ExecutiveSummaryScript
from bi.algorithms import utils as MLUtils
from bi.scripts.random_forest_pyspark import RandomForestPysparkScript
from bi.scripts.logistic_regression_pyspark import LogisticRegressionPysparkScript
from bi.scripts.metadata_new import MetaDataScript
from bi.common import NarrativesTree
from bi.common import NormalCard,SummaryCard,NarrativesTree,HtmlData,C3ChartData,TableData,TreeData,ModelSummary

import traceback
from parser import configparser
from pyspark.sql.functions import col, udf

#if __name__ == '__main__':
LOGGER = []
def main(configJson):
    global LOGGER
    deployEnv = None
    debugMode = True
    testConfigs = {
        "story" :{
            "config" : {
                "COLUMN_SETTINGS" : {
                    "analysis_type" : [
                        "measure"
                    ],
                    "consider_columns" : [
                        "Sales Office",
                        "Brand",
                        "Category",
                        "Sub Category",
                        "Product",
                        "Sales Quantity",
                        "Sales Value",
                        "Gross Margin",
                        "Date"
                    ],
                    "consider_columns_type" : [
                        "including"
                    ],
                    "dateTimeSuggestions" : [
                        {}
                    ],
                    "date_columns" : [
                        "Date"
                    ],
                    "date_format" : None,
                    "ignore_column_suggestion" : [],
                    "polarity" : [
                        "positive"
                    ],
                    "result_column" : [
                        "Sales Quantity"
                    ],
                    "utf8_column_suggestions" : []
                },
                "FILE_SETTINGS" : {
                    "inputfile" : [
                        "file:///home/gulshan/marlabs/datasets/BIDCO_Local_v4.csv"
                    ],
                    "script_to_run" : [
                        "Descriptive analysis",
                        "Measure vs. Dimension",
                        "Predictive modeling",
                        "Trend",
                        "Descriptive analysis",
                        "Measure vs. Dimension",
                        "Predictive modeling",
                        "Trend"
                    ]
                }
            },
            "job_config" : {
                "get_config" : {
                    "action" : "get_config",
                    "method" : "GET"
                },
                "job_type" : "story",
                "job_url" : "http://madvisor.marlabsai.com:80/api/job/insight-bidco-sales-znlfl79g9e-w1kb64gs73/",
                "set_result" : {
                    "action" : "result",
                    "method" : "PUT"
                }
            },
            "deployEnv":"local"
        },
        "metaData" : {
            "config":{
                    'FILE_SETTINGS': {'inputfile': ['file:///home/gulshan/marlabs/datasets/3Yr_BIDCO.csv']},
                    'COLUMN_SETTINGS': {'analysis_type': ['metaData']}
                    },
            "job_config":{
                "job_type":"metaData",
                # "job_url": "http://localhost:8000/api/job/dataset-iriscsv-qpmercq3r8-2fjupdcwdu/",
                "job_url":"",
                "set_result": {
                    "method": "PUT",
                    "action": "result"
                  },
            },
            "deployEnv":"local"
        },
        "training":{
            "config":{
                'FILE_SETTINGS': {
                    'inputfile': ['file:///home/gulshan/marlabs/datasets/adult.csv'],
                    # Model Slug will go instead of model path
                    'modelpath': ["ANKUSH"],
                    'train_test_split' : [0.8],
                    'analysis_type' : ['training']
                },
                'COLUMN_SETTINGS': {
                    'analysis_type': ['training'],
                    'result_column': ['class_label'],
                    'consider_columns_type': ['excluding'],
                    'consider_columns':[],
                    'polarity': ['positive'],
                    'date_format': None,
                    # 'date_columns':["new_date","Month","Order Date"],
                    'date_columns':[],
                    'ignore_column_suggestions': [],
                    # 'ignore_column_suggestions': ["Outlet ID","Visibility to Cosumer","Cleanliness","Days to Resolve","Heineken Lager Share %","Issue Category","Outlet","Accessible_to_consumer","Resultion Status"],
                    'dateTimeSuggestions' : [],
                    'utf8ColumnSuggestion':[],
                    'consider_columns':[],
                }
            },
            "job_config":{
                "job_type":"training",
                # "job_url": "http://localhost:8000/api/job/dataset-iriscsv-qpmercq3r8-2fjupdcwdu/",
                "job_url": "http://localhost:8000/api/job/dataset-iriscsv-qpmercq3r8-2fjupdcwdu/",
                "set_result": {
                    "method": "PUT",
                    "action": "result"
                  },
            }
        },
        "prediction":{
            "config":{
                'FILE_SETTINGS': {
                    'inputfile': ['file:///home/gulshan/marlabs/datasets/adult_test.csv'],
                    'modelpath': ["ANKUSH"],
                    'scorepath': ["DDDDD"],
                    # 'train_test_split' : [0.8],
                    'levelcounts' : [],
                    'modelfeatures' : [],
                    "algorithmslug":["f77631ce2ab24cf78c55bb6a5fce4db8rf"],
                },
                'COLUMN_SETTINGS': {
                    'analysis_type': ['Dimension'],
                    'result_column': ['class_label'],
                    # 'consider_columns_type': ['excluding'],
                    # 'consider_columns':[],
                    # 'date_columns':['Date'],
                    'score_consider_columns_type': ['excluding'],
                    'score_consider_columns':[],
                    "app_id":[2]

                }
            },
            "job_config":{
                "job_type":"prediction",
                "job_url": "http://34.196.204.54:9012/api/job/score-hiohoyuo-bn1ofiupv0-j0irk37cob/set_result/",
                "set_result": {
                    "method": "PUT",
                    "action": "result"
                  },
            }
        }
    }
    ###### used to overwrite the passed config arguments to test locally ######

    # testConfigs = {
    #     "story":{
    #         "config" : {
    #             "COLUMN_SETTINGS" : {
    #                 "analysis_type" : [
    #                     "measure"
    #                 ],
    #                 "consider_columns" : [
    #                     "Month",
    #                     "Deal_Type",
    #                     "Source",
    #                     "Platform",
    #                     "Buyer_Age",
    #                     "Buyer_Gender",
    #                     "Order Date",
    #                     "Tenure_in_Days",
    #                     "Sales",
    #                     "Last_Transaction",
    #                     "new_date"
    #                 ],
    #                 "consider_columns_type" : [
    #                     "including"
    #                 ],
    #                 "dateTimeSuggestions" : [
    #                     {
    #                         "Month" : "%b-%y",
    #                         "Order Date" : "%d-%m-%Y"
    #                     }
    #                 ],
    #                 "date_columns" : [
    #                     "new_date"
    #                 ],
    #                 "date_format" : None,
    #                 "ignore_column_suggestion" : [],
    #                 "polarity" : [
    #                     "positive"
    #                 ],
    #                 "result_column" : [
    #                     "Sales"
    #                 ],
    #                 "utf8_column_suggestions" : []
    #             },
    #             "FILE_SETTINGS" : {
    #                 "inputfile" : [
    #                     "file:///home/gulshan/marlabs/datasets/trend_gulshan_small.csv"
    #                 ],
    #                 "script_to_run" : [
    #                     "Descriptive analysis",
    #                     'Measure vs. Dimension',
    #                     # "Predictive modeling",
    #                     # 'Measure vs. Measure',
    #                     # 'Dimension vs. Dimension',
    #                     "Trend"
    #                 ]
    #             }
    #         },
    #         "job_config" : {
    #             "get_config" : {
    #                 "action" : "get_config",
    #                 "method" : "GET"
    #             },
    #             "job_type" : "story",
    #             "job_url" : "",
    #             "set_result" : {
    #                 "action" : "result",
    #                 "method" : "PUT"
    #             }
    #         }
    #     },
    #     "story":{
    #         "config" : {
    #             "COLUMN_SETTINGS" : {
    #                 "analysis_type" : [
    #                     "measure"
    #                 ],
    #                 "consider_columns" : [
    #                     "Education",
    #                     "Top Organisation",
    #                     "Agent Name",
    #                     "Call Type",
    #                     "State",
    #                     "Region",
    #                     "Agent Experience",
    #                     "Rating",
    #                     "Agent Age",
    #                     "Top Plan Provider",
    #                     "Number of Calls",
    #                     "1st Time callers",
    #                     "No of resolved case",
    #                     "Call date"
    #                 ],
    #                 "consider_columns_type" : [
    #                     "including"
    #                 ],
    #                 "dateTimeSuggestions" : [
    #                     {}
    #                 ],
    #                 "date_columns" : [
    #                     "Call date"
    #                 ],
    #                 "date_format" : None,
    #                 "ignore_column_suggestion" : [
    #                     "Agent Name",
    #                     "State"
    #                 ],
    #                 "polarity" : [
    #                     "positive"
    #                 ],
    #                 "result_column" : [
    #                     "Number of Calls"
    #                 ],
    #                 "utf8_column_suggestions" : []
    #             },
    #             "FILE_SETTINGS" : {
    #                 "inputfile" : [
    #                     "file:///home/gulshan/marlabs/datasets/Callcentre4.csv"
    #                     ],
    #                 "script_to_run" : [
    #                     "Descriptive analysis",
    #                     "Measure vs. Dimension",
    #                     "Measure vs. Measure",
    #                     "Predictive model",
    #                     "Trend"
    #                 ]
    #             }
    #         },
    #         "job_config" : {
    #             "get_config" : {
    #                 "action" : "get_config",
    #                 "method" : "GET"
    #             },
    #             "job_type" : "story",
    #             "job_url" : "http://i/job/insight-call-centre-analysis-v3-qtvziiyszm-7qmhc24pn6/",
    #             "set_result" : {
    #                 "action" : "result",
    #                 "method" : "PUT"
    #             }
    #         }
    #     },
    #     "training":{
    #         "config" : {
    #             "COLUMN_SETTINGS" : {
    #                 "consider_columns" : [
    #                     "Subgroup",
    #                     "Group",
    #                     "Region",
    #                     "Market Route",
    #                     "Size By Revenue",
    #                     "Size By Employees",
    #                     "Revenue",
    #                     "Competitor Type",
    #                     "Deal Size Category",
    #                     "Opportunity Result",
    #                     "Elapsed Day",
    #                     "Sales Stage Change Count",
    #                     "Closing Days",
    #                     "Qualified Days",
    #                     "Amount USD"
    #                 ],
    #                 "consider_columns_type" : [
    #                     "including"
    #                 ],
    #                 "dateTimeSuggestions" : [
    #                     {}
    #                 ],
    #                 "date_columns" : [],
    #                 "date_format" : None,
    #                 "ignore_column_suggestion" : [],
    #                 "polarity" : [
    #                     "positive"
    #                 ],
    #                 "result_column" : [
    #                     "Opportunity Result"
    #                 ],
    #                 "utf8_column_suggestions" : []
    #             },
    #             "FILE_SETTINGS" : {
    #                 "analysis_type" : [
    #                     "training"
    #                 ],
    #                 "inputfile" : [
    #                     "file:///home/gulshan/marlabs/datasets/Opportunity_train.csv"
    #                 ],
    #                 "modelpath" : [
    #                     "opportunity-scoring-9bnwpew23j"
    #                 ],
    #                 "train_test_split" : [
    #                     0.72
    #                 ]
    #             }
    #         },
    #         "job_config" : {
    #             "get_config" : {
    #                 "action" : "get_config",
    #                 "method" : "GET"
    #             },
    #             "job_type" : "training",
    #             "job_url" : "http://34.196.204.54:9012/api/job/trainer-opportunity-scoring-9bnwpew23j-8k8o4rcsuh/",
    #             "set_result" : {
    #                 "action" : "result",
    #                 "method" : "PUT"
    #             }
    #         }
    #     },
    #     "prediction":{
    #         "config" : {
    #             "COLUMN_SETTINGS" : {
    #                 "app_id" : [
    #                     1
    #                 ],
    #                 "dateTimeSuggestions" : [
    #                     {}
    #                 ],
    #                 "date_columns" : [],
    #                 "date_format" : None,
    #                 "ignore_column_suggestion" : [],
    #                 "polarity" : [
    #                     "positive"
    #                 ],
    #                 "result_column" : [
    #                     "Opportunity Result"
    #                 ],
    #                 "score_consider_columns" : [
    #                     "Subgroup",
    #                     "Group",
    #                     "Region",
    #                     "Market Route",
    #                     "Size By Revenue",
    #                     "Size By Employees",
    #                     "Revenue",
    #                     "Competitor Type",
    #                     "Deal Size Category",
    #                     "Elapsed Day",
    #                     "Sales Stage Change Count",
    #                     "Closing Days",
    #                     "Qualified Days",
    #                     "Amount USD"
    #                 ],
    #                 "score_consider_columns_type" : [
    #                     "including"
    #                 ],
    #                 "utf8_column_suggestions" : []
    #             },
    #             "FILE_SETTINGS" : {
    #                 "algorithmslug" : [
    #                     "f77631ce2ab24cf78c55bb6a5fce4db8rf"
    #                 ],
    #                 "analysis_type" : [
    #                     "score"
    #                 ],
    #                 "inputfile" : [
    #                     "file:///home/gulshan/marlabs/datasets/Opportunity_test.csv"
    #                 ],
    #                 "levelcounts" : [],
    #                 "modelfeatures" : [],
    #                 "modelpath" : [
    #                     "opportunity-scoring-9bnwpew23j"
    #                 ],
    #                 "scorepath" : [
    #                     "score-ufehtfv31y"
    #                 ]
    #             }
    #         },
    #         "job_config" : {
    #             "get_config" : {
    #                 "action" : "get_config",
    #                 "method" : "GET"
    #             },
    #             "job_type" : "prediction",
    #             "job_url" : "http://34.196.204.54:9012/api/job/score-score-ufehtfv31y-12g2ccgwi9/",
    #             "set_result" : {
    #                 "action" : "result",
    #                 "method" : "PUT"
    #             }
    #         }
    #     },
    #     "training":{
    #         "config" : {
    #             "COLUMN_SETTINGS" : {
    #                 "consider_columns" : [
    #                     "BusinessTravel",
    #                     "Department",
    #                     "Education",
    #                     "EducationField",
    #                     "EnvironmentSatisfaction",
    #                     "Gender",
    #                     "JobInvolvement",
    #                     "JobRole",
    #                     "JobSatisfaction",
    #                     "MaritalStatus",
    #                     "Over18",
    #                     "OverTime",
    #                     "PerformanceRating",
    #                     "RelationshipSatisfaction",
    #                     "WorkLifeBalance",
    #                     "Attrition",
    #                     "Age",
    #                     "DailyRate",
    #                     "DistanceFromHome",
    #                     "EmployeeCount",
    #                     "EmployeeNumber",
    #                     "HourlyRate",
    #                     "JobLevel",
    #                     "MonthlyIncome",
    #                     "MonthlyRate",
    #                     "NumCompaniesWorked",
    #                     "PercentSalaryHike",
    #                     "StandardHours",
    #                     "StockOptionLevel",
    #                     "TotalWorkingYears",
    #                     "TrainingTimesLastYear",
    #                     "YearsAtCompany",
    #                     "YearsInCurrentRole",
    #                     "YearsSinceLastPromotion",
    #                     "YearsWithCurrManager"
    #                 ],
    #                 "consider_columns_type" : [
    #                     "including"
    #                 ],
    #                 "dateTimeSuggestions" : [
    #                     {}
    #                 ],
    #                 "date_columns" : [],
    #                 "date_format" : None,
    #                 "ignore_column_suggestion" : [
    #                     "EmployeeCount",
    #                     "StandardHours",
    #                     "EmployeeNumber",
    #                     "Over18"
    #                 ],
    #                 "polarity" : [
    #                     "positive"
    #                 ],
    #                 "result_column" : [
    #                     "Attrition"
    #                 ],
    #                 "utf8_column_suggestions" : []
    #             },
    #             "FILE_SETTINGS" : {
    #                 "analysis_type" : [
    #                     "training"
    #                 ],
    #                 "inputfile" : [
    #                     "file:///home/gulshan/marlabs/datasets/EmployeeAttrition_Train.csv"
    #                 ],
    #                 "modelpath" : [
    #                     "attrition-gulshan-44ik5bjdt8"
    #                 ],
    #                 "train_test_split" : [
    #                     0.71
    #                 ]
    #             }
    #         },
    #         "job_config" : {
    #             "get_config" : {
    #                 "action" : "get_config",
    #                 "method" : "GET"
    #             },
    #             "job_type" : "training",
    #             "job_url" : "http://34.196.204.54:9012/api/job/trainer-attrition-gulshan-44ik5bjdt8-flqzktpfzx/",
    #             "set_result" : {
    #                 "action" : "result",
    #                 "method" : "PUT"
    #             }
    #         }
    #     },
    #     "prediction":{
    #         "config" : {
    #             "COLUMN_SETTINGS" : {
    #                 "app_id" : [
    #                     1
    #                 ],
    #                 "dateTimeSuggestions" : [
    #                     {}
    #                 ],
    #                 "date_columns" : [],
    #                 "date_format" : None,
    #                 "ignore_column_suggestion" : [
    #                     "EmployeeCount",
    #                     "StandardHours",
    #                     "EmployeeNumber",
    #                     "Over18"
    #                 ],
    #                 "polarity" : [
    #                     "positive"
    #                 ],
    #                 "result_column" : [
    #                     "Attrition"
    #                 ],
    #                 "consider_columns" : [
    #                     "BusinessTravel",
    #                     "Department",
    #                     "Education",
    #                     "EducationField",
    #                     "EnvironmentSatisfaction",
    #                     "Gender",
    #                     "JobInvolvement",
    #                     "JobRole",
    #                     "JobSatisfaction",
    #                     "MaritalStatus",
    #                     "Over18",
    #                     "OverTime",
    #                     "PerformanceRating",
    #                     "RelationshipSatisfaction",
    #                     "WorkLifeBalance",
    #                     "Age",
    #                     "DailyRate",
    #                     "DistanceFromHome",
    #                     "EmployeeCount",
    #                     "EmployeeNumber",
    #                     "HourlyRate",
    #                     "JobLevel",
    #                     "MonthlyIncome",
    #                     "MonthlyRate",
    #                     "NumCompaniesWorked",
    #                     "PercentSalaryHike",
    #                     "StandardHours",
    #                     "StockOptionLevel",
    #                     "TotalWorkingYears",
    #                     "TrainingTimesLastYear",
    #                     "YearsAtCompany",
    #                     "YearsInCurrentRole",
    #                     "YearsSinceLastPromotion",
    #                     "YearsWithCurrManager"
    #                 ],
    #                 "consider_columns_type" : [
    #                     "including"
    #                 ],
    #                 "score_consider_columns" : [
    #                     "BusinessTravel",
    #                     "Department",
    #                     "Education",
    #                     "EducationField",
    #                     "EnvironmentSatisfaction",
    #                     "Gender",
    #                     "JobInvolvement",
    #                     "JobRole",
    #                     "JobSatisfaction",
    #                     "MaritalStatus",
    #                     "Over18",
    #                     "OverTime",
    #                     "PerformanceRating",
    #                     "RelationshipSatisfaction",
    #                     "WorkLifeBalance",
    #                     "Age",
    #                     "DailyRate",
    #                     "DistanceFromHome",
    #                     "EmployeeCount",
    #                     "EmployeeNumber",
    #                     "HourlyRate",
    #                     "JobLevel",
    #                     "MonthlyIncome",
    #                     "MonthlyRate",
    #                     "NumCompaniesWorked",
    #                     "PercentSalaryHike",
    #                     "StandardHours",
    #                     "StockOptionLevel",
    #                     "TotalWorkingYears",
    #                     "TrainingTimesLastYear",
    #                     "YearsAtCompany",
    #                     "YearsInCurrentRole",
    #                     "YearsSinceLastPromotion",
    #                     "YearsWithCurrManager"
    #                 ],
    #                 "score_consider_columns_type" : [
    #                     "including"
    #                 ],
    #                 "utf8_column_suggestions" : []
    #             },
    #             "FILE_SETTINGS" : {
    #                 "algorithmslug" : [
    #                     "f77631ce2ab24cf78c55bb6a5fce4db8rf"
    #                 ],
    #                 "analysis_type" : [
    #                     "score"
    #                 ],
    #                 "inputfile" : [
    #                     "file:///home/gulshan/marlabs/datasets/EmployeeAttrition_Test.csv"
    #                 ],
    #                 "levelcounts" : [],
    #                 "modelfeatures" : [],
    #                 "modelpath" : [
    #                     "attrition-gulshan-44ik5bjdt8"
    #                 ],
    #                 "scorepath" : [
    #                     "attrition-score-kxnbufg39v"
    #                 ]
    #             }
    #         },
    #         "job_config" : {
    #             "get_config" : {
    #                 "action" : "get_config",
    #                 "method" : "GET"
    #             },
    #             "job_type" : "prediction",
    #             "job_url" : "http://34.196.204.54:9012/api/job/score-attrition-score-kxnbufg39v-8zkfvynoad/",
    #             "set_result" : {
    #                 "action" : "result",
    #                 "method" : "PUT"
    #             }
    #         }
    #         }
    # }
    # if "deployEnv" in configJson:
    # configJson = testConfigs["story"]

    ######################## Craeting Spark Session ###########################
    start_time = time.time()
    APP_NAME = 'mAdvisor'
    spark = CommonUtils.get_spark_session(app_name=APP_NAME)
    spark.sparkContext.setLogLevel("ERROR")
    ######################### Creating the configs #############################
    config = configJson["config"]
    job_config = configJson["job_config"]
    configJsonObj = configparser.ParserConfig(config)
    configJsonObj.set_json_params()
    dataframe_context = ContextSetter(configJsonObj)
    dataframe_context.set_params()
    jobType = job_config["job_type"]
    ########################## Load the dataframe ##############################
    df = DataLoader.load_csv_file(spark, dataframe_context.get_input_file())
    print "FILE LOADED: ", dataframe_context.get_input_file()
    data_load_time = time.time() - start_time
    script_start_time = time.time()

    if jobType == "metaData":
        print "starting Metadata"
        meta_data_class = MetaDataScript(df,spark)
        meta_data_object = meta_data_class.run()
        metaDataJson = CommonUtils.convert_python_object_to_json(meta_data_object)
        print metaDataJson
        response = CommonUtils.save_result_json(configJson["job_config"]["job_url"],metaDataJson)
        return response
    else:
        analysistype = dataframe_context.get_analysis_type()
        print "ANALYSIS TYPE : ", analysistype
        scripts_to_run = dataframe_context.get_scripts_to_run()
        if scripts_to_run==None:
            scripts_to_run = []
        appid = dataframe_context.get_app_id()
        df_helper = DataFrameHelper(df, dataframe_context)
        df_helper.set_params()
        df = df_helper.get_data_frame()
        measure_columns = df_helper.get_numeric_columns()
        dimension_columns = df_helper.get_string_columns()

    LOGGER.append("jobtype: {}".format(jobType))

    if jobType == "story":
        #Initializing the result_setter
        result_setter = ResultSetter(df,dataframe_context)
        story_narrative = NarrativesTree()
        story_narrative.set_name("{} Performance Report".format(dataframe_context.get_result_column()))
        LOGGER.append("analysistype {}".format(analysistype))

        if analysistype == 'dimension':
            print "STARTING DIMENSION ANALYSIS ..."
            LOGGER.append("STARTING DIMENSION ANALYSIS ...")
            df_helper.remove_null_rows(dataframe_context.get_result_column())
            df = df_helper.get_data_frame()

            if ('Descriptive analysis' in scripts_to_run):
                try:
                    fs = time.time()
                    freq_obj = FreqDimensionsScript(df, df_helper, dataframe_context, spark, story_narrative,result_setter)
                    freq_obj.Run()
                    print "Frequency Analysis Done in ", time.time() - fs,  " seconds."
                except Exception as e:
                    print "Frequency Analysis Failed "
                    print "#####ERROR#####"*5
                    print e
                    print "#####ERROR#####"*5
            else:
                print "Descriptive analysis Not in Scripts to run "

            if ('Dimension vs. Dimension' in scripts_to_run):
                try:
                    fs = time.time()
                    chisquare_obj = ChiSquareScript(df, df_helper, dataframe_context, spark, story_narrative,result_setter)
                    chisquare_obj.Run()
                    print "ChiSquare Analysis Done in ", time.time() - fs, " seconds."
                except Exception as e:
                    print "ChiSquare Analysis Failed "
                    print "#####ERROR#####"*5
                    print e
                    print "#####ERROR#####"*5
            else:
                print "Dimension vs. Dimension Not in Scripts to run "

            if ('Trend' in scripts_to_run):
                try:
                    fs = time.time()
                    trend_obj = TrendScript(df_helper, dataframe_context, result_setter, spark, story_narrative)
                    trend_obj.Run()
                    print "Trend Analysis Done in ", time.time() - fs, " seconds."

                except Exception as e:
                    print "Trend Script Failed"
                    print "#####ERROR#####"*5
                    print e
                    print "#####ERROR#####"*5
            else:
                print "Trend not in scripts to run"

            if ('Predictive modeling' in scripts_to_run):
                try:
                    fs = time.time()
                    if df_helper.ignorecolumns != None:
                        df_helper.drop_ignore_columns()
                    df_helper.fill_na_dimension_nulls()
                    df = df_helper.get_data_frame()
                    decision_tree_obj = DecisionTreeScript(df, df_helper, dataframe_context, spark, story_narrative,result_setter)
                    decision_tree_obj.Run()
                    print "DecisionTrees Analysis Done in ", time.time() - fs, " seconds."
                except Exception as e:
                    print "DecisionTrees Analysis Failed"
                    print "#####ERROR#####"*5
                    print e
                    print "#####ERROR#####"*5
            else:
                print "Predictive modeling Not in Scripts to run"

            ordered_node_name_list = ["Overview","Trend","Association","Prediction"]
            # story_narrative.reorder_nodes(ordered_node_name_list)
            dimensionResult = CommonUtils.convert_python_object_to_json(story_narrative)
            # dimensionResult = CommonUtils.as_dict(story_narrative)
            # print dimensionResult

            headNode = result_setter.get_head_node()
            if headNode != None:
                headNode = json.loads(CommonUtils.convert_python_object_to_json(headNode))
            dimensionNode = result_setter.get_distribution_node()
            if dimensionNode != None:
                headNode["listOfNodes"].append(dimensionNode)
            trendNode = result_setter.get_trend_node()
            if trendNode != None:
                headNode["listOfNodes"].append(trendNode)
            chisquareNode = result_setter.get_chisquare_node()
            if chisquareNode != None:
                headNode["listOfNodes"].append(chisquareNode)

            decisionTreeNode = result_setter.get_decision_tree_node()
            if decisionTreeNode != None:
                headNode["listOfNodes"].append(decisionTreeNode)

            print json.dumps(headNode,indent=2)
            response = CommonUtils.save_result_json(configJson["job_config"]["job_url"],json.dumps(headNode))

            # response = CommonUtils.save_result_json(configJson["job_config"]["job_url"],dimensionResult)

            return response

        elif analysistype == 'measure':
            print "STARTING MEASURE ANALYSIS ..."
            LOGGER.append("STARTING MEASURE ANALYSIS ...")
            df_helper.remove_null_rows(dataframe_context.get_result_column())
            df = df_helper.get_data_frame()
            story_narrative.set_name("Measure analysis")
            LOGGER.append("scripts_to_run:: {}".format(",".join(scripts_to_run)))
            if ('Descriptive analysis' in scripts_to_run):
                try:
                    fs = time.time()
                    descr_stats_obj = DescriptiveStatsScript(df, df_helper, dataframe_context, result_setter, spark,story_narrative)
                    LOGGER.append("DescriptiveStats Analysis  Starting")
                    descr_stats_obj.Run()
                    LOGGER.append("DescriptiveStats Analysis Done in {} seconds.".format(time.time() - fs ))
                    print "DescriptiveStats Analysis Done in ", time.time() - fs, " seconds."
                except Exception as e:
                    LOGGER.append("got exception {}".format(e))
                    print 'Descriptive Failed'
                    print "#####ERROR#####"*5
                    print e
                    print "#####ERROR#####"*5

                try:
                    fs = time.time()
                    histogram_obj = HistogramsScript(df, df_helper, dataframe_context, spark)
                    histogram_obj.Run()
                    print "Histogram Analysis Done in ", time.time() - fs, " seconds."
                except Exception as e:
                    print "#####ERROR#####"*5
                    print e
                    print "#####ERROR#####"*5
                try:
                    fs = time.time()
                    d_histogram_obj = DensityHistogramsScript(df, df_helper, dataframe_context, spark)
                    d_histogram_obj.Run()
                    print "Density Histogram Analysis Done in ", time.time() - fs, " seconds."
                except Exception as e:
                    print 'Density Histogram Failed'
                    print "#####ERROR#####"*5
                    print e
                    print "#####ERROR#####"*5

            if df_helper.ignorecolumns != None:
                df_helper.drop_ignore_columns()
            measure_columns = df_helper.get_numeric_columns()
            dimension_columns = df_helper.get_string_columns()
            df = df_helper.get_data_frame()
            #df = df.na.drop(subset=dataframe_context.get_result_column())
            if len(dimension_columns)>0 and 'Measure vs. Dimension' in scripts_to_run:
                try:
                    fs = time.time()
                    # one_way_anova_obj = OneWayAnovaScript(df, df_helper, dataframe_context, spark)
                    # one_way_anova_obj.Run()
                    two_way_obj = TwoWayAnovaScript(df, df_helper, dataframe_context, result_setter, spark,story_narrative)
                    two_way_obj.Run()
                    print "OneWayAnova Analysis Done in ", time.time() - fs, " seconds."
                except Exception as e:
                    print 'Anova Failed'
                    print "#####ERROR#####"*5
                    print e
                    print "#####ERROR#####"*5

            if len(measure_columns)>1 and 'Measure vs. Measure' in scripts_to_run:
                LOGGER.append("Starting Measure Vs. Measure analysis")
                try:
                    fs = time.time()
                    correlation_obj = CorrelationScript(df, df_helper, dataframe_context, spark)
                    correlations = correlation_obj.Run()
                    print "Correlation Analysis Done in ", time.time() - fs ," seconds."

                    try:
                        df = df.na.drop(subset=measure_columns)
                        fs = time.time()
                        regression_obj = RegressionScript(df, df_helper, dataframe_context, result_setter, spark, correlations, story_narrative)
                        regression_obj.Run()
                        print "Regression Analysis Done in ", time.time() - fs, " seconds."
                    except Exception as e:

                        LOGGER.append("got exception {}".format(e))
                        LOGGER.append("detailed exception {}".format(traceback.format_exc()))

                        print 'Regression Failed'
                        print "#####ERROR#####"*5
                        print e
                        print "#####ERROR#####"*5

                except Exception as e:
                    LOGGER.append("got exception {}".format(e))
                    LOGGER.append("detailed exception {}".format(traceback.format_exc()))
                    print 'Correlation Failed. Regression not executed'
                    print "#####ERROR#####"*5
                    print e
                    print "#####ERROR#####"*5
            else:
                print 'Regression not in Scripts to run'
            if ('Trend' in scripts_to_run):
                try:
                    fs = time.time()
                    trend_obj = TrendScript(df_helper,dataframe_context,result_setter,spark,story_narrative)
                    trend_obj.Run()
                    print "Trend Analysis Done in ", time.time() - fs, " seconds."

                except Exception as e:
                    LOGGER.append("got exception {}".format(e))
                    LOGGER.append("detailed exception {}".format(traceback.format_exc()))
                    print "Trend Script Failed"
                    print "#####ERROR#####"*5
                    print e
                    print "#####ERROR#####"*5

            if ('Predictive modeling' in scripts_to_run):
                try:
                    LOGGER.append("starting dtree")
                    fs = time.time()
                    df_helper.fill_na_dimension_nulls()
                    df = df_helper.get_data_frame()
                    dt_reg = DecisionTreeRegressionScript(df, df_helper, dataframe_context, result_setter, spark,story_narrative)
                    dt_reg.Run()
                    print "DecisionTrees Analysis Done in ", time.time() - fs, " seconds."
                except Exception as e:
                    LOGGER.append("got exception {}".format(e))
                    LOGGER.append("detailed exception {}".format(traceback.format_exc()))
                    print "#####ERROR#####"*5
                    print e
                    print "#####ERROR#####"*5
                    print "Decision Tree Regression Script Failed"
            # try:
            #     fs = time.time()
            #     exec_obj = ExecutiveSummaryScript(df_helper,dataframe_context,result_setter,spark)
            #     exec_obj.Run()
            #     print "Executive Summary Done in ", time.time() - fs, " seconds."
            # except Exception as e:
            #     print "#####ERROR#####"*5
            #     print e
            #     print "#####ERROR#####"*5
            #     print "Executive Summary Script Failed"

            measureResult = CommonUtils.convert_python_object_to_json(story_narrative)
            # dimensionResult = CommonUtils.as_dict(story_narrative)
            # print measureResult
            # response = CommonUtils.save_result_json(configJson["job_config"]["job_url"],measureResult)
            headNode = result_setter.get_head_node()
            if headNode != None:
                headNode = json.loads(CommonUtils.convert_python_object_to_json(headNode))
            distributionNode = result_setter.get_distribution_node()
            if distributionNode != None:
                headNode["listOfNodes"].append(distributionNode)
            trendNode = result_setter.get_trend_node()
            if trendNode != None:
                headNode["listOfNodes"].append(trendNode)
            anovaNode = result_setter.get_anova_node()
            if anovaNode != None:
                headNode["listOfNodes"].append(anovaNode)
            regressionNode = result_setter.get_regression_node()
            if regressionNode != None:
                headNode["listOfNodes"].append(regressionNode)
            decisionTreeNode = result_setter.get_decision_tree_node()
            if decisionTreeNode != None:
                headNode["listOfNodes"].append(decisionTreeNode)
            print json.dumps(headNode)
            response = CommonUtils.save_result_json(configJson["job_config"]["job_url"],json.dumps(headNode))
            return response

    elif jobType == 'training':
        prediction_narrative = NarrativesTree()
        prediction_narrative.set_name("models")
        result_setter = ResultSetter(df,dataframe_context)
        df_helper.remove_null_rows(dataframe_context.get_result_column())
        df = df_helper.get_data_frame()
        df = df_helper.fill_missing_values(df)
        categorical_columns = df_helper.get_string_columns()
        result_column = dataframe_context.get_result_column()
        df = df.toPandas()
        df = MLUtils.factorize_columns(df,[x for x in categorical_columns if x != result_column])
        df_helper.set_train_test_data(df)
        model_slug = dataframe_context.get_model_path()
        # model_slug = "slug1"
        basefoldername = "mAdvisorModels"
        subfolders = MLUtils.slug_model_mapping().keys()
        model_file_path = MLUtils.create_model_folders(model_slug,basefoldername,subfolders=subfolders)
        dataframe_context.set_model_path(model_file_path)

        try:
            st = time.time()
            rf_obj = RandomForestScript(df, df_helper, dataframe_context, spark, prediction_narrative,result_setter)
            # rf_obj = RandomForestPysparkScript(df, df_helper, dataframe_context, spark, prediction_narrative,result_setter)
            rf_obj.Train()
            print "Random Forest Model Done in ", time.time() - st,  " seconds."
        except Exception as e:
            LOGGER.append("got exception {}".format(e))
            LOGGER.append("detailed exception {}".format(traceback.format_exc()))
            print "Random Forest Model Failed"
            print "#####ERROR#####"*5
            print e
            print "#####ERROR#####"*5

        try:
            st = time.time()
            lr_obj = LogisticRegressionScript(df, df_helper, dataframe_context, spark, prediction_narrative,result_setter)
            # lr_obj = LogisticRegressionPysparkScript(df, df_helper, dataframe_context, spark, prediction_narrative,result_setter)
            lr_obj.Train()
            print "Logistic Regression Model Done in ", time.time() - st,  " seconds."
        except Exception as e:
            LOGGER.append("got exception {}".format(e))
            LOGGER.append("detailed exception {}".format(traceback.format_exc()))
            print "Logistic Regression Model Failed"
            print "#####ERROR#####"*5
            print e
            print "#####ERROR#####"*5

        try:
            st = time.time()
            xgb_obj = XgboostScript(df, df_helper, dataframe_context, spark, prediction_narrative,result_setter)
            xgb_obj.Train()
            print "XGBoost Model Done in ", time.time() - st,  " seconds."
        except Exception as e:
            LOGGER.append("got exception {}".format(e))
            LOGGER.append("detailed exception {}".format(traceback.format_exc()))
            print "Xgboost Model Failed"
            print "#####ERROR#####"*5
            print e
            print "#####ERROR#####"*5


        collated_summary = result_setter.get_model_summary()

        card1 = NormalCard()
        card1Data = [HtmlData(data="<h4>Model Summary</h4>")]
        card1Data.append(HtmlData(data = MLUtils.get_total_models(collated_summary)))
        card1.set_card_data(card1Data)
        # prediction_narrative.insert_card_at_given_index(card1,0)
        card1 = json.loads(CommonUtils.convert_python_object_to_json(card1))

        card2 = NormalCard()
        card2_elements = MLUtils.get_model_comparison(collated_summary)
        card2Data = [card2_elements[0],card2_elements[1]]
        card2.set_card_data(card2Data)
        # prediction_narrative.insert_card_at_given_index(card2,1)
        card2 = json.loads(CommonUtils.convert_python_object_to_json(card2))


        card3 = NormalCard()
        card3Data = [HtmlData(data="<h5 class = 'sm-ml-15 sm-pb-10'>Feature Importance</h5>")]
        card3Data.append(MLUtils.get_feature_importance(collated_summary))
        card3.set_card_data(card3Data)
        # prediction_narrative.insert_card_at_given_index(card3,2)
        card3 = json.loads(CommonUtils.convert_python_object_to_json(card3))


        modelResult = CommonUtils.convert_python_object_to_json(prediction_narrative)
        modelResult = json.loads(modelResult)
        existing_cards = modelResult["listOfCards"]
        existing_cards = result_setter.get_all_algos_cards()

        # modelResult["listOfCards"] = [card1,card2,card3] + existing_cards
        # print modelResult
        all_cards = [card1,card2,card3] + existing_cards

        modelResult = NarrativesTree()
        modelResult.add_cards(all_cards)
        modelResult = CommonUtils.convert_python_object_to_json(modelResult)
        modelJsonOutput = ModelSummary()
        modelJsonOutput.set_model_summary(json.loads(modelResult))

        rfModelSummary = result_setter.get_random_forest_model_summary()
        lrModelSummary = result_setter.get_logistic_regression_model_summary()
        xgbModelSummary = result_setter.get_xgboost_model_summary()
        model_dropdowns = []
        model_configs = {"target_variable":[result_column]}
        model_features = {}
        for obj in [rfModelSummary,lrModelSummary,xgbModelSummary]:
            if obj != {}:
                print obj["levelcount"]
                model_dropdowns.append(obj["dropdown"])
                model_features[obj["dropdown"]["slug"]] = obj["modelFeatures"]
                model_configs["dimensionLevelCount"] = obj["levelcount"]
        model_configs["modelFeatures"] = model_features
        print model_configs

        modelJsonOutput.set_model_dropdown(model_dropdowns)
        modelJsonOutput.set_model_config(model_configs)
        modelJsonOutput = modelJsonOutput.get_json_data()
        print modelJsonOutput
        response = CommonUtils.save_result_json(configJson["job_config"]["job_url"],json.dumps(modelJsonOutput))
        return response

    elif jobType == 'prediction':
        st = time.time()
        story_narrative = NarrativesTree()
        story_narrative.set_name("scores")
        result_setter = ResultSetter(df,dataframe_context)
        model_path = dataframe_context.get_model_path()
        print "model path",model_path
        result_column = dataframe_context.get_result_column()
        if result_column in df.columns:
            df_helper.remove_null_rows(result_column)
        df = df_helper.get_data_frame()
        df = df_helper.fill_missing_values(df)
        # model_slug = dataframe_context.get_model_slug()
        model_slug = model_path
        score_slug = dataframe_context.get_score_path()
        print "score_slug",score_slug
        # score_slug = dataframe_context.get_score_slug()
        basefoldername = "mAdvisorScores"
        score_file_path = MLUtils.create_scored_data_folder(score_slug,basefoldername)

        algorithm_name_list = ["randomforest","xgboost","logisticregression"]
        # algorithm_name = "randomforest"
        algorithm_name = dataframe_context.get_algorithm_slug()[0]
        print "algorithm_name",algorithm_name
        model_path = score_file_path.split(basefoldername)[0]+"/mAdvisorModels/"+model_slug+"/"+algorithm_name
        dataframe_context.set_model_path(model_path)
        dataframe_context.set_score_path(score_file_path)
        dataframe_context.set_model_path(model_path)

        selected_model_for_prediction = [MLUtils.slug_model_mapping()[algorithm_name]]
        print selected_model_for_prediction
        if "randomforest" in selected_model_for_prediction:
            df = df.toPandas()
            trainedModel = RandomForestScript(df, df_helper, dataframe_context, spark, story_narrative,result_setter)
            # trainedModel = RandomForestPysparkScript(df, df_helper, dataframe_context, spark)
            trainedModel.Predict()
            print "Scoring Done in ", time.time() - st,  " seconds."
        elif "xgboost" in selected_model_for_prediction:
            df = df.toPandas()
            trainedModel = XgboostScript(df, df_helper, dataframe_context, spark, story_narrative,result_setter)
            trainedModel.Predict()
            print "Scoring Done in ", time.time() - st,  " seconds."
        elif "logisticregression" in selected_model_for_prediction:
            df = df.toPandas()
            trainedModel = LogisticRegressionScript(df, df_helper, dataframe_context, spark, story_narrative,result_setter)
            # trainedModel = LogisticRegressionPysparkScript(df, df_helper, dataframe_context, spark)
            trainedModel.Predict()
            print "Scoring Done in ", time.time() - st,  " seconds."
        else:
            print "Could Not Load the Model for Scoring"

        # scoreSummary = CommonUtils.convert_python_object_to_json(story_narrative)

        storycards = result_setter.get_score_cards()
        storyNode = NarrativesTree()
        storyNode.add_cards(storycards)
        # storyNode = {"listOfCards":[storycards],"listOfNodes":[],"name":None,"slug":None}
        scoreSummary = CommonUtils.convert_python_object_to_json(storyNode)
        print scoreSummary
        response = CommonUtils.save_result_json(configJson["job_config"]["job_url"],scoreSummary)
        return response

    print "Scripts Time : ", time.time() - script_start_time, " seconds."
    print "Data Load Time : ", data_load_time, " seconds."
    #spark.stop()
    return (" "+ "="*100 + " ").join(LOGGER)

if __name__ == '__main__':
    main(sys.argv[1])
    print 'Main Method End .....'
