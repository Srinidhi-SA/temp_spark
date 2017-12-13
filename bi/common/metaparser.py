# from bi.decorators import accepts
class MetaParser:

    def __init__(self):
        self.meta_data = {}
        self.column_dict = {}


    def set_params(self, meta_data):
        print "Setting Meta Data Parser"
        self.meta_data = meta_data
        # dict_out = self.extract(self.meta_data['metaData'], self.meta_data['metaData'])
        # self.column_dict = self.get_column_stats(dict_out['columnData'])
        self.column_dict = self.get_column_stats(self.meta_data['columnData'])


    def extract(self,dict_in, dict_out):
        for key, value in dict_in.iteritems():
            if isinstance(value, dict): # If value itself is dictionary
                self.extract(value, dict_out)
            elif isinstance(value, unicode):
                # Write to dict_out
                dict_out[key] = value
        return dict_out

    def get_column_stats(self, columnData):
        for each in columnData:
            self.column_dict[each['name']] = self.parse_stats(each['columnStats'])
            self.column_dict[each['name']]['columnType'] = each['columnType']
        return self.column_dict

    def parse_stats(self, columnStats):
        return_dict = {}
        for each in columnStats:
            return_dict[each['name']] = each['value']
        return return_dict

    # ---------------------- All the getters ---------------------------------

    def get_num_unique_values(self, column_name):
        return self.column_dict[column_name]['numberOfUniqueValues']

    def get_unique_level_dict(self,column_name):
        return self.column_dict[column_name]["LevelCount"]
