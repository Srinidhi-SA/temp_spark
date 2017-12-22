from bi.common.decorators import accepts
class MetaParser:

    def __init__(self):
        self.meta_data = {}
        self.column_dict = {}
        self.ignoreColDict = {}
    def set_params(self, meta_data):
        print "Setting Meta Data Parser"
        self.meta_data = meta_data
        # dict_out = self.extract(self.meta_data['metaData'], self.meta_data['metaData'])
        # self.column_dict = self.get_column_stats(dict_out['columnData'])
        self.column_dict = self.get_column_stats(self.meta_data['columnData'])
        ignorecolobject = [x for x in self.meta_data['metaData'] if x["name"] == "ignoreColumnSuggestions"]
        ignorereasonobj = [x for x in self.meta_data['metaData'] if x["name"] == "ignoreColumnReason"]

        if len(ignorecolobject) > 0:
            if ignorecolobject[0] != {} and len(ignorecolobject[0]["value"]) >0:
                self.ignoreColDict = dict(zip(ignorecolobject[0]["value"],ignorereasonobj[0]["value"]))


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

    def update_column_dict(self,colname,columnStats):
        self.column_dict.update({colname:columnStats})
    # ---------------------- All the getters ---------------------------------

    def get_num_unique_values(self, column_name):
        return self.column_dict[column_name]['numberOfUniqueValues']

    @accepts(object,column_name=(list,tuple,str))
    def get_unique_level_dict(self,column_name):
        if isinstance(column_name,str):
            return self.column_dict[column_name]["LevelCount"]
        elif isinstance(column_name,list) or isinstance(column_name,tuple):
            out = {}
            for col in column_name:
                out[col] = self.column_dict[col]["LevelCount"]
            return out

    def get_uid_column(self):
        uidCol = None
        for k,v in self.ignoreColDict.items():
            if v.startswith("Index Column"):
                uidCol = k
        return uidCol

    def get_unique_level_names(self,column_name):
        return self.column_dict[column_name]["LevelCount"].keys()
