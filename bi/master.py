import os
import sys
import time
import json
import pyhocon
import traceback

# from asn1crypto._ffi import None
# from pyhocon.tool import HOCONConverter

reload(sys)
sys.setdefaultencoding('utf-8')
import ConfigParser

from bi.common import utils as CommonUtils
from bi.settings import *
from bi.common import DataLoader,MetaParser,DataWriter,DataFrameHelper,ContextSetter,ResultSetter
from bi.scripts.frequency_dimensions import FreqDimensionsScript
from bi.scripts.chisquare import ChiSquareScript
from bi.scripts.decision_tree import DecisionTreeScript
from bi.scripts.correlation import CorrelationScript
from bi.scripts.descr_stats import DescriptiveStatsScript
from bi.scripts.density_histogram import DensityHistogramsScript
from bi.scripts.histogram import HistogramsScript
from bi.scripts.two_way_anova import TwoWayAnovaScript
from bi.scripts.linear_regression import LinearRegressionScript
from bi.scripts.timeseries import TrendScript
from bi.scripts.random_forest import RandomForestScript
from bi.scripts.xgboost_classification import XgboostScript
from bi.scripts.logistic_regression import LogisticRegressionScript
from bi.scripts.decision_tree_regression import DecisionTreeRegressionScript
from bi.scripts.executive_summary import ExecutiveSummaryScript
from bi.algorithms import utils as MLUtils
from bi.scripts.random_forest_pyspark import RandomForestPysparkScript
from bi.scripts.logistic_regression_pyspark import LogisticRegressionPysparkScript
from bi.scripts.metadata import MetaDataScript
from bi.common import NarrativesTree
from bi.common import NormalCard,SummaryCard,NarrativesTree,HtmlData,C3ChartData,TableData,TreeData,ModelSummary
from bi.transformations import DataFrameFilterer
from bi.transformations import DataFrameTransformer
from parser import configparser
from pyspark.sql.functions import col, udf
from bi.scripts.stock_advisor import StockAdvisor
#if __name__ == '__main__':
def main(configJson):
    LOGGER = {}
    deployEnv = False  # running the scripts from job-server env
    debugMode = True   # runnning the scripts for local testing and development
    cfgMode = False    # runnning the scripts by passing config.cfg path
    script_start_time = time.time()
    if isinstance(configJson,pyhocon.config_tree.ConfigTree) or isinstance(configJson,dict):
        deployEnv = True
        debugMode = False
        ignoreMsg = False
    elif isinstance(configJson,basestring):
        if configJson.endswith(".cfg"):
            ######################## Running in cfgMode ########################
            cfgMode = True
            debugMode = False
            ignoreMsg = False
        else:
            ######################## Running in debugMode ######################
            print "Running in debugMode"
            cfgMode = False
            debugMode = True
            ignoreMsg = False
            # Test Configs are defined in bi/settings/config.py
            jobType = "story"
            configJson = get_test_configs(jobType)

    ######################## Craeting Spark Session ###########################
    if debugMode:
        APP_NAME = "mAdvisor_running_in_debug_mode"
    else:
        if "job_config" in configJson.keys() and "job_name" in configJson["job_config"].keys():
            APP_NAME = configJson["job_config"]["job_name"]
        else:
            APP_NAME = "--missing--"

    spark = CommonUtils.get_spark_session(app_name=APP_NAME)
    spark.sparkContext.setLogLevel("ERROR")
    ######################### Creating the configs #############################

    config = configJson["config"]
    job_config = configJson["job_config"]

    configJsonObj = configparser.ParserConfig(config)
    configJsonObj.set_json_params()
    dataframe_context = ContextSetter(configJsonObj)
    dataframe_context.set_params()
    if debugMode == True:
        dataframe_context.set_environment("debugMode")
        dataframe_context.set_message_ignore(True)
        ignoreMsg = True
    jobType = job_config["job_type"]
    try:
        errorURL = job_config["error_reporting_url"]+APP_NAME+"/"
    except:
        errorURL = None
    messageUrl = configJson["job_config"]["message_url"]
    dataframe_context.set_job_type(jobType)
    dataframe_context.set_message_url(messageUrl)
    jobName = job_config["job_name"]
    messageURL = dataframe_context.get_message_url()
    analysistype = dataframe_context.get_analysis_type()
    result_setter = ResultSetter(dataframe_context)
    # scripts_to_run = dataframe_context.get_scripts_to_run()
    scripts_to_run = dataframe_context.get_analysis_name_list()
    print "scripts_to_run",scripts_to_run
    if scripts_to_run==None:
        scripts_to_run = []
    appid = dataframe_context.get_app_id()
    
    scriptWeightDict = dataframe_context.get_script_weights()
    print scriptWeightDict
    completionStatus = 0

    ########################## Load the dataframe ##############################
    if jobType == "story":
        if analysistype == "measure":
            progressMessage = CommonUtils.create_progress_message_object("Measure analysis","custom","info","Analyzing Target Variable",completionStatus,completionStatus,display=True)
        else:
            progressMessage = CommonUtils.create_progress_message_object("Dimension analysis","custom","info","Analyzing Target Variable",completionStatus,completionStatus,display=True)
        CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
        dataframe_context.update_completion_status(completionStatus)
    elif jobType == "metaData":
        progressMessage = CommonUtils.create_progress_message_object("metaData","custom","info","Preparing data for loading",completionStatus,completionStatus,display=True)
        CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
        progressMessage = CommonUtils.create_progress_message_object("metaData","custom","info","Initializing the loading process",completionStatus,completionStatus,display=True)
        CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
        progressMessage = CommonUtils.create_progress_message_object("metaData","custom","info","Data Upload in progress",completionStatus,completionStatus,display=True)
        CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
        dataframe_context.update_completion_status(completionStatus)

    df = None
    data_loading_st = time.time()
    progressMessage = CommonUtils.create_progress_message_object("scriptInitialization","scriptInitialization","info","Loading the Dataset",completionStatus,completionStatus)
    CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
    dataframe_context.update_completion_status(completionStatus)
    datasource_type = dataframe_context.get_datasource_type()
    if datasource_type == "fileUpload":
        df = DataLoader.load_csv_file(spark, dataframe_context.get_input_file())
    else:
        dbConnectionParams = dataframe_context.get_dbconnection_params()
        df = DataLoader.create_dataframe_from_jdbc_connector(spark, datasource_type, dbConnectionParams)
    if df != None:
        # Dropping blank rows
        df = df.dropna(how='all', thresh=None, subset=None)
        data_load_time = time.time() - data_loading_st
        print "Data Loading Time ",data_load_time," Seconds"
        metaParserInstance = MetaParser()
        if debugMode != True:
            if jobType != "metaData":
                print "Retrieving MetaData"
                metaDataObj = CommonUtils.get_existing_metadata(dataframe_context)
                if metaDataObj:
                    metaParserInstance.set_params(metaDataObj)
                else:
                    fs = time.time()
                    print "starting Metadata"
                    dataframe_context.set_metadata_ignore_msg_flag(True)
                    meta_data_class = MetaDataScript(df,spark,dataframe_context)
                    meta_data_object = meta_data_class.run()
                    metaDataObj = json.loads(CommonUtils.convert_python_object_to_json(meta_data_object))
                    print "metaData Analysis Done in ", time.time() - fs, " seconds."
                    metaParserInstance.set_params(metaDataObj)
        elif debugMode == True:
            if jobType != "metaData":
                # checking if metadata exist for the dataset
                # else it will run metadata first
                # while running in debug mode the dataset_slug should be correct or some random String
                try:
                    metaDataObj = CommonUtils.get_existing_metadata(dataframe_context)
                except:
                    metaDataObj = None
                if metaDataObj:
                    metaParserInstance.set_params(metaDataObj)
                else:
                    fs = time.time()
                    print "starting Metadata"
                    dataframe_context.set_metadata_ignore_msg_flag(True)
                    meta_data_class = MetaDataScript(df,spark,dataframe_context)
                    meta_data_object = meta_data_class.run()
                    metaDataObj = json.loads(CommonUtils.convert_python_object_to_json(meta_data_object))
                    print "metaData Analysis Done in ", time.time() - fs, " seconds."
                    metaParserInstance.set_params(metaDataObj)

        if jobType != "metaData":
            print "Setting Dataframe Helper Class"
            percentageColumns = metaParserInstance.get_percentage_columns()
            dollarColumns = metaParserInstance.get_dollar_columns()
            dataframe_context.set_percentage_columns(percentageColumns)
            dataframe_context.set_dollar_columns(dollarColumns)

            df_helper = DataFrameHelper(df, dataframe_context)
            df_helper.set_params()
            df = df_helper.get_data_frame()
            measure_columns = df_helper.get_numeric_columns()
            dimension_columns = df_helper.get_string_columns()
            # updating metaData for binned Cols
            colsToBin = df_helper.get_cols_to_bin()
            levelCountDict = df_helper.get_level_counts(colsToBin)
            metaParserInstance.update_level_counts(colsToBin,levelCountDict)


        completionStatus += scriptWeightDict["initialization"]["total"]
        progressMessage = CommonUtils.create_progress_message_object("dataLoading","dataLoading","info","Dataset Loading Finished",completionStatus,completionStatus)
        CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
        dataframe_context.update_completion_status(completionStatus)

        if jobType == "story":
            if analysistype == "measure":
                progressMessage = CommonUtils.create_progress_message_object("Measure analysis","custom","info","Transforming data for analysis",completionStatus,completionStatus,display=True)
            else:
                progressMessage = CommonUtils.create_progress_message_object("Dimension analysis","custom","info","Transforming data for analysis",completionStatus,completionStatus,display=True)
            CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
            dataframe_context.update_completion_status(completionStatus)

    ############################ MetaData Calculation ##########################

    if jobType == "metaData":
        fs = time.time()
        print "Running Metadata"
        meta_data_class = MetaDataScript(df,spark,dataframe_context)
        progressMessage = CommonUtils.create_progress_message_object("metaData","custom","info","Creating Meta data for the dataset",completionStatus,completionStatus,display=True)
        CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
        try:
            meta_data_object = meta_data_class.run()
            metaDataJson = CommonUtils.convert_python_object_to_json(meta_data_object)
            print metaDataJson
            print "metaData Analysis Done in ", time.time() - fs, " seconds."
            response = CommonUtils.save_result_json(configJson["job_config"]["job_url"],metaDataJson)
            completionStatus = dataframe_context.get_completion_status()
            progressMessage = CommonUtils.create_progress_message_object("metaData","custom","info","Your data is uploaded",completionStatus,completionStatus,display=True)
            CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
            progressMessage = CommonUtils.create_progress_message_object("final","final","info","Job Finished",100,100)
            CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
            return response
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(LOGGER,"metadata",e)
            CommonUtils.save_error_messages(errorURL,e,ignore=ignoreMsg)
    ############################################################################

    ################################ Data Sub Setting ##########################
    if jobType == "subSetting":
        st = time.time()
        print "starting subsetting"
        subsetting_class = DataFrameFilterer(df,df_helper,dataframe_context)
        try:
            filtered_df = subsetting_class.applyFilter()
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(LOGGER,"filterDf",e)
            CommonUtils.save_error_messages(errorURL,e,ignore=ignoreMsg)
        try:
            if filtered_df.count() > 0:
                transform_class = DataFrameTransformer(filtered_df,df_helper,dataframe_context)
                transform_class.applyTransformations()
                transformed_df = transform_class.get_transformed_data_frame()
            if transformed_df.count() > 0:
                output_filepath = dataframe_context.get_output_filepath()
                print output_filepath
                transformed_df.write.csv(output_filepath,mode="overwrite",header=True)
                print "starting Metadata for the Filtered Dataframe"
                meta_data_class = MetaDataScript(transformed_df,spark,dataframe_context)
                meta_data_object = meta_data_class.run()
                metaDataJson = CommonUtils.convert_python_object_to_json(meta_data_object)
                print metaDataJson
                response = CommonUtils.save_result_json(configJson["job_config"]["job_url"],metaDataJson)
            else:
                response = CommonUtils.save_result_json(configJson["job_config"]["job_url"],{"status":"failed","message":"Filtered Dataframe has no data"})
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(LOGGER,"transformDf",e)
            CommonUtils.save_error_messages(errorURL,e,ignore=ignoreMsg)
        progressMessage = CommonUtils.create_progress_message_object("final","final","info","Job Finished",100,100,display=True)
        CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
        print "SubSetting Analysis Completed in", time.time()-st," Seconds"
        return response
    ############################################################################

    ################################ Story Creation ############################
    if jobType == "story":
        messageURL = dataframe_context.get_message_url()
        result_setter = ResultSetter(dataframe_context)
        story_narrative = NarrativesTree()
        targetVal = dataframe_context.get_result_column()
        story_narrative.set_name("{} Performance Report".format(targetVal))

        if analysistype == 'dimension':
            st = time.time()
            print "STARTING DIMENSION ANALYSIS ..."
            df_helper.remove_null_rows(dataframe_context.get_result_column())
            df = df_helper.get_data_frame()
            if ('Descriptive analysis' in scripts_to_run):
                dataframe_context.set_analysis_name("Descriptive analysis")
                completionStatus = dataframe_context.get_completion_status()
                progressMessage = CommonUtils.create_progress_message_object("Measure analysis","custom","info","Choosing statistical and Machine Learning techniques for analysis",completionStatus,completionStatus,display=True)
                CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
                try:
                    fs = time.time()
                    freq_obj = FreqDimensionsScript(df, df_helper, dataframe_context, spark, story_narrative,result_setter)
                    freq_obj.Run()
                    print "Frequency Analysis Done in ", time.time() - fs,  " seconds."
                except Exception as e:
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"Descriptive analysis",e)
                    CommonUtils.save_error_messages(errorURL,e,ignore=ignoreMsg)
                    completionStatus = dataframe_context.get_completion_status()
                    completionStatus += scriptWeightDict["Descriptive analysis"]["total"]
                    dataframe_context.update_completion_status(completionStatus)
                    progressMessage = CommonUtils.create_progress_message_object("Frequency analysis","failedState","error","descriptive Stats failed",completionStatus,completionStatus)
                    CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)

            if (len(dimension_columns)>=2 and 'Dimension vs. Dimension' in scripts_to_run):
                dataframe_context.set_analysis_name("Dimension vs. Dimension")
                completionStatus = dataframe_context.get_completion_status()
                progressMessage = CommonUtils.create_progress_message_object("Dimension analysis","custom","info","Evaluating variables for Statistical Association",completionStatus,completionStatus,display=True)
                CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
                try:
                    fs = time.time()
                    chisquare_obj = ChiSquareScript(df, df_helper, dataframe_context, spark, story_narrative,result_setter)
                    chisquare_obj.Run()
                    print "ChiSquare Analysis Done in ", time.time() - fs, " seconds."
                except Exception as e:
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"Dimension vs. Dimension",e)
                    CommonUtils.save_error_messages(errorURL,e,ignore=ignoreMsg)
                    completionStatus = dataframe_context.get_completion_status()
                    completionStatus += scriptWeightDict["Dimension vs. Dimension"]["total"]
                    dataframe_context.update_completion_status(completionStatus)
                    progressMessage = CommonUtils.create_progress_message_object("Dimension vs. Dimension","failedState","error","Dimension vs. Dimension failed",completionStatus,completionStatus)
                    CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)

            if ('Trend' in scripts_to_run):
                dataframe_context.set_analysis_name("Trend")
                completionStatus = dataframe_context.get_completion_status()
                progressMessage = CommonUtils.create_progress_message_object("Dimension analysis","custom","info","Analyzing trend for {}".format(targetVal),completionStatus,completionStatus,display=True)
                CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
                try:
                    fs = time.time()
                    trend_obj = TrendScript(df_helper, dataframe_context, result_setter, spark, story_narrative, metaParserInstance)
                    trend_obj.Run()
                    print "Trend Analysis Done in ", time.time() - fs, " seconds."

                except Exception as e:
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"Trend",e)
                    CommonUtils.save_error_messages(errorURL,e,ignore=ignoreMsg)
                    completionStatus = dataframe_context.get_completion_status()
                    completionStatus += scriptWeightDict["Trend"]["total"]
                    dataframe_context.update_completion_status(completionStatus)
                    progressMessage = CommonUtils.create_progress_message_object("Trend","failedState","error","Trend failed",completionStatus,completionStatus)
                    CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)

            if ('Predictive modeling' in scripts_to_run):
                dataframe_context.set_analysis_name("Predictive modeling")
                completionStatus = dataframe_context.get_completion_status()
                progressMessage = CommonUtils.create_progress_message_object("Dimension analysis","custom","info","Creating Prediction Model for {}".format(targetVal),completionStatus,completionStatus,display=True)
                CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
                try:
                    fs = time.time()
                    df_helper.fill_na_dimension_nulls()
                    df = df_helper.get_data_frame()
                    decision_tree_obj = DecisionTreeScript(df, df_helper, dataframe_context, spark, story_narrative,result_setter,metaParserInstance)
                    decision_tree_obj.Run()
                    print "DecisionTrees Analysis Done in ", time.time() - fs, " seconds."
                except Exception as e:
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"Predictive modeling",e)
                    CommonUtils.save_error_messages(errorURL,e,ignore=ignoreMsg)
                    completionStatus = dataframe_context.get_completion_status()
                    completionStatus += scriptWeightDict["Predictive modeling"]["total"]
                    dataframe_context.update_completion_status(completionStatus)
                    progressMessage = CommonUtils.create_progress_message_object("Predictive modeling","failedState","error","Predictive modeling failed",completionStatus,completionStatus)
                    CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)

            progressMessage = CommonUtils.create_progress_message_object("Dimension analysis","custom","info","Validating analysis results",completionStatus,completionStatus,display=True)
            CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
            time.sleep(3)
            progressMessage = CommonUtils.create_progress_message_object("Dimension analysis","custom","info","Creating Visualizations",completionStatus,completionStatus,display=True)
            CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
            time.sleep(3)
            progressMessage = CommonUtils.create_progress_message_object("Dimension analysis","custom","info","Creating Narratives",completionStatus,completionStatus,display=True)
            CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
            time.sleep(3)
            dataframe_context.update_completion_status(max(completionStatus,100))

            ordered_node_name_list = ["Overview","Trend","Association","Prediction"]
            # story_narrative.reorder_nodes(ordered_node_name_list)
            dimensionResult = CommonUtils.convert_python_object_to_json(story_narrative)
            headNode = result_setter.get_head_node()
            if headNode != None:
                headNode = json.loads(CommonUtils.convert_python_object_to_json(headNode))
            headNode["name"] = jobName
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
            print "Dimension Analysis Completed in", time.time()-st," Seconds"
            progressMessage = CommonUtils.create_progress_message_object("Dimension analysis","custom","info","Your signal is ready",100,100,display=True)
            CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
            return response

        elif analysistype == 'measure':
            st = time.time()
            print "STARTING MEASURE ANALYSIS ..."
            df_helper.remove_null_rows(dataframe_context.get_result_column())
            df = df_helper.get_data_frame()
            measure_columns = df_helper.get_numeric_columns()
            dimension_columns = df_helper.get_string_columns()
            #df = df.na.drop(subset=dataframe_context.get_result_column())

            if ('Descriptive analysis' in scripts_to_run):
                dataframe_context.set_analysis_name("Descriptive analysis")
                completionStatus = dataframe_context.get_completion_status()
                progressMessage = CommonUtils.create_progress_message_object("Measure analysis","custom","info","Choosing statistical and Machine Learning techniques for analysis",completionStatus,completionStatus,display=True)
                CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
                try:
                    fs = time.time()
                    descr_stats_obj = DescriptiveStatsScript(df, df_helper, dataframe_context, result_setter, spark,story_narrative)
                    descr_stats_obj.Run()
                    print "DescriptiveStats Analysis Done in ", time.time() - fs, " seconds."
                except Exception as e:
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"Descriptive analysis",e)
                    CommonUtils.save_error_messages(errorURL,e,ignore=ignoreMsg)
                    completionStatus = dataframe_context.get_completion_status()
                    completionStatus += scriptWeightDict["Descriptive analysis"]["total"]
                    dataframe_context.update_completion_status(completionStatus)
                    progressMessage = CommonUtils.create_progress_message_object("Descriptive analysis","failedState","error","descriptive Stats failed",completionStatus,completionStatus)
                    CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)

            if len(dimension_columns)>0 and 'Measure vs. Dimension' in scripts_to_run:
                dataframe_context.set_analysis_name("Measure vs. Dimension")
                completionStatus = dataframe_context.get_completion_status()
                progressMessage = CommonUtils.create_progress_message_object("Measure analysis","custom","info","Evaluating variables for Performance Analysis",completionStatus,completionStatus,display=True)
                CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
                try:
                    fs = time.time()
                    two_way_obj = TwoWayAnovaScript(df, df_helper, dataframe_context, result_setter, spark,story_narrative)
                    two_way_obj.Run()
                    print "OneWayAnova Analysis Done in ", time.time() - fs, " seconds."
                except Exception as e:
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"Measure vs. Dimension",e)
                    CommonUtils.save_error_messages(errorURL,e,ignore=ignoreMsg)
                    completionStatus = dataframe_context.get_completion_status()
                    completionStatus += scriptWeightDict["Measure vs. Dimension"]["total"]
                    dataframe_context.update_completion_status(completionStatus)
                    progressMessage = CommonUtils.create_progress_message_object("Measure vs. Dimension","failedState","error","Anova failed",completionStatus,completionStatus)
                    CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)

            if len(measure_columns)>1 and 'Measure vs. Measure' in scripts_to_run:
                dataframe_context.set_analysis_name("Measure vs. Measure")
                completionStatus = dataframe_context.get_completion_status()
                progressMessage = CommonUtils.create_progress_message_object("Measure analysis","custom","info","Finding factors that influence target variable",completionStatus,completionStatus,display=True)
                CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
                try:
                    fs = time.time()
                    correlation_obj = CorrelationScript(df, df_helper, dataframe_context, spark)
                    correlations = correlation_obj.Run()
                    print "Correlation Analysis Done in ", time.time() - fs ," seconds."
                    try:
                        df = df.na.drop(subset=measure_columns)
                        fs = time.time()
                        regression_obj = LinearRegressionScript(df, df_helper, dataframe_context, result_setter, spark, correlations, story_narrative,metaParserInstance)
                        regression_obj.Run()
                        print "Regression Analysis Done in ", time.time() - fs, " seconds."
                    except Exception as e:
                        CommonUtils.print_errors_and_store_traceback(LOGGER,"regression",e)
                        CommonUtils.save_error_messages(errorURL,e,ignore=ignoreMsg)
                except Exception as e:
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"Measure vs. Measure",e)
                    CommonUtils.save_error_messages(errorURL,e,ignore=ignoreMsg)
                    completionStatus = dataframe_context.get_completion_status()
                    completionStatus += scriptWeightDict["Measure vs. Measure"]["total"]
                    dataframe_context.update_completion_status(completionStatus)
                    progressMessage = CommonUtils.create_progress_message_object("Measure vs. Measure","failedState","error","Regression failed",completionStatus,completionStatus)
                    CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)

            if ('Trend' in scripts_to_run):
                dataframe_context.set_analysis_name("Trend")
                completionStatus = dataframe_context.get_completion_status()
                progressMessage = CommonUtils.create_progress_message_object("Measure analysis","custom","info","Analyzing trend for {}".format(targetVal),completionStatus,completionStatus,display=True)
                CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
                try:
                    fs = time.time()
                    trend_obj = TrendScript(df_helper,dataframe_context,result_setter,spark,story_narrative, metaParserInstance)
                    trend_obj.Run()
                    print "Trend Analysis Done in ", time.time() - fs, " seconds."

                except Exception as e:
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"Trend",e)
                    CommonUtils.save_error_messages(errorURL,e,ignore=ignoreMsg)
                    completionStatus = dataframe_context.get_completion_status()
                    completionStatus += scriptWeightDict["Trend"]["total"]
                    dataframe_context.update_completion_status(completionStatus)
                    progressMessage = CommonUtils.create_progress_message_object("Trend","failedState","error","Trend failed",completionStatus,completionStatus)
                    CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)

            if ('Predictive modeling' in scripts_to_run):
                dataframe_context.set_analysis_name("Predictive modeling")
                completionStatus = dataframe_context.get_completion_status()
                progressMessage = CommonUtils.create_progress_message_object("Measure analysis","custom","info","Creating Prediction Model for {}".format(targetVal),completionStatus,completionStatus,display=True)
                CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
                try:
                    fs = time.time()
                    df_helper.fill_na_dimension_nulls()
                    df = df_helper.get_data_frame()
                    dt_reg = DecisionTreeRegressionScript(df, df_helper, dataframe_context, result_setter, spark,story_narrative,metaParserInstance)
                    dt_reg.Run()
                    print "DecisionTrees Analysis Done in ", time.time() - fs, " seconds."
                except Exception as e:
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"Predictive modeling",e)
                    CommonUtils.save_error_messages(errorURL,e,ignore=ignoreMsg)
                    completionStatus = dataframe_context.get_completion_status()
                    completionStatus += scriptWeightDict["Predictive modeling"]["total"]
                    dataframe_context.update_completion_status(completionStatus)
                    progressMessage = CommonUtils.create_progress_message_object("Predictive modeling","failedState","error","Predictive modeling failed",completionStatus,completionStatus)
                    CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)

            # try:
            #     fs = time.time()
            #     exec_obj = ExecutiveSummaryScript(df_helper,dataframe_context,result_setter,spark)
            #     exec_obj.Run()
            #     print "Executive Summary Done in ", time.time() - fs, " seconds."
            # except Exception as e:
            #     CommonUtils.print_errors_and_store_traceback(LOGGER,"Executive Summary",e)


            progressMessage = CommonUtils.create_progress_message_object("Measure analysis","custom","info","Validating analysis results",completionStatus,completionStatus,display=True)
            CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
            time.sleep(3)
            progressMessage = CommonUtils.create_progress_message_object("Measure analysis","custom","info","Creating Visualizations",completionStatus,completionStatus,display=True)
            CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
            time.sleep(3)
            progressMessage = CommonUtils.create_progress_message_object("Measure analysis","custom","info","Creating Narratives",completionStatus,completionStatus,display=True)
            CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
            time.sleep(3)
            dataframe_context.update_completion_status(max(completionStatus,100))

            measureResult = CommonUtils.convert_python_object_to_json(story_narrative)
            headNode = result_setter.get_head_node()
            if headNode != None:
                headNode = json.loads(CommonUtils.convert_python_object_to_json(headNode))
            headNode["name"] = jobName
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
            print "Measure Analysis Completed in :", time.time()-st," Seconds"
            progressMessage = CommonUtils.create_progress_message_object("Measure analysis","custom","info","Your signal is ready",100,100,display=True)
            CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
            return response

        progressMessage = CommonUtils.create_progress_message_object("final","final","info","Job Finished",100,100,display=True)
        CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
    ############################################################################

    ################################ Model Training ############################
    elif jobType == 'training':
        st = time.time()
        prediction_narrative = NarrativesTree()
        prediction_narrative.set_name("models")
        result_setter = ResultSetter(dataframe_context)
        df_helper.remove_null_rows(dataframe_context.get_result_column())
        df = df_helper.get_data_frame()
        df = df_helper.fill_missing_values(df)
        categorical_columns = df_helper.get_string_columns()
        result_column = dataframe_context.get_result_column()
        df = df.toPandas()
        df = MLUtils.factorize_columns(df,[x for x in categorical_columns if x != result_column])
        df_helper.set_train_test_data(df)
        model_slug = dataframe_context.get_model_path()
        basefoldername = "mAdvisorModels"
        subfolders = MLUtils.slug_model_mapping().keys()
        model_file_path = MLUtils.create_model_folders(model_slug,basefoldername,subfolders=subfolders)
        dataframe_context.set_model_path(model_file_path)

        try:
            st = time.time()
            rf_obj = RandomForestScript(df, df_helper, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance)
            # rf_obj = RandomForestPysparkScript(df, df_helper, dataframe_context, spark, prediction_narrative,result_setter)
            rf_obj.Train()
            print "Random Forest Model Done in ", time.time() - st,  " seconds."
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(LOGGER,"randomForest",e)
            CommonUtils.save_error_messages(errorURL,e,ignore=ignoreMsg)

        try:
            st = time.time()
            xgb_obj = XgboostScript(df, df_helper, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance)
            xgb_obj.Train()
            print "XGBoost Model Done in ", time.time() - st,  " seconds."
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(LOGGER,"xgboost",e)
            CommonUtils.save_error_messages(errorURL,e,ignore=ignoreMsg)

        try:
            st = time.time()
            lr_obj = LogisticRegressionScript(df, df_helper, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance)
            # lr_obj = LogisticRegressionPysparkScript(df, df_helper, dataframe_context, spark, prediction_narrative,result_setter)
            lr_obj.Train()
            print "Logistic Regression Model Done in ", time.time() - st,  " seconds."
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(LOGGER,"logisticRegression",e)
            CommonUtils.save_error_messages(errorURL,e,ignore=ignoreMsg)

        modelJsonOutput = MLUtils.collated_model_summary_card(result_setter,prediction_narrative)
        print modelJsonOutput
        response = CommonUtils.save_result_json(configJson["job_config"]["job_url"],json.dumps(modelJsonOutput))
        pmmlModels = result_setter.get_pmml_object()
        savepmml = CommonUtils.save_pmml_models(configJson["job_config"]["xml_url"],pmmlModels)
        progressMessage = CommonUtils.create_progress_message_object("final","final","info","Job Finished",100,100,display=True)
        CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
        print "Model Training Completed in ", time.time() - st, " seconds."
        return response
    ############################################################################

    ############################## Model Prediction ############################
    elif jobType == 'prediction':
        print "Prediction Started"
        st = time.time()
        story_narrative = NarrativesTree()
        story_narrative.set_name("scores")
        result_setter = ResultSetter(dataframe_context)
        model_path = dataframe_context.get_model_path()
        print "model path",model_path
        result_column = dataframe_context.get_result_column()
        if result_column in df.columns:
            df_helper.remove_null_rows(result_column)
        df = df_helper.get_data_frame()
        df = df_helper.fill_missing_values(df)
        model_slug = model_path
        score_slug = dataframe_context.get_score_path()
        print "score_slug",score_slug
        basefoldername = "mAdvisorScores"
        score_file_path = MLUtils.create_scored_data_folder(score_slug,basefoldername)
        algorithm_name_list = ["randomforest","xgboost","logisticregression"]
        algorithm_name = dataframe_context.get_algorithm_slug()[0]
        print "algorithm_name",algorithm_name
        model_path = score_file_path.split(basefoldername)[0]+"/mAdvisorModels/"+model_slug+"/"+algorithm_name
        dataframe_context.set_model_path(model_path)
        dataframe_context.set_score_path(score_file_path)
        selected_model_for_prediction = [MLUtils.slug_model_mapping()[algorithm_name]]
        print "selected_model_for_prediction", selected_model_for_prediction
        if "randomforest" in selected_model_for_prediction:
            df = df.toPandas()
            trainedModel = RandomForestScript(df, df_helper, dataframe_context, spark, story_narrative,result_setter,metaParserInstance)
            # trainedModel = RandomForestPysparkScript(df, df_helper, dataframe_context, spark)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"randomForest",e)
                CommonUtils.save_error_messages(errorURL,e,ignore=ignoreMsg)
            print "Scoring Done in ", time.time() - st,  " seconds."
        elif "xgboost" in selected_model_for_prediction:
            df = df.toPandas()
            trainedModel = XgboostScript(df, df_helper, dataframe_context, spark, story_narrative,result_setter,metaParserInstance)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"randomForest",e)
                CommonUtils.save_error_messages(errorURL,e,ignore=ignoreMsg)
            print "Scoring Done in ", time.time() - st,  " seconds."
        elif "logisticregression" in selected_model_for_prediction:
            df = df.toPandas()
            trainedModel = LogisticRegressionScript(df, df_helper, dataframe_context, spark, story_narrative,result_setter,metaParserInstance)
            # trainedModel = LogisticRegressionPysparkScript(df, df_helper, dataframe_context, spark)
            try:
                trainedModel.Predict()
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"randomForest",e)
                CommonUtils.save_error_messages(errorURL,e,ignore=ignoreMsg)
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
        progressMessage = CommonUtils.create_progress_message_object("final","final","info","Job Finished",100,100,display=True)
        CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
        print "Model Scoring Completed in ", time.time() - st, " seconds."
        return response
    ############################################################################

    ################################### Stock ADVISOR ##########################
    if jobType == 'stockAdvisor':
        file_names = dataframe_context.get_stock_symbol_list()
        stockObj = StockAdvisor(spark, file_names,dataframe_context,result_setter)
        stockAdvisorData = stockObj.Run()
        stockAdvisorDataJson = CommonUtils.convert_python_object_to_json(stockAdvisorData)
        response = CommonUtils.save_result_json(configJson["job_config"]["job_url"],stockAdvisorDataJson)

    ############################################################################

    print "Scripts Time : ", time.time() - script_start_time, " seconds."
    #spark.stop()

def submit_job_through_yarn():
    print sys.argv
    print json.loads(sys.argv[1])
    json_config = json.loads(sys.argv[1])
    # json_config["config"] = ""

    main(json_config["job_config"])

if __name__ == '__main__':
    main(sys.argv[1])
    print 'Main Method End .....'
