import sys
import time

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


from parser import configparser

def send_message_API(monitor_api, task, message, complete, progress):
    url = monitor_api
    message_dict = {}
    message_dict['task'] = task
    message_dict['message'] = message
    message_dict['complete'] = complete
    message_dict['progress'] = progress
    #r = requests.post(url, data=json.dumps(message_dict))
    #print json.loads(r.content)['message'] + " for ", task +'\n'


#if __name__ == '__main__':
def main(confFilePath):
    start_time = time.time()
    APP_NAME = 'mAdvisor'
    spark = CommonUtils.get_spark_session(app_name=APP_NAME)
    spark.sparkContext.setLogLevel("ERROR")

    config_file = confFilePath#sys.argv[1]
    config = ConfigParser.ConfigParser()
    config.optionxform=str
    config.read(config_file)
    config_obj = configparser.ParserConfig(config)
    config_obj.set_params()

    dataframe_context = ContextSetter(config_obj)
    dataframe_context.set_params()
    scripts_to_run = dataframe_context.get_scripts_to_run()
    if scripts_to_run==None:
        scripts_to_run = []
    df = DataLoader.load_csv_file(spark, dataframe_context.get_input_file())

    print "FILE LOADED: ", dataframe_context.get_input_file()
    df_helper = DataFrameHelper(df, dataframe_context)
    df_helper.set_params()
    df = df_helper.get_data_frame()
    result_setter = ResultSetter(df,dataframe_context)

    measure_columns = df_helper.get_numeric_columns()
    dimension_columns = df_helper.get_string_columns()
    data_load_time = time.time() - start_time
    script_start_time = time.time()

    analysistype = dataframe_context.get_analysis_type()
    appid = dataframe_context.get_app_id()
    print "ANALYSIS TYPE : ", analysistype

    monitor_api = dataframe_context.get_monitor_api()

    if analysistype == 'Dimension':
        print "STARTING DIMENSION ANALYSIS ..."
        df_helper.remove_nulls(dataframe_context.get_result_column())
        df = df_helper.get_data_frame()

        if ('Descriptive analysis' in scripts_to_run):
            try:
                fs = time.time()
                freq_obj = FreqDimensionsScript(df, df_helper, dataframe_context, spark)
                freq_obj.Run()
                print "Frequency Analysis Done in ", time.time() - fs,  " seconds."
                send_message_API(monitor_api, "FrequencyAnalysis", "FrequencyAnalysis Done", True, 100)
            except Exception as e:
                print "Frequency Analysis Failed "
                send_message_API(monitor_api, "FrequencyAnalysis", "FrequencyAnalysis Script Failed", False, 0)
                print "ERROR"*5
                print e
                print "ERROR"*5
        else:
            DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_narratives_file()+'FreqDimension/')
            print "Descriptive analysis Not in Scripts to run "

        if ('Dimension vs. Dimension' in scripts_to_run):
            try:
                df_helper.remove_nulls(dataframe_context.get_result_column())
                df = df_helper.get_data_frame()
                fs = time.time()
                chisquare_obj = ChiSquareScript(df, df_helper, dataframe_context, spark)
                chisquare_obj.Run()
                print "ChiSquare Analysis Done in ", time.time() - fs, " seconds."
                send_message_API(monitor_api, "ChiSquare", "ChiSquare Done", True, 100)
            except Exception as e:
                print "ChiSquare Analysis Failed "
                send_message_API(monitor_api, "ChiSquare", "ChiSquare Failed", False, 0)
                print "ERROR"*5
                print e
                print "ERROR"*5
        else:
            DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_narratives_file()+'ChiSquare/')
            print "Dimension vs. Dimension Not in Scripts to run "

        if ('Predictive modeling' in scripts_to_run):
            try:
                fs = time.time()
                if df_helper.ignorecolumns != None:
                    df_helper.drop_ignore_columns()
                df_helper.fill_na_dimension_nulls()
                df = df_helper.get_data_frame()
                decision_tree_obj = DecisionTreeScript(df, df_helper, dataframe_context, spark)
                decision_tree_obj.Run()
                print "DecisionTrees Analysis Done in ", time.time() - fs, " seconds."
                send_message_API(monitor_api, "DecisionTrees", "DecisionTrees Done", True, 100)
            except Exception as e:
                send_message_API(monitor_api, "DecisionTrees", "DecisionTrees script Failed", False, 0)
                print "DecisionTrees Analysis Failed"
                print "ERROR"*5
                print e
                print "ERROR"*5
        else:
            DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_narratives_file()+'DecisionTree/')
            print "Predictive modeling Not in Scripts to run"

    elif analysistype == 'Measure':
        print "STARTING MEASURE ANALYSIS ..."
        df_helper.remove_nulls(dataframe_context.get_result_column())
        df = df_helper.get_data_frame()

        if ('Descriptive analysis' in scripts_to_run):
            try:
                fs = time.time()
                descr_stats_obj = DescriptiveStatsScript(df, df_helper, dataframe_context, result_setter, spark)
                descr_stats_obj.Run()
                print "DescriptiveStats Analysis Done in ", time.time() - fs, " seconds."
                send_message_API(monitor_api, "DescriptiveStats", "DescriptiveStats Done", True, 100)
            except Exception as e:
                DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_narratives_file()+'DescrStats/')
                DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_result_file()+'DescrStats/')
                send_message_API(monitor_api, "DescriptiveStats", "DescriptiveStats Failed", False, 0)
                print 'Descriptive Failed'
                print "ERROR"*5
                print e
                print "ERROR"*5

            try:
                fs = time.time()
                histogram_obj = HistogramsScript(df, df_helper, dataframe_context, spark)
                histogram_obj.Run()
                print "Histogram Analysis Done in ", time.time() - fs, " seconds."
                send_message_API(monitor_api, "Histogram", "Histogram Done", True, 100)
            except Exception as e:
                DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_result_file()+'Histogram/')
                send_message_API(monitor_api, "Histogram", "Histogram Failed", False, 0)
                print "ERROR"*5
                print e
                print "ERROR"*5
            try:
                fs = time.time()
                d_histogram_obj = DensityHistogramsScript(df, df_helper, dataframe_context, spark)
                d_histogram_obj.Run()
                print "Density Histogram Analysis Done in ", time.time() - fs, " seconds."
                send_message_API(monitor_api, "Density Histogram", "Density Histogram Done", True, 100)
            except Exception as e:
                DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_result_file()+'Density_Histogram/')
                send_message_API(monitor_api, "Density Histogram", "Density Histogram Failed", False, 0)
                print 'Density Histogram Failed'
                print "ERROR"*5
                print e
                print "ERROR"*5
        else:
            DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_narratives_file()+'DescrStats/')
            DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_result_file()+'DescrStats/')
            DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_result_file()+'Histogram/')
            send_message_API(monitor_api, "DescriptiveStats", "DescriptiveStats Failed", False, 0)
            send_message_API(monitor_api, "Histogram", "Histogram Failed", False, 0)

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
                send_message_API(monitor_api, "OneWayAnova", "OneWayAnova Done", True, 100)
            except Exception as e:
                print 'Anova Failed'
                DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_result_file()+'OneWayAnova/')
                DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_narratives_file()+'OneWayAnova/')
                send_message_API(monitor_api, "OneWayAnova", "OneWayAnova Script Failed", False, 0)
                print "ERROR"*5
                print e
                print "ERROR"*5
        else:
            DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_result_file()+'OneWayAnova/')
            DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_narratives_file()+'OneWayAnova/')
            send_message_API(monitor_api, "OneWayAnova", "OneWayAnova Analysis Not Required", False, 0)

        if len(measure_columns)>1 and 'Measure vs. Measure' in scripts_to_run:
            try:
                fs = time.time()
                correlation_obj = CorrelationScript(df, df_helper, dataframe_context, spark)
                correlations = correlation_obj.Run()
                print "Correlation Analysis Done in ", time.time() - fs ," seconds."
                send_message_API(monitor_api, "Correlation", "Correlation Done", True, 100)
                try:
                    df = df.na.drop(subset=measure_columns)
                    fs = time.time()
                    regression_obj = RegressionScript(df, df_helper, dataframe_context, result_setter, spark, correlations)
                    regression_obj.Run()
                    print "Regression Analysis Done in ", time.time() - fs, " seconds."
                    send_message_API(monitor_api, "Regression", "Regression Done", True, 100)
                except Exception as e:
                    DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_narratives_file()+'Regression/')
                    send_message_API(monitor_api, "Regression", "Regression Failed", False, 0)
                    print 'Regression Failed'
                    print "ERROR"*5
                    print e
                    print "ERROR"*5

            except Exception as e:
                print 'Correlation Failed. Regression not executed'
                DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_result_file()+'Correlation/')
                send_message_API(monitor_api, "Correlation", "Correlation Failed", False, 0)
                DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_narratives_file()+'Regression/')
                DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_result_file()+'Regression/')
                send_message_API(monitor_api, "Regression", "Regression Failed", False, 0)
                print "ERROR"*5
                print e
                print "ERROR"*5

        else:
            print 'Regression not in Scripts to run'
            DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_result_file()+'Correlation/')
            send_message_API(monitor_api, "Correlation", "Correlation Failed", False, 0)
            DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_narratives_file()+'Regression/')
            send_message_API(monitor_api, "Regression", "Regression Failed", False, 0)

        try:
            fs = time.time()
            trend_obj = TrendScript(df_helper,dataframe_context,result_setter,spark)
            trend_obj.Run()
            print "Trend Analysis Done in ", time.time() - fs, " seconds."
            send_message_API(monitor_api, "Trend", "Trend Done", True, 100)

        except Exception as e:
            DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_narratives_file()+'Trend/')
            send_message_API(monitor_api, "Trend", "Trend Failed", False, 0)
            print "Trend Script Failed"
            print "ERROR"*5
            print e
            print "ERROR"*5

        try:
            fs = time.time()
            df_helper.fill_na_dimension_nulls()
            df = df_helper.get_data_frame()
            dt_reg = DecisionTreeRegressionScript(df, df_helper, dataframe_context, result_setter, spark)
            dt_reg.Run()
            print "DecisionTrees Analysis Done in ", time.time() - fs, " seconds."
        except Exception as e:
            print "ERROR"*5
            print e
            print "ERROR"*5
            DataWriter.write_dict_as_json(spark, {}, dataframe_context.get_narratives_file()+'DecisionTreeReg/')
            send_message_API(monitor_api, "Decision Tree Regression", "Decision Tree Regression Failed", False, 0)
            print "Decision Tree Regression Script Failed"

        fs = time.time()
        exec_obj = ExecutiveSummaryScript(df_helper,dataframe_context,result_setter,spark)
        exec_obj.Run()
        print "Executive Summary Done in ", time.time() - fs, " seconds."
        # send_message_API(monitor_api, "ExecutiveSummary", "Executive Summary Done", True, 100)

    elif analysistype == 'Prediction':
        # df_helper.remove_nulls(dataframe_context.get_result_column())
        df = df.toPandas()
        df = df.dropna()
        categorical_columns = df_helper.get_string_columns()
        result_column = dataframe_context.get_result_column()
        drop_column_list = []
        df = df.loc[:,[col for col in df.columns if col not in drop_column_list]]
        df = MLUtils.factorize_columns(df,[x for x in categorical_columns if x != result_column])
        df_helper.set_train_test_data(df)
        try:
            st = time.time()
            # rf_obj = RandomForestScript(df, df_helper, dataframe_context, spark)
            rf_obj = RandomForestPysparkScript(df, df_helper, dataframe_context, spark)
            rf_obj.Train()
            print "Random Foreset Model Done in ", time.time() - st,  " seconds."
        except Exception as e:
            print "Random Foreset Model Failed"
            print "ERROR"*5
            print e
            print "ERROR"*5

        try:
            st = time.time()
            lr_obj = LogisticRegressionScript(df, df_helper, dataframe_context, spark)
            lr_obj.Train()
            print "Logistic Regression Model Done in ", time.time() - st,  " seconds."
        except Exception as e:
            print "Logistic Regression Model Failed"
            print "ERROR"*5
            print e
            print "ERROR"*5

        try:
            st = time.time()
            xgb_obj = XgboostScript(df, df_helper, dataframe_context, spark)
            xgb_obj.Train()
            print "XGBoost Model Done in ", time.time() - st,  " seconds."
        except Exception as e:
            print "Xgboost Model Failed"
            print "ERROR"*5
            print e
            print "ERROR"*5

    elif analysistype == 'Scoring':
        # df_helper.remove_nulls(dataframe_context.get_result_column())
        df = df.toPandas()
        df = df.dropna()
        model_path = dataframe_context.get_model_path()

        if "RandomForest" in model_path:
            st = time.time()
            # trainedModel = RandomForestScript(df, df_helper, dataframe_context, spark)
            trainedModel = RandomForestPysparkScript(df, df_helper, dataframe_context, spark)
            trainedModel.Predict()
            print "Scoring Done in ", time.time() - st,  " seconds."
        elif "XGBoost" in model_path:
            st = time.time()
            trainedModel = XgboostScript(df, df_helper, dataframe_context, spark)
            trainedModel.Predict()
            print "Scoring Done in ", time.time() - st,  " seconds."
        elif "LogisticRegression" in model_path:
            st = time.time()
            trainedModel = LogisticRegressionScript(df, df_helper, dataframe_context, spark)
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
