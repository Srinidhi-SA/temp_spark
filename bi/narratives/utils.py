
"""
Utility functions to be used by various narrative objects
"""
import re

def round_number(num, digits, as_string=True):
    millions = 0
    thousands = 0
    if(num//1000000 > 0) and (as_string):
        num = num/1000000.0
        millions =1
        digits = 2
    elif(num//1000 > 0) and (as_string):
        num = num/1000.0
        thousands = 1
        digits = 2
    result = float(format(num, '0.%df' %(digits,)))
    if as_string:
        result = str(result)
        decs = result[result.find('.'):]
        result = result[:result.find('.')]
        temp = len(str(result))
        if temp>3:
            for insertions in range(len(result)-3,0,-3):
                result = result[:insertions]+','+result[insertions:]
        if millions ==1:
            return result+decs+' Million'
        if thousands == 1:
            return result+decs+'K'
        return result+decs
    return result

def clean_narratives(output):
    output = re.sub('\n',' ',output)
    output = re.sub(' +',' ',output)
    output = re.sub(' ,',',',output)
    output = re.sub(' \.','.',output)
    output = re.sub('\( ','(',output)
    return output

def clean_result_text(text):
    return str.replace("\n", "")

def pluraize(text):
    return pattern.en.pluralize(text)

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
