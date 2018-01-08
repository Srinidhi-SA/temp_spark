def get_story_config():
    storyConfig = {
      "config": {
        "COLUMN_SETTINGS": {
          "polarity": [
            {
              "colSlug": "39c018d65d6d4cae9cc2cc229595661f",
              "polarity": "positive",
              "colName": "Tenure_in_Days"
            },
            {
              "colSlug": "5d36e79778ac4cd99e0221597888d286",
              "polarity": "positive",
              "colName": "Sales"
            },
            {
              "colSlug": "4a82908f2f334367a64fc31fe36431c2",
              "polarity": "positive",
              "colName": "Marketing_Cost"
            },
            {
              "colSlug": "181898e929bb4691a597ec1eae1c7dab",
              "polarity": "positive",
              "colName": "Shipping_Cost"
            },
            {
              "colSlug": "0a4fd0611f914598b13ccc53cdfe6b6d",
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
              "ecommercecsv-3l9blqooh7"
            ]
          },
          "inputfile": [
            "file:///home/gulshan/marlabs/datasets/sampleDatasets/ecommerce.csv"
          ]
        }
      },
      "job_config": {
        "message_url": "http://34.196.204.54:9012/api/messages/Job_master-dtree-chopped-wnb0pz9t2o-mlftwl2s17_123/",
        "get_config": {
          "action": "get_config",
          "method": "GET"
        },
        "error_reporting_url": "http://34.196.204.54:9012/api/set_job_report/master-dtree-chopped-wnb0pz9t2o-mlftwl2s17/",
        "set_result": {
          "action": "result",
          "method": "PUT"
        },
        "job_url": "http://34.196.204.54:9012/api/job/master-dtree-chopped-wnb0pz9t2o-mlftwl2s17/",
        "job_type": "story",
        "job_name": "dtree-chopped",
        "xml_url": "http://34.196.204.54:9012/api/xml/master-dtree-chopped-wnb0pz9t2o-mlftwl2s17/"
      }
    }
    return storyConfig
