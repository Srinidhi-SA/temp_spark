def get_story_config():
    storyConfig = {
    "job_config": {
      "job_url": "http://34.196.204.54:9012/api/job/master-measure-test1-gd721qkcc3-yjifx6qlwo/",
      "job_type": "story",
      "xml_url": "http://34.196.204.54:9012/api/xml/master-measure-test1-gd721qkcc3-yjifx6qlwo/",
      "error_reporting_url": "http://34.196.204.54:9012/api/set_job_report/master-error-check0-m302es9p2d-qm34cqk7mt/",
      "get_config": {
        "action": "get_config",
        "method": "GET"
      },
      "set_result": {
        "action": "result",
        "method": "PUT"
      },
      "message_url": "http://34.196.204.54:9012/api/messages/Insight_measure-test1-gd721qkcc3_123/",
      "job_name": "measure-test1"
    },
    "config": {
      "COLUMN_SETTINGS": {
        "polarity": [
          {
            "colSlug": "4f3e60f4e761481e9d153d44fddffb13",
            "polarity": "positive",
            "colName": "Tenure_in_Days"
          },
          {
            "colSlug": "7390904522104016922e7eeb00994fed",
            "polarity": "positive",
            "colName": "Sales"
          },
          {
            "colSlug": "475bf6e3b9c24021b5bae514c9b822bc",
            "polarity": "positive",
            "colName": "Marketing_Cost"
          },
          {
            "colSlug": "26e23e08ad1e491cbf567f444c844767",
            "polarity": "positive",
            "colName": "Shipping_Cost"
          },
          {
            "colSlug": "afaad041663c4c7091b1b3d870685eaf",
            "polarity": "positive",
            "colName": "Last_Transaction"
          }
        ],
        "date_format": None,
        "consider_columns_type": [
          "including"
        ],
        "customAnalysisDetails": [

        ],
        "result_column": [
          "Sales"
        ],
        "ignore_column_suggestion": [

        ],
        "consider_columns": [
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
        "utf8_column_suggestions": [

        ],
        "date_columns": [
          "new_date"
        ],
        "analysis_type": [
          "measure"
        ],
        "dateTimeSuggestions": [
          {
            "Order Date": "%d-%m-%Y",
            "Month": "%b-%y"
          }
        ]
      },
      "DATA_SOURCE": {
        "datasource_type": "fileUpload",
        "datasource_details": ""
      },
      "ADVANCED_SETTINGS": {
        "analysis": [
          {
            "status": True,
            "noOfColumnsToUse": None,
            "analysisSubTypes": [

            ],
            "displayName": "Overview",
            "name": "overview"
          },
          {
            "status": False,
            "noOfColumnsToUse": None,
            "analysisSubTypes": [
              {
                "status": False,
                "displayName": "Overview",
                "name": "overview"
              },
              {
                "status": False,
                "displayName": "Factors that drive up",
                "name": "factors that drive up"
              },
              {
                "status": False,
                "displayName": "Factors that drive down",
                "name": "factors that drive down"
              },
              {
                "status": False,
                "displayName": "Forecast",
                "name": "forecast"
              }
            ],
            "displayName": "Trend",
            "name": "trend"
          },
          {
            "status": False,
            "noOfColumnsToUse": [
              {
                "status": False,
                "defaultValue": 3,
                "displayName": "Low",
                "name": "low"
              },
              {
                "status": False,
                "defaultValue": 5,
                "displayName": "Medium",
                "name": "medium"
              },
              {
                "status": True,
                "defaultValue": 8,
                "displayName": "High",
                "name": "high"
              },
              {
                "status": False,
                "defaultValue": 3,
                "displayName": "Custom",
                "name": "custom",
                "value": None
              }
            ],
            "analysisSubTypes": [

            ],
            "displayName": "Performance",
            "name": "performance"
          },
          {
            "status": False,
            "noOfColumnsToUse": [
              {
                "status": False,
                "defaultValue": 3,
                "displayName": "Low",
                "name": "low"
              },
              {
                "status": False,
                "defaultValue": 5,
                "displayName": "Medium",
                "name": "medium"
              },
              {
                "status": True,
                "defaultValue": 8,
                "displayName": "High",
                "name": "high"
              },
              {
                "status": False,
                "defaultValue": 3,
                "displayName": "Custom",
                "name": "custom",
                "value": None
              }
            ],
            "analysisSubTypes": [

            ],
            "displayName": "Influencer",
            "name": "influencer"
          },
          {
            "status": False,
            "noOfColumnsToUse": None,
            "analysisSubTypes": [

            ],
            "displayName": "Prediction",
            "name": "prediction"
          }
        ]
      },
      "FILE_SETTINGS": {
        "script_to_run": [
          "Descriptive analysis",
          "Trend",
          "Measure vs. Dimension",
          "Measure vs. Measure",
          "Predictive modeling"
        ],
        "metadata": {
          "url": "34.196.204.54:9012/api/get_metadata_for_mlscripts/",
          "slug_list": [
            "trend_gulshancsv-zuxmcvv8lu"
          ]
        },
        "inputfile": [
          "file:///home/gulshan/marlabs/datasets/trend_gulshan.csv"
        ]
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
