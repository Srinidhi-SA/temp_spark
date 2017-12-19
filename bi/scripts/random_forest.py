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
from bi.algorithms import RandomForest
from bi.algorithms import utils as MLUtils
from bi.common import MLModelSummary
from bi.common import DataFrameHelper
from bi.stats.frequency_dimensions import FreqDimensions
from bi.narratives.dimension.dimension_column import DimensionColumnNarrative
from bi.stats.chisquare import ChiSquare
from bi.narratives.chisquare import ChiSquareNarratives
from bi.common import NormalCard,SummaryCard,NarrativesTree,HtmlData,C3ChartData,TableData,TreeData
from bi.common import ScatterChartData,NormalChartData,ChartJson,ModelSummary





class RandomForestScript:
    def __init__(self, data_frame, df_helper,df_context, spark, prediction_narrative, result_setter,meta_parser):
        self._metaParser = meta_parser
        self._prediction_narrative = prediction_narrative
        self._result_setter = result_setter
        self._data_frame = data_frame
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context
        self._spark = spark
        self._model_summary = {"confusion_matrix":{},"precision_recall_stats":{},"FrequencySummary":{},"ChiSquare":{}}
        self._score_summary = {}
        self._model_slug_map = MLUtils.model_slug_mapping()
        self._slug = self._model_slug_map["randomforest"]

        self._completionStatus = self._dataframe_context.get_completion_status()
        print self._completionStatus,"initial completion status"
        self._analysisName = "randomForest"
        self._messageURL = self._dataframe_context.get_message_url()
        self._scriptWeightDict = self._dataframe_context.get_ml_model_training_weight()

        self._scriptStages = {
            "initialization":{
                "summary":"Initialized the Random Forest Scripts",
                "weight":4
                },
            "training":{
                "summary":"Random Forest Model Training Started",
                "weight":2
                },
            "completion":{
                "summary":"Random Forest Model Training Finished",
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
        random_forest_obj = RandomForest(self._data_frame, self._dataframe_helper, self._spark)
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

        clf_rf = random_forest_obj.initiate_forest_classifier(10,4)
        objs = random_forest_obj.train_and_predict(x_train, x_test, y_train, y_test,clf_rf,False,True,[])
        runtime = round((time.time() - st),2)
        model_filepath = str(model_path)+"/"+str(self._slug)+"/model.pkl"
        summary_filepath = model_path+"/"+self._slug+"/ModelSummary/summary.json"
        print model_filepath
        trained_model_string = pickle.dumps(objs["trained_model"])
        joblib.dump(objs["trained_model"],model_filepath)

        cat_cols = list(set(categorical_columns)-set([result_column]))
        overall_precision_recall = MLUtils.calculate_overall_precision_recall(objs["actual"],objs["predicted"])
        self._model_summary = MLModelSummary()
        self._model_summary.set_algorithm_name("Random Forest")
        self._model_summary.set_algorithm_display_name("Random Forest")
        self._model_summary.set_slug(self._slug)
        self._model_summary.set_training_time(runtime)
        self._model_summary.set_confusion_matrix(MLUtils.calculate_confusion_matrix(objs["actual"],objs["predicted"]))
        self._model_summary.set_feature_importance(objs["feature_importance"])
        self._model_summary.set_model_accuracy(round(metrics.accuracy_score(objs["actual"], objs["predicted"]),2))
        self._model_summary.set_training_time(round((time.time() - st),2))
        self._model_summary.set_precision_recall_stats(overall_precision_recall["classwise_stats"])
        self._model_summary.set_model_precision(overall_precision_recall["precision"])
        self._model_summary.set_model_recall(overall_precision_recall["recall"])
        self._model_summary.set_target_variable(result_column)
        self._model_summary.set_prediction_split(overall_precision_recall["prediction_split"])
        self._model_summary.set_validation_method("Train and Test")
        self._model_summary.set_model_features(list(set(x_train.columns)-set([result_column])))
        self._model_summary.set_level_counts(self._metaParser.get_unique_level_dict(cat_cols))
        self._model_summary.set_num_trees(100)
        self._model_summary.set_num_rules(300)
        modelSummaryJson = {
            "dropdown":{
                        "name":self._model_summary.get_algorithm_name(),
                        "accuracy":self._model_summary.get_model_accuracy(),
                        "slug":self._model_summary.get_slug()
                        },
            "levelcount":[self._model_summary.get_level_counts()],
            "modelFeatures":[],
        }

        rfCards = [json.loads(CommonUtils.convert_python_object_to_json(cardObj)) for cardObj in MLUtils.create_model_summary_cards(self._model_summary)]
        for card in rfCards:
            self._prediction_narrative.add_a_card(card)

        self._result_setter.set_model_summary({"randomforest":json.loads(CommonUtils.convert_python_object_to_json(self._model_summary))})
        self._result_setter.set_random_forest_model_summary(modelSummaryJson)
        self._result_setter.set_rf_cards(rfCards)

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
                "summary":"Initialized the Random Forest Scripts",
                "weight":2
                },
            "prediction":{
                "summary":"Random Forest Model Prediction Finished",
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
        # Match with the level_counts and then clean the data
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

        random_forest_obj = RandomForest(self._data_frame, self._dataframe_helper, self._spark)
        categorical_columns = self._dataframe_helper.get_string_columns()
        numerical_columns = self._dataframe_helper.get_numeric_columns()
        result_column = self._dataframe_context.get_result_column()
        test_data_path = self._dataframe_context.get_input_file()
        score_data_path = self._dataframe_context.get_score_path()+"/data.csv"
        print "score_data_path",score_data_path
        if score_data_path.startswith("file"):
            score_data_path = score_data_path[7:]
        trained_model_path = self._dataframe_context.get_model_path()
        print "trained_model_path",trained_model_path
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
        score = random_forest_obj.predict(pandas_df,trained_model,[result_column])
        df["predicted_class"] = score["predicted_class"]
        df["predicted_probability"] = score["predicted_probability"]
        self._score_summary["prediction_split"] = MLUtils.calculate_scored_probability_stats(df)
        self._score_summary["result_column"] = result_column
        if result_column in df.columns:
            df.drop(result_column, axis=1, inplace=True)
        df = df.rename(index=str, columns={"predicted_class": result_column})
        df.to_csv(score_data_path,header=True,index=False)
        print "Predicted Columns"
        print df.columns

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
        print "columns_to_drop",columns_to_drop
        df.drop(columns_to_drop, axis=1, inplace=True)
        # # Dropping predicted_probability column
        # df.drop('predicted_probability', axis=1, inplace=True)
        self._dataframe_context.set_story_on_scored_data(True)
        SQLctx = SQLContext(sparkContext=self._spark.sparkContext, sparkSession=self._spark)
        spark_scored_df = SQLctx.createDataFrame(df)
        # spark_scored_df.write.csv(score_data_path+"/data",mode="overwrite",header=True)

        df_helper = DataFrameHelper(spark_scored_df, self._dataframe_context)
        df_helper.set_params()
        df = df_helper.get_data_frame()
        print df.columns
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
