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
                        "displayName" : "Performance",
                        "name" : "performance",
                        "noOfColumnsToUse" : [
                            {
                                "defaultValue" : 3,
                                "displayName" : "Low",
                                "name" : "low",
                                "status" : True
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
                                "status" : False
                            },
                            {
                                "defaultValue" : 3,
                                "displayName" : "Custom",
                                "name" : "custom",
                                "status" : False,
                                "value" : 12
                            }
                        ],
                        "status" : True
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
                                "status" : True
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
                                "status" : False
                            },
                            {
                                "defaultValue" : 3,
                                "displayName" : "Custom",
                                "name" : "custom",
                                "status" : False,
                                "value" : 12
                            }
                        ],
                        "status" : False
                    },
                    {
                        "analysisSubTypes" : [],
                        "displayName" : "Association",
                        "name" : "association",
                        "noOfColumnsToUse" : [
                            {
                                "defaultValue" : 3,
                                "displayName" : "Low",
                                "name" : "low",
                                "status" : True
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
                                "status" : False
                            },
                            {
                                "defaultValue" : 3,
                                "displayName" : "Custom",
                                "name" : "custom",
                                "status" : False,
                                "value" : 12
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
                ]
            },
            "COLUMN_SETTINGS" : {
                "customAnalysisDetails":[
                                # {"colName":"Marketing_Cost"},
                            ],
                "analysis_type" : [
                    "measure"
                ],
                "consider_columns" : [
                    "Channel",
                    "Order Status",
                    "City",
                    "State",
                    "Replacement_Cancellation_Reason",
                    "Payment_Method",
                    "Customer_Type",
                    "order_month",
                    "order_day",
                    "BEDS",
                    "OUTDOOR",
                    "MATTRESS",
                    "DINING - OTHERS",
                    "LIVING SEATING",
                    "DECOR",
                    "DINING",
                    "NOT_REQUIRED",
                    "LIVING ESSENTIALS",
                    "STUDY",
                    "WARDROBES",
                    "BEDROOM - OTHERS",
                    "KIDS",
                    "Sales Amount",
                    "Discount",
                    "Customer_Id",
                    "Order Date"
                ],
                "consider_columns_type" : [
                    "including"
                ],
                "dateTimeSuggestions" : [
                    {
                        "Cancellation Date" : "%d-%m-%Y",
                        "Order Date" : "%d-%m-%Y"
                    }
                ],
                "date_columns" : [
                    "Order Date"
                ],
                "date_format" : None,
                "ignore_column_suggestion" : [
                    "Order_Code"
                ],
                "polarity" : [
                    "positive"
                ],
                "result_column" : [
                    "Sales Amount"
                ],
                "utf8_column_suggestions" : []
            },
            "DATA_SOURCE" : {
                "datasource_details" : "",
                "datasource_type" : "fileUpload"
            },
            "FILE_SETTINGS" : {
                "inputfile" : [
                    "/home/marlabs/Documents/mAdvisor/Datasets/ul_new.csv"
                ],
                "script_to_run" : [
                    "Descriptive analysis",
                    "Trend",
                    "Measure vs. Dimension",
                    "Measure vs. Measure",
                    "Predictive modeling"
                ],
                "metadata" : {
                    "slug_list" : [
                        "ul_newcsv-0topj3ub6k"
                    ],
                    "url" : "madvisordev.marlabsai.com:80/api/get_metadata_for_mlscripts/"
                },
            }
        },
        "job_config" : {
            "get_config" : {
                "action" : "get_config",
                "method" : "GET"
            },
            "job_name" : "UL Analysis",
            "job_type" : "story",
            "job_url" : "http://madvisordev.marlabsai.com/api/job/master-credit-balance-mitali-9w9vpxv6oh-6wf67cym8h/",
            "message_url" : "http://luke.marlabsai.com:80/api/messages/Insight_ul-analysis-0k69xakvku_123/",
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
