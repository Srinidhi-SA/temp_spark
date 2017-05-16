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


def predict(x_test,trained_model,drop_cols):
    """
    """
    if len(drop_cols) > 0:
        x_test = drop_columns(x_test,drop_cols)

    y_score = trained_model.predict(x_test)
    y_prob = trained_model.predict_proba(x_test)
    x_test['responded'] = y_score
    print(x_test['responded'].value_counts())
    return x_test

def train_and_predict(x_train, x_test, y_train, y_test,clf,plot_flag,print_flag,drop_cols):
    """
    Output is a dictionary
    y_prob => Array probability values for prediction
    results => Array of predicted class
    feature_importance => features ranked by their Importance
    feature_Weight => weight of features
    """
    if len(drop_cols) > 0:
        x_train = drop_columns(x_train,drop_cols)
        x_test = drop_columns(x_test,drop_cols)

    clf.fit(x_train, y_train)
    y_score = clf.predict(x_test)
    y_prob = clf.predict_proba(x_test)
    results = pd.DataFrame({"actual":y_test,"predicted":y_score,"prob":list(y_prob)})
    importances = clf.feature_importances_
    feature_importance = clf.feature_importances_.argsort()[::-1]
    # if print_flag:
    #     print("Classification Table")
    #     print(pd.crosstab(results.actual, results.predicted, rownames=['actual'], colnames=['preds']))
    #
    # fpr = dict()
    # tpr = dict()
    # roc_auc = dict()
    #
    # fpr["response"], tpr["response"], _ = roc_curve(y_test, y_score)
    # roc_auc["response"] = auc(fpr["response"], tpr["response"])
    # if plot_flag == True:
    #     plt.figure()
    #     lw = 2
    #     plt.plot(fpr['response'], tpr['response'], color='darkorange',
    #              lw=lw, label='ROC curve (area = %0.2f)' % roc_auc['response'])
    #     plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    #     plt.xlim([0.0, 1.0])
    #     plt.ylim([0.0, 1.05])
    #     plt.xlabel('False Positive Rate')
    #     plt.ylabel('True Positive Rate')
    #     plt.title('ROC Curve')
    #     plt.legend(loc="lower right")
    #     plt.show()

    # return {"y_prob":y_prob,"results":results,"feature_importance":feature_importance,
            # "feature_weight":importances,"auc":roc_auc["response"],"trained_model":clf}
    return {"trained_model":clf,"actual":y_test,"predicted":y_score,"probability":y_prob}

def calculate_confusion_matrix(actual,predicted):
    out = pd.crosstab(pd.Series(actual),pd.Series(predicted), rownames=['Known Class'], colnames=['Predicted Class'])
    return out

def calculate_precision_recall(actual,predicted):
    df = pd.DataFrame({"actual":actual,"predicted":predicted})
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
        class_summary["precision"] = round(float(count_dict["tp"])/(count_dict["tp"]+count_dict["fp"]),2)
        class_summary["recall"] = round(float(count_dict["tp"])/(count_dict["tp"]+count_dict["fn"]),2)
        output[str(val)] = class_summary
    return output
