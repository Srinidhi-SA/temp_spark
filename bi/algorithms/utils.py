import random
import os
import shutil
import json

import numpy as np
import pandas as pd
import operator
import __builtin__

from pyspark.sql import functions as FN
from pyspark.sql.functions import mean, stddev, col, sum, count, min, max
from pyspark.sql.types import StringType
from pyspark.sql.types import DoubleType
from pyspark.ml.clustering import KMeans

from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorIndexer, VectorAssembler, SQLTransformer, IndexToString

import numpy as np
import functools
from pyspark.ml.feature import OneHotEncoder
from pyspark.ml.pipeline import PipelineModel
from pyspark.ml.feature import Bucketizer
from pyspark.ml.feature import QuantileDiscretizer
from pyspark.sql.functions import monotonically_increasing_id
from pyspark.ml.classification import RandomForestClassificationModel,OneVsRestModel,LogisticRegressionModel
from bi.common import NormalCard,SummaryCard,NarrativesTree,HtmlData,C3ChartData,TableData,TreeData,ModelSummary
from bi.common import ScatterChartData,NormalChartData,ChartJson
from bi.common import utils as CommonUtils

def bucket_all_measures(df, measure_columns, dimension_columns,target_measure=[]):
    df = df.select([col(c).cast('double').alias(c) if c in measure_columns else col(c) for c in measure_columns+dimension_columns+target_measure])
    for measure_column in measure_columns:
        # quantile_discretizer = QuantileDiscretizer(numBuckets=4, inputCol=measure_column,
        #                                                outputCol='quantile',
        #                                                relativeError=0.01)
        # splits = quantile_discretizer.fit(df).getSplits()
        min_,max_ = df.agg(FN.min(measure_column), FN.max(measure_column)).collect()[0]
        # if len(splits)<5:
        #     diff = (max_ - min_)*1.0
        #     splits = [None,min_+diff*0.25,min_+diff*0.5,min_+diff*0.75,None]
        # print measure_column, min_, max_,splits
        # splits_new = [min_,splits[1],splits[3],max_]
        diff = (max_ - min_)*1.0
        splits_new = [min_,min_+diff*0.2,min_+diff*0.4,min_+diff*0.6,min_+diff*0.8,max_]
        bucketizer = Bucketizer(inputCol=measure_column,outputCol='bucket')
        bucketizer.setSplits(splits_new)
        df = bucketizer.transform(df)
        df = df.select([c for c in df.columns if c!=measure_column])
        df = df.select([col(c).alias(measure_column) if c=='bucket' else col(c) for c in df.columns])
    return df

def generate_random_number_array(df):
    out = [random.random() for idx in range(df.shape[0])]
    return out

def return_filtered_index(random_array,cutoff):
    id_train = []
    id_test = []
    for idx,val in enumerate(random_array):
        if val >= cutoff:
            id_test.append(idx)
        else:
            id_train.append(idx)

    return (id_train,id_test)

def drop_columns(df,drop_column_list):
    new_df = df.loc[:,[col for col in df.columns if col not in drop_column_list]]
    return new_df

def scale_columns(df,column_list):
    for val in column_list:
        norm_df = df[val]
        df[val] = (norm_df - norm_df.mean()) / (norm_df.max() - norm_df.min())

def missing_value_analysis(df,replacement_dict):
    bool_df = df.isnull()
    missing_dict = {}
    for val in bool_df.columns:
        missing_dict[val] = dict(bool_df[val].value_counts())
    missing_cols = [val for val in missing_dict.keys() if True in missing_dict[val].keys()]
    print('columns with missing value : ',missing_cols,'\n')

    if replacement_dict != {}:
        for col in missing_cols:
            if col in replacement_dict.keys():
                df[col] = df[col].apply(lambda x: replacement_dict[col] if pd.isnull(x) == True else x)
    else:
        new_dict = {}
        for col in missing_cols:
            missing_dict[col]['ratio'] = missing_dict[col][True]/sum(missing_dict[col].values())
            new_dict[col] = missing_dict[col]
        print('\n')
        return new_dict


def factorize_columns(df,cat_columns):
    df_copy = df.copy(deep=True)
    df_col = list(df.columns)
    for col in cat_columns:
        if col in df_col:
            uniq_vals = df_copy[col].unique()
            key = [idx for idx,x in enumerate(uniq_vals)]
            rep_dict = dict(zip(uniq_vals,key))
            if col != 'responded':
                df_copy[col]=df_copy[col].apply(lambda x: rep_dict[x])
            else:
                df_copy[col]=df_copy[col].apply(lambda x: 1 if x == 'yes' else 0)
            df_copy[col]=pd.factorize(df_copy[col])[0]
    return df_copy

def generate_train_test_split(df,cutoff,dependent_colname,drop_list):
    levels = df[dependent_colname].unique()
    if len(levels) > 2:
        out = generate_random_number_array(df)
        ids = return_filtered_index(out,0.7)
        df_x = df[[col for col in df.columns if col not in drop_list+[dependent_colname]]]
        x_train = df_x.iloc[ids[0],:]
        x_test = df_x.iloc[ids[1],:]
        r_response = np.array(df[dependent_colname])
        y_train = r_response[ids[0]]
        y_test = r_response[ids[1]]
    else:
        df1 = df[df[dependent_colname]==levels[0]]
        df2 = df[df[dependent_colname]==levels[1]]
        out1 = generate_random_number_array(df1)
        ids1 = return_filtered_index(out1,0.6)
        out2 = generate_random_number_array(df2)
        ids2 = return_filtered_index(out2,0.6)
        df_x1 = df1[[col for col in df.columns if col not in drop_list+[dependent_colname]]]
        x_train1 = df_x1.iloc[ids1[0],:]
        x_test1 = df_x1.iloc[ids1[1],:]
        df_x2 = df2[[col for col in df.columns if col not in drop_list+[dependent_colname]]]
        x_train2 = df_x2.iloc[ids2[0],:]
        x_test2 = df_x2.iloc[ids2[1],:]
        r_response = np.array(df[dependent_colname])
        x_train = pd.concat([x_train1,x_train2])
        x_test = pd.concat([x_test1,x_test2])
        y_train = np.concatenate((r_response[ids1[0]],r_response[ids2[0]]))
        y_test = np.concatenate((r_response[ids1[1]],r_response[ids2[1]]))
    return (x_train,x_test,y_train,y_test)

def calculate_predicted_probability(probability_array):
    out = []
    if len(probability_array[0]) > 1:
        for val in probability_array:
            out.append(__builtin__.max(val))
        return out
    else:
        return probability_array

def calculate_confusion_matrix(actual,predicted):
    """
    confusion matrix structure is defined below
    {"pred1":{"actual1":2,"actal2":3,"actual3":5},"pred2":{"actual1":5,"actal2":7,"actual3":5},"pred3":{"actual1":1,"actal2":3,"actual3":5}}
    """
    out = pd.crosstab(pd.Series(list(actual)),pd.Series(list(predicted)), rownames=['Known Class'], colnames=['Predicted Class'])
    dict_out = out.to_dict()
    actual_classes = list(set(actual))
    predicted_classes = list(set(predicted))
    total_classes = list(set(actual_classes+predicted_classes))
    dummy_dict = dict(zip(total_classes,[0]*len(total_classes)))
    for k in total_classes:
        if k not in predicted_classes:
            dict_out[k] = dummy_dict
    if len(actual_classes) < len(predicted_classes):
        for k in total_classes:
            if k not in predicted_classes:
                dict_out[k] = dummy_dict
            else:
                temp = dict_out[k]
                missing_keys = list(set(total_classes)-set(actual_classes))
                additional_data = dict(zip(missing_keys,[0]*len(missing_keys)))
                temp.update(additional_data)
                dict_out[k] = temp
    print dict_out
    return dict_out

def reformat_confusion_matrix(confusion_matrix):
    levels = confusion_matrix.keys()
    confusion_matrix_data = [[""]+levels]
    for outer in levels:
        inner_list = [outer]
        for inner in levels:
            inner_list.append(confusion_matrix[inner][outer])
        confusion_matrix_data.append(inner_list)
    return [list(x) for x in np.array(confusion_matrix_data).T]

def calculate_overall_precision_recall(actual,predicted):
    # get positive or negative class from the user
    df = pd.DataFrame({"actual":actual,"predicted":predicted})
    classes = df["actual"].unique()
    val_counts_predicted = df["predicted"].value_counts().to_dict()
    for val in classes:
        if val not in val_counts_predicted.keys():
            val_counts_predicted[val] = 0

    prediction_split = {}
    for val in val_counts_predicted.keys():
        prediction_split[val] = round(val_counts_predicted[val]*100/float(len(predicted)),2)
    val_counts = df["actual"].value_counts().to_dict()
    val_counts_tuple = tuple(val_counts.items())
    # positive_class = max(val_counts_tuple,key=lambda x:x[1])[0]
    # positive_class = __builtin__.max(val_counts,key=val_counts.get)
    positive_class = __builtin__.min(val_counts,key=val_counts.get)
    print val_counts
    print "positive_class",positive_class

    output = {"precision":0,"recall":0,"classwise_stats":None,"prediction_split":prediction_split,"positive_class":positive_class}
    if len(classes) > 2:
        class_precision_recall = calculate_precision_recall(actual,predicted)
        output["classwise_stats"] = class_precision_recall
        p = []
        r = []
        for val in class_precision_recall.keys():
            p.append(class_precision_recall[val]["precision"])
            r.append(class_precision_recall[val]["recall"])
        output["precision"] = np.mean(p)
        output["recall"] = np.mean(r)
    else:
        count_dict = {"tp":0,"fp":0,"tn":0,"fn":0}
        count_dict["tp"] = df[(df["actual"]==positive_class) & (df["predicted"]==positive_class)].shape[0]
        count_dict["fp"] = df[(df["actual"]!=positive_class) & (df["predicted"]==positive_class)].shape[0]
        count_dict["tn"] = df[(df["actual"]!=positive_class) & (df["predicted"]!=positive_class)].shape[0]
        count_dict["fn"] = df[(df["actual"]==positive_class) & (df["predicted"]!=positive_class)].shape[0]
        if count_dict["tp"]+count_dict["fp"] > 0:
            output["precision"] = round(float(count_dict["tp"])/(count_dict["tp"]+count_dict["fp"]),2)
        else:
            output["precision"] = 0.0
        if count_dict["tp"]+count_dict["fn"] > 0:
            output["recall"] = round(float(count_dict["tp"])/(count_dict["tp"]+count_dict["fn"]),2)
        else:
            output["recall"] = 0.0
    print output
    return output

def calculate_precision_recall(actual,predicted,df=None):
    if df == None:
        df = pd.DataFrame({"actual":actual,"predicted":predicted})
    else:
        df=df
    classes = df["actual"].unique()
    output = {}
    for val in classes:
        class_summary = {}
        count_dict = {"tp":0,"fp":0,"tn":0,"fn":0}
        count_dict["tp"] = df[(df["actual"]==val) & (df["predicted"]==val)].shape[0]
        count_dict["fp"] = df[(df["actual"]!=val) & (df["predicted"]==val)].shape[0]
        count_dict["tn"] = df[(df["actual"]!=val) & (df["predicted"]!=val)].shape[0]
        count_dict["fn"] = df[(df["actual"]==val) & (df["predicted"]!=val)].shape[0]
        class_summary["counts"] = count_dict
        if count_dict["tp"]+count_dict["fp"] > 0:
            class_summary["precision"] = round(float(count_dict["tp"])/(count_dict["tp"]+count_dict["fp"]),2)
        else:
            class_summary["precision"] = 0.0
        if count_dict["tp"]+count_dict["fn"] > 0:
            class_summary["recall"] = round(float(count_dict["tp"])/(count_dict["tp"]+count_dict["fn"]),2)
        else:
            class_summary["recall"] = 0.0
        output[str(val)] = class_summary
    return output

def calculate_scored_probability_stats(scored_dataframe):
    new_df = scored_dataframe[["predicted_class","predicted_probability"]]
    bands = [0.25,0.50,0.75,0.90]
    output = {}

    for val in bands:
        temp_df = new_df[new_df["predicted_probability"] >= val]
        output[">"+str(100*val)+"%"] = temp_df["predicted_class"].value_counts().to_dict()
    temp_df = new_df[new_df["predicted_probability"] < 0.25]
    output["<25%"] = temp_df["predicted_class"].value_counts().to_dict()
    for key in output.keys():
        if output[key] == {}:
            output.pop(key, None)

    return reformat_prediction_split(output)

def create_dummy_columns(df,colnames):
    df1 = df[[col for col in df.columns if col not in colnames]]
    for col in colnames:
        dummies = pd.get_dummies(df[col],prefix = col)
        df1 = pd.concat([df1,dummies], axis = 1)
    return df1

def transform_feature_importance(feature_importance_dict):
    feature_importance_new = [["Name"],["Value"]]
    for k,v in feature_importance_dict.items():
        feature_importance_new[0].append(k)
        feature_importance_new[1].append(v)
    zipped_feature_importance = zip(feature_importance_new[0],feature_importance_new[1])
    zipped_feature_importance_subset = zipped_feature_importance[1:]
    zipped_feature_importance_subset = sorted(zipped_feature_importance_subset,key=lambda x:x[1],reverse=True)
    zipped_feature_importance = [zipped_feature_importance[0]]+zipped_feature_importance_subset
    feature_importance_new = [[],[]]
    for val in zipped_feature_importance:
        feature_importance_new[0].append(val[0])
        feature_importance_new[1].append(val[1])
    output = [feature_importance_new[0][:6],feature_importance_new[1][:6]]
    return output

def cluster_by_column(df, col_to_cluster, get_aggregation = False):
    my_df = df.select(df.columns)
    assembler = VectorAssembler(inputCols = [col_to_cluster], outputCol = "feature_vector")
    assembled = assembler.transform(my_df)

    avg,std,total = assembled.agg(mean(col_to_cluster).alias('avg'), stddev(col_to_cluster).alias('std'), sum(col_to_cluster).alias('total')).collect()[0]
    assembled_without_outlier = assembled.filter(col(col_to_cluster)>=avg-3*std).filter(col(col_to_cluster)<=avg+3*std)
    assembled_without_outlier = assembled_without_outlier.select([c for c in assembled_without_outlier.columns if c!=col_to_cluster])
    assembled = assembled.select([col(c) if c!=col_to_cluster else col(c).alias('target_col') for c in assembled.columns])
    # mmScaler = StandardScaler(inputCol="feature_vector", outputCol="standard_features",withStd=True, withMean=False)
    # scale_model = mmScaler.fit(assembled)
    # vectorized_data = scale_model.transform(assembled)
    kmeans = KMeans(predictionCol=col_to_cluster, featuresCol='feature_vector').setK(3).setSeed(1)
    model = kmeans.fit(assembled_without_outlier)
    final_df = model.transform(assembled)
    if (get_aggregation):
        agg_df = final_df.groupby(col_to_cluster).agg(sum('target_col').alias('sum'), count('target_col').alias('count'))
        aggr = {}
        for row in agg_df.collect():
            aggr[row[0]] = {'sum': row[1], 'count': row[2], 'sum_percent': row[1]*100.0/total, 'count_percent': row[2]*100.0/final_df.count()}
    final_df = final_df.select([c for c in final_df.columns if c!='feature_vector'])
    final_df = final_df.select([col(c) if c!=col_to_cluster else col(c).alias(col_to_cluster) for c in final_df.columns])
    if (get_aggregation):
        return final_df, aggr
    return final_df, model.clusterCenters()

def add_string_index(df, string_columns=None):
    my_df = df.select(df.columns)
    column_name_maps = {}
    mapping_dict = {}
    if string_columns==None:
        string_columns = [c.name for c in df.schema.fields if type(c.dataType) == StringType]
    for c in string_columns:
        my_df = StringIndexer(inputCol=c, outputCol=c+'_index').fit(my_df).transform(my_df)
        column_name_maps[c+'_index'] = c
        mapping_dict[c] = dict(enumerate(my_df[[c+'_index']].schema[0].metadata['ml_attr']['vals']))
    my_df = my_df.select([c for c in my_df.columns if c not in string_columns])
    my_df = my_df.select([col(c).alias(column_name_maps[c]) if c in column_name_maps.keys() \
                            else col(c) for c in my_df.columns])
    return my_df, mapping_dict

##################################Spark ML Pipelines ###########################

def create_ml_pipeline(numerical_columns,categorical_columns,target_column,algoName=None):
    indexers = [StringIndexer(inputCol=x, outputCol=x+'_indexed') for x in categorical_columns ] #String Indexer
    encoders = [OneHotEncoder(dropLast=False, inputCol=x+"_indexed", outputCol=x+"_encoded") for x in categorical_columns] # one hot encoder
    assembler_features = VectorAssembler(inputCols=[x+"_encoded" for x in sorted(categorical_columns)]+sorted(numerical_columns), outputCol='features')
    if algoName != "lr":
        labelIndexer = StringIndexer(inputCol=target_column, outputCol="label")
    ml_stages = [[i,j] for i,j in zip(indexers, encoders)]
    pipeline_stages = []
    for ml_stage in ml_stages:
        pipeline_stages += ml_stage
    if algoName != "lr":
        pipeline_stages += [assembler_features, labelIndexer]
    else:
        pipeline_stages += [assembler_features]
    pipeline = Pipeline(stages=pipeline_stages)
    return pipeline

def save_pipeline_or_model(pipeline,dir_path):
    """
    Need to check if any folder exist with the given name
    if yes then 1st delete that then proceed
    """
    if dir_path.startswith("file"):
        new_path = dir_path[7:]
    else:
        new_path = dir_path
    if os.path.isdir(new_path):
        shutil.rmtree(new_path)
    pipeline.save(dir_path)

def load_pipeline(filepath):
    model = PipelineModel.load(filepath)
    return model

def load_rf_model(filepath):
    model = RandomForestClassificationModel.load(filepath)
    return model

def load_one_vs_rest_model(filepath):
    model = OneVsRestModel.load(filepath)
    return model

def load_logistic_model(filepath):
    model = LogisticRegressionModel.load(filepath)
    return model

def stratified_sampling(df,target_column,split):
    levels = [x[0] for x in df.select(target_column).distinct().collect()]
    frac = [split]*len(levels)
    sampling_dict = dict(zip(levels,frac))
    sampled_df = df.sampleBy(target_column, fractions = sampling_dict, seed=0)
    return sampled_df

def get_training_and_validation_data(df,target_column,split):
    df = df.withColumn("monotonically_increasing_id", monotonically_increasing_id())
    trainingData = stratified_sampling(df,target_column,split)
    validationIds = df.select("monotonically_increasing_id").subtract(trainingData.select("monotonically_increasing_id"))
    indexed = df.alias("indexed")
    validation = validationIds.alias("validation")
    validationData = indexed.join(validation, col("indexed.monotonically_increasing_id") == col("validation.monotonically_increasing_id"), 'inner').select("indexed.*")
    return trainingData,validationData

def calculate_sparkml_feature_importance(df,modelFit,categorical_columns,numerical_columns):
    featureImportanceSparseVector = modelFit.featureImportances
    feature_importance = {}
    start_idx = 0
    end_idx = 0
    for level in sorted(categorical_columns):
        count = len(df.select(level).distinct().collect())
        end_idx += count
        col_percentage = 0
        for key in range(start_idx,end_idx):
            try:
                col_percentage += featureImportanceSparseVector[key]
            except:
                continue
        feature_importance[level] = col_percentage
        start_idx = end_idx
    for val in sorted(numerical_columns):
        feature_importance[val] = featureImportanceSparseVector[start_idx]
        start_idx += 1
    return feature_importance

def read_string_indexer_mapping(pipeline_path,sqlContext):
    metadata = sqlContext.read.text(pipeline_path+"/metadata")
    stageuids = json.loads(metadata.take(1)[0][0])["paramMap"]["stageUids"]
    if len(stageuids) < 11:
        try:
            parquet_key = "0"+str(len(stageuids)-1)+"_"+stageuids[-1]
            parquet_filepath = pipeline_path+"/stages/"+parquet_key+"/data"
            level_df = sqlContext.read.parquet(parquet_filepath)
        except:
            parquet_key = str(len(stageuids)-1)+"_"+stageuids[-1]
            parquet_filepath = pipeline_path+"/stages/"+parquet_key+"/data"
            level_df = sqlContext.read.parquet(parquet_filepath)
    else:
        parquet_key = str(len(stageuids)-1)+"_"+stageuids[-1]
        parquet_filepath = pipeline_path+"/stages/"+parquet_key+"/data"
        level_df = sqlContext.read.parquet(parquet_filepath)
    levels = [str(v) for v in  [x[0] for x in level_df.select("labels").collect()][0]]
    mapping_dict = dict(enumerate(levels))
    return mapping_dict

def reformat_prediction_split(prediction_split):
    inner_keys = []
    for key,val in prediction_split.items():
        inner_keys += val.keys()
    inner_keys = list(set(inner_keys))
    pred_split_new = [["Range"]]
    for val in inner_keys:
        pred_split_new.append([val])
    for k,v in prediction_split.items():
        pred_split_new[0].append(k)
        for idx,val in enumerate(pred_split_new[1:]):
            if val[0] in v:
                pred_split_new[idx+1].append(v[val[0]])
            else:
                pred_split_new[idx+1].append(0)
    return pred_split_new

def fill_missing_values(df,replacement_dict):
    """
    replacement_dict => {"col1":23,"col2":"GG","col3":45}
    """
    df = df.fillna(replacement_dict)
    return df


def get_model_comparison(collated_summary):
    summary = []
    algos = collated_summary.keys()
    algos_dict = {"randomforest":"Random Forest","xgboost":"XGBoost","logistic":"Logistic Regression"}
    out = []
    for val in algos:
        out.append(algos_dict[val])
    out = [[""]+out]
    first_column = ["Accuracy","Precision","Recall"]
    data_keys = ["modelAccuracy","modelPrecision","modelRecall"]
    summary_map = {"Precision":"Best Precision","Recall":"Best Recall","Best Accuracy":"Accuracy"}
    map_dict = dict(zip(first_column,data_keys))
    for key in first_column:
        row = []
        for val in algos:
            row.append(round(100*(collated_summary[val][map_dict[key]]),2))
        out.append([key]+row)
        max_index = __builtin__.max(xrange(len(row)), key = lambda x: row[x])
        summary.append(["Best "+key,algos_dict[algos[max_index]]])
    runtime = []
    for val in algos:
        runtime.append(collated_summary[val]["trainingTime"])
    max_runtime_index = __builtin__.max(xrange(len(runtime)), key = lambda x: runtime[x])
    summary.append(["Best Runtime",algos_dict[algos[max_runtime_index]]])
    inner_html = []
    for val in summary:
        inner_html.append("<li>{} : {}</li>".format(val[0],val[1]))
    summary_html = "<ul class='list-unstyled bullets_primary'>{}{}{}{}</ul>".format(inner_html[0],inner_html[1],inner_html[2],inner_html[3])
    summaryData = HtmlData(data = summary_html)

    modelTable = TableData()
    modelTable.set_table_data(out)
    modelTable.set_table_type("circularChartTable")
    return modelTable,summaryData

def get_feature_importance(collated_summary):
    feature_importance = collated_summary["randomforest"]["featureImportance"]
    feature_importance_list = [[k,v] for k,v in feature_importance.items()]
    sorted_feature_importance_list = sorted(feature_importance_list,key = lambda x:x[1],reverse=True)
    feature_importance_data = [{"name":x[0],"value":x[1]} for x in sorted_feature_importance_list]
    chart_data = NormalChartData(data=feature_importance_data)
    chart_json = ChartJson()
    chart_json.set_data(chart_data.get_data())
    chart_json.set_chart_type("bar")
    chart_json.set_axes({"x":"name","y":"value"})
    chart_json.set_subchart(False)
    chart_json.set_yaxis_number_format(".2f")
    card3Chart = C3ChartData(data=chart_json)
    return card3Chart

def get_total_models(collated_summary):
    algos = collated_summary.keys()
    n_model = 0
    algorithm_name = []
    for val in algos:
        trees = collated_summary[val].get("nTrees")
        algorithm_name.append(collated_summary[val].get("algorithmName"))
        if trees:
            n_model += trees
    output = "<p>mAdvisor has built {} models using {} algorithms ({}) to predict {} and \
        has come up with the following results:</p>".format(n_model,len(algos),",".join(algorithm_name),collated_summary[algos[0]]["targetVariable"])
    return output

def create_model_folders(model_slug,basefoldername,subfolders=[]):
    home_dir = os.path.expanduser("~")
    filepath = home_dir+"/"+basefoldername
    if not os.path.isdir(filepath):
        os.mkdir(filepath)
    if os.path.isdir(filepath+"/"+model_slug):
        shutil.rmtree(filepath+"/"+model_slug)
    os.mkdir(filepath+"/"+model_slug)
    for foldername in subfolders:
        os.mkdir(filepath+"/"+model_slug+"/"+foldername)
    return filepath+"/"+model_slug+"/"

def create_scored_data_folder(score_slug,basefoldername):
    home_dir = os.path.expanduser("~")
    filepath = home_dir+"/"+basefoldername
    if not os.path.isdir(filepath):
        os.mkdir(filepath)
    if os.path.isdir(filepath+"/"+score_slug):
        shutil.rmtree(filepath+"/"+score_slug)
    os.mkdir(filepath+"/"+score_slug)
    return filepath+"/"+score_slug+"/"

def model_slug_mapping():
    random_slug = "f77631ce2ab24cf78c55bb6a5fce4db8"
    object = {
                "randomforest":random_slug+"rf",
                "logisticregression":random_slug+"lr",
                "xgboost":random_slug+"xgb"
                }
    return object
def slug_model_mapping():
    random_slug = "f77631ce2ab24cf78c55bb6a5fce4db8"
    object = {
                random_slug+"rf":"randomforest",
                random_slug+"lr":"logisticregression",
                random_slug+"xgb":"xgboost"
                }
    return object

def reformat_confusion_matrix(confusion_matrix):
    levels = confusion_matrix.keys()
    confusion_matrix_data = [[""]+levels]
    for outer in levels:
        inner_list = [outer]
        for inner in levels:
            inner_list.append(confusion_matrix[inner][outer])
        confusion_matrix_data.append(inner_list)
    return [list(x) for x in np.array(confusion_matrix_data).T]


def create_model_summary_cards(modelSummaryClass):
    modelSummaryCard1 = NormalCard()
    modelSummaryCard1Data = []
    modelSummaryCard1Data.append(HtmlData(data="<h4 class = 'sm-mb-20'>{}</h4>".format(modelSummaryClass.get_algorithm_display_name())))
    modelSummaryCard1Data.append(HtmlData(data="<h5>Summary</h5>"))
    modelSummaryCard1Data.append(HtmlData(data="<p>Target Varialble - {}</p>".format(modelSummaryClass.get_target_variable())))
    modelSummaryCard1Data.append(HtmlData(data="<p>Independent Variable Chosen - {}</p>".format(len(modelSummaryClass.get_model_features()))))
    modelSummaryCard1Data.append(HtmlData(data="<h5>Predicted Distribution</h5>"))
    prediction_split_array = sorted([(k,v) for k,v in modelSummaryClass.get_prediction_split().items()],key=lambda x:x[1],reverse=True)
    for val in prediction_split_array:
        modelSummaryCard1Data.append(HtmlData(data="<p>{} - {}%</p>".format(val[0],val[1])))
    modelSummaryCard1Data.append(HtmlData(data="<p>Algorithm - {}</p>".format(modelSummaryClass.get_algorithm_name())))
    if modelSummaryClass.get_num_trees():
        modelSummaryCard1Data.append(HtmlData(data="<p>Total Trees - {}</p>".format(modelSummaryClass.get_num_trees())))
    if modelSummaryClass.get_num_rules():
        modelSummaryCard1Data.append(HtmlData(data="<p>Total Rules - {}</p>".format(modelSummaryClass.get_num_rules())))
    modelSummaryCard1Data.append(HtmlData(data="<p>Validation Method - {}</p>".format(modelSummaryClass.get_validation_method())))
    modelSummaryCard1Data.append(HtmlData(data="<p>Model Accuracy - {}</p>".format(modelSummaryClass.get_model_accuracy())))
    modelSummaryCard1.set_card_data(modelSummaryCard1Data)

    modelSummaryCard2 = NormalCard()
    modelSummaryCard2Data = []
    modelSummaryCard2Data.append(HtmlData(data="<h5 class = 'sm-ml-15 sm-pb-10'>Confusion Matrix</h5>"))
    modelSummaryCard2Table = TableData()
    modelSummaryCard2Table.set_table_data(reformat_confusion_matrix(modelSummaryClass.get_confusion_matrix()))
    modelSummaryCard2Table.set_table_type("confusionMatrix")
    modelSummaryCard2Table.set_table_top_header("Actual")
    modelSummaryCard2Table.set_table_left_header("Predicted")
    modelSummaryCard2Data.append(modelSummaryCard2Table)
    modelSummaryCard2.set_card_data(modelSummaryCard2Data)
    return [modelSummaryCard1,modelSummaryCard2]


def collated_model_summary_card(result_setter,prediction_narrative):
    collated_summary = result_setter.get_model_summary()
    card1 = NormalCard()
    card1Data = [HtmlData(data="<h4>Model Summary</h4>")]
    card1Data.append(HtmlData(data = get_total_models(collated_summary)))
    card1.set_card_data(card1Data)
    card1 = json.loads(CommonUtils.convert_python_object_to_json(card1))

    card2 = NormalCard()
    card2_elements = get_model_comparison(collated_summary)
    card2Data = [card2_elements[0],card2_elements[1]]
    card2.set_card_data(card2Data)
    # prediction_narrative.insert_card_at_given_index(card2,1)
    card2 = json.loads(CommonUtils.convert_python_object_to_json(card2))

    card3 = NormalCard()
    card3Data = [HtmlData(data="<h5 class = 'sm-ml-15 sm-pb-10'>Feature Importance</h5>")]
    card3Data.append(get_feature_importance(collated_summary))
    card3.set_card_data(card3Data)
    # prediction_narrative.insert_card_at_given_index(card3,2)
    card3 = json.loads(CommonUtils.convert_python_object_to_json(card3))

    modelResult = CommonUtils.convert_python_object_to_json(prediction_narrative)
    modelResult = json.loads(modelResult)
    existing_cards = modelResult["listOfCards"]
    existing_cards = result_setter.get_all_algos_cards()

    # modelResult["listOfCards"] = [card1,card2,card3] + existing_cards
    all_cards = [card1,card2,card3] + existing_cards

    modelResult = NarrativesTree()
    modelResult.add_cards(all_cards)
    modelResult = CommonUtils.convert_python_object_to_json(modelResult)
    modelJsonOutput = ModelSummary()
    modelJsonOutput.set_model_summary(json.loads(modelResult))
    ####
    rfModelSummary = result_setter.get_random_forest_model_summary()
    lrModelSummary = result_setter.get_logistic_regression_model_summary()
    xgbModelSummary = result_setter.get_xgboost_model_summary()

    model_dropdowns = []
    model_features = {}
    model_configs = {}
    targetVariableLevelcount = {}
    target_variable = collated_summary[collated_summary.keys()[0]]["targetVariable"]
    for obj in [rfModelSummary,lrModelSummary,xgbModelSummary]:
        if obj != {}:
            model_dropdowns.append(obj["dropdown"])
            model_features[obj["dropdown"]["slug"]] = obj["modelFeatureList"]
            if targetVariableLevelcount == {}:
                print obj["levelcount"]
                targetVariableLevelcount = obj["levelcount"][target_variable]
    model_configs = {"target_variable":[target_variable]}
    model_configs["modelFeatures"] = model_features
    model_configs["targetVariableLevelcount"] = [targetVariableLevelcount]

    modelJsonOutput.set_model_dropdown(model_dropdowns)
    modelJsonOutput.set_model_config(model_configs)
    modelJsonOutput = modelJsonOutput.get_json_data()
    return modelJsonOutput
