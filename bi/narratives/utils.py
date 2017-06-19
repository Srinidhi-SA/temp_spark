
"""
Utility functions to be used by various narrative objects
"""
import math
import re

import enchant
import jinja2
import numpy as np
import pandas as pd
import pattern
from datetime import datetime


def round_number(num, digits=2, as_string=True):
    millions = 0
    thousands = 0
    billions = 0
    if(num//1000000000 > 0) and (as_string):
        num = num/1000000000.0
        billions =1
        digits = 2
    elif(num//1000000 > 0) and (as_string):
        num = num/1000000.0
        millions =1
        digits = 2
    elif(num//1000 > 0) and (as_string):
        num = num/1000.0
        thousands = 1
        digits = 2
    elif (abs(num)<1):
        digits = digits + int(abs(math.log(num,10)))
    result = float(format(num, '0.%df' %(digits,)))
    if as_string:
        result = str(result)
        decs = result[result.find('.'):]
        result = result[:result.find('.')]
        temp = len(str(result))
        if temp>3:
            for insertions in range(len(result)-3,0,-3):
                result = result[:insertions]+','+result[insertions:]
        if billions ==1:
            return result+decs+' Billion'
        if millions ==1:
            return result+decs+' Million'
        if thousands == 1:
            return result+decs+'K'
        return result+decs
    return result

def paragraph_splitter(summary):
    output = []
    paragraphs = summary.split("PARASEPARATOR")
    for val in paragraphs:
        if val != "":
            temp = {"header":"","content":[""]}
            if "PARAHEADER" in val:
                parts = val.split("PARAHEADER")
                temp["header"] = parts[0]
                temp["content"] = [parts[1]]
            else:
                temp["content"] = [val]
            output.append(temp)
    return output

def clean_narratives(output):
    output = re.sub('\n',' ',output)
    output = re.sub(' +',' ',output)
    output = re.sub(' ,',',',output)
    output = re.sub(' \.','.',output)
    output = re.sub('\( ','(',output)
    return output

def get_template_output(base_dir, template_file, data_dict):
    templateLoader = jinja2.FileSystemLoader( searchpath=base_dir)
    templateEnv = jinja2.Environment( loader=templateLoader )
    template = templateEnv.get_template(template_file)
    output = template.render(data_dict)
    return clean_narratives(output)

def clean_result_text(text):
    return str.replace("\n", "")

def get_plural_word(text):
    d = enchant.Dict("en_US")
    if text == text.upper():
        plural = text.lower()
        plural = pattern.en.pluralize(text)
        if d.check(plural):
            plural = plural.upper()
        else:
            plural = text
    elif text == text.title():
        plural = text.lower()
        plural = pattern.en.pluralize(text)
        if d.check(plural):
            plural = plural.title()
        else:
            plural = text
    else:
        plural = pattern.en.pluralize(text)
        if not d.check(plural):
            plural = text
    return plural

def pluralize(text):
    matches=[m.start() for m in re.finditer('[^a-zA-Z]', text)]
    if(len(matches)>0):
        br = matches[-1]+1
        text = text[:br]+get_plural_word(text[br:])
    else:
        text = get_plural_word(text)
    return text


def parse_leaf_name(name):
    return name[9:]

def check_leaf_node(node):
    if len(node['children']) == 1:
        return parse_leaf_name(node['children'][0]['name'])
    else:
        return False

def get_leaf_nodes(node):
    leaves = []
    leaf_node = check_leaf_node(node)
    if leaf_node != False:
        leaves += [leaf_node]
        return leaves
    else:
        for child_node in node['children']:
            leaves += get_leaf_nodes(child_node)
        return leaves

def generate_rule_text(rule_path_list,separator):
    return separator.join(rule_path_list[:-1])

def get_rules_dictionary(rules):
    key_dimensions = {}
    key_measures = {}
    rules_list = re.split(r',\s*(?![^()]*\))',rules)
    for rx in rules_list:
        if ' <= ' in rx:
            var,limit = re.split(' <= ',rx)
            if not key_measures.has_key(var):
                key_measures[var] ={}
            key_measures[var]['upper_limit'] = limit
        elif ' > ' in rx:
            var,limit = re.split(' > ',rx)
            if not key_measures.has_key(var):
                key_measures[var] = {}
            key_measures[var]['lower_limit'] = limit
        elif ' not in ' in rx:
            var,levels = re.split(' not in ',rx)
            if not key_dimensions.has_key(var):
                key_dimensions[var]={}
            key_dimensions[var]['not_in'] = levels
        elif ' in ' in rx:
            var,levels = re.split(' in ',rx)
            if not key_dimensions.has_key(var):
                key_dimensions[var]={}
            key_dimensions[var]['in'] = levels
    return [key_dimensions,key_measures]

def generate_leaf_rule_dict(rule_list,separator):
    out = {}
    leaf_list = list(set([x[-1] for x in rule_list]))
    for leaf in leaf_list:
        out[leaf] = [generate_rule_text(x,separator) for x in rule_list if x[-1] == leaf]
    return out

def generate_condensed_rule_dict(rule_list):
    out = {}
    leaf_list = list(set([x[-1] for x in rule_list]))
    for leaf in leaf_list:
        out[leaf] = [",".join(x) for x in rule_list if x[-1] == leaf]
    return out

def flatten_rules(result_tree, current_rule_list=None, all_rules=None):
    if current_rule_list is None:
        current_rule_list = []
    if all_rules is None:
        all_rules = []
    if len(result_tree) == 1:
        current_rule_list.append(parse_leaf_name(result_tree[0]['name']))
        all_rules.append(current_rule_list)
        return
    for val in result_tree:
        new_rule_list = current_rule_list[:]
        new_rule_list.append(val['name'])
        flatten_rules(val['children'], new_rule_list, all_rules)
    return all_rules

def return_template_output(base_dir,filename,data_dict):
    """
    base_dir => path to the folder where templates are stored.
    filename => template file name.
    data_dict => dictionary containing variables used in template file as key and their corresponding values.

    Returns object is the generated sentence
    """
    templateLoader = jinja2.FileSystemLoader( searchpath=base_dir)
    templateEnv = jinja2.Environment( loader=templateLoader )
    template = templateEnv.get_template(filename)
    output = template.render(data_dict)
    return output

def get_bin_names (splits):
    bin_names = []
    start = splits[0]
    for i in splits[1:]:
        bin_names.append(str(start) + ' to ' + str(i))
        start = i
    return bin_names


def longestRun(s):
    output = {"P":None,"N":None}
    if len(s) == 0: return output
    pos = []
    neg = []
    for x,y in zip(s,s[1:]):
        if x == y and x == "P":
            pos.append("*")
        else:
            pos.append(' ')
        if x == y and x == "N":
            neg.append("*")
        else:
            neg.append(' ')
    posruns = ''.join(pos)
    negruns = ''.join(neg)
#     posruns = ''.join('*' if x == y and x == "P" else ' ' for x,y in zip(s,s[1:]))
    starStrings = posruns.split()
    if len(starStrings) == 0:
        output["P"] = 1
        return output
    output["P"] = 1 + max(len(stars) for stars in starStrings)

    starStrings = negruns.split()
    if len(starStrings) == 0:
        output["N"] = 1
        return output
    output["N"] = 1 + max(len(stars) for stars in starStrings)
    return output

def continuous_streak(aggData, direction="increase"):
    data = aggData.T.to_dict().values()
    if len(data) < 2:
        return len(data)
    else:
        start, streaks = -1, []
        for idx, (x, y) in enumerate(zip(data, data[1:])):
            if direction == "increase":
                if x['value'] > y['value']:
                    # streaks.append(idx - start)
                    streaks.append(data[start+1:idx+1])
                    start = idx
            elif direction == "decrease":
                if x['value'] < y['value']:
                    # streaks.append(idx - start)
                    streaks.append(data[start+1:idx+1])
                    start = idx
        else:
            # streaks.append(idx - start + 1)
            streaks.append(data[start+1:idx+1])

        return streaks

def get_max_min_stats(df,dataLevel,trend = "positive", stat_type = "percentage"):
    output = {}
    if stat_type == "percentage":
        col = "perChange"
    elif stat_type == "absolute":
        col = "value"
    if trend == "positive":
        index = np.argmax(list(df[col]))
    elif trend == "negative":
        index = np.argmin(list(df[col]))
    if dataLevel == "day":
        period = str(df["key"][index])
    else:
        period = df["year_month"][index]
    if stat_type == "percentage":
        change = str(round(df[col][index],2))+"%"
    elif stat_type == "absolute":
        change = str(round(df[col][index],2))
    if index != 0:
        changeValues = (df["value"][index-1],df["value"][index])
    else:
        changeValues = (0,df["value"][index])
    if trend == "positive":
        output = {"increase":"Largest (Percentage)","period":period,"increased_by":change,"range":str(changeValues[0])+" to "+str(changeValues[1])}
    else:
        output = {"decrease":"Largest (Percentage)","period":period,"decreased_by":change,"range":str(changeValues[0])+" to "+str(changeValues[1])}
    return output

def get_streak_data(df,trendString,maxRuns,trend,dataLevel):
    output = {}
    if trend == "positive":
        streak_start_index = trendString.index("P"*maxRuns["P"])
        streak_end_index = streak_start_index + maxRuns["P"]-1
    else:
        streak_start_index = trendString.index("P"*maxRuns["P"])
        streak_end_index = streak_start_index + maxRuns["P"]-1

    end_streak_value = round(df["value"][streak_end_index],2)
    start_streak_value = round(df["value"][streak_start_index],2)
    if dataLevel == "day":
        streak_end_month = str(df.iloc[streak_end_index]["key"])
        streak_start_month = str(df.iloc[streak_start_index]["key"])
    else:
        streak_end_month = df.iloc[streak_end_index]["year_month"]
        streak_start_month = df.iloc[streak_start_index]["year_month"]
    change = end_streak_value-start_streak_value
    streak_range = str(start_streak_value)+" to "+str(end_streak_value)

    output = ["Longest Streak",streak_start_month+" to "+streak_end_month,change,streak_range]
    if trend == "positive":
        output = {"increase":"Longest Streak","period":streak_start_month+" to "+streak_end_month,"increased_by":change,"range":streak_range}
    else:
        output = {"decrease":"Longest Streak","period":streak_start_month+" to "+streak_end_month,"decreased_by":change,"range":streak_range}
    return output

def calculate_dimension_contribution(level_cont):
    data_dict = {}
    dimension_contribution = []
    for k,v in level_cont["summary"].items():
        max_level = max(v,key=lambda x: v[x]["growth"])
        while v[max_level]["contribution"] < 5:
            del(v[max_level])
            if len(v.keys()) > 1:
                max_level = max(v,key=lambda x: v[x]["growth"])
            else:
                max_level = None
                break
        if max_level != None:
            dimension_contribution.append((k,max_level,v[max_level]["growth"],v[max_level]["contribution"]))

    ordered_dim_contribution = sorted(dimension_contribution,key=lambda x:x[2],reverse=True)
    data_dict["HighestSigDimension"] = ordered_dim_contribution[0][0]
    data_dict["SecondHighestSigDimension"] = ordered_dim_contribution[1][0]
    k1 = level_cont["summary"][data_dict["HighestSigDimension"]]
    sorted_k1 = sorted(k1.items(),key = lambda x: x[1]["growth"],reverse=True)
    k2 = level_cont["summary"][data_dict["SecondHighestSigDimension"]]
    sorted_k2 = sorted(k1.items(),key = lambda x: x[1]["growth"],reverse=True)
    data_dict["HighestSigDimensionL1"] = [sorted_k1[0][0],sorted_k1[0][1]["growth"]]
    data_dict["HighestSigDimensionL2"] = [sorted_k1[1][0],sorted_k1[1][1]["growth"]]
    data_dict["SecondHighestSigDimensionL1"] = [sorted_k2[0][0],sorted_k2[0][1]["growth"]]
    data_dict["SecondHighestSigDimensionL2"] = [sorted_k2[1][0],sorted_k2[1][1]["growth"]]

    for k,v in level_cont["summary"].items():
        min_level = max(v,key=lambda x: v[x]["growth"])
        while v[min_level]["contribution"] < 5:
            del(v[min_level])
            if len(v.keys()) > 1:
                min_level = max(v,key=lambda x: v[x]["growth"])
            else:
                min_level = None
                break
        if min_level != None:
            dimension_contribution.append((k,min_level,v[min_level]["growth"],v[min_level]["contribution"]))

    ordered_dim_contribution = sorted(dimension_contribution,key=lambda x:x[2])
    data_dict["negativeHighestSigDimension"] = ordered_dim_contribution[0][0]
    data_dict["negativeSecondHighestSigDimension"] = ordered_dim_contribution[1][0]
    k1 = level_cont["summary"][data_dict["negativeHighestSigDimension"]]
    sorted_k1 = sorted(k1.items(),key = lambda x: x[1]["growth"])
    k2 = level_cont["summary"][data_dict["negativeSecondHighestSigDimension"]]
    sorted_k2 = sorted(k1.items(),key = lambda x: x[1]["growth"])
    data_dict["negativeHighestSigDimensionL1"] = [sorted_k1[0][0],sorted_k1[0][1]["growth"]]
    data_dict["negativeHighestSigDimensionL2"] = [sorted_k1[1][0],sorted_k1[1][1]["growth"]]
    data_dict["negativeSecondHighestSigDimensionL1"] = [sorted_k2[0][0],sorted_k2[0][1]["growth"]]
    data_dict["negativeSecondHighestSigDimensionL2"] = [sorted_k2[1][0],sorted_k2[1][1]["growth"]]
    return data_dict

def calculate_level_contribution(df,columns,index_col,datetime_pattern,value_col,max_time):
    out = {}
    # columns = ['EDUCATION','MARRIAGE','AGE_CATEGORY','BILL_AMOUNT_DECEMBER','BILL_AMOUNT_NOVEMBER']
    for column_name in columns:
        data_dict = {"overall_avg":None,"excluding_avg":None,"min_avg":None,"max_avg":None,"diff":None,"contribution":None,"growth":None}
        column_levels = df[column_name].unique()
        out[column_name] = dict(zip(column_levels,[data_dict]*len(column_levels)))
        k = df.pivot_table(index = index_col, columns = column_name, values = value_col, aggfunc="sum")
        k["total"] = k.sum(axis=1)
        k["rank"] = map(lambda x: datetime.strptime(x,datetime_pattern),list(k.index))
        k = k.sort_values(by="rank", ascending=True)
        max_index = list(k.index).index(max_time)
        print k.head()
        print max_index,columns,column_levels
        for level in column_levels:
            data_dict = {"overall_avg":None,"excluding_avg":None,"min_avg":None,"max_avg":None,"diff":None,"contribution":None,"growth":None}
            data_dict["contribution"] = round(float(np.sum(k[level]))*100/np.sum(k["total"]),2)
            data = list(k[level])
            data_dict["growth"] = round((data[-1]-data[0])*100/data[0],2)
            k[level] = (k[level]/k["total"])*100
            data = list(k[level])
            data_dict["overall_avg"] = round(np.mean(data),2)
            data_dict["max_avg"] = round(np.max(data),2)
            data_dict["min_avg"] = round(np.min(data),2)
            del(data[max_index])
            data_dict["excluding_avg"] = round(np.mean(data),2)
            data_dict["diff"] = round(data_dict["max_avg"] - data_dict["excluding_avg"],2)
            out[column_name][level] = data_dict
    return {"summary":out,"pivot":k}

def get_level_cont_dict(level_cont):
    dk = level_cont["summary"]
    output = []
    for k,v in dk.items():
        level_list = v.keys()
        max_level = max(v,key=lambda x: v[x]["diff"])
        t_dict = {}
        for k1,v1 in dk[k][max_level].items():
            t_dict[k1] = v1
            t_dict.update({"level":max_level})
        output.append(t_dict)
    out_dict = dict(zip(dk.keys(),output))
    out_data = {}
    out_data["highest_contributing_variable"] = max(out_dict,key=lambda x:out_dict[x]["diff"])
    out_data["highest_contributing_level"] = out_dict[out_data["highest_contributing_variable"]]["level"]
    out_data["highest_contributing_level_increase"] = out_dict[out_data["highest_contributing_variable"]]["diff"]
    out_data["highest_contributing_level_range"] = str(out_dict[out_data["highest_contributing_variable"]]["max_avg"])+" vis-a-vis "+str(out_dict[out_data["highest_contributing_variable"]]["excluding_avg"])
    output = []
    for k,v in dk.items():
        level_list = v.keys()
        max_level = min(v,key=lambda x: v[x]["diff"])
        t_dict = {}
        for k1,v1 in dk[k][max_level].items():
            t_dict[k1] = v1
            t_dict.update({"level":max_level})
        output.append(t_dict)
    out_dict = dict(zip(dk.keys(),output))
    out_data["lowest_contributing_variable"] = min(out_dict,key=lambda x:out_dict[x]["diff"])
    out_data["lowest_contributing_level"] = out_dict[out_data["lowest_contributing_variable"]]["level"]
    out_data["lowest_contributing_level_decrease"] = out_dict[out_data["lowest_contributing_variable"]]["diff"]
    out_data["lowest_contributing_level_range"] = str(out_dict[out_data["lowest_contributing_variable"]]["min_avg"])+" vis-a-vis "+str(out_dict[out_data["lowest_contributing_variable"]]["excluding_avg"])

    return out_data

def calculate_bucket_data(level_cont):
    df = pd.DataFrame(level_cont["pivot"]["total"])
    min_streak = 2
    max_streak = 9
    if df.shape[0]*0.3 < 9:
        max_streak = int(math.floor(df.shape[0]*0.3))
        if max_streak <= 2:
            max_streak = 2
    streak_range = range(min_streak,max_streak+1)
    max_dict = {}
    for val in streak_range:
        df[str(val)] = df["total"].rolling(val).sum()/val
        temp_dict = {}
        temp_dict["id_max"] = df[str(val)].idxmax()
        temp_dict["max_val"] = round(df.loc[temp_dict["id_max"],str(val)],2)
        start_id = list(df.index).index(temp_dict["id_max"])-val
        temp_dict["start_streak"] = list(df.index)[start_id]
        max_dict[str(val)] = temp_dict

    return max_dict

def get_bucket_data_dict(bucket_dict,level_cont):
#     max_bucket = max(max_dict,key = lambda x: max_dict[x]["max_val"])
    zip_list = []
    for k,v in bucket_dict.items():
        zip_list.append([int(k),v["max_val"]])
    zip_list = sorted(zip_list, key=lambda x:x[1],reverse=True)
    zip_list = sorted(zip_list, key=lambda x:x[0],reverse=False)
    out = {}
    out["bucket_length"] = zip_list[0][0]
    out["bucket_contribution"] = zip_list[0][1]
    out["bucket_duration"] = str(bucket_dict[str(zip_list[0][0])]["start_streak"])+" to "+str(bucket_dict[str(zip_list[0][0])]["id_max"])
    ratio = 45
    if ratio < 20:
        out["ratio_string"] = ""
    elif ratio > 20 and ratio <=30:
        out["ratio_string"] = "one fourth"
    elif ratio > 30 and ratio <=40:
        out["ratio_string"] = "one third"
    elif ratio > 40 and ratio <=55:
        out["ratio_string"] = "half"
    elif ratio > 55 and ratio <=70:
        out["ratio_string"] = "two third"
    elif ratio >70 and ratio <=80:
        out["ratio_string"] = "three fourth"
    else:
        out["ratio_string"] = str(ratio)

    return out

def get_level_cont_dict(level_cont):
    dk = level_cont["summary"]
    output = []
    for k,v in dk.items():
        level_list = v.keys()
        max_level = max(v,key=lambda x: v[x]["diff"])
        t_dict = {}
        for k1,v1 in dk[k][max_level].items():
            t_dict[k1] = v1
            t_dict.update({"level":max_level})
        output.append(t_dict)
    out_dict = dict(zip(dk.keys(),output))
    out_data = {}
    out_data["highest_contributing_variable"] = max(out_dict,key=lambda x:out_dict[x]["diff"])
    out_data["highest_contributing_level"] = out_dict[out_data["highest_contributing_variable"]]["level"]
    out_data["highest_contributing_level_increase"] = out_dict[out_data["highest_contributing_variable"]]["diff"]
    out_data["highest_contributing_level_range"] = str(out_dict[out_data["highest_contributing_variable"]]["max_avg"])+" vis-a-vis "+str(out_dict[out_data["highest_contributing_variable"]]["excluding_avg"])
    output = []
