import time
import json
try:
    import cPickle as pickle
except:
    import pickle

from sklearn.externals import joblib
from sklearn import metrics

from pyspark.sql import SQLContext
from bi.common import utils
from bi.common import DataWriter
from bi.common import BIException
from bi.algorithms import LogisticRegression
from bi.algorithms import utils as MLUtils


class LogisticRegressionScript:
    def __init__(self, data_frame, df_helper,df_context, spark):
        self._data_frame = data_frame
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context
        self._spark = spark
        self._model_summary = {"confusion_matrix":{},"precision_recall_stats":{}}

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
        levels = self._data_frame[result_column].unique()
        logistic_regression_obj = LogisticRegression(self._data_frame, self._dataframe_helper, self._spark)
        logistic_regression_obj.set_number_of_levels(levels)

        df = MLUtils.factorize_columns(self._data_frame,categorical_columns)
        x_train,x_test,y_train,y_test = MLUtils.generate_train_test_split(df,train_test_ratio,result_column,drop_column_list)
        clf_lr = logistic_regression_obj.initiate_logistic_regression_classifier()
        objs = logistic_regression_obj.train_and_predict(x_train, x_test, y_train, y_test,clf_lr,[])

        model_filepath = model_path+"/LogisticRegression/TrainedModels/model.pkl"
        summary_filepath = model_path+"/LogisticRegression/ModelSummary/summary.json"
        trained_model_string = pickle.dumps(objs["trained_model"])
        joblib.dump(objs["trained_model"],model_filepath)

        self._model_summary["confusion_matrix"] = MLUtils.calculate_confusion_matrix(objs["actual"],objs["predicted"]).to_json()
        self._model_summary["precision_recall_stats"] = MLUtils.calculate_precision_recall(objs["actual"],objs["predicted"])
        self._model_summary["feature_importance"] = objs["feature_importance"]
        self._model_summary["accuracy_score"] = metrics.accuracy_score(objs["actual"], objs["predicted"])
        self._model_summary["runtime_in_seconds"] = round((time.time() - st),2)

        # DataWriter.write_dict_as_json(self._spark, {"modelSummary":json.dumps(self._model_summary)}, summary_filepath)
        print self._model_summary
        f = open(summary_filepath, 'w')
        f.write(json.dumps({"modelSummary":self._model_summary}))
        f.close()


    def Predict(self):
        logistic_regression_obj = LogisticRegression(self._data_frame, self._dataframe_helper, self._spark)
        test_data_path = self._dataframe_context.get_input_file()
        score_data_path = self._dataframe_context.get_score_path()+"/ScoredData/data.csv"
        trained_model_path = self._dataframe_context.get_model_path()
        score_summary_path = self._dataframe_context.get_score_path()+"/Summary/summary.json"

        trained_model = joblib.load(trained_model_path)
        pandas_df = self._data_frame.toPandas()
        score = logistic_regression_obj.predict(pandas_df,trained_model,[])
        y_score = score
        pandas_df["predicted_class"] = y_score
        SQLctx = SQLContext(sparkContext=self._spark.sparkContext, sparkSession=self._spark)
        spark_scored_df = SQLctx.createDataFrame(pandas_df)
        spark_scored_df.write.csv(score_data_path+"/data",mode="overwrite",header=True)
