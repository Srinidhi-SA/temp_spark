class DfMetaData:
    """
    Functionalities:
    """
    def __init__(self, metaData=None, columnData=None, headers=None, sampleData=None):
        if metaData is None:
            metaData = []
        if columnData is None:
            columnData = []
        if headers is None:
            headers = []
        if sampleData is None:
            sampleData = []
        self.metaData = metaData
        self.columnData = columnData
        self.headers = headers
        self.sampleData = sampleData

    def set_meta_data(self,data):
        self.metaData = data

    def set_column_data(self,data):
        self.columnData = data

    def set_header(self,data):
        self.headers = data

    def set_sample_data(self,data):
        self.sampleData = data

    def add_meta_data(self,data):
        self.metaData.append(data)

    def add_column_data(self,data):
        self.columnData.append(data)

    def add_headers(self,data):
        self.headers.append(data)


class MetaData:
    def __init__(self,name=None,value=None,display=True,displayName=None):
        self.name = name
        self.value = value
        self.display = display
        self.displayName = displayName


    def set_name(self,data):
        self.name = data

    def set_display_name(self,data):
        self.displayName = data

    def set_value(self,data):
        self.value = data

    def set_display(self,boolData):
        self.display = boolData

class ColumnData:
    def __init__(self, name=None, slug=None, columnStats=None, chartData=None, columnType = None):
        if columnStats is None:
            columnStats = []
        if chartData is None:
            chartData = {}
        self.name = name
        self.slug = None
        self.ignoreSuggestionFlag = False
        self.dateSuggestionFlag = False
        self.ignoreSuggestionMsg = None
        self.columnStats = columnStats
        self.chartData = chartData
        self.columnType = columnType
        self.actualColumnType = None

    def set_name(self,data):
        self.name = data

    def set_slug(self,data):
        self.slug = data

    def set_column_stats(self,data):
        self.columnStats = data

    def set_column_chart(self,data):
        self.chartData = data

    def set_abstract_datatype(self,data):
        self.columnType = data

    def set_actual_datatype(self,data):
        self.actualColumnType = data


    def set_level_count_to_null(self):
        self.columnStats = [obj if obj["name"] != "LevelCount" else {"name":obj["name"],"value":None,"display":False} for obj in self.columnStats]

    def set_chart_data_to_null(self):
        self.chartData = {}

    def set_ignore_suggestion_flag(self,data):
        self.ignoreSuggestionFlag = data

    def set_ignore_suggestion_message(self,data):
        self.ignoreSuggestionMsg = data

    def set_date_suggestion_flag(self,data):
        self.dateSuggestionFlag = data


class ColumnHeader:
    def __init__(self,name = None,slug = None):
        self.name = name
        self.slug = slug

    def set_name(self,data):
        self.name = data

    def set_slug(self,data):
        self.slug = data
