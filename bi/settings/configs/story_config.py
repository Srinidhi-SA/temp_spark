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
              "slug": "5272ccdcaec24492b5c523d1311c8717",
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
              "selected": False,
              "slug": "7c6130e5fd1141c08971feb22cacf93d",
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
              "selected": False,
              "slug": "96728e8d3bd846bb89fbe059c8bbb73b",
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
              "selected": False,
              "slug": "c6a2db5490fc4daba6c72f31d80513c4",
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
              "slug": "806429707f9d40ccbb9ce0943ee61db1",
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
              "slug": "9223ecc8d7be47ff84a9bc646498c053",
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
              "slug": "a7c74ae2cb37457ca163abf017195f6a",
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
              "slug": "a02f0a973077437d84a4b2d46002f6ef",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": "percentage",
              "columnType": "measure",
              "name": "Tenure_in_Days",
              "selected": True,
              "slug": "660fed948e294e2c8fb474f0585b876d",
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
              "slug": "d672239d8d6d4fc5b325e1fc794c8140",
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
              "selected": False,
              "slug": "0210c1186c1c44e1bd00a1dc9c682fd4",
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
              "slug": "4406af5bf3b94ab6b95ecb1406ac73ee",
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
              "slug": "6938b51355fb49c388a913ef3ef0e5bb",
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
              "slug": "2789cdcad08144f2a24c4400c217dc5c",
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
              "slug": "c3c95c5898774aec9738ae58a702c563",
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
              "analysisSubTypes": [
                
              ],
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
              "displayName": "Influencer",
              "name": "influencer"
            },
            {
              "status": False,
              "displayName": "Prediction",
              "name": "prediction",
              "noOfColumnsToUse": None,
              "analysisSubTypes": [
                
              ],
              "levelSetting": [
                
              ]
            }
          ]
        },
        "FILE_SETTINGS": {
          "script_to_run": [
            "Descriptive analysis",
            "Trend",
            "Measure vs. Dimension"
          ],
          "metadata": {
            "url": "34.196.204.54:9012/api/get_metadata_for_mlscripts/",
            "slug_list": [
              "trend_gulshancsv-19w5noe3sl"
            ]
          },
          "inputfile": [
            "/home/marlabs/Downloads/trend_gulshan.csv"
          ]
        }
      },
      "job_config": {
        "message_url": "http://34.196.204.54:9012/api/messages/Job_master-set_var_cent-7j69gmmxls-m09k2qapti_123/",
        "get_config": {
          "action": "get_config",
          "method": "GET"
        },
        "error_reporting_url": "http://34.196.204.54:9012/api/set_job_report/master-set_var_cent-7j69gmmxls-m09k2qapti/",
        "set_result": {
          "action": "result",
          "method": "PUT"
        },
        "job_url": "http://34.196.204.54:9012/api/job/master-set_var_cent-7j69gmmxls-m09k2qapti/",
        "job_type": "story",
        "job_name": "Set_Var_Cent",
        "xml_url": "http://34.196.204.54:9012/api/xml/master-set_var_cent-7j69gmmxls-m09k2qapti/",
        "app_id": None
      }
    }
    return storyConfig
