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
              "selected": True,
              "slug": "b465553e62634b3a9049565aa808b836",
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
              "slug": "5156a7313c92415cb902270b97294a3a",
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
              "slug": "4dbe0ed904e04bc490aa09a993da8d40",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": True,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "Discount_Range",
              "selected": True,
              "slug": "0f8c8798367a4a498d94303fc10776a9",
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
              "slug": "da2209dabde24dac9870630aef456c25",
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
              "slug": "eeeddb5c981e435294541b13ad8d2c0c",
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
              "slug": "078bd84618b5438d8079403976ff2f32",
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
              "slug": "58c3956d01494d6b835613bfd814a0e4",
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
              "slug": "1271ef6f3d6741e3875788c4705ec0b4",
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
              "slug": "c043c25c25b74a88aaba0b2f66f686cb",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "measure",
              "name": "Marketing_Cost",
              "selected": True,
              "slug": "510b3ec245a442688c2441e56c8f2809",
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
              "slug": "2dbc4acb9c354619b57564cec0f2456c",
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
              "slug": "326d9ce98c6a492dada6ef5297f7119e",
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
              "slug": "1459e32722d2458cbfcc54c4a95d8bbf",
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
          "trendSettings": [
            {
              "status": True,
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
            "Dimension vs. Dimension",
            "Predictive modeling"
          ],
          "metadata": {
            "url": "34.196.204.54:9012/api/get_metadata_for_mlscripts/",
            "slug_list": [
              "trend_gulshancsv-jhmf1af87a"
            ]
          },
          "inputfile": [
            "/home/marlabs/Downloads/trend_gulshan.csv"
          ]
        }
      },
      "job_config": {
        "message_url": "http://34.196.204.54:9012/api/messages/Job_master-checkk-qafujm74gk-0dxygkxoh7_123/",
        "get_config": {
          "action": "get_config",
          "method": "GET"
        },
        "error_reporting_url": "http://34.196.204.54:9012/api/set_job_report/master-checkk-qafujm74gk-0dxygkxoh7/",
        "set_result": {
          "action": "result",
          "method": "PUT"
        },
        "job_url": "http://34.196.204.54:9012/api/job/master-checkk-qafujm74gk-0dxygkxoh7/",
        "job_type": "story",
        "job_name": "checkk",
        "xml_url": "http://34.196.204.54:9012/api/xml/master-checkk-qafujm74gk-0dxygkxoh7/",
        "app_id": None
      }
    }
    return storyConfig
