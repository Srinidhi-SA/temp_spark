import time
import json
try:
    import cPickle as pickle
except:
    import pickle

from sklearn.externals import joblib
from sklearn import metrics
import xgboost as xgb

from pyspark.sql import SQLContext
from bi.common import utils
from bi.common import DataWriter
from bi.common import BIException
from bi.algorithms import XgboostClassifier
from bi.algorithms import utils as MLUtils
from bi.common import DataFrameHelper
from bi.stats.frequency_dimensions import FreqDimensions
from bi.narratives.dimension.dimension_column import DimensionColumnNarrative
from bi.stats.chisquare import ChiSquare
from bi.narratives.chisquare import ChiSquareNarratives

class XgboostScript:
    def __init__(self, data_frame, df_helper,df_context, spark):
        self._data_frame = data_frame
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context
        self._spark = spark
        self._model_summary = {"confusion_matrix":{},"precision_recall_stats":{}}
        self._score_summary = {}

    def Train(self):
        st = time.time()
        categorical_columns = self._dataframe_helper.get_string_columns()
        numerical_columns = self._dataframe_helper.get_numeric_columns()
        result_column = self._dataframe_context.get_result_column()
        model_path = self._dataframe_context.get_model_path()
        train_test_ratio = self._dataframe_context.get_train_test_split()
        if train_test_ratio == None:
            train_test_ratio = 0.7

        drop_column_list = []
        self._data_frame = self._data_frame.loc[:,[col for col in self._data_frame.columns if col not in drop_column_list]]
        xgboost_obj = XgboostClassifier(self._data_frame, self._dataframe_helper, self._spark)
        # df = MLUtils.factorize_columns(self._data_frame,categorical_columns)
        df = MLUtils.factorize_columns(self._data_frame,[x for x in categorical_columns if x != result_column])
        x_train,x_test,y_train,y_test = MLUtils.generate_train_test_split(df,train_test_ratio,result_column,drop_column_list)
        clf_xgb = xgboost_obj.initiate_xgboost_classifier()
        objs = xgboost_obj.train_and_predict(x_train, x_test, y_train, y_test,clf_xgb,[])

        model_filepath = model_path+"/XGBoost/TrainedModels/model.pkl"
        summary_filepath = model_path+"/XGBoost/ModelSummary/summary.json"
        trained_model_string = pickle.dumps(objs["trained_model"])
        joblib.dump(objs["trained_model"],model_filepath)
        # confusion matrix keys are the predicted class
        self._model_summary["confusion_matrix"] = MLUtils.calculate_confusion_matrix(objs["actual"],objs["predicted"])
        self._model_summary["feature_importance"] = objs["feature_importance"]
        self._model_summary["model_accuracy"] = metrics.accuracy_score(objs["actual"], objs["predicted"])
        self._model_summary["runtime_in_seconds"] = round((time.time() - st),2)

        overall_precision_recall = MLUtils.calculate_overall_precision_recall(objs["actual"],objs["predicted"])
        self._model_summary["precision_recall_stats"] = overall_precision_recall["classwise_stats"]
        self._model_summary["model_precision"] = overall_precision_recall["precision"]
        self._model_summary["model_recall"] = overall_precision_recall["recall"]
        self._model_summary["target_variable"] = result_column
        self._model_summary["test_sample_prediction"] = overall_precision_recall["prediction_split"]
        self._model_summary["algorithm_name"] = "Xgboost"
        self._model_summary["validation_method"] = "Cross Validation"
        self._model_summary["independent_variables"] = len(list(set(df.columns)-set([result_column])))

        self._model_summary["total_trees"] = 100
        self._model_summary["total_rules"] = 300

        # DataWriter.write_dict_as_json(self._spark, {"modelSummary":json.dumps(self._model_summary)}, summary_filepath)
        # print self._model_summary
        utils.write_to_file(summary_filepath,json.dumps({"modelSummary":self._model_summary}))


    def Predict(self):
        xgboost_obj = XgboostClassifier(self._data_frame, self._dataframe_helper, self._spark)
        categorical_columns = self._dataframe_helper.get_string_columns()
        numerical_columns = self._dataframe_helper.get_numeric_columns()
        result_column = self._dataframe_context.get_result_column()
        test_data_path = self._dataframe_context.get_input_file()
        score_data_path = self._dataframe_context.get_score_path()+"/ScoredData/data.csv"
        trained_model_path = self._dataframe_context.get_model_path()
        score_summary_path = self._dataframe_context.get_score_path()+"/Summary/summary.json"

        trained_model = joblib.load(trained_model_path)
        # pandas_df = self._data_frame.toPandas()
        df = self._data_frame
        pandas_df = MLUtils.factorize_columns(df,[x for x in categorical_columns if x != result_column])
        score = xgboost_obj.predict(pandas_df,trained_model,[result_column])
        df["predicted_class"] = score["predicted_class"]
        df["predicted_probability"] = score["predicted_probability"]
        self._score_summary["prediction_split"] = MLUtils.calculate_scored_probability_stats(df)
        self._score_summary["result_column"] = result_column

        df = df.rename(index=str, columns={"predicted_class": result_column})
        df.to_csv(score_data_path,header=True,index=False)
        utils.write_to_file(score_summary_path,json.dumps({"scoreSummary":self._score_summary}))

        print "STARTING DIMENSION ANALYSIS ..."
        # Dropping predicted_probability column
        df.drop('predicted_probability', axis=1, inplace=True)
        SQLctx = SQLContext(sparkContext=self._spark.sparkContext, sparkSession=self._spark)
        spark_scored_df = SQLctx.createDataFrame(df)
        # spark_scored_df.write.csv(score_data_path+"/data",mode="overwrite",header=True)

        df_helper = DataFrameHelper(spark_scored_df, self._dataframe_context)
        df_helper.set_params()
        df = df_helper.get_data_frame()
        # result_column = "predicted_class"
        try:
            fs = time.time()
            narratives_file = self._dataframe_context.get_score_path()+"/narratives/FreqDimension/data.json"
            result_file = self._dataframe_context.get_score_path()+"/results/FreqDimension/data.json"
            df_freq_dimension_obj = FreqDimensions(spark_scored_df, df_helper, self._dataframe_context).test_all(dimension_columns=[result_column])
            df_freq_dimension_result = utils.as_dict(df_freq_dimension_obj)
            utils.write_to_file(result_file,json.dumps(df_freq_dimension_result))
            # Narratives
            narratives_obj = DimensionColumnNarrative(result_column, df_helper, self._dataframe_context, df_freq_dimension_obj)
            narratives = utils.as_dict(narratives_obj)
            utils.write_to_file(narratives_file,json.dumps(narratives))
            print "Frequency Analysis Done in ", time.time() - fs,  " seconds."
        except:
            print "Frequency Analysis Failed "

        try:
            fs = time.time()
            narratives_file = self._dataframe_context.get_score_path()+"/narratives/ChiSquare/data.json"
            result_file = self._dataframe_context.get_score_path()+"/results/ChiSquare/data.json"
            df_chisquare_obj = ChiSquare(df, df_helper, self._dataframe_context).test_all(dimension_columns= [result_column])
            df_chisquare_result = utils.as_dict(df_chisquare_obj)
            # print 'RESULT: %s' % (json.dumps(df_chisquare_result, indent=2))
            utils.write_to_file(result_file,json.dumps(df_chisquare_result))
            chisquare_narratives = utils.as_dict(ChiSquareNarratives(len(df_helper.get_string_columns()), df_chisquare_obj, self._dataframe_context))
            # print 'Narrarives: %s' %(json.dumps(chisquare_narratives, indent=2))
            utils.write_to_file(narratives_file,json.dumps(chisquare_narratives))
            print "ChiSquare Analysis Done in ", time.time() - fs, " seconds."
        except:
            print "ChiSquare Analysis Failed "