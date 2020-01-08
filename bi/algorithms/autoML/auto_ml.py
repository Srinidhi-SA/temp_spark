#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import sys
import json
from bi.algorithms.autoML.Data_Validation import Data_Validation
from bi.algorithms.autoML.Data_Preprocessing import Data_Preprocessing
from bi.algorithms.autoML.Feature_Engineering import Feature_Engineering
from bi.algorithms.autoML.Sampling import Sampling
from bi.algorithms.autoML.Feature_Selection import Main
import pandas as pd


# In[2]:


class auto_ML:

    def __init__(self,data_path, target, app_type):

        # self.config = config
        self.data_path = data_path
        self.target = target
        self.app_type = app_type
        self.final_json = {}
        self.tree_df = None
        self.linear_df = None
        """DATA VALIDATION"""

        path = self.data_path
        # path = '/home/marlabs/fresh/mAdvisor-MLScripts/bi/algorithms/'
        obj =  Data_Validation(path,target =self.target,method = self.app_type)
        obj.run()

        #print(obj.df.head())
        #print(obj.data_dict.keys())

        data_dict = obj.data_dict
        Dataframe = obj.df
        print("DATA VALIDATION",'\n')
#         print(Dataframe.info())
        print("#"*50)

        self.target = obj.data_dict["target"]

        if(obj.data_dict["target_fitness_check"] == False):
            sys.exit()

        """DATA PREPROCESSING"""

        obj1 =   Data_Preprocessing(data_dict)
        Dataframe,data_dict  = obj1.main(Dataframe)
        print("DATA PREPROCESSING",'\n')
#         print(Dataframe.info())
        print("#"*50)

        #print(obj1.df1.head())
        #print(obj1.data_dict1.keys())

#         data_dict = obj1.data_dict1
#         Dataframe = obj1.df1
#         print(Dataframe.info())

        f = open("dict1.txt","w")
        f.write( str(data_dict) )
        f.close()
########################################################################################
        """Feature Engineering"""

        obj2 =  Feature_Engineering(Dataframe,data_dict)
        obj2.fe_main()

        mr_df1 = obj2.original_df



        print("Feature Engineering",'\n')
#         print(mr_df1.info())
        print("#"*50)
        #print(mr_df1.shape)

        Dataframe2 = obj2.only_created_df

#        print(Dataframe2.shape)
#        print(Dataframe2.head()

        fdata_dict1 = obj2.data_dict2
#         print(Dataframe2.info())
        print("#"*50)
#
        print("Target in AutoML: ",self.target, obj2.data_dict2["Target_analysis"])
        obj3 = Data_Validation(Dataframe2,self.target,self.app_type)
        obj3.run()

        Dataframe3 = obj3.df

        print("DATA VALIDATION pass2",'\n')
#         print(Dataframe3.info())
        print("#"*50)
        #print(Dataframe3.shape)
        #print(Dataframe3.columns)

        data_dict3 = obj3.data_dict
        print(data_dict3.keys())

#         obj4 = Data_Preprocessing(data_dict3,Dataframe3,targetname = self.target,m_type =self.app_type)
#         obj4.fe_main()

        obj4 =   Data_Preprocessing(data_dict)
        Dataframe,data_dict  = obj4.fe_main(Dataframe3,data_dict3)

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

        mr_df2 = Dataframe

        mr_df2.drop([self.target], axis=1,inplace = True)

        result = pd.concat([mr_df1, mr_df2], axis=1, sort=False)
        print(result.info())

        # result.to_csv("for_sampling.csv")


        """ Sampling """

        obj5 = Sampling(result,self.target)

        obj5.OverSampling()

        result = obj5.dataset

#         print(sum(list(result.isna().sum().values)),"NULLL VALUE")

        """ Feature Selection """

        obj6 = Main(result,fdata_dict1,data_dict)

        linear_df,tree_df = obj6.run()

        #print(l.head())

        #print(t.head())

        # print(json.dumps(obj6.data_dict))
        # print (type(obj6.data_dict))
        # f = open("dict.txt","w")
        # f.write( str(obj6.data_dict) )
        # f.close()

        # with open('data.txt',  'w', encoding='utf-8') as f:
        #     json.dumps(obj6.data_dict)
        self.final_json = json.dumps(obj6.data_dict)
        self.linear_df = linear_df
        self.tree_df = tree_df

    def return_values(self):
        return self.final_json, self.linear_df, self.tree_df
        #print(obj6.info,'\n')


# In[3]:


# a = AUTOML({})


# In[4]:


# import pickle
#
# example_dict = a.af
#
# pickle_out = open("dict4.pickle","wb")
# pickle.dump(example_dict, pickle_out)
# pickle_out.close()
#
#
# # In[5]:
#
#
# f = open("dict_final.txt","w")
# f.write( str(example_dict) )
# f.close()
