import os
import sys
import json
from bi.algorithms.autoML.Data_Validation import DataValidation
from bi.algorithms.autoML.Data_Preprocessing import DataPreprocessingAutoMl
from bi.algorithms.autoML.Feature_Engineering import FeatureEngineeringAutoMl
from bi.algorithms.autoML.Sampling import Sampling
from bi.algorithms.autoML.Feature_Selection import Feature_Selection
import pandas as pd
import re
from bi.common import utils as CommonUtils



class auto_ML:

    def __init__(self,df, dataframe_context, app_type):

        # self.config = config
        #self.data_path = data_path
        self.df = df
        self.target = dataframe_context.get_result_column()
        self.app_type = app_type
        self.final_json = {}
        self.tree_df = None
        self.linear_df = None
        self.LOGGER = dataframe_context.get_logger()
        self.errorURL = dataframe_context.get_error_url()
        self.ignoreMsg = dataframe_context.get_message_ignore()

    def run(self):
        """DATA VALIDATION"""

        #path = self.df
        #obj =  Data_Validation(path,target =self.target,method = self.app_type)
        try :
            Data_Validation_auto_obj =  DataValidation(self.df, target =self.target, method = self.app_type)
            Data_Validation_auto_obj.run()

            #print(obj.df.head())
            #print(obj.data_dict.keys())

            # data_dict = Data_Validation_auto_obj.data_dict
            # Dataframe = Data_Validation_auto_obj.df
            print("DATA VALIDATION",'\n')
    #         print(Dataframe.info())
            print("#"*50)

            #self.target = obj.data_dict["target"]
            Data_Validation_auto_obj.data_dict["target"]=self.target
            if(Data_Validation_auto_obj.data_dict["target_fitness_check"] == False):
                sys.exit()
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(self.LOGGER,"datavalidation",e)
            CommonUtils.save_error_messages(self.errorURL,self.app_type,e,ignore=self.ignoreMsg)

        """DATA PREPROCESSING"""

        # this line used before # Data_Preprocessing_auto_obj =   Data_Preprocessing(data_dict)
        # Dataframe,data_dict  = Data_Preprocessing_auto_obj.main(Dataframe)
        try :
            Data_Preprocessing_auto_obj =   DataPreprocessingAutoMl(Data_Validation_auto_obj.data_dict, Data_Validation_auto_obj.df)
            data_dict  = Data_Preprocessing_auto_obj.main()
            print("DATA PREPROCESSING",'\n')
    #         print(Dataframe.info())
            print("#"*50)
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(self.LOGGER,"dataPreprocessing",e)
            CommonUtils.save_error_messages(self.errorURL,self.app_type,e,ignore=self.ignoreMsg)

        #print(obj1.df1.head())
        #print(obj1.data_dict1.keys())

#         data_dict = obj1.data_dict1
#         Dataframe = obj1.df1
#         print(Dataframe.info())

        # f = open("dict1.txt","w")
        # f.write( str(data_dict) )
        # f.close()
########################################################################################
        """Feature Engineering"""
        try :
            Feature_Engineering_auto_obj =  FeatureEngineeringAutoMl(Data_Preprocessing_auto_obj.dataframe, data_dict)
            Feature_Engineering_auto_obj.fe_main()

            mr_df1 = Feature_Engineering_auto_obj.original_df

            date_col = Feature_Engineering_auto_obj.date_time_columns
            cols = list(set(mr_df1)-set(date_col))
            mr_df1 = mr_df1[cols]

            print("Feature Engineering",'\n')
    #         print(mr_df1.info())
            print("#"*50)
            #print(mr_df1.shape)

            # Dataframe2 = Feature_Engineering_auto_obj.only_created_df

    #        print(Dataframe2.shape)
    #        print(Dataframe2.head()

            # fdata_dict1 = Feature_Engineering_auto_obj.data_dict2
    #         print(Dataframe2.info())
            print("#"*50)
    #
            print("Target in AutoML: ",self.target, Feature_Engineering_auto_obj.data_dict2["target_analysis"])
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(self.LOGGER,"Feature Engineering",e)
            CommonUtils.save_error_messages(self.errorURL,self.app_type,e,ignore=self.ignoreMsg)

        try:
            Data_Validation_auto_obj2 = DataValidation(Feature_Engineering_auto_obj.only_created_df, self.target, self.app_type)
            Data_Validation_auto_obj2.run()

            # Dataframe3 = Data_Validation_auto_obj2.df

            print("DATA VALIDATION pass2",'\n')
    #         print(Dataframe3.info())
            print("#"*50)
            #print(Dataframe3.shape)
            #print(Dataframe3.columns)

            # data_dict3 = Data_Validation_auto_obj2.data_dict
            # print(data_dict3.keys())

    #         obj4 = Data_Preprocessing(data_dict3,Dataframe3,targetname = self.target,m_type =self.app_type)
    #         obj4.fe_main()

            ### Data_Preprocessing_auto_obj2 =   Data_Preprocessing(data_dict3)
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(self.LOGGER,"DATA VALIDATION pass2",e)
            CommonUtils.save_error_messages(self.errorURL,self.app_type,e,ignore=self.ignoreMsg)

        try :
            Data_Preprocessing_auto_obj2 = DataPreprocessingAutoMl(Data_Validation_auto_obj2.data_dict, Data_Validation_auto_obj2.df)
            #Dataframe,data_dict  = obj4.fe_main(Dataframe3)
            data_dict  = Data_Preprocessing_auto_obj2.pass2_run()
            ### mr_df2,data_dict  = Data_Preprocessing_auto_obj2.fe_main(Data_Validation_auto_obj2.df,Data_Validation_auto_obj2.data_dict)
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(self.LOGGER,"Data_Preprocessing pass2",e)
            CommonUtils.save_error_messages(self.errorURL,self.app_type,e,ignore=self.ignoreMsg)

        print("Data_Preprocessing pass2",'\n')
#         print(Dataframe.info())
#         print("#"*50)

#         fdata_dict2 = obj4.data_dict1

#        for i in fdata_dict1.keys():
#
#            if i in fdata_dict2.keys():
#
#                self.final_dict[i] = fdata_dict1[i]+fdata_dict2[i]
#
#            else:
#
#                self.final_dict[i] = fdata_dict1[i]
#
#        print(self.final_dict)

        # mr_df2 = Dataframe
        try :
            Data_Preprocessing_auto_obj2.dataframe.drop([self.target], axis=1,inplace = True)

            result = pd.concat([mr_df1, Data_Preprocessing_auto_obj2.dataframe], axis=1, sort=False)
            print(result.info())
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(self.LOGGER,"merging of dataframes automl",e)
            CommonUtils.save_error_messages(self.errorURL,self.app_type,e,ignore=self.ignoreMsg)

        # result.to_csv("for_sampling.csv")


        """ Sampling """
        try :
            Sampling_obj = Sampling(result,self.target)

            Sampling_obj.over_sampling()
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(self.LOGGER,"sampling automl",e)
            CommonUtils.save_error_messages(self.errorURL,self.app_type,e,ignore=self.ignoreMsg)

        # result = Sampling_obj.dataset

#         print(sum(list(result.isna().sum().values)),"NULLL VALUE")

        """ Feature Selection """

        ### Feature_Selection_obj = Feature_Selection(result,fdata_dict1,data_dict)
        try :
            Feature_Selection_obj = Feature_Selection(Sampling_obj.dataset,Feature_Engineering_auto_obj.data_dict2,data_dict)

            linear_df,tree_df = Feature_Selection_obj.run()

            linear_df_cols = [re.sub('\W+','_', col) for col in linear_df.columns]
            linear_df.columns = linear_df_cols

            tree_df_cols = [re.sub('\W+','_', col) for col in tree_df.columns]
            tree_df.columns = tree_df_cols
        except Exception as e:
            CommonUtils.print_errors_and_store_traceback(self.LOGGER,"FEATURE SELECTION AUTOML",e)
            CommonUtils.save_error_messages(self.errorURL,self.app_type,e,ignore=self.ignoreMsg)
        #print(l.head())

        #print(t.head())

        # print(json.dumps(obj6.data_dict))
        # print (type(obj6.data_dict))
        # f = open("dict.txt","w")
        # f.write( str(obj6.data_dict) )
        # f.close()

        # with open('data.txt',  'w', encoding='utf-8') as f:
        #     json.dumps(obj6.data_dict)
        #self.final_json = json.dumps(Feature_Selection_obj.data_dict)
        self.final_json = Feature_Selection_obj.data_dict
        self.linear_df = linear_df
        self.tree_df = tree_df

    def return_values(self):
        return self.final_json, self.linear_df, self.tree_df
        #print(obj6.info,'\n')
