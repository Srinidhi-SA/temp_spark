import json
import time

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
from bi.common import DataFrameHelper
from bi.stats.frequency_dimensions import FreqDimensions
from bi.narratives.dimension.dimension_column import DimensionColumnNarrative
from bi.stats.chisquare import ChiSquare
from bi.narratives.chisquare import ChiSquareNarratives




class RandomForestPysparkScript:
    def __init__(self, data_frame, df_helper,df_context, spark):
        self._data_frame = data_frame
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context
        self._spark = spark
        self._model_summary = {"confusion_matrix":{},"precision_recall_stats":{},"FrequencySummary":{},"ChiSquare":{}}
        self._score_summary = {}

    def Train(self):
        st = time.time()
        categorical_columns = self._dataframe_helper.get_string_columns()
        numerical_columns = self._dataframe_helper.get_numeric_columns()
        result_column = self._dataframe_context.get_result_column()
        model_path = self._dataframe_context.get_model_path()

        pipeline = create_ml_pipeline(numerical_columns,categorical_columns,result_column)
        pipelineModel = pipeline.fit(df)
        indexed = pipelineModel.transform(df)
        print indexed.show()

        save_pipeline(model,"/home/marlabs/jupyter-workbook/Tutorial/")
        trainingData,validationData = get_training_and_validation_data(indexed,target_column,0.8)
        rf = RF(labelCol='label', featuresCol='features',numTrees=200)
        fit = rf.fit(trainingData)
        transformed = fit.transform(validationData)

        feature_importance = calculate_feature_importance(indexed,fit,categorical_columns,numerical_columns)
        print feature_importance

    def Predict(self):
        # Match with the level_counts and then clean the data
        dataSanity = True
        level_counts_train = self._dataframe_context.get_level_count_dict()
        cat_cols = self._dataframe_helper.get_string_columns()
        level_counts_score = CommonUtils.get_level_count_dict(self._data_frame,cat_cols,self._dataframe_context.get_column_separator(),output_type="dict")
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
        score_data_path = self._dataframe_context.get_score_path()+"/ScoredData/data.csv"
        trained_model_path = self._dataframe_context.get_model_path()
        score_summary_path = self._dataframe_context.get_score_path()+"/Summary/summary.json"

        trained_model = joblib.load(trained_model_path)
        # pandas_df = self._data_frame.toPandas()
        df = self._data_frame
        pandas_df = MLUtils.factorize_columns(df,[x for x in categorical_columns if x != result_column])
        score = random_forest_obj.predict(pandas_df,trained_model,[result_column])
        df["predicted_class"] = score["predicted_class"]
        df["predicted_probability"] = score["predicted_probability"]
        self._score_summary["prediction_split"] = MLUtils.calculate_scored_probability_stats(df)

        inner_keys =  self._score_summary["prediction_split"][self._score_summary["prediction_split"].keys()[0]].keys()
        pred_split_new = [["Range"],[inner_keys[0]],[inner_keys[1]]]
        for k,v in self._score_summary["prediction_split"].items():
            pred_split_new[0].append(k)
            pred_split_new[1].append(v[inner_keys[0]])
            pred_split_new[2].append(v[inner_keys[1]])
        self._score_summary["prediction_split"] = pred_split_new

        self._score_summary["result_column"] = result_column

        df = df.rename(index=str, columns={"predicted_class": result_column})
        df.to_csv(score_data_path,header=True,index=False)
        CommonUtils.write_to_file(score_summary_path,json.dumps({"scoreSummary":self._score_summary}))


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
        df.drop(columns_to_drop, axis=1, inplace=True)
        # # Dropping predicted_probability column
        # df.drop('predicted_probability', axis=1, inplace=True)
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
            df_freq_dimension_result = CommonUtils.as_dict(df_freq_dimension_obj)
            CommonUtils.write_to_file(result_file,json.dumps(df_freq_dimension_result))
            narratives_obj = DimensionColumnNarrative(result_column, df_helper, self._dataframe_context, df_freq_dimension_obj)
            narratives = CommonUtils.as_dict(narratives_obj)
            CommonUtils.write_to_file(narratives_file,json.dumps(narratives))
            print "Frequency Analysis Done in ", time.time() - fs,  " seconds."
        except:
            print "Frequency Analysis Failed "

        try:
            fs = time.time()
            narratives_file = self._dataframe_context.get_score_path()+"/narratives/ChiSquare/data.json"
            result_file = self._dataframe_context.get_score_path()+"/results/ChiSquare/data.json"
            df_chisquare_obj = ChiSquare(df, df_helper, self._dataframe_context).test_all(dimension_columns= [result_column])
            df_chisquare_result = CommonUtils.as_dict(df_chisquare_obj)
            # print 'RESULT: %s' % (json.dumps(df_chisquare_result, indent=2))
            CommonUtils.write_to_file(result_file,json.dumps(df_chisquare_result))
            chisquare_narratives = CommonUtils.as_dict(ChiSquareNarratives(len(df_helper.get_string_columns()), df_chisquare_obj,self._dataframe_context))
            # print 'Narrarives: %s' %(json.dumps(chisquare_narratives, indent=2))
            CommonUtils.write_to_file(narratives_file,json.dumps(chisquare_narratives))
            print "ChiSquare Analysis Done in ", time.time() - fs, " seconds."
        except:
            print "ChiSquare Analysis Failed "
