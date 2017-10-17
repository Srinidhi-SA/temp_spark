import os
import math
import json
import time
import requests
from math import *
from re import sub

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
                raise ValueError('Null Vals')
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

def recursiveRemoveNullNodes(tree):
    if isinstance(tree, dict) and "children" not in tree.keys():
        return tree
    elif isinstance(tree, dict) and "children" in tree.keys():
        # if len(tree["children"]) != 0:
        if tree["children"] != [None]:
            for idx,stree in enumerate(tree["children"]):
                if stree != None:
                    tree["children"][idx] = (recursiveRemoveNullNodes(stree))
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

if __name__ == '__main__':
    x = frange(0.01,0.02,5)
