import os
import random
import json
import itertools
import humanize
from bi.common.dataframe import DataFrameHelper
from bi.common.context import ContextSetter
from bi.common.results import DecisionTreeResult
from bi.common.utils import accepts
from bi.narratives import utils as NarrativesUtils
from bi.common import utils as CommonUtils
from bi.common import NarrativesTree
from bi.common import NormalCard,SummaryCard,NarrativesTree,HtmlData,C3ChartData,TableData,TreeData
from bi.common import ScatterChartData,NormalChartData,ChartJson
from bi.common import ResultSetter




class DecisionTreeNarrative:
    MAX_FRACTION_DIGITS = 2

    def _get_new_table(self):
        self._decisionTreeCard1Table = [["PREDICTION","RULES","PERCENTAGE"]]
        for keys in self._table.keys():
            self._new_table[keys]={}
            self._new_table[keys]['rules'] = self._table[keys]
            self._new_table[keys]['probability'] = [round(i,2) for i in self.success_percent[keys]]
            keyTable = [keys,self._new_table[keys]['rules'],self._new_table[keys]['probability']]
            self._decisionTreeCard1Table.append(keyTable)

    # @accepts(object, (str, basestring), DecisionTreeResult,DataFrameHelper,ContextSetter,ResultSetter,NarrativesTree,basestring,dict)
    def __init__(self, column_name, decision_tree_rules,df_helper,df_context,meta_parser,result_setter,story_narrative=None,analysisName=None,scriptWeight=None):
        self._story_narrative = story_narrative
        self._metaParser = meta_parser
        self._dataframe_context = df_context
        self._ignoreMsg = self._dataframe_context.get_message_ignore()
        self._result_setter = result_setter
        self._blockSplitter = self._dataframe_context.get_block_splitter()
        self._column_name = column_name.lower()
        self._colname = column_name

        self._capitalized_column_name = "%s%s" % (column_name[0].upper(), column_name[1:])
        self._decision_rules_dict = decision_tree_rules.get_decision_rules()
        self._decision_tree_json = CommonUtils.as_dict(decision_tree_rules)
        self._decision_tree_raw = self._decision_rules_dict
        # self._decision_tree_raw = {"tree":{"children":None}}
        # self._decision_tree_raw['tree']["children"] = self._decision_tree_json['tree']["children"]
        self._table = decision_tree_rules.get_table()
        self._new_table={}
        self.succesful_predictions=decision_tree_rules.get_success()
        self.total_predictions=decision_tree_rules.get_total()
        self.success_percent= decision_tree_rules.get_success_percent()
        self._important_vars = decision_tree_rules.get_significant_vars()
        self._target_distribution = decision_tree_rules.get_target_contributions()
        self._get_new_table()
        self._df_helper = df_helper
        self.subheader = None
        self.dropdownComment = None
        self.dropdownValues = None
        self._base_dir = "/decisiontree/"


        self._completionStatus = self._dataframe_context.get_completion_status()
        if analysisName == None:
            self._analysisName = self._dataframe_context.get_analysis_name()
        else:
            self._analysisName = analysisName
        self._messageURL = self._dataframe_context.get_message_url()
        if scriptWeight == None:
            self._scriptWeightDict = self._dataframe_context.get_dimension_analysis_weight()
        else:
            self._scriptWeightDict = scriptWeight
        self._scriptStages = {
            "dtreeNarrativeStart":{
                "summary":"Started the Decision Tree Narratives",
                "weight":0
                },
            "dtreeNarrativeEnd":{
                "summary":"Narratives for Decision Tree Finished",
                "weight":10
                },
            }
        self._completionStatus += self._scriptWeightDict[self._analysisName]["narratives"]*self._scriptStages["dtreeNarrativeStart"]["weight"]/10
        progressMessage = CommonUtils.create_progress_message_object(self._analysisName,\
                                    "dtreeNarrativeStart",\
                                    "info",\
                                    self._scriptStages["dtreeNarrativeStart"]["summary"],\
                                    self._completionStatus,\
                                    self._completionStatus)
        CommonUtils.save_progress_message(self._messageURL,progressMessage,ignore=self._ignoreMsg)
        self._dataframe_context.update_completion_status(self._completionStatus)

        self._decisionTreeNode = NarrativesTree()
        self._decisionTreeNode.set_name("Prediction")
        self._generate_narratives()
        # self._story_narrative.add_a_node(self._decisionTreeNode)
        self._result_setter.set_decision_tree_node(self._decisionTreeNode)
        self._result_setter.set_score_dtree_cards(json.loads(CommonUtils.convert_python_object_to_json(self._decisionTreeNode.get_all_cards())))

        self._completionStatus += self._scriptWeightDict[self._analysisName]["narratives"]*self._scriptStages["dtreeNarrativeEnd"]["weight"]/10
        progressMessage = CommonUtils.create_progress_message_object(self._analysisName,\
                                    "dtreeNarrativeEnd",\
                                    "info",\
                                    self._scriptStages["dtreeNarrativeEnd"]["summary"],\
                                    self._completionStatus,\
                                    self._completionStatus)
        CommonUtils.save_progress_message(self._messageURL,progressMessage,ignore=self._ignoreMsg)
        self._dataframe_context.update_completion_status(self._completionStatus)


    def _generate_narratives(self):
        self._generate_summary()

    # def _generate_summary(self):
    #     rules = self._decision_rules_dict
    #     colname = self._colname
    #     data_dict = {"dimension_name":self._colname}
    #     data_dict["plural_colname"] = NarrativesUtils.pluralize(data_dict["dimension_name"])
    #     data_dict["significant_vars"] = []
    #     rules_dict = self._table
    #     self.condensedTable={}
    #     for target in rules_dict.keys():
    #         self.condensedTable[target]=[]
    #         total = self.total_predictions[target]
    #         success = self.succesful_predictions[target]
    #         success_percent = self.success_percent[target]
    #         for idx,rule in enumerate(rules_dict[target]):
    #             rules1 = self._generate_rules(target,rule, total[idx], success[idx], success_percent[idx])
    #             self.condensedTable[target].append(rules1)
    #     self.dropdownValues = rules_dict.keys()
    #     data_dict["blockSplitter"] = self._blockSplitter
    #     data_dict['rules'] = self.condensedTable
    #     data_dict['success'] = self.success_percent
    #     data_dict['significant_vars'] = list(set(itertools.chain.from_iterable(self._important_vars.values())))
    #     data_dict['significant_vars'] = self._important_vars
    #     # print '*'*16
    #     # print data_dict['rules']
    #     # print self._new_table
    #     self.card2_data = NarrativesUtils.paragraph_splitter(NarrativesUtils.get_template_output(self._base_dir,\
    #                                                 'decision_tree_card2.html',data_dict))
    #     self.card2_chart = self._target_distribution
    #
    #     self.dropdownComment = NarrativesUtils.get_template_output(self._base_dir,\
    #                                                 'decision_rule_summary.html',data_dict)
    #     main_card = NormalCard()
    #     main_card_data = []
    #     main_card_narrative = NarrativesUtils.block_splitter(self.dropdownComment,self._blockSplitter)
    #     main_card_data += main_card_narrative
    #     main_card_data.append(TreeData(data=self._decision_tree_raw))
    #     main_card_table = TableData()
    #     main_card_table.set_table_data(self._decisionTreeCard1Table)
    #     main_card_table.set_table_type("decisionTreeTable")
    #     main_card_data.append(main_card_table)
    #     main_card.set_card_data(main_card_data)
    #     main_card.set_card_name("Predicting Key Drivers of {}".format(self._colname))
    #     card2 = NormalCard()
    #     card2Data = NarrativesUtils.block_splitter(NarrativesUtils.get_template_output(self._base_dir,\
    #                                                 'decision_tree_card2.html',data_dict),self._blockSplitter)
    #     card2ChartData = []
    #     for k,v in self._target_distribution.items():
    #         card2ChartData.append({"key":k,"value":v})
    #     card2ChartData = NormalChartData(data=card2ChartData)
    #     card2ChartJson = ChartJson()
    #     card2ChartJson.set_data(card2ChartData.get_data())
    #     card2ChartJson.set_chart_type("bar")
    #     card2ChartJson.set_axes({"x":"key","y":"value"})
    #     card2Data.insert(1,C3ChartData(data=card2ChartJson))
    #     card2.set_card_data(card2Data)
    #     card2.set_card_name("Decision Rules for {}".format(self._colname))
    #     self._decisionTreeNode.add_a_card(main_card)
    #     self._decisionTreeNode.add_a_card(card2)
    #     self.subheader = NarrativesUtils.get_template_output(self._base_dir,\
    #                                     'decision_tree_summary.html',data_dict)

    def _generate_summary(self):
        data_dict = {}
        rules_dict = self._table
        data_dict["blockSplitter"] = self._blockSplitter
        data_dict["targetcol"] = self._colname
        groups = rules_dict.keys()
        probabilityCutoff = 75
        probabilityGroups=[{"probability":probabilityCutoff,"count":0,"range":[probabilityCutoff,100]},{"probability":probabilityCutoff-1,"count":0,"range":[0,probabilityCutoff-1]}]
        tableArray = [[
                "Prediction Rule",
                "Probability",
                "Prediction",
                "Freq",
                "group",
                "richRules"
              ]]
        dropdownData = []
        chartDict = {}
        progressMessage = CommonUtils.create_progress_message_object(self._analysisName,"custom","info","Generating Prediction rules",self._completionStatus,self._completionStatus,display=True)
        CommonUtils.save_progress_message(self._messageURL,progressMessage,ignore=False)
        for idx,target in enumerate(rules_dict.keys()):
            if idx == 0:
                if self._dataframe_context.get_story_on_scored_data() != True:
                    dropdownData.append({"displayName":target,"name":target,"selected":True,"id":idx+1})
                else:
                    dropdownData.append({"displayName":"{} : {}".format(self._colname,target),"name":target,"selected":True,"id":idx+1})
            else:
                if self._dataframe_context.get_story_on_scored_data() != True:
                    dropdownData.append({"displayName":target,"name":target,"selected":False,"id":idx+1})
                else:
                    dropdownData.append({"displayName":"{} : {}".format(self._colname,target),"name":target,"selected":False,"id":idx+1})

            rulesArray = rules_dict[target]
            probabilityArray = [round(x,2) for x in self.success_percent[target]]
            groupArray = ["strong" if x>=probabilityCutoff else "mixed" for x in probabilityArray]
            for idx,obj in enumerate(probabilityGroups):
                grpCount = len([x for x in probabilityArray if x >= obj["range"][0] and x <= obj["range"][1]])
                obj["count"] += grpCount
                probabilityGroups[idx] = obj
            predictionArray = [target]*len(rulesArray)
            freqArray = self.total_predictions[target]
            chartDict[target] = sum(freqArray)
            success = self.succesful_predictions[target]
            success_percent = self.success_percent[target]
            richRulesArray = []
            for idx,crudeRule in enumerate(rulesArray):
                richRule = self._generate_rules(target,crudeRule, freqArray[idx], success[idx], success_percent[idx])
                richRulesArray.append(richRule)
            probabilityArray = map(lambda x:humanize.apnumber(x)+"%" if x >=10 else str(int(x))+"%" ,probabilityArray)
            # targetArray = zip(richRulesArray,probabilityArray,predictionArray,freqArray,groupArray)
            targetArray = zip(rulesArray,probabilityArray,predictionArray,freqArray,groupArray,richRulesArray)
            targetArray = [list(x) for x in targetArray]
            tableArray += targetArray

        donutChartMaxLevel = 10
        if len(chartDict) > donutChartMaxLevel:
            chartDict = NarrativesUtils.restructure_donut_chart_data(chartDict,nLevels=donutChartMaxLevel)
        chartData = NormalChartData([chartDict]).get_data()
        chartJson = ChartJson(data=chartData)
        chartJson.set_title(self._colname)
        chartJson.set_chart_type("donut")
        mainCardChart = C3ChartData(data=chartJson)
        mainCardChart.set_width_percent(33)
        # mainCardChart = {"dataType": "c3Chart","widthPercent":33 ,"data": {"data": [chartDict],"title":self._colname,"axes":{},"label_text":{},"legend":{},"yAxisNumberFormat": ".2s","types":None,"axisRotation":False, "chart_type": "donut"}}


        dropdownDict = {
          "dataType": "dropdown",
          "label": "Showing prediction rules for",
          "data": dropdownData
        }

        data_dict["probabilityGroups"] = probabilityGroups
        if self._dataframe_context.get_story_on_scored_data() != True:
            maincardSummary = NarrativesUtils.get_template_output(self._base_dir,\
                                                        'decisiontreesummary.html',data_dict)
        else:
            levelCountDict = self._metaParser.get_unique_level_dict(self._colname)
            total = float(sum([x for x in levelCountDict.values() if x != None]))
            levelCountTuple = [({"name":k,"count":v,"percentage":humanize.apnumber(v*100/total)+"%"}) for k,v in levelCountDict.items() if v != None]
            levelCountTuple = sorted(levelCountTuple,key=lambda x:x["count"],reverse=True)
            data_dict["nlevel"] = len(levelCountDict.keys())
            data_dict["topLevel"] = levelCountTuple[0]
            data_dict["secondLevel"] = levelCountTuple[1]
            maincardSummary = NarrativesUtils.get_template_output(self._base_dir,\
                                                        'decisiontreescore.html',data_dict)
        main_card = NormalCard()
        main_card_data = []
        main_card_narrative = NarrativesUtils.block_splitter(maincardSummary,self._blockSplitter)
        main_card_data += main_card_narrative

        main_card_data.append(mainCardChart)
        main_card_data.append(dropdownDict)

        main_card_table = TableData()
        if self._dataframe_context.get_story_on_scored_data() == True:
            main_card_table.set_table_width(75)
        main_card_table.set_table_data(tableArray)
        main_card_table.set_table_type("popupDecisionTreeTable")
        main_card_data.append(main_card_table)
        uidTable = self._result_setter.get_unique_identifier_table()
        if uidTable != None:
            main_card_data.append(uidTable)
        else:
            main_card_table.set_table_width(100)
        main_card.set_card_data(main_card_data)
        main_card.set_card_name("Predicting Key Drivers of {}".format(self._colname))
        self._decisionTreeNode.add_a_card(main_card)



    def _generate_rules(self,target,rules, total, success, success_percent):
        colname = self._colname
        key_dimensions,key_measures=NarrativesUtils.get_rules_dictionary(rules)
        temp_narrative = ''
        for var in key_measures.keys():
            if key_measures[var].has_key('upper_limit') and key_measures[var].has_key('lower_limit'):
                temp_narrative = temp_narrative + 'the value of ' + var + ' falls between ' + key_measures[var]['lower_limit'] + ' and ' + key_measures[var]['upper_limit']+', '
            elif key_measures[var].has_key('upper_limit'):
                temp_narrative = temp_narrative + 'the value of ' + var + ' is less than or equal to ' + key_measures[var]['upper_limit']+', '
            elif key_measures[var].has_key('lower_limit'):
                temp_narrative = temp_narrative + 'the value of ' + var + ' is greater than ' + key_measures[var]['lower_limit']+', '
        for var in key_dimensions.keys():
            if key_dimensions[var].has_key('in'):
                temp_narrative = temp_narrative + 'the ' + var + ' falls among ' + key_dimensions[var]['in'] + ', '
            elif key_dimensions[var].has_key('not_in'):
                temp_narrative = temp_narrative + 'the ' + var + ' does not fall in ' + key_dimensions[var]['not_in'] + ', '

        if temp_narrative == '':
            temp_narrative = ""
        else:
            r = random.randint(0,99)%5
            if r == 0:
                narrative = 'Nearly <b>' + NarrativesUtils.round_number(success_percent)+ '%' + \
                            '</b> of observations that have ' + temp_narrative + ' result in '+ \
                            target + ' '+ self._column_name + ' values.'
            elif r == 1:
                narrative = 'If ' + temp_narrative +' it is <b>' + NarrativesUtils.round_number(success_percent)+ '%' + \
                            '</b> likely that the observations are ' + target + ' segment.'
            elif r == 2:
                narrative = 'When ' +  temp_narrative + ' the probability of ' + target + \
                            ' is <b>' + NarrativesUtils.round_number(success_percent)+ '%' + '</b>.'
            elif r == 3:
                narrative = 'If ' + temp_narrative +' then there is <b>' + NarrativesUtils.round_number(success_percent)+ '%' + \
                            '</b> probability that the ' + self._column_name + ' observations would be ' + target + ' valued.'
            else:
                narrative = 'There is a very high chance(<b>' + NarrativesUtils.round_number(success_percent)+ '%' + \
                            '</b>) that ' +  self._column_name + ' would be relatively ' + target + ' when, ' + \
                            temp_narrative[:-2] + '.'
            return narrative
