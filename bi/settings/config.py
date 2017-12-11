def get_story_config():
    storyConfig = {

        "config" : {
                    "ADVANCED_SETTINGS" : {
                        "analysis" : [
                            {
                                "analysisSubTypes" : [],
                                "displayName" : "Overview",
                                "name" : "overview",
                                "noOfColumnsToUse" : None,
                                "status" : True
                            },
                            {
                                "analysisSubTypes" : [],
                                "displayName" : "Trend",
                                "name" : "trend",
                                "noOfColumnsToUse" : None,
                                "status" : False
                            },
                            {
                                "analysisSubTypes" : [],
                                "displayName" : "Association",
                                "name" : "association",
                                "noOfColumnsToUse" : None,
                                "binSetting": [
                                  {
                                    "name": "heading",
                                    "displayName": "Binning of Numerical Values"
                                  },
                                  {
                                    "name": "binLevels",
                                    "displayName": "Number of Bin Levels",
                                    "defaultValue": 5,
                                    "value":5,
                                    "min": 2,
                                    "max": 10
                                  },
                                  {
                                    "name": "binCardinality",
                                    "displayName": "Do not bin numerical values with cardinality less than:",
                                    "defaultValue": 5,
                                    "value":5,
                                    "min": 2,
                                    "max": 10
                                  }
                                ],
                                "status" : True
                            },
                            {
                                "analysisSubTypes" : [],
                                "displayName" : "Performance",
                                "name" : "performance",
                                "noOfColumnsToUse" : [
                                    {
                                        "defaultValue" : 3,
                                        "displayName" : "Low",
                                        "name" : "low",
                                        "status" : False
                                    },
                                    {
                                        "defaultValue" : 5,
                                        "displayName" : "Medium",
                                        "name" : "medium",
                                        "status" : False
                                    },
                                    {
                                        "defaultValue" : 8,
                                        "displayName" : "High",
                                        "name" : "high",
                                        "status" : True
                                    },
                                    {
                                        "defaultValue" : 3,
                                        "displayName" : "Custom",
                                        "name" : "custom",
                                        "status" : False,
                                        "value" : None
                                    }
                                ],
                                "status" : False,
                            },
                            {
                                "analysisSubTypes" : [],
                                "displayName" : "Influencer",
                                "name" : "influencer",
                                "noOfColumnsToUse" : [
                                    {
                                        "defaultValue" : 3,
                                        "displayName" : "Low",
                                        "name" : "low",
                                        "status" : False
                                    },
                                    {
                                        "defaultValue" : 5,
                                        "displayName" : "Medium",
                                        "name" : "medium",
                                        "status" : False
                                    },
                                    {
                                        "defaultValue" : 8,
                                        "displayName" : "High",
                                        "name" : "high",
                                        "status" : True
                                    },
                                    {
                                        "defaultValue" : 3,
                                        "displayName" : "Custom",
                                        "name" : "custom",
                                        "status" : False,
                                        "value" : None
                                    }
                                ],
                                "status" : False
                            },
                            {
                                "analysisSubTypes" : [],
                                "displayName" : "Prediction",
                                "name" : "prediction",
                                "noOfColumnsToUse" : None,
                                "status" : False
                            }
                        ],
                        "trendSettings" : [
                            {
                                "name" : "Count",
                                "status" : False
                            },
                            {
                                "name" : "Specific Measure",
                                "selectedMeasure" : None,
                                "status" : False
                            }
                        ]
                    },
                    "COLUMN_SETTINGS" : {
                        "customAnalysisDetails":[
                            {"colName":"Marketing_Cost"},
                        ],
                        "analysis_type" : [
                            "dimension"
                        ],
                        "consider_columns" : [
                            "Deal_Type",
                            "Price_Range",
                            "Discount_Range",
                            "Source",
                            "Platform",
                            "Buyer_Age",
                            "Buyer_Gender",
                            "Tenure_in_Days",
                            "Sales",
                            "Marketing_Cost",
                            "Shipping_Cost",
                            "Last_Transaction",
                            "new_date"
                        ],
                        "consider_columns_type" : [
                            "including"
                        ],
                        "dateTimeSuggestions" : [
                            {
                                "Month" : "%b-%y",
                                "Order Date" : "%d-%m-%Y"
                            }
                        ],
                        "date_columns" : [
                            "new_date"
                        ],
                        "date_format" : None,
                        "ignore_column_suggestion" : [],
                        "polarity" : [
                            "positive"
                        ],
                        "result_column" : [
                            "Source"
                        ],
                        "utf8_column_suggestions" : []
                    },
                    "DATA_SOURCE" : {
                        "datasource_details" : "",
                        "datasource_type" : "fileUpload"
                    },
                    "FILE_SETTINGS" : {
                        "inputfile" : [
                          "file:///home/gulshan/marlabs/datasets/trend_gulshan.csv"
                        ],
                        "metadata" : {
                            "slug_list" : [
                                "trend_gulshancsv-8lue9pvskm"
                            ],
                            "url" : "34.196.204.54:9012/api/get_metadata_for_mlscripts/"
                        },
                        "script_to_run" : [
                            "Descriptive analysis",
                            "Trend",
                            "Measure vs. Dimension",
                            "Measure vs. Measure",
                            "Predictive modeling"
                        ]
                    }
                },
                "job_config" : {
                    "get_config" : {
                        "action" : "get_config",
                        "method" : "GET"
                    },
                    "job_name" : "test Measure",
                    "job_type" : "story",
                    "job_url" : "http://34.196.204.54:9012/api/job/master-test-measure-weiavw8kgj-5clrf2ywco/",
                    "message_url" : "http://34.196.204.54:9012/api/messages/Insight_test-measure-weiavw8kgj_123/",
                    "set_result" : {
                        "action" : "result",
                        "method" : "PUT"
                    }
                }

    }
    # storyConfig = {
    #         "config" : {
    #             "ADVANCED_SETTINGS" : {
    #                 "analysis" : [
    #                     {
    #                         "analysisSubTypes" : [],
    #                         "displayName" : "Overview",
    #                         "name" : "overview",
    #                         "noOfColumnsToUse" : None,
    #                         "status" : True
    #                     },
    #                     {
    #                         "analysisSubTypes" : [],
    #                         "displayName" : "Trend",
    #                         "name" : "trend",
    #                         "noOfColumnsToUse" : None,
    #                         "status" : False
    #                     },
    #                     {
    #                         "analysisSubTypes" : [],
    #                         "displayName" : "Performance",
    #                         "name" : "performance",
    #                         "noOfColumnsToUse" : [
    #                             {
    #                                 "defaultValue" : 3,
    #                                 "displayName" : "Low",
    #                                 "name" : "low",
    #                                 "status" : False
    #                             },
    #                             {
    #                                 "defaultValue" : 5,
    #                                 "displayName" : "Medium",
    #                                 "name" : "medium",
    #                                 "status" : False
    #                             },
    #                             {
    #                                 "defaultValue" : 8,
    #                                 "displayName" : "High",
    #                                 "name" : "high",
    #                                 "status" : False
    #                             },
    #                             {
    #                                 "defaultValue" : 3,
    #                                 "displayName" : "Custom",
    #                                 "name" : "custom",
    #                                 "status" : True,
    #                                 "value" : 15
    #                             }
    #                         ],
    #                         "status" : False
    #                     },
    #                     {
    #                         "analysisSubTypes" : [],
    #                         "displayName" : "Influencer",
    #                         "name" : "influencer",
    #                         "noOfColumnsToUse" : [
    #                             {
    #                                 "defaultValue" : 3,
    #                                 "displayName" : "Low",
    #                                 "name" : "low",
    #                                 "status" : False
    #                             },
    #                             {
    #                                 "defaultValue" : 5,
    #                                 "displayName" : "Medium",
    #                                 "name" : "medium",
    #                                 "status" : False
    #                             },
    #                             {
    #                                 "defaultValue" : 8,
    #                                 "displayName" : "High",
    #                                 "name" : "high",
    #                                 "status" : False
    #                             },
    #                             {
    #                                 "defaultValue" : 3,
    #                                 "displayName" : "Custom",
    #                                 "name" : "custom",
    #                                 "status" : True,
    #                                 "value" : 14
    #                             }
    #                         ],
    #                         "status" : False
    #                     },
    #                     {
    #                         "analysisSubTypes" : [],
    #                         "displayName" : "Prediction",
    #                         "name" : "prediction",
    #                         "noOfColumnsToUse" : None,
    #                         "status" : False
    #                     }
    #                 ]
    #             },
    #             "COLUMN_SETTINGS" : {
    #                 "analysis_type" : [
    #                     "measure"
    #                 ],
    #                 "consider_columns" : [
    #                     "Channel",
    #                     "Order_Item_Status_String",
    #                     "MTO_MTS",
    #                     "Ship_Address_City",
    #                     "Ship_Address_State",
    #                     "Source_Facility",
    #                     "Fulfilable_Facility",
    #                     "Payment_Method",
    #                     "Customer_Type",
    #                     "NPS_Score",
    #                     "order_month",
    #                     "order_day",
    #                     "Channel",
    #                     "Order_Item_Status_String",
    #                     "BEDS",
    #                     "OUTDOOR",
    #                     "MATTRESS",
    #                     "DINING - OTHERS",
    #                     "LIVING SEATING",
    #                     "DECOR",
    #                     "DINING",
    #                     "NOT_REQUIRED",
    #                     "LIVING ESSENTIALS",
    #                     "STUDY",
    #                     "WARDROBES",
    #                     "BEDROOM - OTHERS",
    #                     "KIDS",
    #                     "Selling_Price",
    #                     "Discount",
    #                     "Customer_Id",
    #                     "Ship_Address_Zipcode",
    #                     "Orderplaced_date"
    #                 ],
    #                 "consider_columns_type" : [
    #                     "including"
    #                 ],
    #                 "dateTimeSuggestions" : [
    #                     {
    #                         "Orderplaced_date" : "%m/%d/%Y"
    #                     }
    #                 ],
    #                 "date_columns" : [
    #                     "Orderplaced_date"
    #                 ],
    #                 "date_format" : None,
    #                 "ignore_column_suggestion" : [
    #                     "Order_Code"
    #                 ],
    #                 "polarity" : [
    #                     "positive"
    #                 ],
    #                 "result_column" : [
    #                     "Selling_Price"
    #                 ],
    #                 "utf8_column_suggestions" : []
    #             },
    #             "DATA_SOURCE" : {
    #                 "datasource_details" : "",
    #                 "datasource_type" : "fileUpload"
    #             },
    #             "FILE_SETTINGS" : {
    #                 "inputfile" : [
    #                     "file:///home/gulshan/marlabs/datasets/ul.csv"
    #                 ],
    #                 "script_to_run" : [
    #                     "Descriptive analysis",
    #                     "Trend",
    #                     "Measure vs. Dimension",
    #                     "Measure vs. Measure",
    #                     "Predictive modeling"
    #                 ],
    #                 "metadata" : {
    # 	                "slug_list" : [
    # 	                    "ulcsv-y85p2r4v43"
    # 	                ],
    # 	                "url" : "34.196.204.54:9012/api/get_metadata_for_mlscripts/"
    # 	            },
    #             }
    #         },
    #         "job_config" : {
    #             "get_config" : {
    #                 "action" : "get_config",
    #                 "method" : "GET"
    #             },
    #             "job_name" : "UL Analysis",
    #             "job_type" : "story",
    #             "job_url" : "http://madvisordev.marlabsai.com/api/job/master-credit-balance-mitali-9w9vpxv6oh-6wf67cym8h/",
    #             "message_url" : "http://luke.marlabsai.com:80/api/messages/Insight_ul-analysis-0k69xakvku_123/",
    #             "set_result" : {
    #                 "action" : "result",
    #                 "method" : "PUT"
    #             }
    #         }
    #     }

    return storyConfig

def get_metadata_config():
    metaDataConfig = {
        "config" : {
            "COLUMN_SETTINGS" : {
                "analysis_type" : [
                    "metaData"
                ]
            },
            "DATA_SOURCE" : {
                "datasource_details" : "",
                "datasource_type" : "fileUpload"
            },
            "DATE_SETTINGS" : {},
            "FILE_SETTINGS" : {
                "inputfile" : [
                    "file:///home/gulshan/marlabs/datasets/sigma/ignoreTest.csv"
                ]
            }
        },
        "job_config" : {
            "get_config" : {
                "action" : "get_config",
                "method" : "GET"
            },
            "job_name" : "Sample1.csv",
            "job_type" : "metaData",
            "message_url" : "http://34.196.204.54:9012/api/messages/Dataset_trend_gulshancsv-h85lh79ybd_123/",
            "job_url" : "http://34.196.204.54:9012/api/job/metadata-sample1csv-e2za8z9u26-o1f6wicswc/",
            "set_result" : {
                "action" : "result",
                "method" : "PUT"
            }
        }
    }
    return metaDataConfig

def get_training_config():
    # trainingConfig = {
    #     "config":{
    #         'FILE_SETTINGS': {
    #             'inputfile': ['file:///home/gulshan/marlabs/datasets/adult.csv'],
    #             # Model Slug will go instead of model path
    #             'modelpath': ["ANKUSH"],
    #             'train_test_split' : [0.8],
    #             'analysis_type' : ['training']
    #         },
    #         'COLUMN_SETTINGS': {
    #             'analysis_type': ['training'],
    #             'result_column': ['class_label'],
    #             'consider_columns_type': ['excluding'],
    #             'consider_columns':[],
    #             'polarity': ['positive'],
    #             'date_format': None,
    #             # 'date_columns':["new_date","Month","Order Date"],
    #             'date_columns':[],
    #             'ignore_column_suggestions': [],
    #             # 'ignore_column_suggestions': ["Outlet ID","Visibility to Cosumer","Cleanliness","Days to Resolve","Heineken Lager Share %","Issue Category","Outlet","Accessible_to_consumer","Resultion Status"],
    #             'dateTimeSuggestions' : [],
    #             'utf8ColumnSuggestion':[],
    #             'consider_columns':[],
    #         },
    #         "DATA_SOURCE" : {
    #             "datasource_details" : "",
    #             "datasource_type" : "fileUpload"
    #         }
    #     },
    #     "job_config":{
    #         "get_config" : {
    #             "action" : "get_config",
    #             "method" : "GET"
    #         },
    #         "job_name" : "Sample1.csv",
    #         "job_type":"training",
    #         "message_url" : "http://34.196.204.54:9012/api/messages/Dataset_trend_gulshancsv-h85lh79ybd_123/",
    #         # "job_url": "http://localhost:8000/api/job/dataset-iriscsv-qpmercq3r8-2fjupdcwdu/",
    #         "job_url": "http://localhost:8000/api/job/dataset-iriscsv-qpmercq3r8-2fjupdcwdu/",
    #         "set_result": {
    #             "method": "PUT",
    #             "action": "result"
    #           },
    #     }
    # }
    trainingConfig = {
        "config" : {
            "COLUMN_SETTINGS" : {
                "consider_columns" : [
                    "Channel",
                    "MTO_MTS",
                    "City",
                    "State",
                    "Source_Facility",
                    "Payment_Method",
                    "Customer_Type",
                    "order_month",
                    "order_day",
                    "Order_Item_Status_String",
                    "BEDS",
                    "OUTDOOR",
                    "MATTRESS",
                    "DINING - OTHERS",
                    "LIVING SEATING",
                    "DECOR",
                    "DINING",
                    "LIVING ESSENTIALS",
                    "STUDY",
                    "WARDROBES",
                    "BEDROOM - OTHERS",
                    "KIDS",
                    "Sales Amount"
                ],
                "consider_columns_type" : [
                    "including"
                ],
                "dateTimeSuggestions" : [
                    {}
                ],
                "date_columns" : [],
                "date_format" : None,
                "ignore_column_suggestion" : [
                ],
                "polarity" : [
                    "positive"
                ],
                "result_column" : [
                    "Order_Item_Status_String"
                ],
                "utf8_column_suggestions" : []
            },
            "DATA_SOURCE" : {
                "datasource_details" : "",
                "datasource_type" : "fileUpload"
            },
            "FILE_SETTINGS" : {
                "analysis_type" : [
                    "training"
                ],
                "inputfile" : [
                    "file:///home/gulshan/marlabs/datasets/ul_5050.csv"
                ],
                "modelpath" : [
                    "ggop-4b7ztc3rmn"
                ],
                "train_test_split" : [
                    0.71
                ]
            }
        },
        "job_config" : {
            "get_config" : {
                "action" : "get_config",
                "method" : "GET"
            },
            "job_name" : "ggop",
            "job_type" : "training",
            "job_url" : "http://34.196.204.54:9012/api/job/model-ggop-4b7ztc3rmn-9tesfpqui8/",
            "message_url" : "http://34.196.204.54:9012/api/messages/Trainer_ggop-4b7ztc3rmn_123/",
            "set_result" : {
                "action" : "result",
                "method" : "PUT"
            }
        }
    }
    return trainingConfig

def get_prediction_config():
    predictionConfig = {
        "config":{
            'FILE_SETTINGS': {
                'inputfile': ['file:///home/gulshan/marlabs/datasets/adult_test.csv'],
                'modelpath': ["ANKUSH"],
                'scorepath': ["DDDDD"],
                # 'train_test_split' : [0.8],
                'levelcounts' : [],
                'modelfeatures' : [],
                "algorithmslug":["f77631ce2ab24cf78c55bb6a5fce4db8rf"],
            },
            'COLUMN_SETTINGS': {
                'analysis_type': ['Dimension'],
                'result_column': ['class_label'],
                # 'consider_columns_type': ['excluding'],
                # 'consider_columns':[],
                # 'date_columns':['Date'],
                'score_consider_columns_type': ['excluding'],
                'score_consider_columns':[],
                "app_id":[2]

            },
            "DATA_SOURCE" : {
                "datasource_details" : "",
                "datasource_type" : "fileUpload"
            },
        },
        "job_config":{
            "get_config" : {
                "action" : "get_config",
                "method" : "GET"
            },
            "job_name" : "Sample1",
            "job_type":"prediction",
            "job_url": "http://34.196.204.54:9012/api/job/score-hiohoyuo-bn1ofiupv0-j0irk37cob/set_result/",
            "message_url" : "http://34.196.204.54:9012/api/messages/Dataset_trend_gulshancsv-h85lh79ybd_123/",
            "set_result": {
                "method": "PUT",
                "action": "result"
              },
        }
    }
    return predictionConfig

def get_subsetting_config():
    subsettingConfig = {
        "config" : {
                    "COLUMN_SETTINGS" : {
                        "analysis_type" : [
                            "metaData"
                        ]
                    },
                    "DATA_SOURCE" : {
                        "datasource_details" : "",
                        "datasource_type" : "fileUpload"
                    },
                    "DATE_SETTINGS" : {},
                    "FILE_SETTINGS" : {
                        "inputfile" : [
                            # "hdfs://ec2-34-205-203-38.compute-1.amazonaws.com:8020/dev/dataset/subsetting_testcsv-zxhdwhl5u2/subsetting_test_3n3aZh5.csv"
                            "file:///home/gulshan/marlabs/datasets/subsetting_test.csv"
                        ],
                        "outputfile" : [
                            # "hdfs://ec2-34-205-203-38.compute-1.amazonaws.com:8020/dev/dataset/subsetting_test_new-tqj35ger3q"
                            "file:///home/gulshan/marlabs/csvout/data"
                        ]
                    },
                    "FILTER_SETTINGS" : {
                        "dimensionColumnFilters" : [],
                        "measureColumnFilters" : [],
                        "timeDimensionColumnFilters" : []
                    },
                    "TRANSFORMATION_SETTINGS" : {
                        "existingColumns" : [
                            {
                                "columnSetting" : [
                                    {
                                        "actionName" : "delete",
                                        "displayName" : "Delete Column",
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "rename",
                                        "displayName" : "Rename Column",
                                        "newName" : None,
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "replace",
                                        "displayName" : "Replace Values",
                                        "replaceTypeList" : [
                                            {
                                                "displayName" : "Contains",
                                                "name" : "contains"
                                            },
                                            {
                                                "displayName" : "Equal To",
                                                "name" : "equals"
                                            },
                                            {
                                                "displayName" : "Starts With",
                                                "name" : "startsWith"
                                            },
                                            {
                                                "displayName" : "Ends With",
                                                "name" : "endsWith"
                                            }
                                        ],
                                        "replacementValues" : [],
                                        "status" : False
                                    }
                                ],
                                "name" : "CREDIT_BALANCE1",
                                "slug" : "167338ffe707492a9a2f0667ecc26a13"
                            },
                            {
                                "columnSetting" : [
                                    {
                                        "actionName" : "delete",
                                        "displayName" : "Delete Column",
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "rename",
                                        "displayName" : "Rename Column",
                                        "newName" : None,
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "replace",
                                        "displayName" : "Replace Values",
                                        "replaceTypeList" : [
                                            {
                                                "displayName" : "Contains",
                                                "name" : "contains"
                                            },
                                            {
                                                "displayName" : "Equal To",
                                                "name" : "equals"
                                            },
                                            {
                                                "displayName" : "Starts With",
                                                "name" : "startsWith"
                                            },
                                            {
                                                "displayName" : "Ends With",
                                                "name" : "endsWith"
                                            }
                                        ],
                                        "replacementValues" : [],
                                        "status" : False
                                    }
                                ],
                                "name" : "CREDIT_BALANCE2",
                                "slug" : "8b94ae1a2fa54e14b6602ac25344085f"
                            },
                            {
                                "columnSetting" : [
                                    {
                                        "actionName" : "delete",
                                        "displayName" : "Delete Column",
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "rename",
                                        "displayName" : "Rename Column",
                                        "newName" : None,
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "replace",
                                        "displayName" : "Replace Values",
                                        "replaceTypeList" : [
                                            {
                                                "displayName" : "Contains",
                                                "name" : "contains"
                                            },
                                            {
                                                "displayName" : "Equal To",
                                                "name" : "equals"
                                            },
                                            {
                                                "displayName" : "Starts With",
                                                "name" : "startsWith"
                                            },
                                            {
                                                "displayName" : "Ends With",
                                                "name" : "endsWith"
                                            }
                                        ],
                                        "replacementValues" : [],
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "data_type",
                                        "displayName" : "Change Datatype",
                                        "listOfActions" : [
                                            {
                                                "displayName" : "Numeric",
                                                "name" : "numeric",
                                                "status" : True
                                            },
                                            {
                                                "displayName" : "Text",
                                                "name" : "text",
                                                "status" : False
                                            }
                                        ],
                                        "status" : True
                                    }
                                ],
                                "name" : "CREDIT_BALANCE3",
                                "slug" : "684126299d4742c58ca9b460e5ff43a1"
                            },
                            {
                                "columnSetting" : [
                                    {
                                        "actionName" : "delete",
                                        "displayName" : "Delete Column",
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "rename",
                                        "displayName" : "Rename Column",
                                        "newName" : None,
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "replace",
                                        "displayName" : "Replace Values",
                                        "replaceTypeList" : [
                                            {
                                                "displayName" : "Contains",
                                                "name" : "contains"
                                            },
                                            {
                                                "displayName" : "Equal To",
                                                "name" : "equals"
                                            },
                                            {
                                                "displayName" : "Starts With",
                                                "name" : "startsWith"
                                            },
                                            {
                                                "displayName" : "Ends With",
                                                "name" : "endsWith"
                                            }
                                        ],
                                        "replacementValues" : [],
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "data_type",
                                        "displayName" : "Change Datatype",
                                        "listOfActions" : [
                                            {
                                                "displayName" : "Numeric",
                                                "name" : "numeric",
                                                "status" : False
                                            },
                                            {
                                                "displayName" : "Text",
                                                "name" : "text",
                                                "status" : False
                                            }
                                        ],
                                        "status" : False
                                    }
                                ],
                                "name" : "SEX",
                                "slug" : "27aadfb44d8f4fcc837654316e9b1bf4"
                            },
                            {
                                "columnSetting" : [
                                    {
                                        "actionName" : "delete",
                                        "displayName" : "Delete Column",
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "rename",
                                        "displayName" : "Rename Column",
                                        "newName" : None,
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "replace",
                                        "displayName" : "Replace Values",
                                        "replaceTypeList" : [
                                            {
                                                "displayName" : "Contains",
                                                "name" : "contains"
                                            },
                                            {
                                                "displayName" : "Equal To",
                                                "name" : "equals"
                                            },
                                            {
                                                "displayName" : "Starts With",
                                                "name" : "startsWith"
                                            },
                                            {
                                                "displayName" : "Ends With",
                                                "name" : "endsWith"
                                            }
                                        ],
                                        "replacementValues" : [],
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "data_type",
                                        "displayName" : "Change Datatype",
                                        "listOfActions" : [
                                            {
                                                "displayName" : "Numeric",
                                                "name" : "numeric",
                                                "status" : False
                                            },
                                            {
                                                "displayName" : "Text",
                                                "name" : "text",
                                                "status" : False
                                            }
                                        ],
                                        "status" : False
                                    }
                                ],
                                "name" : "EDUCATION",
                                "slug" : "c5c42c0f7b3a4632bd7e0269f998ec30"
                            },
                            {
                                "columnSetting" : [
                                    {
                                        "actionName" : "delete",
                                        "displayName" : "Delete Column",
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "rename",
                                        "displayName" : "Rename Column",
                                        "newName" : None,
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "replace",
                                        "displayName" : "Replace Values",
                                        "replaceTypeList" : [
                                            {
                                                "displayName" : "Contains",
                                                "name" : "contains"
                                            },
                                            {
                                                "displayName" : "Equal To",
                                                "name" : "equals"
                                            },
                                            {
                                                "displayName" : "Starts With",
                                                "name" : "startsWith"
                                            },
                                            {
                                                "displayName" : "Ends With",
                                                "name" : "endsWith"
                                            }
                                        ],
                                        "replacementValues" : [],
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "data_type",
                                        "displayName" : "Change Datatype",
                                        "listOfActions" : [
                                            {
                                                "displayName" : "Numeric",
                                                "name" : "numeric",
                                                "status" : False
                                            },
                                            {
                                                "displayName" : "Text",
                                                "name" : "text",
                                                "status" : False
                                            }
                                        ],
                                        "status" : False
                                    }
                                ],
                                "name" : "MARRIAGE",
                                "slug" : "800b2f543eb5455a8ffcbc48bcdc0abf"
                            },
                            {
                                "columnSetting" : [
                                    {
                                        "actionName" : "delete",
                                        "displayName" : "Delete Column",
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "rename",
                                        "displayName" : "Rename Column",
                                        "newName" : None,
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "replace",
                                        "displayName" : "Replace Values",
                                        "replaceTypeList" : [
                                            {
                                                "displayName" : "Contains",
                                                "name" : "contains"
                                            },
                                            {
                                                "displayName" : "Equal To",
                                                "name" : "equals"
                                            },
                                            {
                                                "displayName" : "Starts With",
                                                "name" : "startsWith"
                                            },
                                            {
                                                "displayName" : "Ends With",
                                                "name" : "endsWith"
                                            }
                                        ],
                                        "replacementValues" : [],
                                        "status" : False
                                    }
                                ],
                                "name" : "new_date",
                                "slug" : "5e1fb20628d04549970d84da96fcb60e"
                            },
                            {
                                "columnSetting" : [
                                    {
                                        "actionName" : "delete",
                                        "displayName" : "Delete Column",
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "rename",
                                        "displayName" : "Rename Column",
                                        "newName" : None,
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "replace",
                                        "displayName" : "Replace Values",
                                        "replaceTypeList" : [
                                            {
                                                "displayName" : "Contains",
                                                "name" : "contains"
                                            },
                                            {
                                                "displayName" : "Equal To",
                                                "name" : "equals"
                                            },
                                            {
                                                "displayName" : "Starts With",
                                                "name" : "startsWith"
                                            },
                                            {
                                                "displayName" : "Ends With",
                                                "name" : "endsWith"
                                            }
                                        ],
                                        "replacementValues" : [],
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "data_type",
                                        "displayName" : "Change Datatype",
                                        "listOfActions" : [
                                            {
                                                "displayName" : "Numeric",
                                                "name" : "numeric",
                                                "status" : False
                                            },
                                            {
                                                "displayName" : "Text",
                                                "name" : "text",
                                                "status" : False
                                            }
                                        ],
                                        "status" : False
                                    }
                                ],
                                "name" : "colToReplace",
                                "slug" : "d8f87c8c454f4aae992a0f05cc9b2edb"
                            },
                            {
                                "columnSetting" : [
                                    {
                                        "actionName" : "delete",
                                        "displayName" : "Delete Column",
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "rename",
                                        "displayName" : "Rename Column",
                                        "newName" : None,
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "replace",
                                        "displayName" : "Replace Values",
                                        "replaceTypeList" : [
                                            {
                                                "displayName" : "Contains",
                                                "name" : "contains"
                                            },
                                            {
                                                "displayName" : "Equal To",
                                                "name" : "equals"
                                            },
                                            {
                                                "displayName" : "Starts With",
                                                "name" : "startsWith"
                                            },
                                            {
                                                "displayName" : "Ends With",
                                                "name" : "endsWith"
                                            }
                                        ],
                                        "replacementValues" : [],
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "data_type",
                                        "displayName" : "Change Datatype",
                                        "listOfActions" : [
                                            {
                                                "displayName" : "Numeric",
                                                "name" : "numeric",
                                                "status" : False
                                            },
                                            {
                                                "displayName" : "Text",
                                                "name" : "text",
                                                "status" : False
                                            }
                                        ],
                                        "status" : False
                                    }
                                ],
                                "name" : "toDelete",
                                "slug" : "28b1ba754bfa4782a644ed93357cf1e9"
                            },
                            {
                                "columnSetting" : [
                                    {
                                        "actionName" : "delete",
                                        "displayName" : "Delete Column",
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "rename",
                                        "displayName" : "Rename Column",
                                        "newName" : None,
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "replace",
                                        "displayName" : "Replace Values",
                                        "replaceTypeList" : [
                                            {
                                                "displayName" : "Contains",
                                                "name" : "contains"
                                            },
                                            {
                                                "displayName" : "Equal To",
                                                "name" : "equals"
                                            },
                                            {
                                                "displayName" : "Starts With",
                                                "name" : "startsWith"
                                            },
                                            {
                                                "displayName" : "Ends With",
                                                "name" : "endsWith"
                                            }
                                        ],
                                        "replacementValues" : [],
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "data_type",
                                        "displayName" : "Change Datatype",
                                        "listOfActions" : [
                                            {
                                                "displayName" : "Numeric",
                                                "name" : "numeric",
                                                "status" : False
                                            },
                                            {
                                                "displayName" : "Text",
                                                "name" : "text",
                                                "status" : False
                                            }
                                        ],
                                        "status" : False
                                    }
                                ],
                                "name" : "toReplace",
                                "slug" : "e628974095ce42de8e5114976979db0e"
                            }
                        ]
                    }
                },
                "job_config" : {
                    "get_config" : {
                        "action" : "get_config",
                        "method" : "GET"
                    },
                    "job_name" : "subsetting_test_new",
                    "job_type" : "subSetting",
                    "job_url" : "http://34.196.204.54:9012/api/job/subsetting-subsetting_test_new-tqj35ger3q-bp9kq1alzn/",
                    "message_url" : "http://34.196.204.54:9012/api/messages/Dataset_subsetting_test_new-tqj35ger3q_123/",
                    "set_result" : {
                        "action" : "result",
                        "method" : "PUT"
                    }
                }
    }
    return subsettingConfig

def get_stockadvisor_config():
    stockAdvisorConfig = {
        'job_config': {
          'job_url': 'http://34.196.204.54:9012/api/job/stockadvisor-stocking_is_what_i_do-6ryt9x72e8-ynolqb82hb/',
          'job_type': 'stockAdvisor',
          'set_result': {
            'action': 'result',
            'method': 'PUT'
          },
          'get_config': {
            'action': 'get_config',
            'method': 'GET'
          },
          'message_url': 'http://34.196.204.54:9012/api/messages/StockDataset_stocking_is_what_i_do-6ryt9x72e8_123/',
          'job_name': u'stocking_is_what_i_do'
        },
        u'config': {
          u'COLUMN_SETTINGS': {
            u'analysis_type': [
              u'metaData'
            ]
          },
          u'DATE_SETTINGS': {

          },
          u'DATA_SOURCE': {
            u'datasource_details': u''
          },
          u'STOCK_SETTINGS': {
            u'stockSymbolList': [
              'googl','appl'
            ],
            u'dataAPI': 'http://34.196.204.54:9012/api/stockdatasetfiles/stocking_is_what_i_do-imlizu9xul/',
          },
          u'FILE_SETTINGS': {
            u'inputfile': [
              u''
            ]
          }
        }
      }
    return stockAdvisorConfig

def get_test_configs(jobType):
    testConfigs = {
        "story"        : get_story_config(),
        "metaData"     : get_metadata_config(),
        "training"     : get_training_config(),
        "prediction"   : get_prediction_config(),
        "subSetting"   : get_subsetting_config(),
        "stockAdvisor" : get_stockadvisor_config()
    }
    return testConfigs[jobType]
