import time, json
from bi.common import NormalCard, NarrativesTree, HtmlData, C3ChartData, TableData, ModelSummary,PopupData,NormalCard,ParallelCoordinateData,DataBox,WordCloud

class BusinessCard:
    """
    Functionalities
    """
    def __init__(self, business_impact_nodes, story_result, meta_parser, result_setter):
        self._business_impact_nodes = business_impact_nodes
        self._story_result = story_result
        self._meta_parser = meta_parser
        self._result_setter = result_setter
        self.subheader = "Business Impact"

    def get_number_charts(self):
        return 15

    def get_number_analysis(self):
        return 270

    def get_number_prediction_rules(self):
        return 21

    def get_number_pages(self):
        return 20

    def get_number_data_points(self):
        return self._meta_parser.get_num_rows()*self._meta_parser.get_num_columns()

    def get_data_dict(self):
        self.data_points = self.get_number_data_points()
        self.number_analysis = self.get_number_analysis()
        self.number_charts = self.get_number_charts()
        self.number_prediction_rules = self.get_number_prediction_rules()
        self.number_pages = self.get_number_pages()

    def Run(self):
        print "In Run of BusinessCard"
        self._businessImpactNode = NarrativesTree()
        self._businessImpactNode.set_name("Business Impact")
        data_dict = self.get_data_dict()
        business_card1 = NormalCard()
        business_card1.set_card_name("Overview")
        businessCardData = []
        summaryData = [
            {
              "name":"Total Points",
              "value":str(self.data_points)
            },
            {
              "name": "Total Analysis",
              "value": str(self.number_analysis)
            },
            {
              "name": "Number of Charts",
              "value": str(self.number_charts)
            },
            {
              "name": "Number of Prediction Rules",
              "value": str(self.number_prediction_rules)
            },
            {
              "name": "Number Pages",
              "value": str(self.number_pages)
            },
            {
              "name": "Max Decrease in Price",
              "value": "mitali"
            }
        ]
        # summaryData = HtmlData(data="<p> Hello World!!! </p>")
        summaryDataClass = DataBox(data=summaryData)
        businessCardData.append(summaryDataClass)
        # businessCardData.append(summaryData)
        business_card1.set_card_data(businessCardData)
        self._businessImpactNode.add_a_card(business_card1)
        self._result_setter.set_business_impact_node(self._businessImpactNode)
