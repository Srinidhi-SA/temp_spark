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
        "message_url": "http://34.196.204.54:9012/api/messages/Job_master-dimension-test-7dcj6tsagk-mh869u5gn4_123/",
        "get_config": {
        "action": "get_config",
        "method": "GET"
        },
        "error_reporting_url": "http://34.196.204.54:9012/api/set_job_report/master-dimension-test-7dcj6tsagk-mh869u5gn4/",
        "set_result": {
        "action": "result",
        "method": "PUT"
        },
        "job_url": "http://34.196.204.54:9012/api/job/master-dimension-test-7dcj6tsagk-mh869u5gn4/",
        "job_type": "story",
        "job_name": "dimension-test",
        "xml_url": "http://34.196.204.54:9012/api/xml/master-dimension-test-7dcj6tsagk-mh869u5gn4/"
    },
"config": {
"COLUMN_SETTINGS": {
"polarity": [
  {
    "colSlug": "8901cd187f804a5c89c9588b0ab993d6",
    "polarity": "positive",
    "colName": "Tenure_in_Days"
  },
  {
    "colSlug": "5cb5d3e72f444b83a2ebdef6a4657083",
    "polarity": "positive",
    "colName": "Sales"
  },
  {
    "colSlug": "f4afdbf2e93142e2b835d738f937d789",
    "polarity": "positive",
    "colName": "Marketing_Cost"
  },
  {
    "colSlug": "a9d41dd5c56c4018afd7914980ff1cc0",
    "polarity": "positive",
    "colName": "Shipping_Cost"
  },
  {
    "colSlug": "d538a497f58f497e8f415bc8699233bf",
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
  "Platform",
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
<<<<<<< HEAD
      "FILE_SETTINGS": {
        "script_to_run": [
          "Descriptive analysis"
        ],
        "metadata": {
          "url": "34.196.204.54:9012/api/get_metadata_for_mlscripts/",
          "slug_list": [
            "adult_newcsv-j0ak4a53pp"
          ]
        },
        "inputfile": [
        #   "hdfs://ec2-34-205-203-38.compute-1.amazonaws.com:8020/dev/dataset/adultcsv-roudox26di/adult_YGVxCWQ.csv"
            "/home/marlabs/Documents/mAdvisor/Datasets/adult_new.csv"
=======
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
>>>>>>> bfae8b68b0be912d10b89e905672aead2ba83d33

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
  "Trend",
  "Dimension vs. Dimension",
  "Predictive modeling"
],
"metadata": {
  "url": "34.196.204.54:9012/api/get_metadata_for_mlscripts/",
  "slug_list": [
    "ecommercecsv-3hcogr1svt"
  ]
},
"inputfile": [
  "file:///home/gulshan/marlabs/datasets/sampleDatasets/ecommerce.csv"
]
}
}
    }
    return storyConfig
