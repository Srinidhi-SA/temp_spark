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
from bi.common import NormalCard,SummaryCard,NarrativesTree,HtmlData,C3ChartData,TableData,TreeData

import traceback


from parser import configparser
from pyspark.sql.functions import col, udf

def configtree_to_dict(configJson):
    out={}
    config = {}
    job_config = {}
    for k,v in configJson._dictionary.items():
        config[k] = v
    # for k,v in configJson._dictionary.items():
    #     job_config[k] = v
    out["config"] = config
    out["job_config"] = job_config
    return out
#if __name__ == '__main__':
LOGGER = []
def main(configJson):
    global LOGGER
    start_time = time.time()
    testConfigs = {
                "story" :{
                    "config":{
                                'FILE_SETTINGS': {
                                                  'script_to_run': [
                                                                    'Descriptive analysis',
                                                                    'Measure vs. Dimension',
                                                                    'Dimension vs. Dimension',
                                                                    'Predictive modeling',
                                                                    # 'Measure vs. Measure',
                                                                    'Trend'
                                                                    ],
                                                  'inputfile': ['file:///home/gulshan/marlabs/datasets/ub_data_cleaned.csv'],
                                                #   'inputfile': ['file:///home/gulshan/marlabs/datasets/trend_gulshan_small.csv'],
                                                  },
                                'COLUMN_SETTINGS': {
                                                    'polarity': ['positive'],
                                                    'consider_columns_type': ['excluding'],
                                                    'date_format': None,
                                                    # 'date_columns':["new_date","Month","Order Date"],
                                                    'date_columns':["Month"],
                                                    # 'ignore_column_suggestions': [],
                                                    'ignore_column_suggestions': ["Outlet ID","Visibility to Cosumer","Cleanliness","Days to Resolve","Heineken Lager Share %","Issue Category","Outlet","Accessible_to_consumer","Resultion Status"],
                                                    'result_column': ['Sales'],
                                                    'consider_columns':[],
                                                    # 'consider_columns': ['Date', 'Gender', 'Education', 'Model', 'Free service count',
                                                    #                      'Free service labour cost', 'Status'], 'date_columns': ['Date'],
                                                    'analysis_type': ['measure'],
                                                    # 'score_consider_columns': None
                                                    }
                             },
                    "job_config":{
                                    "job_type":"story",
                                    # "job_url": "http://34.196.204.54:9012/api/job/insight-winter-is-coming-eic37ggik1-mjsqu2nvlo/",
                                    # "job_url": "http://34.196.204.54:9012/api/job/insight-measure_check_1-ha6rkphong-cx01jezouw/",
                                    # "job_url": "http://192.168.33.94:9012/api/job/insight-adult-dimen-test-b6rim5juu3-hrswfad8w9/",
                                    "job_url":"",
                                    "set_result": {
                                        "method": "PUT",
                                        "action": "result"
                                      },
                                 }
                  },
                "metaData" : {
                    "config":{
                            'FILE_SETTINGS': {'inputfile': ['file:///home/gulshan/marlabs/datasets/ub_data.csv']},
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
                    }
                },
                "prediction":{
                    "config":{
                            'FILE_SETTINGS': {
                                    'inputfile': ['file:///home/gulshan/marlabs/datasets/opportunity_train.csv'],
                                    'modelpath': ["file:///home/gulshan/marlabs/test1/algos/"],
                                    'train_test_split' : [0.8]
                                    },
                            'COLUMN_SETTINGS': {
                                'analysis_type': ['prediction'],
                                'result_column': ['Opportunity Result'],
                                'consider_columns_type': ['excluding'],
                                'consider_columns':[],

                            }
                            },
                    "job_config":{
                        "job_type":"prediction",
                        # "job_url": "http://localhost:8000/api/job/dataset-iriscsv-qpmercq3r8-2fjupdcwdu/",
                        "job_url": "http://localhost:8000/api/job/dataset-iriscsv-qpmercq3r8-2fjupdcwdu/",
                        "set_result": {
                            "method": "PUT",
                            "action": "result"
                          },
                    }

                },
                "scoring":{
                    "config":{
                            'FILE_SETTINGS': {
                                    'inputfile': ['file:///home/gulshan/marlabs/datasets/opportunity_test.csv'],
                                    'modelpath': ["file:///home/gulshan/marlabs/test1/algos/RandomForest/TrainedModels/model.pkl"],
                                    'scorepath': ["file:///home/gulshan/marlabs/test1/algos/output"],
                                    'train_test_split' : [0.8],
                                    'levelcounts' : "GG|~|34|~|HH|~|4"
                                    },
                            'COLUMN_SETTINGS': {
                                'analysis_type': ['Dimension'],
                                'result_column': ['Price'],
                                'consider_columns_type': ['excluding'],
                                'consider_columns':[],
                                'date_columns':['Date'],
                                'score_consider_columns_type': ['excluding'],
                                'score_consider_columns':[],

                            }
                            },
                    "job_config":{
                        "job_type":"scoring",
                        "job_url": "http://localhost:8000/api/job/dataset-iriscsv-qpmercq3r8-2fjupdcwdu/",
                        "set_result": {
                            "method": "PUT",
                            "action": "result"
                          },
                    }

                }
    }
    APP_NAME = 'mAdvisor'
    spark = CommonUtils.get_spark_session(app_name=APP_NAME)
    spark.sparkContext.setLogLevel("ERROR")

    # configJson = testConfigs["story"]
    config = configJson["config"]
    job_config = configJson["job_config"]
    configJsonObj = configparser.ParserConfig(config)
    configJsonObj.set_json_params()
    dataframe_context = ContextSetter(configJsonObj)
    dataframe_context.set_params()
    jobType = job_config["job_type"]

    #Load the dataframe
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
        # url = configJson["job_config"]["job_url"]
        # url += "set_result"
        # return {"data":metaDataJson,"url":url}
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

            # print json.dumps(headNode,indent=2)
            response = CommonUtils.save_result_json(configJson["job_config"]["job_url"],json.dumps(headNode))
            return response

    elif jobType == 'prediction':
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
        # model_slug = dataframe_context.get_model_slug()
        model_slug = "slug1"
        basefoldername = "mAdvisorModels"
        model_file_path = MLUtils.create_model_folders(model_slug,basefoldername,subfolders=["RandomForest","LogisticRegression","Xgboost"])
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
        prediction_narrative.insert_card_at_given_index(card1,0)

        card2 = NormalCard()
        card2_elements = MLUtils.get_model_comparison(collated_summary)
        card2Data = [card2_elements[0],card2_elements[1]]
        card2.set_card_data(card2Data)
        prediction_narrative.insert_card_at_given_index(card2,1)

        card3 = NormalCard()
        card3Data = [HtmlData(data="<h2>Feature Importance</h2>")]
        card3Data.append(MLUtils.get_feature_importance(collated_summary))
        card3.set_card_data(card3Data)
        prediction_narrative.insert_card_at_given_index(card3,2)

        modelResult = CommonUtils.convert_python_object_to_json(prediction_narrative)
        print modelResult
        response = CommonUtils.save_result_json(configJson["job_config"]["job_url"],modelResult)
        # return response

    elif jobType == 'scoring':
        st = time.time()
        story_narrative = NarrativesTree()
        story_narrative.set_name("scores")
        result_setter = ResultSetter(df,dataframe_context)
        model_path = dataframe_context.get_model_path()
        result_column = dataframe_context.get_result_column()
        if result_column in df.columns:
            df_helper.remove_null_rows(result_column)
        df = df_helper.get_data_frame()
        df = df_helper.fill_missing_values(df)
        # model_slug = dataframe_context.get_model_slug()
        model_slug = "slug1"
        score_slug = "slug1"
        # score_slug = dataframe_context.get_score_slug()
        basefoldername = "mAdvisorScores"
        score_file_path = MLUtils.create_scored_data_folder(score_slug,basefoldername)
        algorithm_name_list = ["RandomForest","XGBoost","LogisticRegression"]
        algorithm_name = "RandomForest"
        model_path = score_file_path.split(basefoldername)[0]+"/mAdvisorModels/"+model_slug+"/"+algorithm_name
        print model_path
        dataframe_context.set_model_path(model_path)
        dataframe_context.set_score_path(score_file_path)

        if "RandomForest" in model_path:
            df = df.toPandas()
            trainedModel = RandomForestScript(df, df_helper, dataframe_context, spark, story_narrative,result_setter)
            # trainedModel = RandomForestPysparkScript(df, df_helper, dataframe_context, spark)
            trainedModel.Predict()
            print "Scoring Done in ", time.time() - st,  " seconds."
        elif "XGBoost" in model_path:
            df = df.toPandas()
            trainedModel = XgboostScript(df, df_helper, dataframe_context, spark, story_narrative,result_setter)
            trainedModel.Predict()
            print "Scoring Done in ", time.time() - st,  " seconds."
        elif "LogisticRegression" in model_path:
            df = df.toPandas()
            trainedModel = LogisticRegressionScript(df, df_helper, dataframe_context, spark, story_narrative,result_setter)
            # trainedModel = LogisticRegressionPysparkScript(df, df_helper, dataframe_context, spark)
            trainedModel.Predict()
            print "Scoring Done in ", time.time() - st,  " seconds."
        else:
            print "Could Not Load the Model for Scoring"

        scoreSummary = CommonUtils.convert_python_object_to_json(story_narrative)
        print scoreSummary
        response = CommonUtils.save_result_json(configJson["job_config"]["job_url"],scoreSummary)
        # return response

    print "Scripts Time : ", time.time() - script_start_time, " seconds."
    print "Data Load Time : ", data_load_time, " seconds."
    #spark.stop()
    return (" "+ "="*100 + " ").join(LOGGER)

if __name__ == '__main__':
    main(sys.argv[1])
    print 'Main Method End .....'
