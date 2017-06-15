import os
import operator
import jinja2
import re
import pattern.en
import numpy as np
import json
from bi.common.utils import accepts

from bi.narratives import utils as NarrativesUtils
from bi.common.results import FreqDimensionResult

class DimensionColumnNarrative:
    MAX_FRACTION_DIGITS = 2

    def __init__(self, column_name, df_helper, df_context, freq_dimension_stats):
        self._column_name = column_name.lower()
        self._colname = column_name
        self._capitalized_column_name = "%s%s" % (column_name[0].upper(), column_name[1:])
        self._dimension_col_freq_dict = freq_dimension_stats.get_frequency_dict()
        self.header = None
        self.subheader = None
        self.count = {}
        self.summary = []
        self.analysis = []
        self.frequency_dict = json.loads(self._dimension_col_freq_dict)
        self.appid = df_context.get_app_id()
        # self._base_dir = os.path.dirname(os.path.realpath(__file__))+"/../../templates/dimensions/"
        self._base_dir = os.environ.get('MADVISOR_BI_HOME')+"/templates/dimensions/"
        if self.appid != None:
            if self.appid == "1":
                self._base_dir += "appid1/"
            elif self.appid == "2":
                self._base_dir += "appid2/"
        self._dataframe_context = df_context
        self._dataframe_helper = df_helper

        self._generate_narratives()
        # NarrativesUtils.round_number(num, 2)

    def _generate_narratives(self):
        if self.appid != None:
            if self.appid == "1":
                self._generate_title()
                self._generate_summary()
                self.analysis = self._generate_analysis()
            elif self.appid == "2":
                self._generate_title()
                self._generate_summary()
                self.analysis = self._generate_analysis2()
        else:
            self._generate_title()
            self._generate_summary()
            self.analysis = self._generate_analysis()

    def _generate_title(self):
        self.header = '%s Performance Report' % (self._capitalized_column_name,)

    def _generate_summary(self):
        ignored_columns = self._dataframe_context.get_ignore_column_suggestions()
        if ignored_columns == None:
            ignored_columns = []

        data_dict = {"n_c" : len(self._dataframe_helper.get_columns()),
                    "n_m" : len(self._dataframe_helper.get_numeric_columns()),
                    "n_d" : len(self._dataframe_helper.get_string_columns()),
                    "n_td" : len(self._dataframe_helper.get_timestamp_columns()),
                    "c" : self._column_name,
                    "d" : self._dataframe_helper.get_string_columns(),
                    "m" : self._dataframe_helper.get_numeric_columns(),
                    "td" : self._dataframe_helper.get_timestamp_columns(),
                    "observations" : self._dataframe_helper.get_num_rows(),
                    "ignorecolumns" : ignored_columns,
                    "n_t" : self._dataframe_helper.get_num_columns()+len(ignored_columns),
                    "separator" : "~~"
        }
        templateLoader = jinja2.FileSystemLoader( searchpath=self._base_dir)
        templateEnv = jinja2.Environment( loader=templateLoader )
        template = templateEnv.get_template('dimension_report_summary.temp')
        output = template.render(data_dict).replace("\n", "")
        output = re.sub(' +',' ',output)
        output = re.sub(' ,',',',output)
        output = re.sub(' \.','.',output)
        self.summary = output.split(data_dict["separator"])
        self.vartype = {"Dimensions":data_dict["n_d"],"Measures":data_dict["n_m"],"Time Dimension":data_dict["n_td"]}

    def _generate_analysis(self):
        lines = []
        freq_dict = self._dimension_col_freq_dict
        json_freq_dict = json.dumps(freq_dict)
        freq_dict = json.loads(freq_dict)
        colname = self._colname
        data_dict = {"colname":self._colname}
        data_dict["plural_colname"] = pattern.en.pluralize(data_dict["colname"])
        count = freq_dict[colname]['count']

        max_key = max(count,key=count.get)
        min_key = min(count, key=count.get)
        data_dict["max"] = {"key":freq_dict[colname][colname][max_key],"val":count[max_key]}
        data_dict["min"] = {"key":freq_dict[colname][colname][min_key],"val":count[min_key]}
        data_dict["keys"] = freq_dict[colname][colname].values()
        data_dict["avg"] = round(sum(count.values())/float(len(count.values())),2)
        data_dict["above_avg"] = [freq_dict[colname][colname][key] for key in count.keys() if count[key] > data_dict["avg"]]
        data_dict["per_bigger_avg"] = round(data_dict["max"]["val"]/float(data_dict["avg"]),2)
        data_dict["per_bigger_low"] = round(data_dict["max"]["val"]/float(data_dict["min"]["val"]),2)
        uniq_val = list(set(count.values()))
        data_dict["n_uniq"] = len(uniq_val)
        if len(uniq_val) == 1:
            data_dict["count"] = uniq_val[0]
        if len(data_dict["keys"]) >= 3:
            #percent_75 = np.percentile(count.values(),75)
            #kv=[(freq_dict[colname][colname][key],count[key]) for key in count.keys()]
            percent_75 = sum(count.values())*0.75
            kv = sorted(count.items(),key = operator.itemgetter(1),reverse=True)
            kv_75 = [(k,v) for k,v in kv if v <= percent_75]
            kv_75 = []
            temp_sum = 0
            for k,v in kv:
                temp_sum = temp_sum + v
                kv_75.append((freq_dict[colname][colname][k],v))
                if temp_sum >= percent_75:
                    break
            data_dict["percent_contr"] = round(temp_sum*100/float(sum(count.values())),2)
            data_dict["kv_75"] = len(kv_75)

            data_dict["kv_75_cat"] = [k for k,v in kv_75]

        largest_text = " %s is the largest with %d observations" % (data_dict["max"]["key"],data_dict["max"]["val"])
        smallest_text = " %s is the smallest with %d observations" % (data_dict["min"]["key"],data_dict["min"]["val"])
        largest_per = round(data_dict["max"]["val"]/float(sum(count.values())),2)*100
        smallest_per = round(data_dict["min"]["val"]/float(sum(count.values())),2)*100
        self.count = {"largest" :[largest_text,str(round(largest_per,0))+'%'],"smallest" : [smallest_text,str(round(smallest_per,0))+'%']}
        if len(data_dict["keys"]) >=3:
            self.subheader = "Top %d %s account for more than three quarters (%d percent) of observations." % (data_dict["kv_75"],data_dict["plural_colname"],data_dict["percent_contr"])
        else:
            self.subheader = ""
        templateLoader = jinja2.FileSystemLoader( searchpath=self._base_dir)
        templateEnv = jinja2.Environment( loader=templateLoader )

        template1 = templateEnv.get_template('dimension_distribution1.temp')
        output1 = template1.render(data_dict).replace("\n", "")
        output1 = re.sub(' +',' ',output1)
        output1 = re.sub(' ,',',',output1)
        output1 = re.sub(' \.','.',output1)

        template2 = templateEnv.get_template('dimension_distribution2.temp')
        output2 = template2.render(data_dict).replace("\n", "")
        output2 = re.sub(' +',' ',output2)
        output2 = re.sub(' ,',',',output2)
        output2 = re.sub(' \.','.',output2)
        lines.append(output1)
        lines.append(output2)
        return lines

    def _generate_analysis2(self):
        lines = []
        freq_dict = self._dimension_col_freq_dict
        json_freq_dict = json.dumps(freq_dict)
        freq_dict = json.loads(freq_dict)
        colname = self._colname
        data_dict = {"colname":self._colname}
        data_dict["plural_colname"] = pattern.en.pluralize(data_dict["colname"])
        count = freq_dict[colname]['count']

        max_key = max(count,key=count.get)
        min_key = min(count, key=count.get)
        data_dict["max"] = {"key":freq_dict[colname][colname][max_key],"val":count[max_key]}
        data_dict["min"] = {"key":freq_dict[colname][colname][min_key],"val":count[min_key]}
        data_dict["keys"] = freq_dict[colname][colname].values()
        data_dict["avg"] = round(sum(count.values())/float(len(count.values())),2)
        data_dict["above_avg"] = [freq_dict[colname][colname][key] for key in count.keys() if count[key] > data_dict["avg"]]
        data_dict["per_bigger_avg"] = round(data_dict["max"]["val"]/float(data_dict["avg"]),2)
        data_dict["per_bigger_low"] = round(data_dict["max"]["val"]/float(data_dict["min"]["val"]),2)
        uniq_val = list(set(count.values()))
        data_dict["n_uniq"] = len(uniq_val)
        if len(uniq_val) == 1:
            data_dict["count"] = uniq_val[0]
        if len(data_dict["keys"]) >= 3:
            #percent_75 = np.percentile(count.values(),75)
            #kv=[(freq_dict[colname][colname][key],count[key]) for key in count.keys()]
            percent_75 = sum(count.values())*0.75
            kv = sorted(count.items(),key = operator.itemgetter(1),reverse=True)
            kv_75 = [(k,v) for k,v in kv if v <= percent_75]
            kv_75 = []
            temp_sum = 0
            for k,v in kv:
                temp_sum = temp_sum + v
                kv_75.append((freq_dict[colname][colname][k],v))
                if temp_sum >= percent_75:
                    break
            data_dict["percent_contr"] = round(temp_sum*100/float(sum(count.values())),2)
            data_dict["kv_75"] = len(kv_75)

            data_dict["kv_75_cat"] = [k for k,v in kv_75]

        largest_text = " %s is the largest with %d observations" % (data_dict["max"]["key"],data_dict["max"]["val"])
        smallest_text = " %s is the smallest with %d observations" % (data_dict["min"]["key"],data_dict["min"]["val"])
        largest_per = round(data_dict["max"]["val"]/float(sum(count.values())),2)*100
        smallest_per = round(data_dict["min"]["val"]/float(sum(count.values())),2)*100
        self.count = {"largest" :[largest_text,str(round(largest_per,0))+'%'],"smallest" : [smallest_text,str(round(smallest_per,0))+'%']}
        self.subheader = "Snapshot of "+data_dict["colname"]
        templateLoader = jinja2.FileSystemLoader( searchpath=self._base_dir)
        templateEnv = jinja2.Environment( loader=templateLoader )

        template1 = templateEnv.get_template('dimension_distribution1.temp')
        output1 = template1.render(data_dict).replace("\n", "")
        output1 = re.sub(' +',' ',output1)
        output1 = re.sub(' ,',',',output1)
        output1 = re.sub(' \.','.',output1)

        template2 = templateEnv.get_template('dimension_distribution2.temp')
        output2 = template2.render(data_dict).replace("\n", "")
        output2 = re.sub(' +',' ',output2)
        output2 = re.sub(' ,',',',output2)
        output2 = re.sub(' \.','.',output2)
        lines.append(output1)
        lines.append(output2)
        return lines
