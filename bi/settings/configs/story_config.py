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
                                "status" : True
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
                                "status" : False
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
                                "status" : True,
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
                            "measure"
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
                            "Order Date"
                        ],
                        "date_format" : None,
                        "ignore_column_suggestion" : [],
                        "polarity" : [
                            "positive"
                        ],
                        "result_column" : [
                            "Sales"
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
