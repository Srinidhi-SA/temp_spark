import json
import time
import collections


try:
    import cPickle as pickle
except:
    import pickle

from sklearn.externals import joblib
from sklearn import metrics

from pyspark.sql import SQLContext
from bi.common import utils as CommonUtils
from bi.algorithms import XgboostClassifier
from bi.algorithms import utils as MLUtils
from bi.common import DataFrameHelper
from bi.stats.frequency_dimensions import FreqDimensions
from bi.narratives.dimension.dimension_column import DimensionColumnNarrative
from bi.stats.chisquare import ChiSquare
from bi.narratives.chisquare import ChiSquareNarratives
from bi.common import NormalCard,SummaryCard,NarrativesTree,HtmlData,C3ChartData,TableData,TreeData
from bi.common import ScatterChartData,NormalChartData,ChartJson


class XgboostScript:
    def __init__(self, data_frame, df_helper,df_context, spark, prediction_narrative, result_setter):
        self._prediction_narrative = prediction_narrative
        self._result_setter = result_setter
        self._data_frame = data_frame
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context
        self._spark = spark
        self._model_summary = {"confusion_matrix":{},"precision_recall_stats":{}}
        self._score_summary = {}
        self._model_slug_map = MLUtils.model_slug_mapping()
        self._slug = self._model_slug_map["xgboost"]

        self._completionStatus = self._dataframe_context.get_completion_status()
        print self._completionStatus,"initial completion status"
        self._analysisName = "randomForest"
        self._messageURL = self._dataframe_context.get_message_url()
        self._scriptWeightDict = self._dataframe_context.get_ml_model_training_weight()

        self._scriptStages = {
            "initialization":{
                "summary":"Initialized the Logistic Regression Scripts",
                "weight":4
                },
            "training":{
                "summary":"Logistic Regression Model Training Started",
                "weight":2
                },
            "completion":{
                "summary":"Logistic Regression Model Training Finished",
                "weight":4
                },
            }

    def Train(self):
        st = time.time()

        self._completionStatus += self._scriptWeightDict[self._analysisName]["total"]*self._scriptStages["initialization"]["weight"]/10
        progressMessage = CommonUtils.create_progress_message_object(self._analysisName,\
                                    "initialization",\
                                    "info",\
                                    self._scriptStages["initialization"]["summary"],\
                                    self._completionStatus,\
                                    self._completionStatus)
        CommonUtils.save_progress_message(self._messageURL,progressMessage)
        self._dataframe_context.update_completion_status(self._completionStatus)

        categorical_columns = self._dataframe_helper.get_string_columns()
        numerical_columns = self._dataframe_helper.get_numeric_columns()
        result_column = self._dataframe_context.get_result_column()
        model_path = self._dataframe_context.get_model_path()
        if model_path.startswith("file"):
            model_path = model_path[7:]
        xgboost_obj = XgboostClassifier(self._data_frame, self._dataframe_helper, self._spark)
        x_train,x_test,y_train,y_test = self._dataframe_helper.get_train_test_data()

        self._completionStatus += self._scriptWeightDict[self._analysisName]["total"]*self._scriptStages["training"]["weight"]/10
        progressMessage = CommonUtils.create_progress_message_object(self._analysisName,\
                                    "training",\
                                    "info",\
                                    self._scriptStages["training"]["summary"],\
                                    self._completionStatus,\
                                    self._completionStatus)
        CommonUtils.save_progress_message(self._messageURL,progressMessage)
        self._dataframe_context.update_completion_status(self._completionStatus)

        clf_xgb = xgboost_obj.initiate_xgboost_classifier()
        objs = xgboost_obj.train_and_predict(x_train, x_test, y_train, y_test,clf_xgb,[])

        model_filepath = model_path+"/"+self._slug+"/model.pkl"
        summary_filepath = model_path+"/"+self._slug+"/ModelSummary/summary.json"
        trained_model_string = pickle.dumps(objs["trained_model"])
        joblib.dump(objs["trained_model"],model_filepath)
        # confusion matrix keys are the predicted class
        self._model_summary["confusion_matrix"] = MLUtils.calculate_confusion_matrix(objs["actual"],objs["predicted"])
        self._model_summary["feature_importance"] = objs["feature_importance"]
        # self._model_summary["feature_importance"] = MLUtils.transform_feature_importance(objs["feature_importance"])

        self._model_summary["model_accuracy"] = round(metrics.accuracy_score(objs["actual"], objs["predicted"]),2)
        self._model_summary["runtime_in_seconds"] = round((time.time() - st),2)

        overall_precision_recall = MLUtils.calculate_overall_precision_recall(objs["actual"],objs["predicted"])
        self._model_summary["precision_recall_stats"] = overall_precision_recall["classwise_stats"]
        self._model_summary["model_precision"] = overall_precision_recall["precision"]
        self._model_summary["model_recall"] = overall_precision_recall["recall"]
        self._model_summary["target_variable"] = result_column
        self._model_summary["test_sample_prediction"] = overall_precision_recall["prediction_split"]
        self._model_summary["algorithm_name"] = "Xgboost"
        self._model_summary["validation_method"] = "Train and Test"
        self._model_summary["independent_variables"] = len(list(set(x_train.columns)-set([result_column])))
        cat_cols = list(set(categorical_columns)-set([result_column]))
        self._model_summary["level_counts"] = CommonUtils.get_level_count_dict(x_train,cat_cols,self._dataframe_context.get_column_separator())

        self._model_summary["total_trees"] = 100
        self._model_summary["total_rules"] = 300

        prediction_split_dict = dict(collections.Counter(objs["predicted"]))
        prediction_split_array = []
        for k,v in prediction_split_dict.items():
            prediction_split_array.append([k,v])
        prediction_split_array = sorted(prediction_split_array,key=lambda x:x[1],reverse=True)
        total = len(objs["predicted"])
        prediction_split_array = [[val[0],round(float(val[1])*100/total,2)] for val in prediction_split_array]
        self._result_setter.set_model_summary({"xgboost":self._model_summary})
        xgbCard1 = NormalCard()
        xgbCard1Data = []
        xgbCard1Data.append(HtmlData(data="<h4 class = 'sm-mb-20'>XGBoost</h4>"))
        xgbCard1Data.append(HtmlData(data="<h5>Summary</h5>"))
        xgbCard1Data.append(HtmlData(data="<p>Target Varialble - {}</p>".format(result_column)))
        xgbCard1Data.append(HtmlData(data="<p>Independent Variable Chosen - {}</p>".format(self._model_summary["independent_variables"])))
        xgbCard1Data.append(HtmlData(data="<h5>Predicted Distribution</h5>"))
        for val in prediction_split_array:
            xgbCard1Data.append(HtmlData(data="<p>{} - {}%</p>".format(val[0],val[1])))
        xgbCard1Data.append(HtmlData(data="<p>Algorithm - {}</p>".format(self._model_summary["algorithm_name"])))
        xgbCard1Data.append(HtmlData(data="<p>Total Trees - {}</p>".format(self._model_summary["total_trees"])))
        xgbCard1Data.append(HtmlData(data="<p>Total Rules - {}</p>".format(self._model_summary["total_rules"])))
        xgbCard1Data.append(HtmlData(data="<p>Validation Method - {}</p>".format(self._model_summary["validation_method"])))
        xgbCard1Data.append(HtmlData(data="<p>Model Accuracy - {}</p>".format(self._model_summary["model_accuracy"])))
        xgbCard1.set_card_data(xgbCard1Data)

        confusion_matrix = self._model_summary["confusion_matrix"]
        predictedLevels = confusion_matrix.keys()
        confusion_matrix_data = [[""]+predictedLevels]

        for outer in predictedLevels:
            inner_list = [outer]
            for inner in predictedLevels:
                inner_list.append(confusion_matrix[outer][inner])
            confusion_matrix_data.append(inner_list)

        xgbCard2 = NormalCard()
        xgbCard2Data = []
        xgbCard2Data.append(HtmlData(data="<h5 class = 'sm-ml-15 sm-pb-10' >Confusion Matrix</h5>"))
        card2Table = TableData()
        card2Table.set_table_data(confusion_matrix_data)
        card2Table.set_table_type("confusionMatrix")
        card2Table.set_table_top_header("Actual")
        card2Table.set_table_left_header("Predicted")
        xgbCard2Data.append(card2Table)
        xgbCard2.set_card_data(xgbCard2Data)
        self._prediction_narrative.add_a_card(xgbCard1)
        self._prediction_narrative.add_a_card(xgbCard2)
        modelSummaryJson = {
            "dropdown":{"name":"Xgboost","accuracy":self._model_summary["model_accuracy"],"slug":self._slug},
            "levelcount":[self._model_summary["level_counts"]],
            "modelFeatures":[],
        }
        self._result_setter.set_xgboost_model_summary(modelSummaryJson)
        xgbCard1 = json.loads(CommonUtils.convert_python_object_to_json(xgbCard1))
        xgbCard2 = json.loads(CommonUtils.convert_python_object_to_json(xgbCard2))
        self._result_setter.set_xgb_cards([xgbCard1,xgbCard2])

        self._completionStatus += self._scriptWeightDict[self._analysisName]["total"]*self._scriptStages["completion"]["weight"]/10
        progressMessage = CommonUtils.create_progress_message_object(self._analysisName,\
                                    "completion",\
                                    "info",\
                                    self._scriptStages["completion"]["summary"],\
                                    self._completionStatus,\
                                    self._completionStatus)
        CommonUtils.save_progress_message(self._messageURL,progressMessage)
        self._dataframe_context.update_completion_status(self._completionStatus)
        # DataWriter.write_dict_as_json(self._spark, {"modelSummary":json.dumps(self._model_summary)}, summary_filepath)
        # print self._model_summary
        # CommonUtils.write_to_file(summary_filepath,json.dumps({"modelSummary":self._model_summary}))


    def Predict(self):
        self._scriptWeightDict = self._dataframe_context.get_ml_model_prediction_weight()
        self._scriptStages = {
            "initialization":{
                "summary":"Initialized the Xgboost Scripts",
                "weight":2
                },
            "prediction":{
                "summary":"XGBoost Model Prediction Finished",
                "weight":2
                },
            "frequency":{
                "summary":"descriptive analysis finished",
                "weight":2
                },
            "chisquare":{
                "summary":"chi Square analysis finished",
                "weight":4
                },
            "completion":{
                "summary":"all analysis finished",
                "weight":4
                },
            }

        self._completionStatus += self._scriptWeightDict[self._analysisName]["total"]*self._scriptStages["initialization"]["weight"]/10
        progressMessage = CommonUtils.create_progress_message_object(self._analysisName,\
                                    "initialization",\
                                    "info",\
                                    self._scriptStages["initialization"]["summary"],\
                                    self._completionStatus,\
                                    self._completionStatus)
        CommonUtils.save_progress_message(self._messageURL,progressMessage)
        self._dataframe_context.update_completion_status(self._completionStatus)

        dataSanity = True
        level_counts_train = self._dataframe_context.get_level_count_dict()
        cat_cols = self._dataframe_helper.get_string_columns()
        level_counts_score = CommonUtils.get_level_count_dict(self._data_frame,cat_cols,self._dataframe_context.get_column_separator(),output_type="dict")
        if level_counts_train != {}:
            for key in level_counts_train:
                if key in level_counts_score:
                    if level_counts_train[key] != level_counts_score[key]:
                        dataSanity = False
                else:
                    dataSanity = False

        xgboost_obj = XgboostClassifier(self._data_frame, self._dataframe_helper, self._spark)
        categorical_columns = self._dataframe_helper.get_string_columns()
        numerical_columns = self._dataframe_helper.get_numeric_columns()
        result_column = self._dataframe_context.get_result_column()
        test_data_path = self._dataframe_context.get_input_file()
        score_data_path = self._dataframe_context.get_score_path()+"/data.csv"
        if score_data_path.startswith("file"):
            score_data_path = score_data_path[7:]
        trained_model_path = self._dataframe_context.get_model_path()
        print trained_model_path
        trained_model_path += "/model.pkl"

        if trained_model_path.startswith("file"):
            trained_model_path = trained_model_path[7:]
        score_summary_path = self._dataframe_context.get_score_path()+"/Summary/summary.json"
        if score_summary_path.startswith("file"):
            score_summary_path = score_summary_path[7:]
        trained_model = joblib.load(trained_model_path)
        # pandas_df = self._data_frame.toPandas()
        df = self._data_frame
        pandas_df = MLUtils.factorize_columns(df,[x for x in categorical_columns if x != result_column])
        score = xgboost_obj.predict(pandas_df,trained_model,[result_column])
        df["predicted_class"] = score["predicted_class"]
        df["predicted_probability"] = score["predicted_probability"]
        self._score_summary["prediction_split"] = MLUtils.calculate_scored_probability_stats(df)
        self._score_summary["result_column"] = result_column
        if result_column in df.columns:
            df.drop(result_column, axis=1, inplace=True)
        df = df.rename(index=str, columns={"predicted_class": result_column})
        df.to_csv(score_data_path,header=True,index=False)

        self._completionStatus += self._scriptWeightDict[self._analysisName]["total"]*self._scriptStages["prediction"]["weight"]/10
        progressMessage = CommonUtils.create_progress_message_object(self._analysisName,\
                                    "prediction",\
                                    "info",\
                                    self._scriptStages["prediction"]["summary"],\
                                    self._completionStatus,\
                                    self._completionStatus)
        CommonUtils.save_progress_message(self._messageURL,progressMessage)
        self._dataframe_context.update_completion_status(self._completionStatus)

        # CommonUtils.write_to_file(score_summary_path,json.dumps({"scoreSummary":self._score_summary}))

        print "STARTING DIMENSION ANALYSIS ..."
        columns_to_keep = []
        columns_to_drop = []
        considercolumnstype = self._dataframe_context.get_score_consider_columns_type()
        considercolumns = self._dataframe_context.get_score_consider_columns()
        if considercolumnstype != None:
            if considercolumns != None:
                if considercolumnstype == ["excluding"]:
                    columns_to_drop = considercolumns
                elif considercolumnstype == ["including"]:
                    columns_to_keep = considercolumns
        if len(columns_to_keep) > 0:
            columns_to_drop = list(set(df.columns)-set(columns_to_keep))
        else:
            columns_to_drop += ["predicted_probability"]
        columns_to_drop = [x for x in columns_to_drop if x in df.columns and x != result_column]
        df.drop(columns_to_drop, axis=1, inplace=True)
        # # Dropping predicted_probability column
        # df.drop('predicted_probability', axis=1, inplace=True)
        SQLctx = SQLContext(sparkContext=self._spark.sparkContext, sparkSession=self._spark)
        spark_scored_df = SQLctx.createDataFrame(df)
        # spark_scored_df.write.csv(score_data_path+"/data",mode="overwrite",header=True)

        df_helper = DataFrameHelper(spark_scored_df, self._dataframe_context)
        df_helper.set_params()
        df = df_helper.get_data_frame()
        try:
            fs = time.time()
            narratives_file = self._dataframe_context.get_score_path()+"/narratives/FreqDimension/data.json"
            if narratives_file.startswith("file"):
                narratives_file = narratives_file[7:]
            result_file = self._dataframe_context.get_score_path()+"/results/FreqDimension/data.json"
            if result_file.startswith("file"):
                result_file = result_file[7:]
            init_freq_dim = FreqDimensions(df, df_helper, self._dataframe_context,scriptWeight=self._scriptWeightDict,analysisName=self._analysisName)
            df_freq_dimension_obj = init_freq_dim.test_all(dimension_columns=[result_column])
            df_freq_dimension_result = CommonUtils.as_dict(df_freq_dimension_obj)
            narratives_obj = DimensionColumnNarrative(result_column, df_helper, self._dataframe_context, df_freq_dimension_obj,self._result_setter,self._prediction_narrative,scriptWeight=self._scriptWeightDict,analysisName=self._analysisName)
            narratives = CommonUtils.as_dict(narratives_obj)

            print "Frequency Analysis Done in ", time.time() - fs,  " seconds."
            self._completionStatus += self._scriptWeightDict[self._analysisName]["total"]*self._scriptStages["frequency"]["weight"]/10
            progressMessage = CommonUtils.create_progress_message_object(self._analysisName,\
                                        "frequency",\
                                        "info",\
                                        self._scriptStages["frequency"]["summary"],\
                                        self._completionStatus,\
                                        self._completionStatus)
            CommonUtils.save_progress_message(self._messageURL,progressMessage)
            self._dataframe_context.update_completion_status(self._completionStatus)
            print "Frequency ",self._completionStatus
        except:
            print "Frequency Analysis Failed "

        try:
            fs = time.time()
            narratives_file = self._dataframe_context.get_score_path()+"/narratives/ChiSquare/data.json"
            if narratives_file.startswith("file"):
                narratives_file = narratives_file[7:]
            result_file = self._dataframe_context.get_score_path()+"/results/ChiSquare/data.json"
            if result_file.startswith("file"):
                result_file = result_file[7:]
            init_chisquare_obj = ChiSquare(df, df_helper, self._dataframe_context,scriptWeight=self._scriptWeightDict,analysisName=self._analysisName)
            df_chisquare_obj = init_chisquare_obj.test_all(dimension_columns= [result_column])
            df_chisquare_result = CommonUtils.as_dict(df_chisquare_obj)
            chisquare_narratives = CommonUtils.as_dict(ChiSquareNarratives(df_helper, df_chisquare_obj, self._dataframe_context,df,self._prediction_narrative,self._result_setter,scriptWeight=self._scriptWeightDict,analysisName=self._analysisName))
        except:
            print "ChiSquare Analysis Failed "
