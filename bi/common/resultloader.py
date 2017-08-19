from bi.common import utils as CommonUtils


class ResultSetter:
    """
    Provides helper method to store all the different result and narratives.
    """

    def __init__(self, data_frame, df_context):
        self._data_frame = data_frame
        self.executiveSummaryDataDict = {}
        self.trend_subsection_name = None
        self.trend_subsection_data = None
        self.trend_subsection_complete = False
        self.model_summary = {}

    # def set_params(self):
    #     self.columns = [field.name for field in self._data_frame.schema.fields]
    #     self.ignorecolumns = self._df_context.get_ignore_column_suggestions()

    def update_executive_summary_data(self,data_dict):
        if data_dict != None:
            self.executiveSummaryDataDict.update(data_dict)

    def get_executive_summary_data(self):
        return self.executiveSummaryDataDict

    def set_trend_section_name(self,name):
        self.trend_subsection_name = name

    def set_trend_section_completion_status(self,status):
        self.trend_subsection_complete = status

    def set_model_summary(self,data):
        """data will be a key value dictionary
        {"model_name":"model_summary"}
        """
        self.model_summary.update(data)

    def get_trend_section_name(self):
        return self.trend_subsection_name

    def set_trend_section_data(self,dataDict):
        self.trend_subsection_data = dataDict

    def get_trend_section_data(self):
        return self.trend_subsection_data

    def get_trend_section_completion_status(self):
        return self.trend_subsection_complete

    def get_model_summary(self):
        return self.model_summary
