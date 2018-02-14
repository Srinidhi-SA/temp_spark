from bi.common import DataLoader,MetaParser, DataFrameHelper,ContextSetter,ResultSetter
from bi.common import utils as CommonUtils
from bi.algorithms import utils as MLUtils
from bi.scripts.metadata import MetaDataScript
from bi.common import NarrativesTree
from bi.settings import setting as GLOBALSETTINGS

from bi.scripts.random_forest import RandomForestScript
from bi.scripts.xgboost_classification import XgboostScript
from bi.scripts.logistic_regression import LogisticRegressionScript
from bi.scripts.svm import SupportVectorMachineScript

from bi.transformations import DataFrameFilterer
from bi.transformations import DataFrameTransformer

from bi.scripts.frequency_dimensions import FreqDimensionsScript
from bi.scripts.chisquare import ChiSquareScript
from bi.scripts.decision_tree import DecisionTreeScript
from bi.scripts.correlation import CorrelationScript
from bi.scripts.descr_stats import DescriptiveStatsScript
from bi.scripts.two_way_anova import TwoWayAnovaScript
from bi.scripts.linear_regression import LinearRegressionScript
from bi.scripts.timeseries import TrendScript
from bi.scripts.decision_tree_regression import DecisionTreeRegressionScript



import json
import time


def load_dataset(spark,dataframe_context):
    datasource_type = dataframe_context.get_datasource_type()
    if datasource_type == "fileUpload":
        df = DataLoader.load_csv_file(spark, dataframe_context.get_input_file())
    else:
        dbConnectionParams = dataframe_context.get_dbconnection_params()
        df = DataLoader.create_dataframe_from_jdbc_connector(spark, datasource_type, dbConnectionParams)
    if df != None:
        # Dropping blank rows
        df = df.dropna(how='all', thresh=None, subset=None)
    return df

def get_metadata(df,spark,dataframe_context):
    debugMode = dataframe_context.get_debug_mode()
    jobType = dataframe_context.get_job_type()
    if df != None:
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
            dataframe_context.set_ignore_column_suggestions(metaParserInstance.get_ignore_columns())
            dataframe_context.set_utf8_columns(metaParserInstance.get_utf8_columns())
            dataframe_context.set_date_format(metaParserInstance.get_date_format())

            percentageColumns = metaParserInstance.get_percentage_columns()
            dollarColumns = metaParserInstance.get_dollar_columns()
            dataframe_context.set_percentage_columns(percentageColumns)
            dataframe_context.set_dollar_columns(dollarColumns)
        return metaParserInstance
    else:
        return None

def set_dataframe_helper(df,dataframe_context,metaParserInstance):
    dataframe_helper = DataFrameHelper(df, dataframe_context,metaParserInstance)
    dataframe_helper.set_params()
    df = dataframe_helper.get_data_frame()
    return df,dataframe_helper

def train_models(spark,df,dataframe_context,dataframe_helper,metaParserInstance):
    LOGGER = dataframe_context.get_logger()
    jobUrl = dataframe_context.get_job_url()
    errorURL = dataframe_context.get_error_url()
    xmlUrl = dataframe_context.get_xml_url()
    ignoreMsg = dataframe_context.get_message_ignore()
    messageURL = dataframe_context.get_message_url()
    APP_NAME = dataframe_context.get_app_name()

    st = time.time()
    prediction_narrative = NarrativesTree()
    prediction_narrative.set_name("models")
    result_setter = ResultSetter(dataframe_context)
    dataframe_helper.remove_null_rows(dataframe_context.get_result_column())
    df = dataframe_helper.fill_missing_values(df)
    categorical_columns = dataframe_helper.get_string_columns()
    uid_col = dataframe_context.get_uid_column()
    if metaParserInstance.check_column_isin_ignored_suggestion(uid_col):
        categorical_columns = list(set(categorical_columns) - {uid_col})
    result_column = dataframe_context.get_result_column()
    df = df.toPandas()
    df = MLUtils.factorize_columns(df,[x for x in categorical_columns if x != result_column])
    dataframe_helper.set_train_test_data(df)
    model_slug = dataframe_context.get_model_path()
    basefoldername = GLOBALSETTINGS.BASEFOLDERNAME_MODELS
    subfolders = GLOBALSETTINGS.SLUG_MODEL_MAPPING.keys()
    model_file_path = MLUtils.create_model_folders(model_slug,basefoldername,subfolders=subfolders)
    dataframe_context.set_model_path(model_file_path)

    try:
        st = time.time()
        rf_obj = RandomForestScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance)
        # rf_obj = RandomForestPysparkScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative,result_setter)
        rf_obj.Train()
        print "Random Forest Model Done in ", time.time() - st,  " seconds."
    except Exception as e:
        CommonUtils.print_errors_and_store_traceback(LOGGER,"randomForest",e)
        CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)

    try:
        st = time.time()
        xgb_obj = XgboostScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance)
        xgb_obj.Train()
        print "XGBoost Model Done in ", time.time() - st,  " seconds."
    except Exception as e:
        CommonUtils.print_errors_and_store_traceback(LOGGER,"xgboost",e)
        CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)

    try:
        st = time.time()
        lr_obj = LogisticRegressionScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance)
        # lr_obj = LogisticRegressionPysparkScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative,result_setter)
        lr_obj.Train()
        print "Logistic Regression Model Done in ", time.time() - st,  " seconds."
    except Exception as e:
        CommonUtils.print_errors_and_store_traceback(LOGGER,"logisticRegression",e)
        CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)

    # try:
    #     st = time.time()
    #     svm_obj = SupportVectorMachineScript(df, dataframe_helper, dataframe_context, spark, prediction_narrative,result_setter,metaParserInstance)
    #     svm_obj.Train()
    #     print "SVM Model Done in ", time.time() - st,  " seconds."
    # except Exception as e:
    #     CommonUtils.print_errors_and_store_traceback(LOGGER,"svm",e)
    #     CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)

    appid = dataframe_context.get_app_id()
    modelJsonOutput = MLUtils.collated_model_summary_card(result_setter,prediction_narrative,appid=appid)
    print modelJsonOutput
    response = CommonUtils.save_result_json(jobUrl,json.dumps(modelJsonOutput))
    pmmlModels = result_setter.get_pmml_object()
    savepmml = CommonUtils.save_pmml_models(xmlUrl,pmmlModels)
    progressMessage = CommonUtils.create_progress_message_object("final","final","info","Job Finished",100,100,display=True)
    CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
    print "Model Training Completed in ", time.time() - st, " seconds."

def score_model(spark,df,dataframe_context,dataframe_helper,metaParserInstance):
    LOGGER = dataframe_context.get_logger()
    messageURL = dataframe_context.get_message_url()
    APP_NAME = dataframe_context.get_app_name()
    errorURL = dataframe_context.get_error_url()
    jobUrl = dataframe_context.get_job_url()
    ignoreMsg = dataframe_context.get_message_ignore()
    targetLevel = dataframe_context.get_target_level_for_model()
    print "Prediction Started"
    st = time.time()
    story_narrative = NarrativesTree()
    story_narrative.set_name("scores")
    result_setter = ResultSetter(dataframe_context)
    model_path = dataframe_context.get_model_path()
    print "model path",model_path
    result_column = dataframe_context.get_result_column()
    if result_column in df.columns:
        dataframe_helper.remove_null_rows(result_column)
    df = dataframe_helper.get_data_frame()
    df = dataframe_helper.fill_missing_values(df)
    model_slug = model_path
    score_slug = dataframe_context.get_score_path()
    print "score_slug",score_slug
    basefoldername = GLOBALSETTINGS.BASEFOLDERNAME_SCORES
    score_file_path = MLUtils.create_scored_data_folder(score_slug,basefoldername)
    algorithm_name_list = ["randomforest","xgboost","logisticregression"]
    algorithm_name = dataframe_context.get_algorithm_slug()[0]
    print "algorithm_name",algorithm_name
    print "score_file_path",score_file_path
    print "model_slug",model_slug
    model_path = score_file_path.split(basefoldername)[0]+"/"+GLOBALSETTINGS.BASEFOLDERNAME_MODELS+"/"+model_slug+"/"+algorithm_name
    dataframe_context.set_model_path(model_path)
    dataframe_context.set_score_path(score_file_path)
    selected_model_for_prediction = [GLOBALSETTINGS.SLUG_MODEL_MAPPING[algorithm_name]]
    print "selected_model_for_prediction", selected_model_for_prediction
    if "randomforest" in selected_model_for_prediction:
        df = df.toPandas()
        trainedModel = RandomForestScript(df, dataframe_helper, dataframe_context, spark, story_narrative,result_setter,metaParserInstance)
        # trainedModel = RandomForestPysparkScript(df, dataframe_helper, dataframe_context, spark)
        try:
            trainedModel.Predict()
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(LOGGER,"randomForest",e)
            CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
        print "Scoring Done in ", time.time() - st,  " seconds."
    elif "xgboost" in selected_model_for_prediction:
        df = df.toPandas()
        trainedModel = XgboostScript(df, dataframe_helper, dataframe_context, spark, story_narrative,result_setter,metaParserInstance)
        try:
            trainedModel.Predict()
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(LOGGER,"randomForest",e)
            CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
        print "Scoring Done in ", time.time() - st,  " seconds."
    elif "logisticregression" in selected_model_for_prediction:
        df = df.toPandas()
        trainedModel = LogisticRegressionScript(df, dataframe_helper, dataframe_context, spark, story_narrative,result_setter,metaParserInstance)
        # trainedModel = LogisticRegressionPysparkScript(df, dataframe_helper, dataframe_context, spark)
        try:
            trainedModel.Predict()
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(LOGGER,"randomForest",e)
            CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
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
    jobUrl = dataframe_context.get_job_url()
    response = CommonUtils.save_result_json(jobUrl,scoreSummary)
    progressMessage = CommonUtils.create_progress_message_object("final","final","info","Job Finished",100,100,display=True)
    CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
    print "Model Scoring Completed in ", time.time() - st, " seconds."

def run_metadata(spark,df,dataframe_context):
    fs = time.time()
    LOGGER = dataframe_context.get_logger()
    messageURL = dataframe_context.get_message_url()
    APP_NAME = dataframe_context.get_app_name()
    errorURL = dataframe_context.get_error_url()
    jobUrl = dataframe_context.get_job_url()
    ignoreMsg = dataframe_context.get_message_ignore()


    meta_data_class = MetaDataScript(df,spark,dataframe_context)
    completionStatus = dataframe_context.get_completion_status()
    progressMessage = CommonUtils.create_progress_message_object("metaData","custom","info","Creating Meta data for the dataset",completionStatus,completionStatus,display=True)
    CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
    try:
        meta_data_object = meta_data_class.run()
        metaDataJson = CommonUtils.convert_python_object_to_json(meta_data_object)
        print metaDataJson
        print "metaData Analysis Done in ", time.time() - fs, " seconds."
        response = CommonUtils.save_result_json(jobUrl,metaDataJson)
        completionStatus = dataframe_context.get_completion_status()
        progressMessage = CommonUtils.create_progress_message_object("metaData","custom","info","Your data is uploaded",completionStatus,completionStatus,display=True)
        CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
        progressMessage = CommonUtils.create_progress_message_object("final","final","info","Job Finished",100,100)
        CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
        return response
    except Exception as e:
        CommonUtils.print_errors_and_store_traceback(LOGGER,"metadata",e)
        CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)

def run_subsetting(spark,df,dataframe_context,dataframe_helper):
    st = time.time()
    LOGGER = dataframe_context.get_logger()
    ignoreMsg = dataframe_context.get_message_ignore()
    messageURL = dataframe_context.get_message_url()
    APP_NAME = dataframe_context.get_app_name()
    errorURL = dataframe_context.get_error_url()
    jobUrl = dataframe_context.get_job_url()
    print "starting subsetting"
    subsetting_class = DataFrameFilterer(df,dataframe_helper,dataframe_context)
    try:
        filtered_df = subsetting_class.applyFilter()
    except Exception as e:
        CommonUtils.print_errors_and_store_traceback(LOGGER,"filterDf",e)
        CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
    try:
        if filtered_df.count() > 0:
            transform_class = DataFrameTransformer(filtered_df,dataframe_helper,dataframe_context)
            transform_class.applyTransformations()
            transformed_df = transform_class.get_transformed_data_frame()
        if transformed_df.count() > 0:
            output_filepath = dataframe_context.get_output_filepath()
            transformed_df.write.csv(output_filepath,mode="overwrite",header=True)
            print "starting Metadata for the Filtered Dataframe"
            meta_data_class = MetaDataScript(transformed_df,spark,dataframe_context)
            meta_data_object = meta_data_class.run()
            metaDataJson = CommonUtils.convert_python_object_to_json(meta_data_object)
            print metaDataJson
            response = CommonUtils.save_result_json(jobUrl,metaDataJson)
        else:
            response = CommonUtils.save_result_json(jobUrl,{"status":"failed","message":"Filtered Dataframe has no data"})
        return response
    except Exception as e:
        CommonUtils.print_errors_and_store_traceback(LOGGER,"transformDf",e)
        CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
    progressMessage = CommonUtils.create_progress_message_object("final","final","info","Job Finished",100,100,display=True)
    CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
    print "SubSetting Analysis Completed in", time.time()-st," Seconds"

def run_dimension_analysis(spark,df,dataframe_context,dataframe_helper,metaParserInstance):
    LOGGER = dataframe_context.get_logger()
    ignoreMsg = dataframe_context.get_message_ignore()
    messageURL = dataframe_context.get_message_url()
    APP_NAME = dataframe_context.get_app_name()
    errorURL = dataframe_context.get_error_url()
    jobUrl = dataframe_context.get_job_url()
    targetVal = dataframe_context.get_result_column()
    jobName = dataframe_context.get_job_name()
    # scripts_to_run = dataframe_context.get_scripts_to_run()
    scripts_to_run = dataframe_context.get_analysis_name_list()
    print "scripts_to_run",scripts_to_run
    measure_columns = dataframe_helper.get_numeric_columns()
    dimension_columns = dataframe_helper.get_string_columns()

    result_setter = ResultSetter(dataframe_context)
    story_narrative = NarrativesTree()
    story_narrative.set_name("{} Performance Report".format(targetVal))
    scriptWeightDict = dataframe_context.get_script_weights()
    print scriptWeightDict

    st = time.time()
    print "STARTING DIMENSION ANALYSIS ..."
    dataframe_helper.remove_null_rows(dataframe_context.get_result_column())
    df = dataframe_helper.get_data_frame()
    if ('Descriptive analysis' in scripts_to_run):
        dataframe_context.set_analysis_name("Descriptive analysis")
        completionStatus = dataframe_context.get_completion_status()
        progressMessage = CommonUtils.create_progress_message_object("Measure analysis","custom","info","Choosing statistical and Machine Learning techniques for analysis",completionStatus,completionStatus,display=True)
        CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
        # try:
        fs = time.time()
        freq_obj = FreqDimensionsScript(df, dataframe_helper, dataframe_context, spark, story_narrative,result_setter)
        freq_obj.Run()
        print "Frequency Analysis Done in ", time.time() - fs,  " seconds."
        # except Exception as e:
        #     CommonUtils.print_errors_and_store_traceback(LOGGER,"Descriptive analysis",e)
        #     CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
        #     completionStatus = dataframe_context.get_completion_status()
        #     completionStatus += scriptWeightDict["Descriptive analysis"]["total"]
        #     dataframe_context.update_completion_status(completionStatus)
        #     progressMessage = CommonUtils.create_progress_message_object("Frequency analysis","failedState","error","descriptive Stats failed",completionStatus,completionStatus)
        #     CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)

    if (len(dimension_columns)>=2 and 'Dimension vs. Dimension' in scripts_to_run):
        dataframe_context.set_analysis_name("Dimension vs. Dimension")
        completionStatus = dataframe_context.get_completion_status()
        progressMessage = CommonUtils.create_progress_message_object("Dimension analysis","custom","info","Evaluating variables for Statistical Association",completionStatus,completionStatus,display=True)
        CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
        try:
            fs = time.time()
            chisquare_obj = ChiSquareScript(df, dataframe_helper, dataframe_context, spark, story_narrative,result_setter,metaParserInstance)
            chisquare_obj.Run()
            print "ChiSquare Analysis Done in ", time.time() - fs, " seconds."
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(LOGGER,"Dimension vs. Dimension",e)
            CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
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
            trend_obj = TrendScript(dataframe_helper, dataframe_context, result_setter, spark, story_narrative, metaParserInstance)
            trend_obj.Run()
            print "Trend Analysis Done in ", time.time() - fs, " seconds."

        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(LOGGER,"Trend",e)
            CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
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
            dataframe_helper.fill_na_dimension_nulls()
            df = dataframe_helper.get_data_frame()
            decision_tree_obj = DecisionTreeScript(df, dataframe_helper, dataframe_context, spark, story_narrative,result_setter,metaParserInstance)
            decision_tree_obj.Run()
            print "DecisionTrees Analysis Done in ", time.time() - fs, " seconds."
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(LOGGER,"Predictive modeling",e)
            CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            completionStatus = dataframe_context.get_completion_status()
            completionStatus += scriptWeightDict["Predictive modeling"]["total"]
            dataframe_context.update_completion_status(completionStatus)
            progressMessage = CommonUtils.create_progress_message_object("Predictive modeling","failedState","error","Predictive modeling failed",completionStatus,completionStatus)
            CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
    completionStatus = dataframe_context.get_completion_status()
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
    response = CommonUtils.save_result_json(jobUrl,json.dumps(headNode))
    print "Dimension Analysis Completed in", time.time()-st," Seconds"
    progressMessage = CommonUtils.create_progress_message_object("Dimension analysis","custom","info","Your signal is ready",100,100,display=True)
    CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)

def run_measure_analysis(spark,df,dataframe_context,dataframe_helper,metaParserInstance):
    LOGGER = dataframe_context.get_logger()
    ignoreMsg = dataframe_context.get_message_ignore()
    messageURL = dataframe_context.get_message_url()
    APP_NAME = dataframe_context.get_app_name()
    errorURL = dataframe_context.get_error_url()
    jobUrl = dataframe_context.get_job_url()
    targetVal = dataframe_context.get_result_column()
    jobName = dataframe_context.get_job_name()
    # scripts_to_run = dataframe_context.get_scripts_to_run()
    scripts_to_run = dataframe_context.get_analysis_name_list()
    print "scripts_to_run",scripts_to_run
    measure_columns = dataframe_helper.get_numeric_columns()
    dimension_columns = dataframe_helper.get_string_columns()

    result_setter = ResultSetter(dataframe_context)
    story_narrative = NarrativesTree()
    story_narrative.set_name("{} Performance Report".format(targetVal))
    scriptWeightDict = dataframe_context.get_script_weights()
    print scriptWeightDict


    st = time.time()
    print "STARTING MEASURE ANALYSIS ..."
    dataframe_helper.remove_null_rows(dataframe_context.get_result_column())
    df = dataframe_helper.get_data_frame()

    #df = df.na.drop(subset=dataframe_context.get_result_column())

    if ('Descriptive analysis' in scripts_to_run):
        dataframe_context.set_analysis_name("Descriptive analysis")
        completionStatus = dataframe_context.get_completion_status()
        progressMessage = CommonUtils.create_progress_message_object("Measure analysis","custom","info","Choosing statistical and Machine Learning techniques for analysis",completionStatus,completionStatus,display=True)
        CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
        try:
            fs = time.time()
            descr_stats_obj = DescriptiveStatsScript(df, dataframe_helper, dataframe_context, result_setter, spark,story_narrative)
            descr_stats_obj.Run()
            print "DescriptiveStats Analysis Done in ", time.time() - fs, " seconds."
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(LOGGER,"Descriptive analysis",e)
            CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
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
            two_way_obj = TwoWayAnovaScript(df, dataframe_helper, dataframe_context, result_setter, spark,story_narrative,metaParserInstance)
            two_way_obj.Run()
            print "OneWayAnova Analysis Done in ", time.time() - fs, " seconds."
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(LOGGER,"Measure vs. Dimension",e)
            CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
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
            correlation_obj = CorrelationScript(df, dataframe_helper, dataframe_context, spark)
            correlations = correlation_obj.Run()
            print "Correlation Analysis Done in ", time.time() - fs ," seconds."
            try:
                df = df.na.drop(subset=measure_columns)
                fs = time.time()
                regression_obj = LinearRegressionScript(df, dataframe_helper, dataframe_context, result_setter, spark, correlations, story_narrative,metaParserInstance)
                regression_obj.Run()
                print "Regression Analysis Done in ", time.time() - fs, " seconds."
            except Exception as e:
                CommonUtils.print_errors_and_store_traceback(LOGGER,"regression",e)
                CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(LOGGER,"Measure vs. Measure",e)
            CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
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
            trend_obj = TrendScript(dataframe_helper,dataframe_context,result_setter,spark,story_narrative, metaParserInstance)
            trend_obj.Run()
            print "Trend Analysis Done in ", time.time() - fs, " seconds."

        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(LOGGER,"Trend",e)
            CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
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
            dataframe_helper.fill_na_dimension_nulls()
            df = dataframe_helper.get_data_frame()
            dt_reg = DecisionTreeRegressionScript(df, dataframe_helper, dataframe_context, result_setter, spark,story_narrative,metaParserInstance)
            dt_reg.Run()
            print "DecisionTrees Analysis Done in ", time.time() - fs, " seconds."
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(LOGGER,"Predictive modeling",e)
            CommonUtils.save_error_messages(errorURL,APP_NAME,e,ignore=ignoreMsg)
            completionStatus = dataframe_context.get_completion_status()
            completionStatus += scriptWeightDict["Predictive modeling"]["total"]
            dataframe_context.update_completion_status(completionStatus)
            progressMessage = CommonUtils.create_progress_message_object("Predictive modeling","failedState","error","Predictive modeling failed",completionStatus,completionStatus)
            CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)

    # try:
    #     fs = time.time()
    #     exec_obj = ExecutiveSummaryScript(dataframe_helper,dataframe_context,result_setter,spark)
    #     exec_obj.Run()
    #     print "Executive Summary Done in ", time.time() - fs, " seconds."
    # except Exception as e:
    #     CommonUtils.print_errors_and_store_traceback(LOGGER,"Executive Summary",e)

    completionStatus = dataframe_context.get_completion_status()
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
    response = CommonUtils.save_result_json(jobUrl,json.dumps(headNode))
    print "Measure Analysis Completed in :", time.time()-st," Seconds"
    progressMessage = CommonUtils.create_progress_message_object("Measure analysis","custom","info","Your signal is ready",100,100,display=True)
    CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)