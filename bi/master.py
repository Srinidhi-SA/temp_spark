import sys
import time
import json
import pyhocon
# from asn1crypto._ffi import None
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
import traceback
from parser import configparser
from pyspark.sql.functions import col, udf
from bi.scripts.stock_advisor import StockAdvisor
#if __name__ == '__main__':
LOGGER = {}
def main(configJson):
    global LOGGER
    deployEnv = False  # running the scripts from job-server env
    debugMode = True   # runnning the scripts for local testing and development
    cfgMode = False    # runnning the scripts by passing config.cfg path
    script_start_time = time.time()

    if isinstance(configJson,pyhocon.config_tree.ConfigTree):
        deployEnv = True
        debugMode = False
    elif isinstance(configJson,basestring):
        if configJson.endswith(".cfg"):
            ######################## Running in cfgMode ########################
            cfgMode = True
            debugMode = False
        else:
            ######################## Running in debugMode ######################
            print "Running in debugMode"
            cfgMode = False
            debugMode = True
            # Test Configs are defined in bi/common/utils.py
            jobType = "metaData"
            testConfigs = CommonUtils.get_test_configs()
            configJson = testConfigs[jobType]


    ######################## Craeting Spark Session ###########################
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
    if debugMode == True:
        dataframe_context.set_environment("debugMode")
    jobType = job_config["job_type"]
    messageUrl = configJson["job_config"]["message_url"]
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
    if jobType == "story":
        if analysistype == "dimension":
            scriptWeightDict = dataframe_context.get_dimension_analysis_weight()
        elif analysistype == "measure":
            scriptWeightDict = dataframe_context.get_measure_analysis_weight()
    elif jobType == "training":
        scriptWeightDict = dataframe_context.get_ml_model_training_weight()
    elif jobType == "prediction":
        scriptWeightDict = dataframe_context.get_ml_model_prediction_weight()
    elif jobType == "metaData":
        scriptWeightDict = dataframe_context.get_metadata_script_weight()

    completionStatus = 0


    ########################## Load the dataframe ##############################
    df = None
    data_loading_st = time.time()
    progressMessage = CommonUtils.create_progress_message_object("scriptInitialization","scriptInitialization","info","Dataset Loading Process Started",0,0)
    CommonUtils.save_progress_message(messageURL,progressMessage)
    datasource_type = dataframe_context.get_datasource_type()
    if datasource_type == "Hana":
        dbConnectionParams = dataframe_context.get_dbconnection_params()
        df = DataLoader.create_dataframe_from_hana_connector(spark, dbConnectionParams)
    elif datasource_type == "fileUpload":
        df = DataLoader.load_csv_file(spark, dataframe_context.get_input_file())

    if df != None:
        # Dropping blank rows
        df = df.dropna(how='all', thresh=None, subset=None)
        data_load_time = time.time() - data_loading_st
        print "Data Loading Time ",data_load_time," Seconds"
        print "Retrieving MetaData"
         # if debugMode != True:
        #     if jobType != "metaData":
        #         print "Retrieving MetaData"
        #         metaDataObj = CommonUtils.get_metadata(dataframe_context)
        #         dataframe_context.set_metadata_object(metaDataObj)
        # else:
        #     try:
        #         # checking if metadata exist for the dataset
        #         # else it will run metadata first
        #         # while running in debug mode the dataset_slug should be correct or some random String
        #         metaDataObj = CommonUtils.get_metadata(dataframe_context)
        #         dataframe_context.set_metadata_object(metaDataObj)
        #     except:
        #         fs = time.time()
        #         print "starting Metadata"
        #         dataframe_context.set_metadata_ignore_msg_flag(True)
        #         meta_data_class = MetaDataScript(df,spark,dataframe_context)
        #         meta_data_object = meta_data_class.run()
        #         metaDataObj = CommonUtils.convert_python_object_to_json(meta_data_object)
        #         print "metaData Analysis Done in ", time.time() - fs, " seconds."
        #         dataframe_context.set_metadata_object(metaDataObj)


        if jobType != "metaData":
            print "Setting Dataframe Helper Class"
            df_helper = DataFrameHelper(df, dataframe_context)
            df_helper.set_params()
            df = df_helper.get_data_frame()
            measure_columns = df_helper.get_numeric_columns()
            dimension_columns = df_helper.get_string_columns()

        print scriptWeightDict
        completionStatus += scriptWeightDict["initialization"]["total"]
        progressMessage = CommonUtils.create_progress_message_object("dataLoading","dataLoading","info","Dataset Loading Finished",completionStatus,completionStatus)
        CommonUtils.save_progress_message(messageURL,progressMessage)
        dataframe_context.update_completion_status(completionStatus)

    ############################ MetaData Calculation ##########################

    if jobType == "metaData":
        fs = time.time()
        print "starting Metadata"
        meta_data_class = MetaDataScript(df,spark,dataframe_context)
        meta_data_object = meta_data_class.run()
        metaDataJson = CommonUtils.convert_python_object_to_json(meta_data_object)
        print metaDataJson
        print "metaData Analysis Done in ", time.time() - fs, " seconds."
        response = CommonUtils.save_result_json(configJson["job_config"]["job_url"],metaDataJson)
        return response
    ############################################################################

    ################################ Data Sub Setting ##########################
    if jobType == "subSetting":
        st = time.time()
        print "starting subsetting"
        subsetting_class = DataFrameFilterer(df,df_helper,dataframe_context)
        filtered_df = subsetting_class.applyFilter()
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
        print "SubSetting Analysis Completed in", time.time()-st," Seconds"
        return response
    ############################################################################

    ################################ Story Creation ############################
    if jobType == "story":
        messageURL = dataframe_context.get_message_url()
        result_setter = ResultSetter(dataframe_context)
        story_narrative = NarrativesTree()
        story_narrative.set_name("{} Performance Report".format(dataframe_context.get_result_column()))

        if analysistype == 'dimension':
            st = time.time()
            print "STARTING DIMENSION ANALYSIS ..."
            df_helper.remove_null_rows(dataframe_context.get_result_column())
            df = df_helper.get_data_frame()
            if ('Descriptive analysis' in scripts_to_run):
                try:
                    fs = time.time()
                    dataframe_context.set_analysis_name("Descriptive analysis")
                    freq_obj = FreqDimensionsScript(df, df_helper, dataframe_context, spark, story_narrative,result_setter)
                    freq_obj.Run()
                    print "Frequency Analysis Done in ", time.time() - fs,  " seconds."
                except Exception as e:
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"Descriptive analysis",e)
                    completionStatus += scriptWeightDict["Descriptive analysis"]["total"]
                    dataframe_context.update_completion_status(completionStatus)
                    progressMessage = CommonUtils.create_progress_message_object("Frequency analysis","failedState","error","descriptive Stats failed",completionStatus,completionStatus)
                    CommonUtils.save_progress_message(messageURL,progressMessage)

            if ('Dimension vs. Dimension' in scripts_to_run):
                try:
                    fs = time.time()
                    dataframe_context.set_analysis_name("Dimension vs. Dimension")
                    chisquare_obj = ChiSquareScript(df, df_helper, dataframe_context, spark, story_narrative,result_setter)
                    chisquare_obj.Run()
                    print "ChiSquare Analysis Done in ", time.time() - fs, " seconds."
                except Exception as e:
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"Dimension vs. Dimension",e)
                    completionStatus += scriptWeightDict["Dimension vs. Dimension"]["total"]
                    dataframe_context.update_completion_status(completionStatus)
                    progressMessage = CommonUtils.create_progress_message_object("Dimension vs. Dimension","failedState","error","Dimension vs. Dimension failed",completionStatus,completionStatus)
                    CommonUtils.save_progress_message(messageURL,progressMessage)

            if ('Trend' in scripts_to_run):
                try:
                    fs = time.time()
                    dataframe_context.set_analysis_name("Trend")
                    trend_obj = TrendScript(df_helper, dataframe_context, result_setter, spark, story_narrative)
                    trend_obj.Run()
                    print "Trend Analysis Done in ", time.time() - fs, " seconds."

                except Exception as e:
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"Trend",e)
                    completionStatus += scriptWeightDict["Trend"]["total"]
                    dataframe_context.update_completion_status(completionStatus)
                    progressMessage = CommonUtils.create_progress_message_object("Trend","failedState","error","Trend failed",completionStatus,completionStatus)
                    CommonUtils.save_progress_message(messageURL,progressMessage)

            if ('Predictive modeling' in scripts_to_run):
                try:
                    fs = time.time()
                    dataframe_context.set_analysis_name("Predictive modeling")
                    if df_helper.ignorecolumns != None:
                        df_helper.drop_ignore_columns()
                    df_helper.fill_na_dimension_nulls()
                    df = df_helper.get_data_frame()
                    decision_tree_obj = DecisionTreeScript(df, df_helper, dataframe_context, spark, story_narrative,result_setter)
                    decision_tree_obj.Run()
                    print "DecisionTrees Analysis Done in ", time.time() - fs, " seconds."
                except Exception as e:
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"Predictive modeling",e)
                    completionStatus += scriptWeightDict["Predictive modeling"]["total"]
                    dataframe_context.update_completion_status(completionStatus)
                    progressMessage = CommonUtils.create_progress_message_object("Predictive modeling","failedState","error","Predictive modeling failed",completionStatus,completionStatus)
                    CommonUtils.save_progress_message(messageURL,progressMessage)

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
            return response

        elif analysistype == 'measure':
            st = time.time()
            print "STARTING MEASURE ANALYSIS ..."
            df_helper.remove_null_rows(dataframe_context.get_result_column())
            df = df_helper.get_data_frame()
            story_narrative.set_name("Measure analysis")

            if ('Descriptive analysis' in scripts_to_run):
                try:
                    fs = time.time()
                    dataframe_context.set_analysis_name("Descriptive analysis")
                    descr_stats_obj = DescriptiveStatsScript(df, df_helper, dataframe_context, result_setter, spark,story_narrative)
                    descr_stats_obj.Run()
                    print "DescriptiveStats Analysis Done in ", time.time() - fs, " seconds."
                except Exception as e:
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"Descriptive analysis",e)
                    completionStatus += scriptWeightDict["Descriptive analysis"]["total"]
                    dataframe_context.update_completion_status(completionStatus)
                    progressMessage = CommonUtils.create_progress_message_object("Descriptive analysis","failedState","error","descriptive Stats failed",completionStatus,completionStatus)
                    CommonUtils.save_progress_message(messageURL,progressMessage)

            if df_helper.ignorecolumns != None:
                df_helper.drop_ignore_columns()
            measure_columns = df_helper.get_numeric_columns()
            dimension_columns = df_helper.get_string_columns()
            df = df_helper.get_data_frame()
            #df = df.na.drop(subset=dataframe_context.get_result_column())
            if len(dimension_columns)>0 and 'Measure vs. Dimension' in scripts_to_run:
                try:
                    fs = time.time()
                    dataframe_context.set_analysis_name("Measure vs. Dimension")
                    two_way_obj = TwoWayAnovaScript(df, df_helper, dataframe_context, result_setter, spark,story_narrative)
                    two_way_obj.Run()
                    print "OneWayAnova Analysis Done in ", time.time() - fs, " seconds."
                except Exception as e:
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"Measure vs. Dimension",e)
                    completionStatus += scriptWeightDict["Measure vs. Dimension"]["total"]
                    dataframe_context.update_completion_status(completionStatus)
                    progressMessage = CommonUtils.create_progress_message_object("Measure vs. Dimension","failedState","error","Anova failed",completionStatus,completionStatus)
                    CommonUtils.save_progress_message(messageURL,progressMessage)

            if len(measure_columns)>1 and 'Measure vs. Measure' in scripts_to_run:
                try:
                    fs = time.time()
                    dataframe_context.set_analysis_name("Measure vs. Measure")
                    correlation_obj = CorrelationScript(df, df_helper, dataframe_context, spark)
                    correlations = correlation_obj.Run()
                    print "Correlation Analysis Done in ", time.time() - fs ," seconds."
                    try:
                        df = df.na.drop(subset=measure_columns)
                        fs = time.time()
                        regression_obj = LinearRegressionScript(df, df_helper, dataframe_context, result_setter, spark, correlations, story_narrative)
                        regression_obj.Run()
                        print "Regression Analysis Done in ", time.time() - fs, " seconds."
                    except Exception as e:
                        CommonUtils.print_errors_and_store_traceback(LOGGER,"regression",e)
                except Exception as e:
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"Measure vs. Measure",e)
                    completionStatus += scriptWeightDict["Measure vs. Measure"]["total"]
                    dataframe_context.update_completion_status(completionStatus)
                    progressMessage = CommonUtils.create_progress_message_object("Measure vs. Measure","failedState","error","Regression failed",completionStatus,completionStatus)
                    CommonUtils.save_progress_message(messageURL,progressMessage)

            if ('Trend' in scripts_to_run):
                try:
                    fs = time.time()
                    dataframe_context.set_analysis_name("Trend")
                    trend_obj = TrendScript(df_helper,dataframe_context,result_setter,spark,story_narrative)
                    trend_obj.Run()
                    print "Trend Analysis Done in ", time.time() - fs, " seconds."

                except Exception as e:
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"Trend",e)
                    completionStatus += scriptWeightDict["Trend"]["total"]
                    dataframe_context.update_completion_status(completionStatus)
                    progressMessage = CommonUtils.create_progress_message_object("Trend","failedState","error","Trend failed",completionStatus,completionStatus)
                    CommonUtils.save_progress_message(messageURL,progressMessage)

            if ('Predictive modeling' in scripts_to_run):
                try:
                    fs = time.time()
                    dataframe_context.set_analysis_name("Predictive modeling")
                    df_helper.fill_na_dimension_nulls()
                    df = df_helper.get_data_frame()
                    dt_reg = DecisionTreeRegressionScript(df, df_helper, dataframe_context, result_setter, spark,story_narrative)
                    dt_reg.Run()
                    print "DecisionTrees Analysis Done in ", time.time() - fs, " seconds."
                except Exception as e:
                    CommonUtils.print_errors_and_store_traceback(LOGGER,"Predictive modeling",e)
                    completionStatus += scriptWeightDict["Predictive modeling"]["total"]
                    dataframe_context.update_completion_status(completionStatus)
                    progressMessage = CommonUtils.create_progress_message_object("Predictive modeling","failedState","error","Predictive modeling failed",completionStatus,completionStatus)
                    CommonUtils.save_progress_message(messageURL,progressMessage)

            # try:
            #     fs = time.time()
            #     exec_obj = ExecutiveSummaryScript(df_helper,dataframe_context,result_setter,spark)
            #     exec_obj.Run()
            #     print "Executive Summary Done in ", time.time() - fs, " seconds."
            # except Exception as e:
            #     CommonUtils.print_errors_and_store_traceback(LOGGER,"Executive Summary",e)
            dataframe_context.update_completion_status(max(completionStatus,100))
            measureResult = CommonUtils.convert_python_object_to_json(story_narrative)
            # dimensionResult = CommonUtils.as_dict(story_narrative)
            # print measureResult
            # response = CommonUtils.save_result_json(configJson["job_config"]["job_url"],measureResult)
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
            return response
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
            CommonUtils.print_errors_and_store_traceback(LOGGER,"randomForest",e)

        try:
            st = time.time()
            lr_obj = LogisticRegressionScript(df, df_helper, dataframe_context, spark, prediction_narrative,result_setter)
            # lr_obj = LogisticRegressionPysparkScript(df, df_helper, dataframe_context, spark, prediction_narrative,result_setter)
            lr_obj.Train()
            print "Logistic Regression Model Done in ", time.time() - st,  " seconds."
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(LOGGER,"logisticRegression",e)

        try:
            st = time.time()
            xgb_obj = XgboostScript(df, df_helper, dataframe_context, spark, prediction_narrative,result_setter)
            xgb_obj.Train()
            print "XGBoost Model Done in ", time.time() - st,  " seconds."
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(LOGGER,"xgboost",e)


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
                model_dropdowns.append(obj["dropdown"])
                model_features[obj["dropdown"]["slug"]] = obj["modelFeatures"]
                model_configs["dimensionLevelCount"] = obj["levelcount"]
        model_configs["modelFeatures"] = model_features
        # print "Model Configs",model_configs

        modelJsonOutput.set_model_dropdown(model_dropdowns)
        modelJsonOutput.set_model_config(model_configs)
        modelJsonOutput = modelJsonOutput.get_json_data()
        print modelJsonOutput
        response = CommonUtils.save_result_json(configJson["job_config"]["job_url"],json.dumps(modelJsonOutput))
        print "Model Training Completed in ", time.time() - st, " seconds."
        return response
    ############################################################################

    ############################## Model Prediction ############################
    elif jobType == 'prediction':
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

if __name__ == '__main__':
    main(sys.argv[1])
    print 'Main Method End .....'
