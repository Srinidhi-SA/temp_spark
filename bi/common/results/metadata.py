from bi.common.decorators import accepts

class DfMetaData:
    """
    Functionalities:
    """
    def __init__(self,metaData = [],columnData = [] , headers=[], sampleData=[]):
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
    def __init__(self,name=None,value=None,display=True):
        self.name = name
        self.value = value
        self.display = display

    def set_name(self,data):
        self.name = data

    def set_value(self,data):
        self.value = data

    def set_display(self,boolData):
        self.display = boolData

class ColumnData:
    def __init__(self,name=None,slug=None,columnStats={},chartData={},columnType = None):
        self.name = name
        self.slug = None
        self.columnStats = columnStats
        self.chartData = chartData
        self.columnType = columnType

    def set_name(self,data):
        self.name = data

    def set_slug(self,data):
        self.slug = data

    def set_column_stats(self,data):
        self.columnStats = data

    def set_column_chart(self,data):
        self.chartData = data

    def set_column_type(self,data):
        self.columnType = data

    def set_level_count_to_null(self):
        self.columnStat = [obj if obj["name"] != "LevelCount" else {"name":obj["name"],"value":None} for obj in self.columnStat]

    def set_chart_data_to_null(self):
        self.chartData = {}


class ColumnHeader:
    def __init__(self,name = None,slug = None):
        self.name = name
        self.slug = slug

    def set_name(self,data):
        self.name = data

    def set_slug(self,data):
        self.slug = data
