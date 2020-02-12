import locale
import pandas as pd
import numpy as np
import re
import pint
from pint import UnitRegistry
import random
import pickle
from validate_email import validate_email


class Data_Preprocessing(object):

    def __init__(self,pre_dict,dataframe):
        self.pre_dict=pre_dict
        self.dataframe=dataframe

    def drop_duplicate_rows(self):
        '''Drops Duplicate rows of a dataframe and returns a new dataframe'''
        self.dataframe = self.dataframe.drop_duplicates()
        #return dataframe

    def drop_na_columns(self, pre_dict):
        pre_dict["Dropped_columns"]=[]
        col_settings = pre_dict['Column_settings']
        for i in range(len(col_settings)):
            col = col_settings[i]["re_column_name"]
            if(col in self.dataframe):
                if(self.dataframe[col].isna().sum()>(0.75*self.dataframe.shape[0])):
                    self.dataframe = self.dataframe.drop([col],axis=1)
                    col_settings[i]["droped_column"] = True
                    pre_dict["Dropped_columns"].append(col)
        #return dataset

    def Dimension_Measure(self,columns):
        '''Identifies columns which are measures and have been wrongly identified as dimension
        returns a list of columns to be converted to measure and removes the rows which have other than numeric
        for that particular column'''
        DimToMeasureColumn=[]
        for column in columns:
            column_val=self.dataframe[column]
            updatedRowNum=self.dataframe[column].index
            r1 = random.randint(0, len(updatedRowNum)-1)
            if re.match("^\d*[.]?\d*$",str(column_val[updatedRowNum[r1]])):
                #out=column_val.str.isdigit()
                out = column_val.str.contains("[0-9]+[.]{0,1}[0-9]*\s*")
                if out[out==False].count() <= 0.01*self.dataframe.shape[0]:
                    rowIndex=out.index[out==False].tolist()
                    self.dataframe=self.dataframe.drop(rowIndex,axis=0)
                    DimToMeasureColumn.append(column)
                    ## below line code change during optimization
                    self.dataframe[column]=pd.to_numeric(self.dataframe[column])
        return DimToMeasureColumn

    def handle_outliers(self,columns):
        '''Hanles outliers for measure columns and returns a list of columns which have high number of outliers'''
        outlier_col=[]
        capped_col=[]
        for column in columns:
            df1=self.dataframe[column]
            #print(column)  ## Commented
            col_summary=self.dataframe[column].describe()
            #print(col_summary) ## Commented
            outlier_LR, outlier_UR = col_summary["mean"] - (3*col_summary["std"]), col_summary["mean"] + (3*col_summary["std"])
            outlier_per = len(df1[(df1 > outlier_UR) | (df1 < outlier_LR)])/self.dataframe.shape[0]
            if outlier_per < 8/100 and outlier_per>0:
                capped_col.append(column)
                df1=df1.replace(to_replace = df1[df1>outlier_UR], value =outlier_UR)
                df1=df1.replace(to_replace = df1[df1<outlier_LR],value = outlier_LR)
            elif outlier_per!=0 :
                outlier_col.append(column)
            self.dataframe[column]=df1
        return outlier_col,capped_col

    def mean_impute(self,column_val):
        '''Returns a column with mean impute'''
        mean=np.mean(column_val)
        column_val=column_val.fillna(mean)
        return column_val

    def median_impute(self,column_val):
        '''Returns a column with median impute'''
        median=np.mean(column_val)
        column_val=column_val.fillna(median)
        return column_val

    def mode_impute(self,column_val):
        '''Returns a column with mode impute'''
        mode=column_val.mode()[0]
        column_val=column_val.fillna(mode)
        return column_val

    def measureCol_imputation(self,columns,median_col):
        '''Does missing value imputation for measure columns'''
        mean_impute_cols=[]
        median_impute_cols=[]
        for column in columns:
            if column not in median_col:
                mean_impute_cols.append(column)
                self.dataframe[column]=self.mean_impute(dataself.dataframeset[column])
            else:
                median_impute_cols.append(column)
                self.dataframe[column]=self.median_impute(self.dataframe[column])
        return mean_impute_cols,median_impute_cols

    def dimCol_imputation(self,columns):
        '''Does missing value imputation for dimension columns'''
        for column in columns:
            self.dataframe[column]=self.mode_impute(self.dataframe[column])
        #return dataset

    def regex_catch(self,column):
        '''Returns a list of columns and the pattern it has'''
        ## considering currency_list and metric_list are globally defined.
        Dict={"Column_name":column,"email-id":False,"website":False,"Percentage":False,"CurrencyCol":{"value":False,"currency":None},"MetricCol":{"value":False,"metric":None},"SepSymbols":{"value":False,"Symbol":None}}
        column_val=self.dataframe[column].astype(str).str.strip()
        df1 = self.dataframe[column_val.apply(validate_email)]
        if(df1.shape[0]>=(0.8*self.dataframe.shape[0])):
            Dict["email-id"]=True
        elif column_val.str.contains("%$",na=True).all():
            Dict["Percentage"]=True
        elif column_val.str.contains("^https:|^http:|^www.",na=True).all():
            Dict["website"]=True
        elif column_val.str.contains("[0-9]+[.]{0,1}[0-9]*\s*[Aa-zZ]{1,2}$").all():
            metric=list(map(lambda x:re.sub("[0-9]+[.]{0,1}[0-9]*\s*","",x),column_val))
            if len(set(metric))==1:
                if metric[0] in Metric_list:
                    Dict["MetricCol"]["value"]=True
                    Dict["MetricCol"]["metric"]=metric[0]
        elif column_val.str.contains("([0-9]+[.]{0,1}[0-9]*\s*\W$)|(^\W[0-9]+[.]{0,1}[0-9]*)").all():
            currency=list(map(lambda x:re.sub("[0-9.\s]+","",x),column_val))
            if len(set(currency))==1:
                if currency[0] in currency_list:
                    Dict["CurrencyCol"]["value"]=True
                    Dict["CurrencyCol"]["currency"]=currency[0]
        elif column_val.str.contains("\S+\s*[\W_]+\s*\S+").all():
            seperators=list(map(lambda x:re.sub("\s*[a-zA-Z0-9]+$","",x),list(map(lambda x:re.sub('^[a-zA-Z0-9]+\s*', '', x),column_val))))
            if len(set(seperators))==1:
                if seperators[0]=="":
                    seperators[0] = ' '
                Dict["SepSymbols"]["value"]=True
                Dict["SepSymbols"]["Symbol"]=seperators[0]
        return Dict

    def Target_analysis(self, targetname, m_type):
        '''Gives information of target column'''
        self.dataframe=self.dataframe.dropna(axis=0, subset=[targetname])
        output_dict={"Target_analysis":{"target":targetname,"unique_count":int,"value_counts":{},"balanced": None ,"binary": None}}
        target_variable=self.dataframe[targetname]
        counts = target_variable.value_counts()
        self.dataframe = self.dataframe[~target_variable.isin(counts[counts <= 10].index)]
        if (m_type.lower()=='classification'):
            ## convert target column into object
            output_dict['Target_analysis']['converted_to_str'] = False
            if self.dataframe[targetname].dtype != 'O':
                self.dataframe[targetname] = "'" + self.dataframe[targetname].astype(str) + "'"
                output_dict['Target_analysis']['converted_to_str'] = True
                print("!!!!!!! Converted to str!!!!!!")
            unique_count=target_variable.nunique()
            output_dict['Target_analysis']['unique_count']=unique_count
            level_count=target_variable.value_counts()
            count_check=level_count[level_count >=10]
            output_dict['Target_analysis']['value_counts']=count_check.to_dict()
            percen_level_count= round((count_check/count_check.sum())*100)
            n=len(count_check)
            if (n == 0):
                out_dict={"Target_analysis":{"target_name":targetname,"descrp_status":{}}}
                out_dict['Target_analysis']['descrp_status']=target_variable.describe().to_dict()
                return out_dict,DataFrame
            if((percen_level_count[percen_level_count < ((1/(2*n))*100)]).empty==False):
                output_dict['Target_analysis']['balanced']=False
                if (len(count_check)==2):
                       output_dict['Target_analysis']['binary']=True # binary (true)
                else:
                    output_dict['Target_analysis']['binary']=False# not binary(False)
            else:
                output_dict['Target_analysis']['balanced']=True # balanced (True)
                if (len(count_check)==2):
                       output_dict['Target_analysis']['binary']=True # binary (true)
                else:
                    output_dict['Target_analysis']['binary']=False# not binary(False)
            return output_dict
        else:
            out_dict={"Target_analysis":{"target_name":targetname,"descrp_status":{}}}
            out_dict['Target_analysis']['descrp_status']=target_variable.describe().to_dict()
            return out_dict

    def update_column_settings(self,regexd,datad):
            col_settings = datad['Column_settings']
            for i in range(len(col_settings)):
                col_settings[i]["email-id"]=False
                col_settings[i]["Percentage"]=False
                col_settings[i]["website"]=False
                col_settings[i]["MetricCol"] = {}
                col_settings[i]["MetricCol"]["value"]=False
                col_settings[i]["MetricCol"]["metric"]=None
                col_settings[i]["CurrencyCol"] = {}
                col_settings[i]["CurrencyCol"]["value"]=False
                col_settings[i]["CurrencyCol"]["currency"]=None
                col_settings[i]["SepSymbols"] = {}
                col_settings[i]["SepSymbols"]["value"]=False
                col_settings[i]["SepSymbols"]["Symbol"]=None
            for i in range(len(col_settings)):
                col = col_settings[i]["re_column_name"]
                for j in range(len(regexd)):
                    regex_col = regexd[j]["Column_name"]
                    if(col == regex_col):
                        col_settings[i]["email-id"]=regexd[j]["email-id"]
                        col_settings[i]["Percentage"]=regexd[j]["Percentage"]
                        col_settings[i]["website"]=regexd[j]["website"]
                        col_settings[i]["MetricCol"] = {}
                        col_settings[i]["MetricCol"]["value"]=regexd[j]["MetricCol"]["value"]
                        col_settings[i]["MetricCol"]["metric"]=regexd[j]["MetricCol"]["metric"]
                        col_settings[i]["CurrencyCol"] = {}
                        col_settings[i]["CurrencyCol"]["value"]=regexd[j]["CurrencyCol"]["value"]
                        col_settings[i]["CurrencyCol"]["currency"]=regexd[j]["CurrencyCol"]["currency"]
                        col_settings[i]["SepSymbols"] = {}
                        col_settings[i]["SepSymbols"]["value"]=regexd[j]["SepSymbols"]["value"]
                        col_settings[i]["SepSymbols"]["Symbol"]=regexd[j]["SepSymbols"]["Symbol"]
            datad['Column_settings']=col_settings
            return datad

    def main(self):
        global currency_list
        global Metric_list
        target = self.pre_dict['target']
        app_type = self.pre_dict['app_type']
        data_dict=self.pre_dict
        try:
            locales=('en_AU.utf8', 'en_BW.utf8', 'en_CA.utf8',
                'en_DK.utf8', 'en_GB.utf8', 'en_HK.utf8', 'en_IE.utf8', 'en_IN', 'en_NG',
                'en_PH.utf8', 'en_US.utf8', 'en_ZA.utf8',
                'en_ZW.utf8')
            d={}
            for l in locales:
                locale.setlocale(locale.LC_ALL, l)
                conv=locale.localeconv()
                d[conv['int_curr_symbol']] = conv['currency_symbol']
            currency_list=list(set(d.values()))
        except :
            currency_list=['₹', 'kr.', '₱', 'P', 'R', '£', '₦', '€', 'HK$', '$']
        currency_list
        Metric_list=list(set(dir(UnitRegistry())))
        self.drop_duplicate_rows()
        self.drop_na_columns(data_dict)
        ## check the below line to improve
        #data_dict['Dropped_columns']=list(set(df1)-set(df))
        a=self.Target_analysis(target,app_type)
        measureCol=[]
        dimCol=[]
        ## pass this measure column and dim col to other modules
        measureCol = list(self.dataframe.select_dtypes(include=['int32','int64','float32','float64','int','float']).columns) ## measureCol = list(df.select_dtypes(include=['int','float']).columns)
        dimCol = list(self.dataframe.select_dtypes(include=['object','datetime64','category','bool']).columns)
        data_dict["Target_analysis"]=a["Target_analysis"]
        outlier_columns,capped_cols=self.handle_outliers(measureCol)
        print("capped_cols: ",capped_cols)
        data_dict["Cap_outlier"]=capped_cols
        measureColImpu=[i for i in measureCol if self.dataframe[i].isna().sum()>0 ]
        dimColImpu=[i for i in dimCol if self.dataframe[i].isna().sum()>0 ]
        mean_impute_cols,median_impute_cols=self.measureCol_imputation(measureColImpu,outlier_columns)
        data_dict["Mean_imputeCols"]=mean_impute_cols
        data_dict["Median_imputeCols"]=median_impute_cols
        self.dimCol_imputation(dimColImpu)
        data_dict["Mode_imputeCols"]=dimColImpu
        dimRegex=[i for i in dimCol if self.dataframe[i].dtypes == "object" ]
        if data_dict['target'] in dimRegex:
            dimRegex.remove(data_dict['target'])
        regex_dic=[self.regex_catch(i)for i in dimRegex]
        data_dict=self.update_column_settings(regex_dic,data_dict)
        data_dict["MeasureColsToDim"]=self.Dimension_Measure(dimCol)
        for column in data_dict["MeasureColsToDim"]:
            self.dataframe[column]=pd.to_numeric(self.dataframe[column])
        ### Setting orginal_columns value in the dictionary:
        orginal_columns=self.dataframe.columns.to_list()
        data_dict['original_cols'] = orginal_columns
        print("Original Columns:  ",orginal_columns)
        return data_dict

    #def fe_main(self,df,data_dict):
    def fe_main(self):
        data_dict=self.pre_dict
        target = self.pre_dict['target']
        app_type = self.pre_dict['app_type']
        try:
            locales=('en_AU.utf8', 'en_BW.utf8', 'en_CA.utf8',
                'en_DK.utf8', 'en_GB.utf8', 'en_HK.utf8', 'en_IE.utf8', 'en_IN', 'en_NG',
                'en_PH.utf8', 'en_US.utf8', 'en_ZA.utf8',
                'en_ZW.utf8')
            d={}
            for l in locales:
                locale.setlocale(locale.LC_ALL, l)
                conv=locale.localeconv()
                d[conv['int_curr_symbol']] = conv['currency_symbol']
            currency_list=list(set(d.values()))
        except :
            currency_list=['₹', 'kr.', '₱', 'P', 'R', '£', '₦', '€', 'HK$', '$']
        currency_list
        Metric_list=list(set(dir(UnitRegistry())))
        measureCol=[]
        dimCol=[]
        measureCol = list(self.dataframe.select_dtypes(include=['int32','int64','float32','float64','int','float']).columns) ## measureCol = list(df.select_dtypes(include=['int','float']).columns)
        dimCol = list(self.dataframe.select_dtypes(include=['object','datetime64','category','bool']).columns)
        outlier_columns,capped_cols=self.handle_outliers(measureCol)
        data_dict["Cap_outlier"]=capped_cols
        measureColImpu=[i for i in measureCol if self.dataframe[i].isna().sum()>0 ]
        dimColImpu=[i for i in dimCol if self.dataframe[i].isna().sum()>0 ]
        mean_impute_cols,median_impute_cols=self.measureCol_imputation(measureColImpu,outlier_columns)
        data_dict["Mean_imputeCols"]=mean_impute_cols
        data_dict["Median_imputeCols"]=median_impute_cols
        self.dimCol_imputation(dimColImpu)
        data_dict["Mode_imputeCols"]=dimColImpu
        dimRegex=[i for i in dimCol if self.dataframe[i].dtypes == "object" ]
        regex_dic=[self.regex_catch(i)for i in dimRegex]
        data_dict=self.update_column_settings(regex_dic,data_dict)
        data_dict["MeasureColsToDim"]=self.Dimension_Measure(dimCol)
        for column in data_dict["MeasureColsToDim"]:
            self.dataframe[column]=pd.to_numeric(self.dataframe[column])
        return data_dict
