def get_story_config():
    storyConfig = {
      "config": {
        "COLUMN_SETTINGS": {
          "variableSelection": [
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "Month",
              "selected": False,
              "slug": "4342fa163f3a4108a376222a2326505d",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": True,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "Deal_Type",
              "selected": True,
              "slug": "e0f9557403654dbdbeacf9397a1fc693",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "Price_Range",
              "selected": True,
              "slug": "5d67416f5bab466bbc251234309bb6bb",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "Discount_Range",
              "selected": True,
              "slug": "cb927a057fd34bb7babefc52ded78536",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "Source",
              "selected": True,
              "slug": "1bcb4b9d51d44a83b626f56fe004f73e",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "Platform",
              "selected": True,
              "slug": "2df287170deb48a9a1f5c7291bcda9ee",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "Buyer_Age",
              "selected": True,
              "slug": "ce2e6a55ff9446d9a680b5aef3db433d",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "Buyer_Gender",
              "selected": True,
              "slug": "578e6bd338074b12ad70a3fb9d25109b",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "measure",
              "name": "Tenure_in_Days",
              "selected": True,
              "slug": "39c018d65d6d4cae9cc2cc229595661f",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "measure",
              "name": "Sales",
              "selected": True,
              "slug": "5d36e79778ac4cd99e0221597888d286",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": True,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "measure",
              "name": "Marketing_Cost",
              "selected": True,
              "slug": "4a82908f2f334367a64fc31fe36431c2",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "measure",
              "name": "Shipping_Cost",
              "selected": True,
              "slug": "181898e929bb4691a597ec1eae1c7dab",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "measure",
              "name": "Last_Transaction",
              "selected": True,
              "slug": "0a4fd0611f914598b13ccc53cdfe6b6d",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "datetime",
              "name": "new_date",
              "selected": True,
              "slug": "57016c35904640ff8cf45d70a780041d",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "Order Date",
              "selected": False,
              "slug": "d1ab01e4118749e085e426233be4bb4d",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": True,
              "targetColumn": False,
              "uidCol": False
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
              "analysisSubTypes": [],
              "displayName": "Overview",
              "name": "overview"
            },
            {
              "status": True,
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
              "status": True,
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
              "analysisSubTypes": [],
              "displayName": "Performance",
              "name": "performance"
            },
            {
              "status": True,
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
              "analysisSubTypes": [],
              "displayName": "Influencer",
              "name": "influencer"
            },
            {
              "status": True,
              "displayName": "Prediction",
              "name": "prediction",
              "noOfColumnsToUse": None,
              "analysisSubTypes": [],
              "levelSetting": []
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
              "ecommercecsv-3l9blqooh7"
            ]
          },
          "inputfile": [
            "file:///home/gulshan/marlabs/datasets/sampleDatasets/ecommerce.csv"
          ]
        }
      },
      "job_config": {
        "message_url": "http://34.196.204.54:9012/api/messages/Job_master-lll-75f3939i95-ptlhsocwja_123/",
        "get_config": {
          "action": "get_config",
          "method": "GET"
        },
        "error_reporting_url": "http://34.196.204.54:9012/api/set_job_report/master-lll-75f3939i95-ptlhsocwja/",
        "set_result": {
          "action": "result",
          "method": "PUT"
        },
        "job_url": "http://34.196.204.54:9012/api/job/master-lll-75f3939i95-ptlhsocwja/",
        "job_type": "story",
        "job_name": "lll",
        "xml_url": "http://34.196.204.54:9012/api/xml/master-lll-75f3939i95-ptlhsocwja/",
        "app_id": None
      }
    }
    return storyConfig
