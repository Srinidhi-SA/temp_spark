def get_story_config():
    storyConfig = {
      "config": {
        "COLUMN_SETTINGS": {
          "variableSelection": [
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "measure",
              "name": "Age",
              "selected": True,
              "slug": "0d82a1520049475f98fa11226f6ceebd",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "Employment",
              "selected": True,
              "slug": "a800ae33a88343c4bb8b084768808d6c",
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
              "slug": "2ce376ee2287406daed87d147cbed014",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "Marital",
              "selected": True,
              "slug": "f2bf7b9fb5a246d19a73bfefd9f0ac84",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "Occupation",
              "selected": True,
              "slug": "604690b6a6ed44d5bd99065ffa53d219",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "measure",
              "name": "Income",
              "selected": True,
              "slug": "ca6caa97ee8e4e8d935dadb10b5d6de9",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": True,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "Gender",
              "selected": True,
              "slug": "ae1c3ac8fe824b25abce73b3ce874db4",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "Deductions",
              "selected": True,
              "slug": "024a9466a96d4af9a2040eb37aa4b7bc",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "measure",
              "name": "Hours",
              "selected": True,
              "slug": "95fae51677e744348e6544ed197441c7",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "measure",
              "name": "Adjusted",
              "selected": True,
              "slug": "0d074183ec7e486daabe5e18f1b929fd",
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
            "Measure vs. Dimension",
            "Measure vs. Measure",
            "Predictive modeling"
          ],
          "metadata": {
            "url": "34.196.204.54:9012/api/get_metadata_for_mlscripts/",
            "slug_list": [
              "audit_boolcsv-hfnzqhw8xf"
            ]
          },
          "inputfile": [
            "file:///home/gulshan/marlabs/datasets/audit_bool.csv"
          ]
        }
      },
      "job_config": {
        "message_url": "http://34.196.204.54:9012/api/messages/Job_master-check-bool-oc4kwwp2z1-1w1rl0ta9k_123/",
        "get_config": {
          "action": "get_config",
          "method": "GET"
        },
        "error_reporting_url": "http://34.196.204.54:9012/api/set_job_report/master-check-bool-oc4kwwp2z1-1w1rl0ta9k/",
        "set_result": {
          "action": "result",
          "method": "PUT"
        },
        "job_url": "http://34.196.204.54:9012/api/job/master-check-bool-oc4kwwp2z1-1w1rl0ta9k/",
        "job_type": "story",
        "job_name": "check bool",
        "xml_url": "http://34.196.204.54:9012/api/xml/master-check-bool-oc4kwwp2z1-1w1rl0ta9k/",
        "app_id": None
      }
    }
    return storyConfig
