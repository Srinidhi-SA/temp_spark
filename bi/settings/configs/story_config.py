def get_story_config():
    storyConfig = {
        "job_config": {
          "message_url": "http://34.196.204.54:9012/api/messages/Job_master-dtree-dims-jm4f6iota6-nbyyp3ld0k_123/",
          "get_config": {
            "action": "get_config",
            "method": "GET"
          },
          "error_reporting_url": "http://34.196.204.54:9012/api/set_job_report/master-dtree-dims-jm4f6iota6-nbyyp3ld0k/",
          "set_result": {
            "action": "result",
            "method": "PUT"
          },
          "job_url": "http://34.196.204.54:9012/api/job/master-dtree-dims-jm4f6iota6-nbyyp3ld0k/",
          "job_type": "story",
          "job_name": "dtree-dims",
          "xml_url": "http://34.196.204.54:9012/api/xml/master-dtree-dims-jm4f6iota6-nbyyp3ld0k/"
        },
        "config": {
          "COLUMN_SETTINGS": {
            "polarity": [
              {
                "colSlug": "416c3889bd044d1ba8fe7ad94b53feb2",
                "polarity": "positive",
                "colName": "Tenure_in_Days"
              },
              {
                "colSlug": "948a3583116d414998ade3d4a5782a40",
                "polarity": "positive",
                "colName": "Sales"
              },
              {
                "colSlug": "8b2b24e7fd274bf48365963e261bc66e",
                "polarity": "positive",
                "colName": "Marketing_Cost"
              },
              {
                "colSlug": "8a0a5135473241d7af1a7ca91b6774e7",
                "polarity": "positive",
                "colName": "Shipping_Cost"
              },
              {
                "colSlug": "185ed7989464496a9d82b54c102e2e16",
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
              "Platform"
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
              "dimension"
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
            "trendSettings": [
              {
                "status": False,
                "name": "Count"
              },
              {
                "status": False,
                "name": "Specific Measure",
                "selectedMeasure": None
              }
            ],
            "targetLevels": [
              [

              ]
            ],
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
                "displayName": "Association",
                "name": "association",
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
                    "status": False,
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
                "binSetting": [
                  {
                    "displayName": "Binning of Numerical Values",
                    "name": "heading"
                  },
                  {
                    "displayName": "Number of Bin Levels",
                    "name": "binLevels",
                    "min": 2,
                    "max": 10,
                    "defaultValue": 5,
                    "value": 5
                  },
                  {
                    "displayName": "Do not bin numerical values with cardinality less than:",
                    "name": "binCardinality",
                    "min": 2,
                    "max": 10,
                    "defaultValue": 5,
                    "value": 5
                  }
                ]
              },
              {
                "status": True,
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
              "Predictive modeling"
            ],
            "metadata": {
              "url": "34.196.204.54:9012/api/get_metadata_for_mlscripts/",
              "slug_list": [
                "ecommercecsv-ttkyjgl2q8"
              ]
            },
            "inputfile": [
              "file:///home/gulshan/marlabs/datasets/sampleDatasets/ecommerce.csv"
            ]
          }
        }
      }
    return storyConfig
