def get_story_config():
    storyConfig = {
      "config": {
        "COLUMN_SETTINGS": {
          "polarity": [
            {
              "colSlug": "45acf251d8fb4a64a574213211fff4fe",
              "polarity": "positive",
              "colName": "age"
            },
            {
              "colSlug": "612c305f7ed44751bddd2b03aed0de76",
              "polarity": "positive",
              "colName": "fnlwgt"
            },
            {
              "colSlug": "00869a1a210644738cbf3b64b37541ba",
              "polarity": "positive",
              "colName": "education-num"
            },
            {
              "colSlug": "c553feb40fb542dc86d68e91854c1c34",
              "polarity": "positive",
              "colName": "Capital-gain"
            },
            {
              "colSlug": "cfa46535fb844c4a97242128b29bcc1c",
              "polarity": "positive",
              "colName": "Capital-loss"
            },
            {
              "colSlug": "e20604526aec42b080ee56971a9961e3",
              "polarity": "positive",
              "colName": "hours-per-week"
            }
          ],
          "date_format": None,
          "consider_columns_type": [
            "including"
          ],
          "customAnalysisDetails": [

          ],
          "result_column": [
            "age"
          ],
          "ignore_column_suggestion": [

          ],
          "consider_columns": [
            "workclass",
            "education",
            "marital-status",
            "occupation",
            "relationship",
            "race",
            "sex",
            "native-country",
            "class_label",
            "fnlwgt",
            "education-num",
            "Capital-gain",
            "Capital-loss",
            "hours-per-week"
          ],
          "utf8_column_suggestions": [

          ],
          "date_columns": [

          ],
          "analysis_type": [
            "measure"
          ],
          "dateTimeSuggestions": [
            {

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
            "Measure vs. Dimension"
          ],
          "metadata": {
            "url": "34.196.204.54:9012/api/get_metadata_for_mlscripts/",
            "slug_list": [
              "demographycsv-9xczlu9n11"
            ]
          },
          "inputfile": [
            "file:///home/gulshan/marlabs/datasets/sampleDatasets/demography.csv"
          ]
        }
      },
      "job_config": {
        "message_url": "http://34.196.204.54:9012/api/messages/Job_master-test-demography-3s1qenhsv4-84mqewjhir_123/",
        "get_config": {
          "action": "get_config",
          "method": "GET"
        },
        "error_reporting_url": "http://34.196.204.54:9012/api/set_job_report/master-test-demography-3s1qenhsv4-84mqewjhir/",
        "set_result": {
          "action": "result",
          "method": "PUT"
        },
        "job_url": "http://34.196.204.54:9012/api/job/master-test-demography-3s1qenhsv4-84mqewjhir/",
        "job_type": "story",
        "job_name": "test-demography",
        "xml_url": "http://34.196.204.54:9012/api/xml/master-test-demography-3s1qenhsv4-84mqewjhir/"
      }
    }
    return storyConfig
