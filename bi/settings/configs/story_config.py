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
          "slug": "be0c515869374fd09c54a624e3d7e9bb",
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
          "slug": "b13f389ae68144efbd8bae439a19fd00",
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
          "slug": "489f57876498416fb963926d0b7929b0",
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
          "slug": "fd9a2fc693874d74a06bb0de327bfba8",
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
          "slug": "322b026cea13450eb410617b2059f881",
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
          "slug": "57eae03aaa1f47f79ce249d3173f744e",
          "targetColSetVarAs": None,
          "dateSuggestionFlag": False,
          "targetColumn": True,
          "uidCol": False
        },
        {
          "polarity": None,
          "setVarAs": None,
          "columnType": "dimension",
          "name": "Buyer_Age",
          "selected": True,
          "slug": "54b7609862824257946136da075ba904",
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
          "slug": "d599a85dac6240f39be5a330bb5f2b29",
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
          "slug": "079e8ab1b1fe4293b1086c6584ed2c3b",
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
          "slug": "dc5fc60ed1514370babaabd978f39493",
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
          "slug": "c8a30e5cdb3b4d1eb6230bee4e7b93ce",
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
          "slug": "1e6b2921179b48aa8e171a28fedce3b7",
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
          "slug": "e5613945f6c24aacb0c80ea0588800ab",
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
          "slug": "5778735b2f174d38943ff72536dd36ff",
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
          "slug": "af99d6eaa7a84d1792ef458d62fd2fbf",
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
          "status": False,
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
          "ecommercecsv-um51c5oq52"
        ]
      },
      "inputfile": [
        "file:///home/gulshan/marlabs/datasets/sampleDatasets/ecommerce.csv"
      ]
    }
  },
  "job_config": {
    "message_url": "http://34.196.204.54:9012/api/messages/Job_master-lllsad-l0y0qms0bi-759vlmr9qr_123/",
    "get_config": {
      "action": "get_config",
      "method": "GET"
    },
    "error_reporting_url": "http://34.196.204.54:9012/api/set_job_report/master-lllsad-l0y0qms0bi-759vlmr9qr/",
    "set_result": {
      "action": "result",
      "method": "PUT"
    },
    "job_url": "http://34.196.204.54:9012/api/job/master-lllsad-l0y0qms0bi-759vlmr9qr/",
    "job_type": "story",
    "job_name": "lllsad",
    "xml_url": "http://34.196.204.54:9012/api/xml/master-lllsad-l0y0qms0bi-759vlmr9qr/",
    "app_id": None
  }
}
    return storyConfig
