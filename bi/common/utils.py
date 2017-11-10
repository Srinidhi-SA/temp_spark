import os
import math
import json
import time
import requests
from math import *
from re import sub
import traceback

from pyspark.conf import SparkConf
from pyspark.sql import SparkSession

from decorators import accepts
from math import log10, floor



def round_sig(x, sig=3):
    try:
        if abs(x)>=1:
            x = round(x,sig)
        else:
            x = round(x, sig-int(floor(log10(abs(x))))-1)
    except:
        pass
    return x

@accepts((int, long, float), (int, long, float), num_steps=int)
def frange(start, stop, num_steps=10):
    """
    Create num_step equal sized ranges form start to stop, useful in histogram generation
    :param start:
    :param stop:
    :param num_steps:
    :return:
    """
    step_size = start+1
    if start == stop:
        start=start - 0.8
        stop = stop + 0.8
    step_size = 1.0 * (stop-start) / num_steps
    rounding_digits = 0
    if step_size >= 1:
        step_size = int(math.ceil(step_size))
    else:
        rounding_digits = 1
        while num_steps >= (step_size * math.pow(10, rounding_digits)):
            rounding_digits += 1
        step_size = round(step_size, rounding_digits)

    rounded_start = math.floor(1.0 * start / step_size) * step_size
    rounded_stop = math.ceil(1.0 * (stop+step_size/num_steps) / step_size) * step_size
    i = rounded_start
    result = []
    while i < rounded_stop:
        result.append(round(i, rounding_digits))
        i += step_size
    if result[-1] < rounded_stop:
        result.append(round(rounded_stop, rounding_digits))
    result = list(set(result))
    result.sort()
    return result


@accepts(app_name=basestring)
def get_spark_session(app_name='Demo App'):
    return SparkSession.builder.appName(app_name).config(conf=SparkConf()).getOrCreate()
    #return SparkSession.builder.appName(app_name).getOrCreate()

def clean(x):
    from re import sub
    # \g<1> is whatever matches the the first (...)
    #x = sub( r'(\d+)[kK]', r'\g<1>000', x )
    x = sub('[^0-9.a-zA-z/-]','',x)
    return x

def get_updated_colnames(df):
    num_rows = len(df.index)
    final_column_names = []
    changed_cols = []
    for col in df.columns:
        if not df[col].dtype==object:
            final_column_names.append(col)
            continue
        temp = []
        try:
            temp = [x for x in df.dropna(subset=[col])[col]]
            initial_length = len(temp)
            if (initial_length<num_rows/2):
                raise ValueError('None Vals')
            temp1 = [float(clean(x)) for x in temp]
            final_length = len(temp1)
            if initial_length == final_length:
                changed_cols.append(col)
                try:
                    pre=int(temp[0][0])
                except:
                    col = col + '||pre:' + temp[0][0]
                try:
                    post=int(temp[0][-1])
                except:
                    col = col + '||post:' + temp[0][-1]

        except ValueError:
            # print "e1"
            pass
        else:
            pass
            # print "e2"
        final_column_names.append(col)
    return {'f':final_column_names, 'c':changed_cols}

def tryconvert(x):
    if x==None:
        return None
    try:
        x =float(sub('[^0-9.a-zA-z:/-]','',x))
        return x
    except:
        pass
    return None

def as_dict(obj):
    """
    Converts an object hierarchy into a dictionary object
    Ref: http://stackoverflow.com/questions/1036409/recursively-convert-python-object-graph-to-dictionary
    :param obj:
    :return:
    """
    if isinstance(obj, dict):
        return {k: as_dict(v) for (k, v) in obj.items()}
    elif hasattr(obj, "_ast"):
        return as_dict(obj._ast())
    elif hasattr(obj, '__iter__'):
        return [as_dict(v) for v in obj]
    elif hasattr(obj, '__dict__'):
        return dict([(key, as_dict(value))
                     for key, value in obj.__dict__.iteritems()
                     if not callable(value) and not key.startswith('_')])
    else:
        return obj

def recursiveRemoveNoneNodes(tree):
    if isinstance(tree, dict) and "children" not in tree.keys():
        return tree
    elif isinstance(tree, dict) and "children" in tree.keys():
        # if len(tree["children"]) != 0:
        if tree["children"] != [None]:
            for idx,stree in enumerate(tree["children"]):
                if stree != None:
                    tree["children"][idx] = (recursiveRemoveNoneNodes(stree))
            return tree
        else:
            tree.pop("children")
            return tree

def dateTimeFormatsSupported():
    data = {}
    data["formats"] = ('%m/%d/%Y %H:%M','%d/%m/%Y %H:%M','%m/%d/%y %H:%M','%d/%m/%y %H:%M',
            '%m-%d-%Y %H:%M','%d-%m-%Y %H:%M','%m-%d-%y %H:%M','%d-%m-%y %H:%M',
            '%b/%d/%Y %H:%M','%d/%b/%Y %H:%M','%b/%d/%y %H:%M','%d/%b/%y %H:%M',
            '%b-%d-%Y %H:%M','%d-%b-%Y %H:%M','%b-%d-%y %H:%M','%d-%b-%y %H:%M',
            '%B/%d/%Y %H:%M','%d/%B/%Y %H:%M','%B/%d/%y %H:%M','%d/%B/%y %H:%M',
            '%B-%d-%Y %H:%M','%d-%B-%Y %H:%M','%B-%d-%y %H:%M','%d-%B-%y %H:%M',
            '%Y-%m-%d %H:%M','%Y/%m/%d %H:%M','%Y-%b-%d %H:%M','%Y-%B-%d %H:%M',
            '%m-%d-%Y %r','%d-%m-%Y %r','%m-%d-%Y %R',
            '%d-%m-%Y %R', '%m-%d-%y %r','%d-%m-%y %r','%m-%d-%y %R',
            '%d-%m-%y %R', '%b-%d-%Y %r','%d-%b-%Y %r', '%Y-%b-%d %r','%b-%d-%Y %R',
            '%d-%b-%Y %R', '%b-%d-%y %r','%d-%b-%y %r','%b-%d-%y %R','%d-%b-%y %R',
            '%B-%d-%Y %r','%d-%B-%Y %r','%B-%d-%Y %R','%d-%B-%y %R',
            '%d-%B-%Y %R', '%B-%d-%y %r','%d-%B-%y %r','%B-%d-%y %R',
            '%y-%m-%d %R','%y-%m-%d %r','%Y-%m-%d %r','%Y-%B-%d %r',
            '%d %B %Y', '%d %B %y', '%d %b %y', '%d %b %Y',
            '%m/%d/%Y','%d/%m/%Y','%m/%d/%y','%d/%m/%y',
            '%m-%d-%Y','%d-%m-%Y','%m-%d-%y','%d-%m-%y',
            '%b/%d/%Y','%d/%b/%Y','%b/%d/%y','%d/%b/%y',
            '%b-%d-%Y','%d-%b-%Y','%b-%d-%y','%d-%b-%y',
            '%B/%d/%Y','%d/%B/%Y','%B/%d/%y','%d/%B/%y',
            '%B-%d-%Y','%d-%B-%Y','%B-%d-%y','%d-%B-%y',
            '%Y-%m-%d','%Y/%m/%d','%Y-%b-%d','%Y-%B-%d',
            '%b %d, %Y','%B %d, %Y','%B %d %Y','%m/%d/%Y',
            '%d %B, %Y', '%d %B, %y','%d %b, %Y', '%d %b, %y',
            '%m/%d/%y', '%b %Y','%B %y','%m/%y','%m/%Y',
            '%B%Y','%b %d,%Y','%m.%d.%Y','%m.%d.%y','%b/%y',
            '%m - %d - %Y','%m - %d - %y','%B %d, %y','%b %d, %y',
            '%d-%B','%d-%b', '%b,%y','%B,%y','%b,%Y','%B,%Y',
            '%b %Y', '%b %y','%B %Y','%B %y','%b-%y','%b/%Y','%b-%Y')

    data["dual_checks"] = ('%m/%d/%Y %H:%M','%m/%d/%y %H:%M','%m-%d-%Y %H:%M','%m-%d-%y %H:%M','%m-%d-%Y %r','%m-%d-%Y %R', '%m-%d-%y %r','%m-%d-%y %R',
                            '%m/%d/%Y %r','%m/%d/%Y %R', '%m/%d/%y %r','%m/%d/%y %R','%m/%d/%Y','%m/%d/%y','%m-%d-%Y','%m-%d-%y','%m.%d.%Y','%m.%d.%y','%m - %d - %Y',
                            '%m - %d - %y')
    return data

def write_to_file(filepath,obj):
    if filepath.startswith("file"):
        filepath = filepath[7:]
    f = open(filepath, 'w')
    f.write(obj)
    f.close()

def get_level_count_dict(df,categorical_columns,separator,output_type="string",dataType="pandas"):
    count_dict = {}
    out = []
    for col in categorical_columns:
        if dataType == "spark":
            count_dict[col] = len(df.select(col).distinct().collect())
        else:
            count_dict[col] = len(df[col].unique())
        out.append(col)
        out.append(str(count_dict[col]))
    if output_type == "string":
        return separator.join(out)
    else:
        return count_dict

def send_message_API(monitor_api, task, message, complete, progress):
    url = monitor_api
    message_dict = {}
    message_dict['task'] = task
    message_dict['message'] = message
    message_dict['complete'] = complete
    message_dict['progress'] = progress
    #r = requests.post(url, data=json.dumps(message_dict))
    #print json.loads(r.content)['message'] + " for ", task +'\n'

def temp_convertor(x):
    try:
        return x.__dict__
    except Exception as e:
        return "{}".format(x)

def convert_python_object_to_json(object):
    return json.dumps(object, default=temp_convertor)


def byteify(input):
    if isinstance(input, dict):
        return dict([(byteify(key), byteify(value)) for key, value in input.iteritems()])
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


def save_result_json(url,jsonData):
    url += "set_result"
    res = requests.put(url=url,data=jsonData)
    return res

def create_progress_message_object(sectionDict,name,timeTaken,completionStatus):
    progressMessage = {
        "name" : name,
        "displayName" : sectionDict[name]["displayName"],
        "timeTaken" : timeTaken,
        "completionStatus" : completionStatus
    }
    return progressMessage

def create_progress_message_object(analysisName,stageName,messageType,shortExplanation,stageCompletionPercentage,globalCompletionPercentage):
    progressMessage = {
        "analysisName" : analysisName,
        "stageName" : stageName,
        "messageType" : messageType,
        "shortExplanation" : shortExplanation,
        "stageCompletionTimestamp" : time.time(),
        "globalCompletionPercentage" : globalCompletionPercentage,
        "stageCompletionPercentage" : stageCompletionPercentage
    }
    return progressMessage

def save_progress_message(url,jsonData):
    res = requests.put(url=url,data=json.dumps(jsonData))
    return res

def keyWithMaxVal(dictObj):
     """ a) create a list of the dict's keys and values;
         b) return the key with the max value"""
     v=list(dictObj.values())
     k=list(dictObj.keys())
     return k[v.index(max(v))]

def print_errors_and_store_traceback(loggerDict,scriptName,error):
    print error
    exception = {"exception":error,"traceback":traceback.format_exc()}
    loggerDict[scriptName] = exception
    print "#####ERROR#####"*5
    print error
    print "#####ERROR#####"*5
    print "{} Script Failed".format("scriptName")

def get_story_config():
    storyConfig = {

        "config" : {
            "ADVANCED_SETTINGS" : {
                "analysis" : [
                    {
                        "analysisSubTypes" : [],
                        "displayName" : "Overview",
                        "name" : "overview",
                        "noOfColumnsToUse" : None,
                        "status" : True
                    },
                    {
                        "analysisSubTypes" : [
                            {
                                "displayName" : "Overview",
                                "name" : "overview",
                                "status" : False
                            },
                            {
                                "displayName" : "Factors that drive up",
                                "name" : "factors that drive up",
                                "status" : False
                            },
                            {
                                "displayName" : "Factors that drive down",
                                "name" : "factors that drive down",
                                "status" : False
                            },
                            {
                                "displayName" : "Forecast",
                                "name" : "forecast",
                                "status" : False
                            }
                        ],
                        "displayName" : "Trend",
                        "name" : "trend",
                        "noOfColumnsToUse" : None,
                        "status" : False
                    },
                    {
                        "analysisSubTypes" : [],
                        "displayName" : "Association",
                        "name" : "association",
                        "noOfColumnsToUse" : [
                            {
                                "defaultValue" : 3,
                                "displayName" : "Low",
                                "name" : "low",
                                "status" : True
                            },
                            {
                                "defaultValue" : 5,
                                "displayName" : "Medium",
                                "name" : "medium",
                                "status" : False
                            },
                            {
                                "defaultValue" : 8,
                                "displayName" : "High",
                                "name" : "high",
                                "status" : False
                            },
                            {
                                "defaultValue" : 3,
                                "displayName" : "Custom",
                                "name" : "custom",
                                "status" : False,
                                "value" : None
                            }
                        ],
                        "status" : False
                    },
                    {
                        "analysisSubTypes" : [],
                        "displayName" : "Influencer",
                        "name" : "influencer",
                        "noOfColumnsToUse" : [
                            {
                                "defaultValue" : 3,
                                "displayName" : "Low",
                                "name" : "low",
                                "status" : True
                            },
                            {
                                "defaultValue" : 5,
                                "displayName" : "Medium",
                                "name" : "medium",
                                "status" : False
                            },
                            {
                                "defaultValue" : 8,
                                "displayName" : "High",
                                "name" : "high",
                                "status" : False
                            },
                            {
                                "defaultValue" : 3,
                                "displayName" : "Custom",
                                "name" : "custom",
                                "status" : False,
                                "value" : None
                            }
                        ],
                        "status" : True
                    },
                    {
                        "analysisSubTypes" : [],
                        "displayName" : "Prediction",
                        "name" : "prediction",
                        "noOfColumnsToUse" : None,
                        "status" : True
                    }
                ],
                "targetLevels" : [
                    []
                ],
                "trendSettings" : [
                    {
                        "name" : "Count",
                        "status" : True
                    },
                    {
                        "name" : "Specific Measure",
                        "selectedMeasure" : None,
                        "status" : False
                    }
                ]
            },
            "COLUMN_SETTINGS" : {
                "analysis_type" : [
                    "measure"
                ],
                "consider_columns" : [
                    "Education",
                    "Top Organization",
                    "Agent Name",
                    "Call Type",
                    "State",
                    "Region",
                    "Agent Experience",
                    "Agent Rating",
                    "Agent Age",
                    "Top Plan Provider",
                    "Call Volume",
                    "First call resolution",
                    "Average Call duration (in Minutes)",
                    "Call date"
                ],
                "consider_columns_type" : [
                    "including"
                ],
                "dateTimeSuggestions" : [
                    {}
                ],
                "date_columns" : [
                    "Call date"
                ],
                "date_format" : None,
                "ignore_column_suggestion" : [],
                "polarity" : [
                    "positive"
                ],
                "result_column" : [
                    "Call Volume"
                ],
                "utf8_column_suggestions" : []
            },
            "DATA_SOURCE" : {
                "datasource_details" : "",
                "datasource_type" : "fileUpload"
            },
            "FILE_SETTINGS" : {
                "inputfile" : [
                    # "hdfs://ec2-34-205-203-38.compute-1.amazonaws.com:8020/dev/dataset/health-care-callcentre-v10csv-b3z14xn6dj/Health_Care_Callcentre-_V10.csv"
                    "file:///home/gulshan/marlabs/datasets/Health Care Callcentre- V10.csv"
                ],
                "script_to_run" : [
                    "Descriptive analysis",
                    "Trend",
                    "Dimension vs. Dimension",
                    "Predictive modeling"
                ]
            }
        },
        "job_config" : {
            "get_config" : {
                "action" : "get_config",
                "method" : "GET"
            },
            "job_name" : "Healthcare Education",
            "job_type" : "story",
            "job_url" : "http://34.196.204.54:9012/api/job/master-healthcare-education-4rzbktxf81-lrmr3gqec2/",
            "message_url" : "http://34.196.204.54:9012/api/messages/Insight_healthcare-education-4rzbktxf81_123/",
            "set_result" : {
                "action" : "result",
                "method" : "PUT"
            }
        }
    }
    return storyConfig

def get_metadata_config():
    metaDataConfig = {
        "config" : {
            "COLUMN_SETTINGS" : {
                "analysis_type" : [
                    "metaData"
                ]
            },
            "DATA_SOURCE" : {
                "datasource_details" : "",
                "datasource_type" : "fileUpload"
            },
            "DATE_SETTINGS" : {},
            "FILE_SETTINGS" : {
                "inputfile" : [
                    "file:///home/gulshan/marlabs/datasets/sigma/ignoreTest.csv"
                ]
            }
        },
        "job_config" : {
            "get_config" : {
                "action" : "get_config",
                "method" : "GET"
            },
            "job_name" : "Sample1.csv",
            "job_type" : "metaData",
            "message_url" : "http://34.196.204.54:9012/api/messages/Dataset_trend_gulshancsv-h85lh79ybd_123/",
            "job_url" : "http://34.196.204.54:9012/api/job/metadata-sample1csv-e2za8z9u26-o1f6wicswc/",
            "set_result" : {
                "action" : "result",
                "method" : "PUT"
            }
        }
    }
    return metaDataConfig

def get_training_config():
    trainingConfig = {
        "config":{
            'FILE_SETTINGS': {
                'inputfile': ['file:///home/gulshan/marlabs/datasets/adult.csv'],
                # Model Slug will go instead of model path
                'modelpath': ["ANKUSH"],
                'train_test_split' : [0.8],
                'analysis_type' : ['training']
            },
            'COLUMN_SETTINGS': {
                'analysis_type': ['training'],
                'result_column': ['class_label'],
                'consider_columns_type': ['excluding'],
                'consider_columns':[],
                'polarity': ['positive'],
                'date_format': None,
                # 'date_columns':["new_date","Month","Order Date"],
                'date_columns':[],
                'ignore_column_suggestions': [],
                # 'ignore_column_suggestions': ["Outlet ID","Visibility to Cosumer","Cleanliness","Days to Resolve","Heineken Lager Share %","Issue Category","Outlet","Accessible_to_consumer","Resultion Status"],
                'dateTimeSuggestions' : [],
                'utf8ColumnSuggestion':[],
                'consider_columns':[],
            },
            "DATA_SOURCE" : {
                "datasource_details" : "",
                "datasource_type" : "fileUpload"
            }
        },
        "job_config":{
            "get_config" : {
                "action" : "get_config",
                "method" : "GET"
            },
            "job_name" : "Sample1.csv",
            "job_type":"training",
            "message_url" : "http://34.196.204.54:9012/api/messages/Dataset_trend_gulshancsv-h85lh79ybd_123/",
            # "job_url": "http://localhost:8000/api/job/dataset-iriscsv-qpmercq3r8-2fjupdcwdu/",
            "job_url": "http://localhost:8000/api/job/dataset-iriscsv-qpmercq3r8-2fjupdcwdu/",
            "set_result": {
                "method": "PUT",
                "action": "result"
              },
        }
    }
    return trainingConfig

def get_prediction_config():
    predictionConfig = {
        "config":{
            'FILE_SETTINGS': {
                'inputfile': ['file:///home/gulshan/marlabs/datasets/adult_test.csv'],
                'modelpath': ["ANKUSH"],
                'scorepath': ["DDDDD"],
                # 'train_test_split' : [0.8],
                'levelcounts' : [],
                'modelfeatures' : [],
                "algorithmslug":["f77631ce2ab24cf78c55bb6a5fce4db8lr"],
            },
            'COLUMN_SETTINGS': {
                'analysis_type': ['Dimension'],
                'result_column': ['class_label'],
                # 'consider_columns_type': ['excluding'],
                # 'consider_columns':[],
                # 'date_columns':['Date'],
                'score_consider_columns_type': ['excluding'],
                'score_consider_columns':[],
                "app_id":[2]

            },
            "DATA_SOURCE" : {
                "datasource_details" : "",
                "datasource_type" : "fileUpload"
            },
        },
        "job_config":{
            "get_config" : {
                "action" : "get_config",
                "method" : "GET"
            },
            "job_name" : "Sample1",
            "job_type":"prediction",
            "job_url": "http://34.196.204.54:9012/api/job/score-hiohoyuo-bn1ofiupv0-j0irk37cob/set_result/",
            "message_url" : "http://34.196.204.54:9012/api/messages/Dataset_trend_gulshancsv-h85lh79ybd_123/",
            "set_result": {
                "method": "PUT",
                "action": "result"
              },
        }
    }
    return predictionConfig

def get_subsetting_config():
    subsettingConfig = {
        "config" : {
                    "COLUMN_SETTINGS" : {
                        "analysis_type" : [
                            "metaData"
                        ]
                    },
                    "DATA_SOURCE" : {
                        "datasource_details" : "",
                        "datasource_type" : "fileUpload"
                    },
                    "DATE_SETTINGS" : {},
                    "FILE_SETTINGS" : {
                        "inputfile" : [
                            # "hdfs://ec2-34-205-203-38.compute-1.amazonaws.com:8020/dev/dataset/subsetting_testcsv-zxhdwhl5u2/subsetting_test_3n3aZh5.csv"
                            "file:///home/gulshan/marlabs/datasets/subsetting_test.csv"
                        ],
                        "outputfile" : [
                            # "hdfs://ec2-34-205-203-38.compute-1.amazonaws.com:8020/dev/dataset/subsetting_test_new-tqj35ger3q"
                            "file:///home/gulshan/marlabs/csvout/data"
                        ]
                    },
                    "FILTER_SETTINGS" : {
                        "dimensionColumnFilters" : [],
                        "measureColumnFilters" : [],
                        "timeDimensionColumnFilters" : []
                    },
                    "TRANSFORMATION_SETTINGS" : {
                        "existingColumns" : [
                            {
                                "columnSetting" : [
                                    {
                                        "actionName" : "delete",
                                        "displayName" : "Delete Column",
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "rename",
                                        "displayName" : "Rename Column",
                                        "newName" : None,
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "replace",
                                        "displayName" : "Replace Values",
                                        "replaceTypeList" : [
                                            {
                                                "displayName" : "Contains",
                                                "name" : "contains"
                                            },
                                            {
                                                "displayName" : "Equal To",
                                                "name" : "equals"
                                            },
                                            {
                                                "displayName" : "Starts With",
                                                "name" : "startsWith"
                                            },
                                            {
                                                "displayName" : "Ends With",
                                                "name" : "endsWith"
                                            }
                                        ],
                                        "replacementValues" : [],
                                        "status" : False
                                    }
                                ],
                                "name" : "CREDIT_BALANCE1",
                                "slug" : "167338ffe707492a9a2f0667ecc26a13"
                            },
                            {
                                "columnSetting" : [
                                    {
                                        "actionName" : "delete",
                                        "displayName" : "Delete Column",
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "rename",
                                        "displayName" : "Rename Column",
                                        "newName" : None,
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "replace",
                                        "displayName" : "Replace Values",
                                        "replaceTypeList" : [
                                            {
                                                "displayName" : "Contains",
                                                "name" : "contains"
                                            },
                                            {
                                                "displayName" : "Equal To",
                                                "name" : "equals"
                                            },
                                            {
                                                "displayName" : "Starts With",
                                                "name" : "startsWith"
                                            },
                                            {
                                                "displayName" : "Ends With",
                                                "name" : "endsWith"
                                            }
                                        ],
                                        "replacementValues" : [],
                                        "status" : False
                                    }
                                ],
                                "name" : "CREDIT_BALANCE2",
                                "slug" : "8b94ae1a2fa54e14b6602ac25344085f"
                            },
                            {
                                "columnSetting" : [
                                    {
                                        "actionName" : "delete",
                                        "displayName" : "Delete Column",
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "rename",
                                        "displayName" : "Rename Column",
                                        "newName" : None,
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "replace",
                                        "displayName" : "Replace Values",
                                        "replaceTypeList" : [
                                            {
                                                "displayName" : "Contains",
                                                "name" : "contains"
                                            },
                                            {
                                                "displayName" : "Equal To",
                                                "name" : "equals"
                                            },
                                            {
                                                "displayName" : "Starts With",
                                                "name" : "startsWith"
                                            },
                                            {
                                                "displayName" : "Ends With",
                                                "name" : "endsWith"
                                            }
                                        ],
                                        "replacementValues" : [],
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "data_type",
                                        "displayName" : "Change Datatype",
                                        "listOfDataTypes" : [
                                            {
                                                "displayName" : "Numeric",
                                                "name" : "numeric",
                                                "status" : True
                                            },
                                            {
                                                "displayName" : "Text",
                                                "name" : "text",
                                                "status" : False
                                            }
                                        ],
                                        "status" : True
                                    }
                                ],
                                "name" : "CREDIT_BALANCE3",
                                "slug" : "684126299d4742c58ca9b460e5ff43a1"
                            },
                            {
                                "columnSetting" : [
                                    {
                                        "actionName" : "delete",
                                        "displayName" : "Delete Column",
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "rename",
                                        "displayName" : "Rename Column",
                                        "newName" : None,
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "replace",
                                        "displayName" : "Replace Values",
                                        "replaceTypeList" : [
                                            {
                                                "displayName" : "Contains",
                                                "name" : "contains"
                                            },
                                            {
                                                "displayName" : "Equal To",
                                                "name" : "equals"
                                            },
                                            {
                                                "displayName" : "Starts With",
                                                "name" : "startsWith"
                                            },
                                            {
                                                "displayName" : "Ends With",
                                                "name" : "endsWith"
                                            }
                                        ],
                                        "replacementValues" : [],
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "data_type",
                                        "displayName" : "Change Datatype",
                                        "listOfDataTypes" : [
                                            {
                                                "displayName" : "Numeric",
                                                "name" : "numeric",
                                                "status" : False
                                            },
                                            {
                                                "displayName" : "Text",
                                                "name" : "text",
                                                "status" : False
                                            }
                                        ],
                                        "status" : False
                                    }
                                ],
                                "name" : "SEX",
                                "slug" : "27aadfb44d8f4fcc837654316e9b1bf4"
                            },
                            {
                                "columnSetting" : [
                                    {
                                        "actionName" : "delete",
                                        "displayName" : "Delete Column",
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "rename",
                                        "displayName" : "Rename Column",
                                        "newName" : None,
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "replace",
                                        "displayName" : "Replace Values",
                                        "replaceTypeList" : [
                                            {
                                                "displayName" : "Contains",
                                                "name" : "contains"
                                            },
                                            {
                                                "displayName" : "Equal To",
                                                "name" : "equals"
                                            },
                                            {
                                                "displayName" : "Starts With",
                                                "name" : "startsWith"
                                            },
                                            {
                                                "displayName" : "Ends With",
                                                "name" : "endsWith"
                                            }
                                        ],
                                        "replacementValues" : [],
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "data_type",
                                        "displayName" : "Change Datatype",
                                        "listOfDataTypes" : [
                                            {
                                                "displayName" : "Numeric",
                                                "name" : "numeric",
                                                "status" : False
                                            },
                                            {
                                                "displayName" : "Text",
                                                "name" : "text",
                                                "status" : False
                                            }
                                        ],
                                        "status" : False
                                    }
                                ],
                                "name" : "EDUCATION",
                                "slug" : "c5c42c0f7b3a4632bd7e0269f998ec30"
                            },
                            {
                                "columnSetting" : [
                                    {
                                        "actionName" : "delete",
                                        "displayName" : "Delete Column",
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "rename",
                                        "displayName" : "Rename Column",
                                        "newName" : None,
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "replace",
                                        "displayName" : "Replace Values",
                                        "replaceTypeList" : [
                                            {
                                                "displayName" : "Contains",
                                                "name" : "contains"
                                            },
                                            {
                                                "displayName" : "Equal To",
                                                "name" : "equals"
                                            },
                                            {
                                                "displayName" : "Starts With",
                                                "name" : "startsWith"
                                            },
                                            {
                                                "displayName" : "Ends With",
                                                "name" : "endsWith"
                                            }
                                        ],
                                        "replacementValues" : [],
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "data_type",
                                        "displayName" : "Change Datatype",
                                        "listOfDataTypes" : [
                                            {
                                                "displayName" : "Numeric",
                                                "name" : "numeric",
                                                "status" : False
                                            },
                                            {
                                                "displayName" : "Text",
                                                "name" : "text",
                                                "status" : False
                                            }
                                        ],
                                        "status" : False
                                    }
                                ],
                                "name" : "MARRIAGE",
                                "slug" : "800b2f543eb5455a8ffcbc48bcdc0abf"
                            },
                            {
                                "columnSetting" : [
                                    {
                                        "actionName" : "delete",
                                        "displayName" : "Delete Column",
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "rename",
                                        "displayName" : "Rename Column",
                                        "newName" : None,
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "replace",
                                        "displayName" : "Replace Values",
                                        "replaceTypeList" : [
                                            {
                                                "displayName" : "Contains",
                                                "name" : "contains"
                                            },
                                            {
                                                "displayName" : "Equal To",
                                                "name" : "equals"
                                            },
                                            {
                                                "displayName" : "Starts With",
                                                "name" : "startsWith"
                                            },
                                            {
                                                "displayName" : "Ends With",
                                                "name" : "endsWith"
                                            }
                                        ],
                                        "replacementValues" : [],
                                        "status" : False
                                    }
                                ],
                                "name" : "new_date",
                                "slug" : "5e1fb20628d04549970d84da96fcb60e"
                            },
                            {
                                "columnSetting" : [
                                    {
                                        "actionName" : "delete",
                                        "displayName" : "Delete Column",
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "rename",
                                        "displayName" : "Rename Column",
                                        "newName" : None,
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "replace",
                                        "displayName" : "Replace Values",
                                        "replaceTypeList" : [
                                            {
                                                "displayName" : "Contains",
                                                "name" : "contains"
                                            },
                                            {
                                                "displayName" : "Equal To",
                                                "name" : "equals"
                                            },
                                            {
                                                "displayName" : "Starts With",
                                                "name" : "startsWith"
                                            },
                                            {
                                                "displayName" : "Ends With",
                                                "name" : "endsWith"
                                            }
                                        ],
                                        "replacementValues" : [],
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "data_type",
                                        "displayName" : "Change Datatype",
                                        "listOfDataTypes" : [
                                            {
                                                "displayName" : "Numeric",
                                                "name" : "numeric",
                                                "status" : False
                                            },
                                            {
                                                "displayName" : "Text",
                                                "name" : "text",
                                                "status" : False
                                            }
                                        ],
                                        "status" : False
                                    }
                                ],
                                "name" : "colToReplace",
                                "slug" : "d8f87c8c454f4aae992a0f05cc9b2edb"
                            },
                            {
                                "columnSetting" : [
                                    {
                                        "actionName" : "delete",
                                        "displayName" : "Delete Column",
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "rename",
                                        "displayName" : "Rename Column",
                                        "newName" : None,
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "replace",
                                        "displayName" : "Replace Values",
                                        "replaceTypeList" : [
                                            {
                                                "displayName" : "Contains",
                                                "name" : "contains"
                                            },
                                            {
                                                "displayName" : "Equal To",
                                                "name" : "equals"
                                            },
                                            {
                                                "displayName" : "Starts With",
                                                "name" : "startsWith"
                                            },
                                            {
                                                "displayName" : "Ends With",
                                                "name" : "endsWith"
                                            }
                                        ],
                                        "replacementValues" : [],
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "data_type",
                                        "displayName" : "Change Datatype",
                                        "listOfDataTypes" : [
                                            {
                                                "displayName" : "Numeric",
                                                "name" : "numeric",
                                                "status" : False
                                            },
                                            {
                                                "displayName" : "Text",
                                                "name" : "text",
                                                "status" : False
                                            }
                                        ],
                                        "status" : False
                                    }
                                ],
                                "name" : "toDelete",
                                "slug" : "28b1ba754bfa4782a644ed93357cf1e9"
                            },
                            {
                                "columnSetting" : [
                                    {
                                        "actionName" : "delete",
                                        "displayName" : "Delete Column",
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "rename",
                                        "displayName" : "Rename Column",
                                        "newName" : None,
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "replace",
                                        "displayName" : "Replace Values",
                                        "replaceTypeList" : [
                                            {
                                                "displayName" : "Contains",
                                                "name" : "contains"
                                            },
                                            {
                                                "displayName" : "Equal To",
                                                "name" : "equals"
                                            },
                                            {
                                                "displayName" : "Starts With",
                                                "name" : "startsWith"
                                            },
                                            {
                                                "displayName" : "Ends With",
                                                "name" : "endsWith"
                                            }
                                        ],
                                        "replacementValues" : [],
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "data_type",
                                        "displayName" : "Change Datatype",
                                        "listOfDataTypes" : [
                                            {
                                                "displayName" : "Numeric",
                                                "name" : "numeric",
                                                "status" : False
                                            },
                                            {
                                                "displayName" : "Text",
                                                "name" : "text",
                                                "status" : False
                                            }
                                        ],
                                        "status" : False
                                    }
                                ],
                                "name" : "toReplace",
                                "slug" : "e628974095ce42de8e5114976979db0e"
                            }
                        ]
                    }
                },
                "job_config" : {
                    "get_config" : {
                        "action" : "get_config",
                        "method" : "GET"
                    },
                    "job_name" : "subsetting_test_new",
                    "job_type" : "subSetting",
                    "job_url" : "http://34.196.204.54:9012/api/job/subsetting-subsetting_test_new-tqj35ger3q-bp9kq1alzn/",
                    "message_url" : "http://34.196.204.54:9012/api/messages/Dataset_subsetting_test_new-tqj35ger3q_123/",
                    "set_result" : {
                        "action" : "result",
                        "method" : "PUT"
                    }
                }
    }
    return subsettingConfig

def get_stockadvisor_config():
    stockAdvisorConfig = {
        'job_config': {
          'job_url': 'http://34.196.204.54:9012/api/job/stockadvisor-stocking_is_what_i_do-6ryt9x72e8-ynolqb82hb/',
          'job_type': 'stockAdvisor',
          'set_result': {
            'action': 'result',
            'method': 'PUT'
          },
          'get_config': {
            'action': 'get_config',
            'method': 'GET'
          },
          'message_url': 'http://34.196.204.54:9012/api/messages/StockDataset_stocking_is_what_i_do-6ryt9x72e8_123/',
          'job_name': u'stocking_is_what_i_do'
        },
        u'config': {
          u'COLUMN_SETTINGS': {
            u'analysis_type': [
              u'metaData'
            ]
          },
          u'DATE_SETTINGS': {

          },
          u'DATA_SOURCE': {
            u'datasource_details': u''
          },
          u'STOCK_SETTINGS': {
            u'stockSymbolList': [
              'googl','appl'
            ],
            u'dataAPI': 'http://34.196.204.54:9012/api/stockdatasetfiles/stocking_is_what_i_do-imlizu9xul/',
          },
          u'FILE_SETTINGS': {
            u'inputfile': [
              u''
            ]
          }
        }
      }
    return stockAdvisorConfig

def get_test_configs():
    testConfigs = {
        "story"        : get_story_config(),
        "metaData"     : get_metadata_config(),
        "training"     : get_training_config(),
        "prediction"   : get_prediction_config(),
        "subSetting"   : get_subsetting_config(),
        "stockAdvisor" : get_stockadvisor_config()
    }
    return testConfigs

if __name__ == '__main__':
    x = frange(0.01,0.02,5)
