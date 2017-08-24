import json
import operator
import os

from bi.narratives import utils as NarrativesUtils
from bi.common import NormalCard,SummaryCard,NarrativesTree,HtmlData,C3ChartData
from bi.common import ScatterChartData,NormalChartData,ChartJson
class DimensionColumnNarrative:
    MAX_FRACTION_DIGITS = 2

    def __init__(self, column_name, df_helper, df_context, freq_dimension_stats,result_setter,story_narrative):
        self._story_narrative = story_narrative
        self._result_setter = result_setter
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
        self._blockSplitter = "|~NEWBLOCK~|"
        self._dimensionSummaryNode = NarrativesTree()
        self._dimensionSummaryNode.set_name("Overview")
        self._headNode = NarrativesTree()
        self._headNode.set_name("Overview")
        self._generate_narratives()
        self._story_narrative.add_a_node(self._dimensionSummaryNode)

        self._result_setter.set_head_node(self._headNode)
        self._result_setter.set_distribution_node(self._dimensionSummaryNode)

    def _generate_narratives(self):
        if self.appid != None:
            if self.appid == "1":
                # self._generate_title()
                # self._generate_summary()
                # self.analysis = self._generate_analysis()
                self._generate_title()
                self._generate_summary()
                self._generate_analysis()
            elif self.appid == "2":
                # self._generate_title()
                # self._generate_summary()
                # self.analysis = self._generate_analysis2()
                self._generate_title()
                self._generate_summary()
                self._generate_analysis()
        else:
            self._generate_title()
            self._generate_summary()
            self._generate_analysis()

    def _generate_title(self):
        self.header = '%s Performance Report' % (self._capitalized_column_name,)
        # self._dimensionSummaryNode.set_name(self.header)

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
                    "blockSplitter" : self._blockSplitter
        }
        output = NarrativesUtils.get_template_output(self._base_dir,\
                                        'dimension_report_summary.temp',data_dict)
        summary = NarrativesUtils.block_splitter(output,self._blockSplitter)
        dimensionSummaryCard = SummaryCard(name=self.header,slug=None,cardData = None)
        dimensionSummaryCard.set_no_of_measures(data_dict["n_m"])
        dimensionSummaryCard.set_no_of_dimensions(data_dict["n_d"])
        dimensionSummaryCard.set_no_of_time_dimensions(data_dict["n_td"])

        dimensionSummaryCard.set_summary_html(summary)
        dimensionSummaryCard.set_card_name("overall summary card")
        # dimensionSummaryCard.set_quote_html
        self._story_narrative.add_a_card(dimensionSummaryCard)
        self._headNode.add_a_card(dimensionSummaryCard)

    def _generate_analysis(self):
        lines = []
        freq_dict = self._dimension_col_freq_dict
        json_freq_dict = json.dumps(freq_dict)
        freq_dict = json.loads(freq_dict)
        colname = self._colname
        freq_data = []
        for k,v in freq_dict[colname][colname].items():
            freq_data.append({"key":v,"value":freq_dict[colname]["count"][k]})
        freq_data = sorted(freq_data,key=lambda x:x["value"],reverse=True)
        data_dict = {"colname":self._colname}
        data_dict["plural_colname"] = NarrativesUtils.pluralize(data_dict["colname"])
        count = freq_dict[colname]['count']
        max_key = max(count,key=count.get)
        min_key = min(count, key=count.get)
        data_dict["blockSplitter"] = self._blockSplitter
        data_dict["max"] = {"key":freq_dict[colname][colname][max_key],"val":count[max_key]}
        data_dict["min"] = {"key":freq_dict[colname][colname][min_key],"val":count[min_key]}
        data_dict["keys"] = freq_dict[colname][colname].values()
        data_dict["avg"] = round(sum(count.values())/float(len(count.values())),2)
        data_dict["above_avg"] = [freq_dict[colname][colname][key] for key in count.keys() if count[key] > data_dict["avg"]]
        data_dict["per_bigger_avg"] = round(data_dict["max"]["val"]/float(data_dict["avg"]),4)
        data_dict["per_bigger_low"] = round(data_dict["max"]["val"]/float(data_dict["min"]["val"]),4)
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
            data_dict["percent_contr"] = round(temp_sum*100.0/float(sum(count.values())),2)
            data_dict["kv_75"] = len(kv_75)

            data_dict["kv_75_cat"] = [k for k,v in kv_75]

        largest_text = " %s is the largest with %s observations" % (data_dict["max"]["key"],NarrativesUtils.round_number(data_dict["max"]["val"]))
        smallest_text = " %s is the smallest with %s observations" % (data_dict["min"]["key"],NarrativesUtils.round_number(data_dict["min"]["val"]))
        largest_per = round(data_dict["max"]["val"]*100.0/float(sum(count.values())),2)
        data_dict['largest_per']=largest_per
        smallest_per = round(data_dict["min"]["val"]*100.0/float(sum(count.values())),2)
        self.count = {"largest" :[largest_text,str(round(largest_per,1))+'%'],"smallest" : [smallest_text,str(round(smallest_per,1))+'%']}
        if len(data_dict["keys"]) >=3:
            # self.subheader = "Top %d %s account for more than three quarters (%d percent) of observations." % (data_dict["kv_75"],data_dict["plural_colname"],data_dict["percent_contr"])
            self.subheader = 'Distribution of '+self._capitalized_column_name
        else:
            self.subheader = 'Distribution of '+self._capitalized_column_name
        output1 =  NarrativesUtils.get_template_output(self._base_dir,\
                                                'dimension_distribution1.temp',data_dict)
        output1 = NarrativesUtils.block_splitter(output1,self._blockSplitter)
        output2 = NarrativesUtils.get_template_output(self._base_dir,\
                                                'dimension_distribution2.temp',data_dict)
        output2 = NarrativesUtils.block_splitter(output2,self._blockSplitter)
        chart_data = NormalChartData(data=freq_data)
        chart_json = ChartJson()
        chart_json.set_data(chart_data.get_data())
        chart_json.set_chart_type("bar")
        chart_json.set_axes({"x":"key","y":"value"})
        lines += output1
        lines += [C3ChartData(data=chart_json)]
        lines += output2
        bubble_data = "<div class='col-md-6 col-xs-12'><h2 class='text-center'><span>{}%</span><br /><small>{}</small></h2></div><div class='col-md-6 col-xs-12'><h2 class='text-center'><span>{}%</span><br /><small>{}</small></h2></div>".format(largest_per,largest_text,smallest_per,smallest_text)
        lines.append(HtmlData(data=bubble_data))
        # print lines
        dimensionCard1 = NormalCard(name=self.subheader,slug=None,cardData = lines)
        self._dimensionSummaryNode.add_a_card(dimensionCard1)
        self._result_setter.set_score_freq_card(dimensionCard1)
        return lines

    def _generate_analysis2(self):
        lines = []
        freq_dict = self._dimension_col_freq_dict
        json_freq_dict = json.dumps(freq_dict)
        freq_dict = json.loads(freq_dict)
        colname = self._colname
        data_dict = {"colname":self._colname}
        data_dict["plural_colname"] = NarrativesUtils.pluralize(data_dict["colname"])
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
        if len(data_dict["keys"]) >= 2:
            percent_75 = sum(count.values())*0.75
            kv = sorted(count.items(),key = operator.itemgetter(1),reverse=True)
            kv_75 = [(k,v) for k,v in kv if v <= percent_75]
            kv_75 = []
            temp_sum = 0
            for k,v in kv[:-1]:
                temp_sum = temp_sum + v
                kv_75.append((freq_dict[colname][colname][k],v))
                if temp_sum >= percent_75:
                    break
            data_dict["percent_contr"] = round(temp_sum*100/float(sum(count.values())),2)
            data_dict["kv_75"] = len(kv_75)

            data_dict["kv_75_cat"] = [k for k,v in kv_75]

        largest_text = " %s is the largest with %s observations" % (data_dict["max"]["key"],str(NarrativesUtils.round_number(data_dict["max"]["val"])))
        smallest_text = " %s is the smallest with %s observations" % (data_dict["min"]["key"],str(NarrativesUtils.round_number(data_dict["min"]["val"])))
        largest_per = NarrativesUtils.round_number(data_dict["max"]["val"]/float(sum(count.values())),2)*100
        smallest_per = NarrativesUtils.round_number(data_dict["min"]["val"]/float(sum(count.values())),2)*100
        data_dict['largest_per']=largest_per
        self.count = {"largest" :[largest_text,str(round(largest_per,0))+'%'],"smallest" : [smallest_text,str(round(smallest_per,0))+'%']}
        self.subheader = "Snapshot of "+data_dict["colname"]
        output1 =  NarrativesUtils.get_template_output(self._base_dir,\
                                                'dimension_distribution1.temp',data_dict)
        output2 = NarrativesUtils.get_template_output(self._base_dir,\
                                                'dimension_distribution2.temp',data_dict)
        lines.append(output1)
        lines.append(output2)
        return lines
