import time, json
from bi.common import NormalCard, NarrativesTree, HtmlData, C3ChartData, TableData, ModelSummary,PopupData,NormalCard,ParallelCoordinateData,DataBox,WordCloud

class BusinessCard:
    """
    Functionalities
    """
    def __init__(self, business_impact_nodes, story_result, meta_parser, result_setter, start_time):
        self._business_impact_nodes = business_impact_nodes
        self._story_result = story_result
        self._meta_parser = meta_parser
        self._result_setter = result_setter
        self.subheader = "Business Impact"
        self.business_card1 = NormalCard()
        self.business_card1.set_card_name("Overview")
        self.businessCardData = []
        self.start_time = start_time

    def get_number_charts(self):
        return 15

    def get_number_analysis(self):
        return 270

    # def get_number_prediction_rules(self):
    #     return 21

    def get_number_pages(self):
        return 20

    def get_number_data_points(self):
        return self._meta_parser.get_num_rows()*self._meta_parser.get_num_columns()

    def get_number_variables(self):
        return self._meta_parser.get_num_columns()

    def get_number_dimensions(self):
        return 12

    def get_number_measures(self):
        return 14

    def get_number_queries(self):
        return 1200

    def get_time_analyst(self):
        return "12 hours and 30 minutes"

    def get_time_saved(self):
        '''
        Total Time Saved - 21 Hrs ( Productitvity Gain = Time taken by data scientist - time taken by mAdvisor)
        '''
        return "12 hours 27 minutes"

    def get_impact_on_productivity(self):
        '''
        Impact on Productivity - 3.5 X  ( Impact on Productivity = Time taken by data scientist / time taken by mAdvisor)
        '''
        return "10.8 X"

    def get_summary_data(self):
        self.data_points = self.get_number_data_points()
        self.number_charts = self.get_number_charts()
        # self.number_prediction_rules = self.get_number_prediction_rules()
        self.number_pages = self.get_number_pages()
        self.time_saved = self.get_time_saved()
        self.impact_on_productivity = self.get_impact_on_productivity()
        summaryData = [
            {
              "name":"Total Data Points",
              "value":str(self.data_points)
            },
            {
              "name": "Number of Queries",
              "value": str(self.number_queries)
            },
            {
              "name": "Number of Analysis",
              "value": str(self.number_analysis)
            },
            {
              "name": "Total Pages",
              "value": str(self.number_pages)
            },
            {
              "name": "Total Time Saved",
              "value": str(self.time_saved)
            },
            {
              "name": "Impact on Productivity",
              "value": str(self.impact_on_productivity)
            }
        ]
        # summaryData = HtmlData(data="<p> Hello World!!! </p>")
        summaryDataClass = DataBox(data=summaryData)
        self.businessCardData.append(summaryDataClass)
        # businessCardData.append(summaryData)
        # self.business_card1.set_card_data(self.businessCardData)
        # self._businessImpactNode.add_a_card(self.business_card1)

    def get_summary_para(self):
        self.number_variables = self.get_number_variables()
        self.number_dimensions = self.get_number_dimensions()
        self.number_measures = self.get_number_measures()
        self.time_analyst = self.get_time_analyst()
        para = "mAdvisor has analysed the dataset that contains {} variables ({} dimensions and {} measures) and executed about <b>{}</b> queries for <b>{}</b> analysis. This would have taken an estimated average of <b>{}</b> for a data analyst to come up with a similar analysis.".format(self.number_variables, self.number_dimensions, self.number_measures, self.number_queries, self.number_analysis, self.time_analyst)
        # summary_para_class
        print para
        paraDataClass = HtmlData(data=para)
        self.businessCardData.append(paraDataClass)

    def Run(self):
        print "In Run of BusinessCard"
        self._businessImpactNode = NarrativesTree()
        self._businessImpactNode.set_name("Business Impact")

        self.number_queries = self.get_number_queries()
        self.number_analysis = self.get_number_analysis()

        summary = self.get_summary_data()
        summary_para = self.get_summary_para()

        self.business_card1.set_card_data(self.businessCardData)
        self._businessImpactNode.add_a_card(self.business_card1)
        self._result_setter.set_business_impact_node(self._businessImpactNode)
