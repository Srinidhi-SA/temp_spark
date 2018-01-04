def get_story_config():
    storyConfig = {
    "job_config": {
      "message_url": "http://34.196.204.54:9012/api/messages/Insight_mitali-adult-data-test-povjiqm01g_123/",
      "get_config": {
        "action": "get_config",
        "method": "GET"
      },
      "error_reporting_url": "http://34.196.204.54:9012/api/set_job_report/master-mitali-adult-data-test-povjiqm01g-go78ugxh21/",
      "set_result": {
        "action": "result",
        "method": "PUT"
      },
      "job_url": "http://34.196.204.54:9012/api/job/master-mitali-adult-data-test-povjiqm01g-go78ugxh21/",
      "job_type": "story",
      "job_name": "mitali adult data test",
      "xml_url": "http://34.196.204.54:9012/api/xml/master-mitali-adult-data-test-povjiqm01g-go78ugxh21/"
    },
    "config": {
      "COLUMN_SETTINGS": {
        "polarity": [
          {
            "colSlug": "3b2449a11eff43c699e373894af2ab3a",
            "polarity": "positive",
            "colName": "age"
          },
          {
            "colSlug": "409f47cd921e4005ade05efabc60ab66",
            "polarity": "positive",
            "colName": "fnlwgt"
          },
          {
            "colSlug": "ad351fe2ada94dc9bf6c808a734f63f6",
            "polarity": "positive",
            "colName": "education-num"
          },
          {
            "colSlug": "fdbdf2fa7c44419f931717a9d58111ec",
            "polarity": "positive",
            "colName": "Capital-gain"
          },
          {
            "colSlug": "c7865e8e543f40daaa6a220996e237ec",
            "polarity": "positive",
            "colName": "Capital-loss"
          },
          {
            "colSlug": "9b044de7e03a4f86804eb5a530208d68",
            "polarity": "positive",
            "colName": "hours-per-week"
          }
        ],
        "date_format": None,
        "consider_columns_type": [
          "including"
        ],
        "customAnalysisDetails": [
          {
            "colSlug": "3b2449a11eff43c699e373894af2ab3a",
            "colName": "age",
            "treatAs": "percentage"
          }
        ],
        "result_column": [
          "age"
        ],
        "ignore_column_suggestion": [],
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
          "age",
          "fnlwgt",
          "education-num",
          "Capital-gain",
          "Capital-loss",
          "hours-per-week"
        ],
        "utf8_column_suggestions": [],
        "date_columns": [],
        "analysis_type": [
          "dimension"
        ],
        "dateTimeSuggestions": [
          {}
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
        "analysis": [
          {
            "status": True,
            "noOfColumnsToUse": None,
            "analysisSubTypes": [],
            "displayName": "Overview",
            "name": "overview"
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
            "analysisSubTypes": [],
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
            "noOfColumnsToUse": None,
            "analysisSubTypes": [],
            "displayName": "Prediction",
            "name": "prediction"
          }
        ],
        "targetLevels": [
          []
        ]
      },
      "FILE_SETTINGS": {
        "script_to_run": [
          "Descriptive analysis"
        ],
        "metadata": {
          "url": "34.196.204.54:9012/api/get_metadata_for_mlscripts/",
          "slug_list": [
            "adultcsv-roudox26di"
          ]
        },
        "inputfile": [
        #   "hdfs://ec2-34-205-203-38.compute-1.amazonaws.com:8020/dev/dataset/adultcsv-roudox26di/adult_YGVxCWQ.csv"
            "/home/marlabs/Documents/mAdvisor/Datasets/adult.csv"

        ]
      }
    }
    }
    return storyConfig
