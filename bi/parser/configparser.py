class ParserConfig():
    """docstring for ParserConfig."""
    def __init__(self, config):
        self.config = config
        self.FileSettings = {}
        self.ColumnSettings = {}
        self.DateSettings = {}
        self.DimensionFilter = {}
        self.MeasureFilter = {}
        self.DateFilter = {}

    def get_dimension_filters(self):
        return self.DimensionFilter

    def get_measure_filters(self):
        return self.MeasureFilter

    def get_date_filters(self):
        return self.DateFilter

    def get_date_settings(self):
        return self.DateSettings

    def get_file_settings(self):
        return self.FileSettings

    def get_column_settings(self):
        return self.ColumnSettings

    def get_filter_settings(self):
        return self.FilterSettings

    def ConfigSectionMap(self, section):
        dict1 = {}
        try:
            options = self.config.options(section)
        except:
            return dict1
        for option in options:
            try:
                if self.config.get(section, option).strip() is "":
                    dict1[option] = None
                else:
                    dict1[option] = map(str.strip,self.config.get(section, option).strip().split(','))
                if dict1[option] == -1:
                    DebugPrint("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

    def set_params(self):
        self.FileSettings = self.ConfigSectionMap('FILE_SETTINGS')
        self.ColumnSettings = self.ConfigSectionMap('COLUMN_SETTINGS')
        self.DateSettings = self.ConfigSectionMap('DATE_SETTINGS')
        # self.DimensionFilter = self.ConfigSectionMap('DIMENSION_FILTER')
        # self.MeasureFilter = self.ConfigSectionMap('MEASURE_FILTER')
        # self.DateFilter = self.ConfigSectionMap('DATE_FILTER')
        self.FilterSettings = self.ConfigSectionMap('FILTER_SETTINGS')

    def set_json_params(self):
        self.FileSettings = self.config.get('FILE_SETTINGS')
        self.ColumnSettings = self.config.get('COLUMN_SETTINGS')
        self.FilterSettings = self.config.get('FILTER_SETTINGS')
        # self.DateSettings = self.config.get('DATE_SETTINGS')
        # self.DimensionFilter = self.config.get('DIMENSION_FILTER')
        # self.MeasureFilter = self.config.get('MEASURE_FILTER')
        # self.DateFilter = self.config.get('DATE_FILTER')
