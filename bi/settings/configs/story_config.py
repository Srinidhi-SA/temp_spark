def get_story_config():
    # storyConfig = {
    # "job_config": {
    #   "job_url": "http://34.196.204.54:9012/api/job/master-measure-test1-gd721qkcc3-yjifx6qlwo/",
    #   "job_type": "story",
    #   "xml_url": "http://34.196.204.54:9012/api/xml/master-measure-test1-gd721qkcc3-yjifx6qlwo/",
    #   "error_reporting_url": "http://34.196.204.54:9012/api/set_job_report/master-error-check0-m302es9p2d-qm34cqk7mt/",
    #   "get_config": {
    #     "action": "get_config",
    #     "method": "GET"
    #   },
    #   "set_result": {
    #     "action": "result",
    #     "method": "PUT"
    #   },
    #   "message_url": "http://34.196.204.54:9012/api/messages/Insight_measure-test1-gd721qkcc3_123/",
    #   "job_name": "measure-test1"
    # },
    # "config": {
    #   "COLUMN_SETTINGS": {
    #     "polarity": [
    #       {
    #         "colSlug": "4f3e60f4e761481e9d153d44fddffb13",
    #         "polarity": "positive",
    #         "colName": "Tenure_in_Days"
    #       },
    #       {
    #         "colSlug": "7390904522104016922e7eeb00994fed",
    #         "polarity": "positive",
    #         "colName": "Sales"
    #       },
    #       {
    #         "colSlug": "475bf6e3b9c24021b5bae514c9b822bc",
    #         "polarity": "positive",
    #         "colName": "Marketing_Cost"
    #       },
    #       {
    #         "colSlug": "26e23e08ad1e491cbf567f444c844767",
    #         "polarity": "positive",
    #         "colName": "Shipping_Cost"
    #       },
    #       {
    #         "colSlug": "afaad041663c4c7091b1b3d870685eaf",
    #         "polarity": "positive",
    #         "colName": "Last_Transaction"
    #       }
    #     ],
    #     "date_format": None,
    #     "consider_columns_type": [
    #       "including"
    #     ],
    #     "customAnalysisDetails": [
    #
    #     ],
    #     "result_column": [
    #       "Platform"
    #     ],
    #     "ignore_column_suggestion": [
    #
    #     ],
    #     "consider_columns": [
    #       "Deal_Type",
    #       "Price_Range",
    #       "Discount_Range",
    #       "Source",
    #       "Platform",
    #       "Buyer_Age",
    #       "Buyer_Gender",
    #       "Tenure_in_Days",
    #       "Sales",
    #       "Marketing_Cost",
    #       "Shipping_Cost",
    #       "Last_Transaction",
    #       "new_date"
    #     ],
    #     "utf8_column_suggestions": [
    #
    #     ],
    #     "date_columns": [
    #       "new_date"
    #     ],
    #     "analysis_type": [
    #       "dimension"
    #     ],
    #     "dateTimeSuggestions": [
    #       {
    #         "Order Date": "%d-%m-%Y",
    #         "Month": "%b-%y"
    #       }
    #     ]
    #   },
    #   "DATA_SOURCE": {
    #     "datasource_type": "fileUpload",
    #     "datasource_details": ""
    #   },
    #   "ADVANCED_SETTINGS": {
    #     "analysis": [
    #       {
    #         "status": True,
    #         "noOfColumnsToUse": None,
    #         "analysisSubTypes": [
    #
    #         ],
    #         "displayName": "Overview",
    #         "name": "overview"
    #       },
    #       {
    #         "status": False,
    #         "noOfColumnsToUse": None,
    #         "analysisSubTypes": [
    #           {
    #             "status": False,
    #             "displayName": "Overview",
    #             "name": "overview"
    #           },
    #           {
    #             "status": False,
    #             "displayName": "Factors that drive up",
    #             "name": "factors that drive up"
    #           },
    #           {
    #             "status": False,
    #             "displayName": "Factors that drive down",
    #             "name": "factors that drive down"
    #           },
    #           {
    #             "status": False,
    #             "displayName": "Forecast",
    #             "name": "forecast"
    #           }
    #         ],
    #         "displayName": "Trend",
    #         "name": "trend"
    #       },
    #       {
    #         "status": False,
    #         "noOfColumnsToUse": [
    #           {
    #             "status": False,
    #             "defaultValue": 3,
    #             "displayName": "Low",
    #             "name": "low"
    #           },
    #           {
    #             "status": False,
    #             "defaultValue": 5,
    #             "displayName": "Medium",
    #             "name": "medium"
    #           },
    #           {
    #             "status": True,
    #             "defaultValue": 8,
    #             "displayName": "High",
    #             "name": "high"
    #           },
    #           {
    #             "status": False,
    #             "defaultValue": 3,
    #             "displayName": "Custom",
    #             "name": "custom",
    #             "value": None
    #           }
    #         ],
    #         "analysisSubTypes": [
    #
    #         ],
    #         "displayName": "Performance",
    #         "name": "performance"
    #       },
    #       {
    #         "status": False,
    #         "noOfColumnsToUse": [
    #           {
    #             "status": False,
    #             "defaultValue": 3,
    #             "displayName": "Low",
    #             "name": "low"
    #           },
    #           {
    #             "status": False,
    #             "defaultValue": 5,
    #             "displayName": "Medium",
    #             "name": "medium"
    #           },
    #           {
    #             "status": True,
    #             "defaultValue": 8,
    #             "displayName": "High",
    #             "name": "high"
    #           },
    #           {
    #             "status": False,
    #             "defaultValue": 3,
    #             "displayName": "Custom",
    #             "name": "custom",
    #             "value": None
    #           }
    #         ],
    #         "analysisSubTypes": [
    #
    #         ],
    #         "displayName": "Influencer",
    #         "name": "influencer"
    #       },
    #       {
    #         "status": True,
    #         "noOfColumnsToUse": None,
    #         "analysisSubTypes": [
    #
    #         ],
    #         "displayName": "Prediction",
    #         "name": "prediction"
    #       },
    #       {
    #         "status": True,
    #         "noOfColumnsToUse": [
    #           {
    #             "status": False,
    #             "defaultValue": 3,
    #             "displayName": "Low",
    #             "name": "low"
    #           },
    #           {
    #             "status": False,
    #             "defaultValue": 5,
    #             "displayName": "Medium",
    #             "name": "medium"
    #           },
    #           {
    #             "status": True,
    #             "defaultValue": 8,
    #             "displayName": "High",
    #             "name": "high"
    #           },
    #           {
    #             "status": False,
    #             "defaultValue": 3,
    #             "displayName": "Custom",
    #             "name": "custom",
    #             "value": None
    #           }
    #         ],
    #         "analysisSubTypes": [
    #
    #         ],
    #         "displayName": "Association",
    #         "name": "association"
    #       },
    #     ]
    #   },
    #   "FILE_SETTINGS": {
    #     "script_to_run": [
    #       "Descriptive analysis",
    #       "Trend",
    #       "Measure vs. Dimension",
    #       "Measure vs. Measure",
    #       "Predictive modeling"
    #     ],
    #     "metadata": {
    #       "url": "34.196.204.54:9012/api/get_metadata_for_mlscripts/",
    #       "slug_list": [
    #         "trend_gulshancsv-zuxmcvv8lu"
    #       ]
    #     },
    #     "inputfile": [
    #       "file:///home/gulshan/marlabs/datasets/trend_gulshan.csv"
    #     ]
    #   }
    # }
    # }
    storyConfig = {
      "job_config": {
        "message_url": "http://34.196.204.54:9012/api/messages/Insight_dimension-test-dsuex2arqz_123/",
        "get_config": {
          "action": "get_config",
          "method": "GET"
        },
        "error_reporting_url": "http://34.196.204.54:9012/api/set_job_report/master-dimension-test-dsuex2arqz-ks5xbn6a1p/",
        "set_result": {
          "action": "result",
          "method": "PUT"
        },
        "job_url": "http://34.196.204.54:9012/api/job/master-dimension-test-dsuex2arqz-ks5xbn6a1p/",
        "job_type": "story",
        "job_name": "dimension-test",
        "xml_url": "http://34.196.204.54:9012/api/xml/master-dimension-test-dsuex2arqz-ks5xbn6a1p/"
      },
      "config": {
        "COLUMN_SETTINGS": {
          "polarity": [
            {
              "colSlug": "2edc6da1c4504d308f2e60e487d79a14",
              "polarity": "positive",
              "colName": "age"
            },
            {
              "colSlug": "0a15d89d54d74dcbba01f84d14fc5776",
              "polarity": "positive",
              "colName": "fnlwgt"
            },
            {
              "colSlug": "b2c54610cbbf4efb921e675c0b298845",
              "polarity": "positive",
              "colName": "education-num"
            },
            {
              "colSlug": "69169a5855834f6ea8a15832bf946075",
              "polarity": "positive",
              "colName": "Capital-gain"
            },
            {
              "colSlug": "76faf826731843b3a612bf49e9a19e9b",
              "polarity": "positive",
              "colName": "Capital-loss"
            },
            {
              "colSlug": "616b886e12384cc3a9b0b45180e2d0ec",
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
            "age",
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
            "dimension"
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
              "noOfColumnsToUse": None,
              "analysisSubTypes": [

              ],
              "displayName": "Prediction",
              "name": "prediction"
            }
          ],
          "targetLevels": [
            [

            ]
          ]
        },
        "FILE_SETTINGS": {
          "script_to_run": [
            "Descriptive analysis",
            "Dimension vs. Dimension",
            "Predictive modeling"
          ],
          "metadata": {
            "url": "34.196.204.54:9012/api/get_metadata_for_mlscripts/",
            "slug_list": [
              "adultcsv-cjzdoqhdcg"
            ]
          },
          "inputfile": [
            "file:///home/marlabs/Downloads/adult.csv"
          ]
        }
      }
    }
    return storyConfig
