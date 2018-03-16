import json
import time

try:
    import cPickle as pickle
except:
    import pickle

from itertools import chain

from pyspark.sql import SQLContext
from pyspark.sql.types import DoubleType
from bi.common import utils as CommonUtils
from bi.algorithms import utils as MLUtils
from bi.common import DataFrameHelper
from bi.common import MLModelSummary

from bi.stats.frequency_dimensions import FreqDimensions
from bi.narratives.dimension.dimension_column import DimensionColumnNarrative
from bi.stats.chisquare import ChiSquare
from bi.narratives.chisquare import ChiSquareNarratives

from pyspark.sql.functions import udf
from pyspark.sql import functions as FN
from pyspark.sql.types import *
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.feature import IndexToString
from pyspark.ml.tuning import ParamGridBuilder, TrainValidationSplit,CrossValidator
from pyspark.ml.evaluation import RegressionEvaluator

from bi.settings import setting as GLOBALSETTINGS







class RFRegressionModelPysparkScript:
    def __init__(self, data_frame, df_helper,df_context, spark, prediction_narrative, result_setter,meta_parser):
        self._metaParser = meta_parser
        self._prediction_narrative = prediction_narrative
        self._result_setter = result_setter
        self._data_frame = data_frame
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context
        self._spark = spark
        self._model_summary = MLModelSummary()
        self._score_summary = {}
        self._slug = GLOBALSETTINGS.MODEL_SLUG_MAPPING["rfregression"]

    def Train(self):
        st_global = time.time()
        algosToRun = self._dataframe_context.get_algorithms_to_run()
        algoSetting = filter(lambda x:x["algorithmSlug"]==GLOBALSETTINGS.MODEL_SLUG_MAPPING["rfregression"],algosToRun)[0]
        categorical_columns = self._dataframe_helper.get_string_columns()
        numerical_columns = self._dataframe_helper.get_numeric_columns()
        result_column = self._dataframe_context.get_result_column()
        categorical_columns = [x for x in categorical_columns if x != result_column]

        model_path = self._dataframe_context.get_model_path()
        if model_path.startswith("file"):
            model_path = model_path[7:]
        validationDict = self._dataframe_context.get_validation_dict()
        print "model_path",model_path
        pipeline_filepath = "file://"+str(model_path)+"/"+str(self._slug)+"/pipeline/"
        model_filepath = "file://"+str(model_path)+"/"+str(self._slug)+"/model"
        pmml_filepath = "file://"+str(model_path)+"/"+str(self._slug)+"/modelPmml"

        df = self._data_frame
        pipeline = MLUtils.create_ml_pipeline(numerical_columns,categorical_columns,result_column,algoType="regression")

        pipelineModel = pipeline.fit(df)
        indexed = pipelineModel.transform(df)
        featureMapping = sorted((attr["idx"], attr["name"]) for attr in (chain(*indexed.schema["features"].metadata["ml_attr"]["attrs"].values())))

        # print indexed.select([result_column,"features"]).show(5)
        # MLUtils.save_pipeline_or_model(pipelineModel,pipeline_filepath)
        # OriginalTargetconverter = IndexToString(inputCol="label", outputCol="originalTargetColumn")
        rfr = RandomForestRegressor(labelCol=result_column, featuresCol='features',predictionCol="prediction")
        if validationDict["name"] == "kFold":
            defaultSplit = GLOBALSETTINGS.DEFAULT_VALIDATION_OBJECT["value"]
            numFold = validationDict["value"]
            if numFold == 0:
                numFold = 3
            trainingData,validationData = indexed.randomSplit([defaultSplit,1-defaultSplit], seed=12345)
            paramGrid = ParamGridBuilder()\
                .addGrid(rfr.regParam, [0.1, 0.01]) \
                .addGrid(rfr.fitIntercept, [False, True])\
                .addGrid(rfr.elasticNetParam, [0.0, 0.5, 1.0])\
                .build()
            crossval = CrossValidator(estimator=rfr,
                          estimatorParamMaps=paramGrid,
                          evaluator=RegressionEvaluator(predictionCol="prediction", labelCol=result_column),
                          numFolds=numFold)
            st = time.time()
            cvModel = crossval.fit(indexed)
            trainingTime = time.time()-st
            print "cvModel training takes",trainingTime
            bestModel = cvModel.bestModel
        elif validationDict["name"] == "trainAndtest":
            trainingData,validationData = indexed.randomSplit([float(validationDict["value"]),1-float(validationDict["value"])], seed=12345)
            st = time.time()
            fit = rfr.fit(trainingData)
            trainingTime = time.time()-st
            print "time to train",trainingTime
            bestModel = fit

        featureImportance = bestModel.featureImportances
        print featureImportance,type(featureImportance)
        # print featureImportance[0],len(featureImportance[1],len(featureImportance[2]))
        print len(featureMapping)
        featuresArray = [(name, featureImportance[idx]) for idx, name in featureMapping]
        print featuresArray
        # MLUtils.save_pipeline_or_model(bestModel,model_filepath)
        transformed = bestModel.transform(validationData)
        transformed = transformed.withColumn(result_column,transformed[result_column].cast(DoubleType()))
        transformed = transformed.select([result_column,"prediction",transformed[result_column]-transformed["prediction"]])
        transformed = transformed.withColumnRenamed(transformed.columns[-1],"difference")
        transformed = transformed.select([result_column,"prediction","difference",FN.abs(transformed["difference"])*100/transformed[result_column]])
        transformed = transformed.withColumnRenamed(transformed.columns[-1],"mape")
        sampleData = None
        nrows = transformed.count()
        if nrows > 100:
            sampleData = transformed.sample(False, float(100)/nrows, seed=420)
        else:
            sampleData = transformed
        print sampleData.show()
        evaluator = RegressionEvaluator(predictionCol="prediction",labelCol=result_column)
        metrics = {}
        metrics["r2"] = evaluator.evaluate(transformed,{evaluator.metricName: "r2"})
        metrics["rmse"] = evaluator.evaluate(transformed,{evaluator.metricName: "rmse"})
        metrics["mse"] = evaluator.evaluate(transformed,{evaluator.metricName: "mse"})
        metrics["mae"] = evaluator.evaluate(transformed,{evaluator.metricName: "mae"})
        runtime = round((time.time() - st_global),2)
        # print transformed.count()
        mapeDf = transformed.select("mape")
        # print mapeDf.show()
        mapeStats = MLUtils.get_mape_stats(mapeDf,"mape")
        mapeStatsArr = mapeStats.items()
        mapeStatsArr = sorted(mapeStatsArr,key=lambda x:int(x[0]))
        # print mapeStatsArr
        quantileDf = transformed.select("prediction")
        # print quantileDf.show()
        quantileSummaryDict = MLUtils.get_quantile_summary(quantileDf,"prediction")
        quantileSummaryArr = quantileSummaryDict.items()
        quantileSummaryArr = sorted(quantileSummaryArr,key=lambda x:int(x[0]))
        # print quantileSummaryArr
        self._model_summary.set_model_type("regression")
        self._model_summary.set_algorithm_name("rf Regression")
        self._model_summary.set_algorithm_display_name("rf Regression")
        self._model_summary.set_slug(self._slug)
        self._model_summary.set_training_time(runtime)
        self._model_summary.set_training_time(trainingTime)
        self._model_summary.set_target_variable(result_column)
        self._model_summary.set_validation_method(validationDict["displayName"])
        self._model_summary.set_model_evaluation_metrics(metrics)
        self._model_summary.set_model_params(algoSetting["algorithmParams"])
        self._model_summary.set_quantile_summary(quantileSummaryArr)
        self._model_summary.set_mape_stats(mapeStatsArr)
        self._model_summary.set_sample_data(sampleData.toPandas().to_dict())
        self._model_summary.set_feature_importance(featureImportance)
        # print CommonUtils.convert_python_object_to_json(self._model_summary)
        modelSummaryJson = {
            "dropdown":{
                        "name":self._model_summary.get_algorithm_name(),
                        "accuracy":self._model_summary.get_model_evaluation_metrics()["r2"],
                        "slug":self._model_summary.get_slug()
                        },
            "levelcount":self._model_summary.get_level_counts(),
            "modelFeatureList":self._model_summary.get_feature_list(),
            "levelMapping":self._model_summary.get_level_map_dict()
        }

        rfrCards = [json.loads(CommonUtils.convert_python_object_to_json(cardObj)) for cardObj in MLUtils.create_model_summary_cards(self._model_summary)]

        for card in rfrCards:
            self._prediction_narrative.add_a_card(card)
        self._result_setter.set_model_summary({"rfregression":json.loads(CommonUtils.convert_python_object_to_json(self._model_summary))})
        self._result_setter.set_rf_regression_model_summart(modelSummaryJson)
        self._result_setter.set_rfr_cards(rfrCards)

    def Predict(self):
        SQLctx = SQLContext(sparkContext=self._spark.sparkContext, sparkSession=self._spark)
        dataSanity = True
        level_counts_train = self._dataframe_context.get_level_count_dict()
        categorical_columns = self._dataframe_helper.get_string_columns()
        numerical_columns = self._dataframe_helper.get_numeric_columns()
        time_dimension_columns = self._dataframe_helper.get_timestamp_columns()
        result_column = self._dataframe_context.get_result_column()
        categorical_columns = [x for x in categorical_columns if x != result_column]

        level_counts_score = CommonUtils.get_level_count_dict(self._data_frame,categorical_columns,self._dataframe_context.get_column_separator(),output_type="dict",dataType="spark")
        for key in level_counts_train:
            if key in level_counts_score:
                if level_counts_train[key] != level_counts_score[key]:
                    dataSanity = False
            else:
                dataSanity = False

        test_data_path = self._dataframe_context.get_input_file()
        score_data_path = self._dataframe_context.get_score_path()+"/ScoredData/data.csv"
        trained_model_path = self._dataframe_context.get_model_path()
        if trained_model_path.endswith(".pkl"):
            trained_model_path = "/".join(trained_model_path.split("/")[:-1])+"/model"
        pipeline_path = "/".join(trained_model_path.split("/")[:-1])+"/pipeline"
        score_summary_path = self._dataframe_context.get_score_path()+"/Summary/summary.json"

        pipelineModel = MLUtils.load_pipeline(pipeline_path)
        trained_model = MLUtils.load_rf_model(trained_model_path)
        df = self._data_frame
        indexed = pipelineModel.transform(df)
        transformed = trained_model.transform(indexed)
        label_indexer_dict = MLUtils.read_string_indexer_mapping(pipeline_path,SQLctx)
        prediction_to_levels = udf(lambda x:label_indexer_dict[x],StringType())
        transformed = transformed.withColumn(result_column,prediction_to_levels(transformed.prediction))
        # udf_to_calculate_probability = udf(lambda x:max(x[0]))
        # transformed = transformed.withColumn("predicted_probability",udf_to_calculate_probability(transformed.probability))
        # print transformed.select("predicted_probability").show(5)
        probability_dataframe = transformed.select([result_column,"probability"]).toPandas()
        probability_dataframe = probability_dataframe.rename(index=str, columns={result_column: "predicted_class"})
        probability_dataframe["predicted_probability"] = probability_dataframe["probability"].apply(lambda x:max(x))
        self._score_summary["prediction_split"] = MLUtils.calculate_scored_probability_stats(probability_dataframe)
        self._score_summary["result_column"] = result_column
        scored_dataframe = transformed.select(categorical_columns+time_dimension_columns+numerical_columns+[result_column,"probability"]).toPandas()
        # scored_dataframe = scored_dataframe.rename(index=str, columns={"predicted_probability": "probability"})
        if score_data_path.startswith("file"):
            score_data_path = score_data_path[7:]
        scored_dataframe.to_csv(score_data_path,header=True,index=False)
        # print json.dumps({"scoreSummary":self._score_summary},indent=2)
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
        # spark_scored_df = transformed.select(categorical_columns+time_dimension_columns+numerical_columns+[result_column])
        scored_df = transformed.select(categorical_columns+time_dimension_columns+numerical_columns+[result_column])

        SQLctx = SQLContext(sparkContext=self._spark.sparkContext, sparkSession=self._spark)
        spark_scored_df = SQLctx.createDataFrame(scored_df.toPandas())
        columns_to_drop = [x for x in columns_to_drop if x in spark_scored_df.columns]
        modified_df = spark_scored_df.select([x for x in spark_scored_df.columns if x not in columns_to_drop])
        df_helper = DataFrameHelper(modified_df, self._dataframe_context)
        df_helper.set_params()
        df = df_helper.get_data_frame()
        try:
            fs = time.time()
            narratives_file = self._dataframe_context.get_score_path()+"/narratives/FreqDimension/data.json"
            result_file = self._dataframe_context.get_score_path()+"/results/FreqDimension/data.json"
            df_freq_dimension_obj = FreqDimensions(df, df_helper, self._dataframe_context).test_all(dimension_columns=[result_column])
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
            print 'RESULT: %s' % (json.dumps(df_chisquare_result, indent=2))
            CommonUtils.write_to_file(result_file,json.dumps(df_chisquare_result))
            chisquare_narratives = CommonUtils.as_dict(ChiSquareNarratives(df_helper, df_chisquare_obj, self._dataframe_context,df))
            # print 'Narrarives: %s' %(json.dumps(chisquare_narratives, indent=2))
            CommonUtils.write_to_file(narratives_file,json.dumps(chisquare_narratives))
            print "ChiSquare Analysis Done in ", time.time() - fs, " seconds."
        except:
           print "ChiSquare Analysis Failed "
