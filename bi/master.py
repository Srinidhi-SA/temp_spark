import sys
import time
import json
import requests

reload(sys)
sys.setdefaultencoding('utf-8')
import ConfigParser

from bi.common import utils as CommonUtils
from bi.common import DataLoader
from bi.common import DataWriter
from bi.common import DataFrameHelper
from bi.common import ContextSetter
from bi.common import ResultSetter
from bi.common import NarrativesTree

from bi.algorithms import utils as MLUtils

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
from bi.scripts.random_forest_pyspark import RandomForestPysparkScript
from bi.scripts.logistic_regression_pyspark import LogisticRegressionPysparkScript
from bi.scripts.metadata_new import MetaDataScript


from parser import configparser
from pyspark.sql.functions import col, udf

#if __name__ == '__main__':
def main(configJson):
    start_time = time.time()
    APP_NAME = 'mAdvisor'
    spark = CommonUtils.get_spark_session(app_name=APP_NAME)
    spark.sparkContext.setLogLevel("ERROR")
    # Setting The Config Parameters
    #sys.argv[1]
    # job_type = {"metaData","signal","prediction","scoring"}

    if isinstance(configJson, basestring):
        config_file = configJson
        config = ConfigParser.ConfigParser()
        config.optionxform=str
        config.read(config_file)
        config_obj = configparser.ParserConfig(config)
        config_obj.set_params()
        # Setting the Dataframe Context
        dataframe_context = ContextSetter(config_obj)
        dataframe_context.set_params()
    else:
        # configJson = {
        #                 "config":{
        #                             'FILE_SETTINGS': {
        #                                               'monitor_api': ['http://52.77.216.14/api/errand/1/log_status'],
        #                                               'levelcounts': ['GG|~|34|~|HH|~|4'],
        #                                               'narratives_file': ['file:///home/gulshan/marlabs/test2/algos/kill/'],
        #                                               'scorepath': ['file:///home/gulshan/marlabs/test1/algos/output'],
        #                                               'modelpath': ['file:///home/gulshan/marlabs/test1/algos/'],
        #                                               'train_test_split': ['0.8'],
        #                                               'result_file': ['file:///home/gulshan/marlabs/test1/algos/kill/'],
        #                                               'script_to_run': ['Descriptive analysis',
        #                                                                 # 'Measure vs. Dimension',
        #                                                                 # 'Dimension vs. Dimension',
        #                                                                 'Predictive modeling',
        #                                                                 # 'Measure vs. Measure',
        #                                                                 # 'Trend'
        #                                                                 ],
        #                                               'inputfile': ['file:///home/gulshan/marlabs/datasets/trend_gulshan.csv']
        #                                               },
        #                             'COLUMN_SETTINGS': {
        #                                                 'polarity': ['positive'],
        #                                                 'consider_columns_type': ['excluding'],
        #                                                 'score_consider_columns_type': ['excluding'],
        #                                                 'measure_suggestions': None,
        #                                                 'date_format': None,
        #                                                 'date_columns':["Month"],
        #                                                 'ignore_column_suggestions': ["Order Date"],
        #                                                 'result_column': ['Platform'],
        #                                                 'consider_columns':[],
        #                                                 # 'consider_columns': ['Date', 'Gender', 'Education', 'Model', 'Free service count',
        #                                                 #                      'Free service labour cost', 'Status'], 'date_columns': ['Date'],
        #                                                 'analysis_type': ['Dimension'],
        #                                                 'score_consider_columns': None
        #                                                 }
        #                          },
        #                 "job_config":{
        #                                 "job_type":"story",
        #                                 "job_url": "http://localhost:8000/api/job/dataset-iriscsv-qpmercq3r8-2fjupdcwdu/",
        #                                 "set_result": {
        #                                     "method": "PUT",
        #                                     "action": "result"
        #                                   },
        #                              }
        #             }
        # configJson = {
        #     "config":{
        #             'FILE_SETTINGS': {'inputfile': ['file:///home/gulshan/marlabs/datasets/trend_gulshan.csv']},
        #             'COLUMN_SETTINGS': {'analysis_type': ['metaData']}
        #             },
        #     "job_config":{
        #         "job_type":"metaData",
        #         "job_url": "http://localhost:8000/api/job/dataset-iriscsv-qpmercq3r8-2fjupdcwdu/",
        #         "set_result": {
        #             "method": "PUT",
        #             "action": "result"
        #           },
        #     }}
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



    if jobType == "story":
        #Initializing the result_setter
        result_setter = ResultSetter(df,dataframe_context)
        story_narrative = NarrativesTree()
        if analysistype == 'Dimension':
            print "STARTING DIMENSION ANALYSIS ..."
            story_narrative.set_name("Dimension analysis")
            df_helper.remove_null_rows(dataframe_context.get_result_column())
            df = df_helper.get_data_frame()

            if ('Descriptive analysis' in scripts_to_run):
                try:
                    fs = time.time()
                    freq_obj = FreqDimensionsScript(df, df_helper, dataframe_context, spark, story_narrative)
                    freq_obj.Run()
                    print "Frequency Analysis Done in ", time.time() - fs,  " seconds."
                except Exception as e:
                    print "Frequency Analysis Failed "
                    print "#####ERROR#####"*5
                    print e
                    print "#####ERROR#####"*5
            else:
                DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_narratives_file()+'FreqDimension/')
                print "Descriptive analysis Not in Scripts to run "

            if ('Dimension vs. Dimension' in scripts_to_run):
                try:
                    fs = time.time()
                    chisquare_obj = ChiSquareScript(df, df_helper, dataframe_context, spark, story_narrative)
                    chisquare_obj.Run()
                    print "ChiSquare Analysis Done in ", time.time() - fs, " seconds."
                except Exception as e:
                    print "ChiSquare Analysis Failed "
                    DataWriter.write_dict_as_json(spark, {'narratives':{'main_card':{},'cards':[]}}, dataframe_context.get_narratives_file()+'ChiSquare/')
                    print "#####ERROR#####"*5
                    print e
                    print "#####ERROR#####"*5
            else:
                DataWriter.write_dict_as_json(spark, {'narratives':{'main_card':{},'cards':[]}}, dataframe_context.get_narratives_file()+'ChiSquare/')
                print "Dimension vs. Dimension Not in Scripts to run "

            if ('Predictive modeling' in scripts_to_run):
                try:
                    fs = time.time()
                    if df_helper.ignorecolumns != None:
                        df_helper.drop_ignore_columns()
                    df_helper.fill_na_dimension_nulls()
                    df = df_helper.get_data_frame()
                    decision_tree_obj = DecisionTreeScript(df, df_helper, dataframe_context, spark, story_narrative)
                    decision_tree_obj.Run()
                    print "DecisionTrees Analysis Done in ", time.time() - fs, " seconds."
                except Exception as e:
                    print "DecisionTrees Analysis Failed"
                    print "#####ERROR#####"*5
                    print e
                    print "#####ERROR#####"*5
            else:
                DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_narratives_file()+'DecisionTree/')
                print "Predictive modeling Not in Scripts to run"

            if ('Trend' in scripts_to_run):
                try:
                    fs = time.time()
                    trend_obj = TrendScript(df_helper, dataframe_context, result_setter, spark, story_narrative)
                    trend_obj.Run()
                    print "Trend Analysis Done in ", time.time() - fs, " seconds."

                except Exception as e:
                    DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_narratives_file()+'Trend/')
                    print "Trend Script Failed"
                    print "#####ERROR#####"*5
                    print e
                    print "#####ERROR#####"*5

            dimensionResult = CommonUtils.convert_python_object_to_json(story_narrative)
            # dimensionResult = CommonUtils.as_dict(story_narrative)
            print dimensionResult
            response = CommonUtils.save_result_json(configJson["job_config"]["job_url"],dimensionResult)
            return response

        elif analysistype == 'Measure':
            print "STARTING MEASURE ANALYSIS ..."
            df_helper.remove_null_rows(dataframe_context.get_result_column())
            df = df_helper.get_data_frame()

            if ('Descriptive analysis' in scripts_to_run):
                try:
                    fs = time.time()
                    descr_stats_obj = DescriptiveStatsScript(df, df_helper, dataframe_context, result_setter, spark)
                    descr_stats_obj.Run()
                    print "DescriptiveStats Analysis Done in ", time.time() - fs, " seconds."
                except Exception as e:
                    DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_narratives_file()+'DescrStats/')
                    DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_result_file()+'DescrStats/')
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
                    DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_result_file()+'Histogram/')
                    print "#####ERROR#####"*5
                    print e
                    print "#####ERROR#####"*5
                try:
                    fs = time.time()
                    d_histogram_obj = DensityHistogramsScript(df, df_helper, dataframe_context, spark)
                    d_histogram_obj.Run()
                    print "Density Histogram Analysis Done in ", time.time() - fs, " seconds."
                except Exception as e:
                    DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_result_file()+'Density_Histogram/')
                    print 'Density Histogram Failed'
                    print "#####ERROR#####"*5
                    print e
                    print "#####ERROR#####"*5
            else:
                DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_narratives_file()+'DescrStats/')
                DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_result_file()+'DescrStats/')
                DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_result_file()+'Histogram/')
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
                    two_way_obj = TwoWayAnovaScript(df, df_helper, dataframe_context, result_setter, spark)
                    two_way_obj.Run()
                    print "OneWayAnova Analysis Done in ", time.time() - fs, " seconds."
                except Exception as e:
                    print 'Anova Failed'
                    DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_result_file()+'OneWayAnova/')
                    DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_narratives_file()+'OneWayAnova/')
                    print "#####ERROR#####"*5
                    print e
                    print "#####ERROR#####"*5
            else:
                DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_result_file()+'OneWayAnova/')
                DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_narratives_file()+'OneWayAnova/')

            if len(measure_columns)>1 and 'Measure vs. Measure' in scripts_to_run:
                try:
                    fs = time.time()
                    correlation_obj = CorrelationScript(df, df_helper, dataframe_context, spark)
                    correlations = correlation_obj.Run()
                    print "Correlation Analysis Done in ", time.time() - fs ," seconds."
                    try:
                        df = df.na.drop(subset=measure_columns)
                        fs = time.time()
                        regression_obj = RegressionScript(df, df_helper, dataframe_context, result_setter, spark, correlations)
                        regression_obj.Run()
                        print "Regression Analysis Done in ", time.time() - fs, " seconds."
                    except Exception as e:
                        DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_narratives_file()+'Regression/')
                        print 'Regression Failed'
                        print "#####ERROR#####"*5
                        print e
                        print "#####ERROR#####"*5

                except Exception as e:
                    print 'Correlation Failed. Regression not executed'
                    DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_result_file()+'Correlation/')
                    DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_narratives_file()+'Regression/')
                    DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_result_file()+'Regression/')
                    print "#####ERROR#####"*5
                    print e
                    print "#####ERROR#####"*5

            else:
                print 'Regression not in Scripts to run'
                DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_result_file()+'Correlation/')
                DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_narratives_file()+'Regression/')

            try:
                fs = time.time()
                trend_obj = TrendScript(df_helper,dataframe_context,result_setter,spark)
                trend_obj.Run()
                print "Trend Analysis Done in ", time.time() - fs, " seconds."

            except Exception as e:
                DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_narratives_file()+'Trend/')
                print "Trend Script Failed"
                print "#####ERROR#####"*5
                print e
                print "#####ERROR#####"*5

            try:
                fs = time.time()
                df_helper.fill_na_dimension_nulls()
                df = df_helper.get_data_frame()
                dt_reg = DecisionTreeRegressionScript(df, df_helper, dataframe_context, result_setter, spark)
                dt_reg.Run()
                print "DecisionTrees Analysis Done in ", time.time() - fs, " seconds."
            except Exception as e:
                print "#####ERROR#####"*5
                print e
                print "#####ERROR#####"*5
                DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_narratives_file()+'DecisionTreeReg/')
                print "Decision Tree Regression Script Failed"
            try:
                fs = time.time()
                exec_obj = ExecutiveSummaryScript(df_helper,dataframe_context,result_setter,spark)
                exec_obj.Run()
                print "Executive Summary Done in ", time.time() - fs, " seconds."
            except Exception as e:
                print "#####ERROR#####"*5
                print e
                print "#####ERROR#####"*5
                DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_narratives_file()+'ExecutiveSummary/')
                print "Executive Summary Script Failed"

    elif jobType == 'prediction':
        prediction_narrative = NarrativesTree()
        df_helper.remove_null_rows(dataframe_context.get_result_column())
        df = df_helper.get_data_frame()
        df = df_helper.fill_missing_values(df)
        categorical_columns = df_helper.get_string_columns()
        result_column = dataframe_context.get_result_column()
        df = df.toPandas()
        df = MLUtils.factorize_columns(df,[x for x in categorical_columns if x != result_column])
        df_helper.set_train_test_data(df)

        try:
            st = time.time()
            rf_obj = RandomForestScript(df, df_helper, dataframe_context, spark, prediction_narrative)
            # rf_obj = RandomForestPysparkScript(df, df_helper, dataframe_context, spark, prediction_narrative)
            rf_obj.Train()
            print "Random Forest Model Done in ", time.time() - st,  " seconds."
        except Exception as e:
            print "Random Forest Model Failed"
            print "#####ERROR#####"*5
            print e
            print "#####ERROR#####"*5

        try:
            st = time.time()
            lr_obj = LogisticRegressionScript(df, df_helper, dataframe_context, spark, prediction_narrative)
            # lr_obj = LogisticRegressionPysparkScript(df, df_helper, dataframe_context, spark, prediction_narrative)
            lr_obj.Train()
            print "Logistic Regression Model Done in ", time.time() - st,  " seconds."
        except Exception as e:
            print "Logistic Regression Model Failed"
            print "#####ERROR#####"*5
            print e
            print "#####ERROR#####"*5

        try:
            st = time.time()
            xgb_obj = XgboostScript(df, df_helper, dataframe_context, spark, prediction_narrative)
            xgb_obj.Train()
            print "XGBoost Model Done in ", time.time() - st,  " seconds."
        except Exception as e:
            print "Xgboost Model Failed"
            print "#####ERROR#####"*5
            print e
            print "#####ERROR#####"*5

    elif jobType == 'scoring':
        st = time.time()
        model_path = dataframe_context.get_model_path()
        result_column = dataframe_context.get_result_column()
        if result_column in df.columns:
            df_helper.remove_null_rows(result_column)
        df = df_helper.get_data_frame()
        df = df_helper.fill_missing_values(df)

        if "RandomForest" in model_path:
            df = df.toPandas()
            trainedModel = RandomForestScript(df, df_helper, dataframe_context, spark)
            # trainedModel = RandomForestPysparkScript(df, df_helper, dataframe_context, spark)
            trainedModel.Predict()
            print "Scoring Done in ", time.time() - st,  " seconds."
        elif "XGBoost" in model_path:
            df = df.toPandas()
            trainedModel = XgboostScript(df, df_helper, dataframe_context, spark)
            trainedModel.Predict()
            print "Scoring Done in ", time.time() - st,  " seconds."
        elif "LogisticRegression" in model_path:
            df = df.toPandas()
            trainedModel = LogisticRegressionScript(df, df_helper, dataframe_context, spark)
            # trainedModel = LogisticRegressionPysparkScript(df, df_helper, dataframe_context, spark)
            trainedModel.Predict()
            print "Scoring Done in ", time.time() - st,  " seconds."
        else:
            print "Could Not Load the Model for Scoring"

    print "Scripts Time : ", time.time() - script_start_time, " seconds."
    print "Data Load Time : ", data_load_time, " seconds."
    #spark.stop()

if __name__ == '__main__':
    main(sys.argv[1])
    print 'Main Method End .....'
