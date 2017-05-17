import pandas as pd
import numpy as np
import math
import random
from statistics import mean,median,mode,pstdev


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
    df_col = list(df.columns)
    for col in cat_columns:
        if col in df_col:
            uniq_vals = df[col].unique()
            key = [idx for idx,x in enumerate(uniq_vals)]
            rep_dict = dict(zip(uniq_vals,key))
            if col != 'responded':
                df[col]=df[col].apply(lambda x: rep_dict[x])
            else:
                df[col]=df[col].apply(lambda x: 1 if x == 'yes' else 0)
            df[col]=pd.factorize(df[col])[0]
    return df

def generate_train_test_split(df,cutoff,dependent_colname,drop_list):
    out = generate_random_number_array(df)
    ids = return_filtered_index(out,0.7)
    df_x = df[[col for col in df.columns if col not in drop_list+[dependent_colname]]]

    x_train = df_x.iloc[ids[0],:]
    x_test = df_x.iloc[ids[1],:]

    r_response = np.array(df[dependent_colname])
    y_train = r_response[ids[0]]
    y_test = r_response[ids[1]]
    return (x_train,x_test,y_train,y_test)

def calculate_confusion_matrix(actual,predicted):
    out = pd.crosstab(pd.Series(actual),pd.Series(predicted), rownames=['Known Class'], colnames=['Predicted Class'])
    return out

def calculate_precision_recall(actual,predicted):
    df = pd.DataFrame({"actual":actual,"predicted":predicted})
    classes = df["actual"].unique()
    output = {}
    if len(classes) > 2:
        for val in classes:
            class_summary = {}
            count_dict = {"tp":0,"fp":0,"tn":0,"fn":0}
            count_dict["tp"] = df[(df["actual"]==val) & (df["predicted"]==val)].shape[0]
            count_dict["fp"] = df[(df["actual"]!=val) & (df["predicted"]==val)].shape[0]
            count_dict["tn"] = df[(df["actual"]!=val) & (df["predicted"]!=val)].shape[0]
            count_dict["fn"] = df[(df["actual"]==val) & (df["predicted"]!=val)].shape[0]
            class_summary["counts"] = count_dict
            class_summary["precision"] = round(float(count_dict["tp"])/(count_dict["tp"]+count_dict["fp"]),2)
            class_summary["recall"] = round(float(count_dict["tp"])/(count_dict["tp"]+count_dict["fn"]),2)
            output[str(val)] = class_summary
    else:
        conf_matrix = calculate_confusion_matrix(actual,predicted)
        k = conf_matrix.to_dict()
        class_summary = {}
        count_dict = {"tp":0,"fp":0,"tn":0,"fn":0}
        count_dict["tp"] = k[1][1]
        count_dict["fp"] = k[0][1]
        count_dict["tn"] = k[0][0]
        count_dict["fn"] = k[1][0]
        class_summary["counts"] = count_dict
        class_summary["precision"] = round(float(count_dict["tp"])/(count_dict["tp"]+count_dict["fp"]),2)
        class_summary["recall"] = round(float(count_dict["tp"])/(count_dict["tp"]+count_dict["fn"]),2)
        output["overall"] = class_summary
    return output
