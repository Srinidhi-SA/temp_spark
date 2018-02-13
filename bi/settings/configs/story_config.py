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
              "slug": "1079d9b5c92347a38eb33a904ad53627",
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
              "slug": "e9f4f6c23dcc4b1cba7d91a3de1ec3f9",
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
              "slug": "9ab12704c7d44fb6890e6e269e55f1ab",
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
              "slug": "7a9aa516250e43daba1c6d786874179b",
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
              "slug": "478c24a1f5804c6e90f519acc8d66a9f",
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
              "slug": "709d6190aafd492eb604fa527f206ab6",
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
              "slug": "5d15dde176674e8faf48c3e50075e531",
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
              "slug": "0e5e67cf60ef4b23aaba9f266fe9381b",
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
              "slug": "9b0122df3dc7436ea7760b99eca928b6",
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
              "slug": "01fde3e8a3484394813838187ca5428e",
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
              "slug": "dcf2b5a6f9ba43229277c5b6ec1f4046",
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
              "slug": "518af3f3b4d04a1ba2a2fb9a141570eb",
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
              "slug": "872b7fa6a95748cca4479cf0010acf89",
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
              "slug": "14b79f01e5a0492fb00d18bbe29585c8",
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
              "slug": "eaace674d7114dd4b31273f83a594d51",
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
              "displayName": "Influencer",
              "name": "influencer"
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
            "Measure vs. Dimension",
            "Measure vs. Measure",
            "Predictive modeling"
          ],
          "metadata": {
            "url": "34.196.204.54:9012/api/get_metadata_for_mlscripts/",
            "slug_list": [
              "ecommercecsv-ldkbiz9ql7"
            ]
          },
          "inputfile": [
            "file:///home/gulshan/marlabs/datasets/sampleDatasets/ecommerce.csv"
          ]
        }
      },
      "job_config": {
        "message_url": "http://34.196.204.54:9012/api/messages/Job_master-measure1-hpocudew8z-hfuxcdzch9_123/",
        "get_config": {
          "action": "get_config",
          "method": "GET"
        },
        "error_reporting_url": "http://34.196.204.54:9012/api/set_job_report/master-measure1-hpocudew8z-hfuxcdzch9/",
        "set_result": {
          "action": "result",
          "method": "PUT"
        },
        "job_url": "http://34.196.204.54:9012/api/job/master-measure1-hpocudew8z-hfuxcdzch9/",
        "job_type": "story",
        "job_name": "measure1",
        "xml_url": "http://34.196.204.54:9012/api/xml/master-measure1-hpocudew8z-hfuxcdzch9/",
        "app_id": None
      }
    }
    return storyConfig
