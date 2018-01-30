def get_story_config():
    storyConfig = {
      "config": {
        "COLUMN_SETTINGS": {
          "variableSelection": [
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "measure",
              "name": "Call Volume",
              "selected": True,
              "slug": "6fd94da3149b4fc18bf9a5d82ece2a06",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "measure",
              "name": "First call resolution",
              "selected": True,
              "slug": "e101ecf97ff94df5b74a3d0bdf36bedf",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "measure",
              "name": "Average Call duration (in Minutes)",
              "selected": True,
              "slug": "ea0554416e66490a889d21702bfcd215",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "datetime",
              "name": "Call date",
              "selected": True,
              "slug": "907930c9896e4034bbef1d3086655279",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "Education",
              "selected": True,
              "slug": "4dd51af67eb34469a1e7055ca7f46f1d",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": True,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "Top Organization",
              "selected": True,
              "slug": "9c8f2f354b0d4411a3f7adf6bcc344ee",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "Agent Name",
              "selected": True,
              "slug": "19357fe66be64c1ca9030d774e31bc0e",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "Call Type",
              "selected": True,
              "slug": "0d062d4393344d05bd9d360e49c892f3",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "State",
              "selected": True,
              "slug": "89fb18022a144aaf875cb9b5c88c6844",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "Region",
              "selected": True,
              "slug": "5429020a74d44d47a242cdd7fa544cf9",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "Agent Experience",
              "selected": True,
              "slug": "1a2c29c2510647e0b6b736821bddb605",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "Agent Rating",
              "selected": True,
              "slug": "2d4802e02d3d4b7884ddf5f3ffc0f803",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "Agent Age",
              "selected": True,
              "slug": "e449bf6acf72489a8683d9f18a60799d",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "Top Plan Provider",
              "selected": True,
              "slug": "dabac2e5ec594561baf99f650671458e",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
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
            "Trend"
          ],
          "metadata": {
            "url": "34.196.204.54:9012/api/get_metadata_for_mlscripts/",
            "slug_list": [
              "health-care-callcentre-v10csv-1ww6kaai9r"
            ]
          },
          "inputfile": [
            "file:///home/gulshan/marlabs/datasets/Health Care Callcentre- V10.csv"
          ]
        }
      },
      "job_config": {
        "message_url": "http://34.196.204.54:9012/api/messages/Job_master-lklsdaa-5hs5loh3nh-5d5ltbrg20_123/",
        "get_config": {
          "action": "get_config",
          "method": "GET"
        },
        "error_reporting_url": "http://34.196.204.54:9012/api/set_job_report/master-lklsdaa-5hs5loh3nh-5d5ltbrg20/",
        "set_result": {
          "action": "result",
          "method": "PUT"
        },
        "job_url": "http://34.196.204.54:9012/api/job/master-lklsdaa-5hs5loh3nh-5d5ltbrg20/",
        "job_type": "story",
        "job_name": "lklsdaa",
        "xml_url": "http://34.196.204.54:9012/api/xml/master-lklsdaa-5hs5loh3nh-5d5ltbrg20/",
        "app_id": None
      }
    }
    return storyConfig
