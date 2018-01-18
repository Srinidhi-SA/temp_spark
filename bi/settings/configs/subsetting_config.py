def get_subsetting_config():
    subsettingConfig = {
      "config": {
        "FILTER_SETTINGS": {
          "measureColumnFilters": [
            {
              "filterType": "valueRange",
              "lowerBound": 8888,
              "colname": "CREDIT_BALANCE1",
              "upperBound": 21600
            }
          ],
          "dimensionColumnFilters": [

          ],
          "timeDimensionColumnFilters": [

          ]
        },
        "DATA_SOURCE": {
          "datasource_type": "fileUpload",
          "datasource_details": ""
        },
        "COLUMN_SETTINGS": {
          "analysis_type": [
            "metaData"
          ]
        },
        "TRANSFORMATION_SETTINGS": {
          "existingColumns": [
            {
              "slug": "9937723d4db0404e85238f8f6a232704",
              "name": "CREDIT_BALANCE1",
              "columnSetting": [
                {
                  "status": False,
                  "actionName": "unique_identifier",
                  "displayName": "Unique Identifier"
                },
                {
                  "status": False,
                  "actionName": "delete",
                  "displayName": "Delete Column"
                },
                {
                  "status": False,
                  "actionName": "rename",
                  "displayName": "Rename Column",
                  "newName": None
                },
                {
                  "status": False,
                  "actionName": "replace",
                  "replaceTypeList": [
                    {
                      "displayName": "Contains",
                      "name": "contains"
                    },
                    {
                      "displayName": "Equal To",
                      "name": "equals"
                    },
                    {
                      "displayName": "Starts With",
                      "name": "startsWith"
                    },
                    {
                      "displayName": "Ends With",
                      "name": "endsWith"
                    }
                  ],
                  "displayName": "Replace Values",
                  "replacementValues": [

                  ]
                },
                {
                  "status": False,
                  "actionName": "data_type",
                  "displayName": "Change Datatype",
                  "listOfActions": [
                    {
                      "status": True,
                      "displayName": "Numeric",
                      "name": "numeric"
                    },
                    {
                      "status": False,
                      "displayName": "Text",
                      "name": "text"
                    }
                  ]
                },
                {
                  "status": False,
                  "actionName": "set_variable",
                  "displayName": "Set Variable as",
                  "listOfActions": [
                    {
                      "status": True,
                      "displayName": "General Numeric",
                      "name": "general_numeric"
                    },
                    {
                      "status": False,
                      "displayName": "Percentage",
                      "name": "percentage"
                    },
                    {
                      "status": False,
                      "displayName": "Index",
                      "name": "index"
                    },
                    {
                      "status": False,
                      "displayName": "Average",
                      "name": "average"
                    }
                  ]
                },
                {
                  "status": False,
                  "actionName": "set_polarity",
                  "displayName": "Set Polarity as",
                  "listOfActions": [
                    {
                      "status": True,
                      "displayName": "Positive",
                      "name": "positive"
                    },
                    {
                      "status": False,
                      "displayName": "Negative",
                      "name": "negative"
                    }
                  ]
                },
                {
                  "status": False,
                  "actionName": "ignore_suggestion",
                  "displayName": "Ignore for Analysis"
                }
              ]
            },
            {
              "slug": "79ee669a8c18445b99e0c482ceb872a1",
              "name": "CREDIT_BALANCE2",
              "columnSetting": [
                {
                  "status": False,
                  "actionName": "unique_identifier",
                  "displayName": "Unique Identifier"
                },
                {
                  "status": False,
                  "actionName": "delete",
                  "displayName": "Delete Column"
                },
                {
                  "status": False,
                  "actionName": "rename",
                  "displayName": "Rename Column",
                  "newName": None
                },
                {
                  "status": False,
                  "actionName": "replace",
                  "replaceTypeList": [
                    {
                      "displayName": "Contains",
                      "name": "contains"
                    },
                    {
                      "displayName": "Equal To",
                      "name": "equals"
                    },
                    {
                      "displayName": "Starts With",
                      "name": "startsWith"
                    },
                    {
                      "displayName": "Ends With",
                      "name": "endsWith"
                    }
                  ],
                  "displayName": "Replace Values",
                  "replacementValues": [

                  ]
                },
                {
                  "status": False,
                  "actionName": "data_type",
                  "displayName": "Change Datatype",
                  "listOfActions": [
                    {
                      "status": True,
                      "displayName": "Numeric",
                      "name": "numeric"
                    },
                    {
                      "status": False,
                      "displayName": "Text",
                      "name": "text"
                    }
                  ]
                },
                {
                  "status": False,
                  "actionName": "set_variable",
                  "displayName": "Set Variable as",
                  "listOfActions": [
                    {
                      "status": True,
                      "displayName": "General Numeric",
                      "name": "general_numeric"
                    },
                    {
                      "status": False,
                      "displayName": "Percentage",
                      "name": "percentage"
                    },
                    {
                      "status": False,
                      "displayName": "Index",
                      "name": "index"
                    },
                    {
                      "status": False,
                      "displayName": "Average",
                      "name": "average"
                    }
                  ]
                },
                {
                  "status": False,
                  "actionName": "set_polarity",
                  "displayName": "Set Polarity as",
                  "listOfActions": [
                    {
                      "status": True,
                      "displayName": "Positive",
                      "name": "positive"
                    },
                    {
                      "status": False,
                      "displayName": "Negative",
                      "name": "negative"
                    }
                  ]
                },
                {
                  "status": False,
                  "actionName": "ignore_suggestion",
                  "displayName": "Ignore for Analysis"
                }
              ]
            },
            {
              "slug": "d6f4499f4bdb4e4abaa161b0a5e36272",
              "name": "CREDIT_BALANCE3",
              "columnSetting": [
                {
                  "status": False,
                  "actionName": "unique_identifier",
                  "displayName": "Unique Identifier"
                },
                {
                  "status": False,
                  "actionName": "delete",
                  "displayName": "Delete Column"
                },
                {
                  "status": False,
                  "actionName": "rename",
                  "displayName": "Rename Column",
                  "newName": None
                },
                {
                  "status": False,
                  "actionName": "replace",
                  "replaceTypeList": [
                    {
                      "displayName": "Contains",
                      "name": "contains"
                    },
                    {
                      "displayName": "Equal To",
                      "name": "equals"
                    },
                    {
                      "displayName": "Starts With",
                      "name": "startsWith"
                    },
                    {
                      "displayName": "Ends With",
                      "name": "endsWith"
                    }
                  ],
                  "displayName": "Replace Values",
                  "replacementValues": [

                  ]
                },
                {
                  "status": False,
                  "actionName": "ignore_suggestion",
                  "displayName": "Ignore for Analysis"
                }
              ]
            },
            {
              "slug": "1218952a758d464a82175052dad8d83e",
              "name": "SEX",
              "columnSetting": [
                {
                  "status": False,
                  "actionName": "unique_identifier",
                  "displayName": "Unique Identifier"
                },
                {
                  "status": False,
                  "actionName": "delete",
                  "displayName": "Delete Column"
                },
                {
                  "status": False,
                  "actionName": "rename",
                  "displayName": "Rename Column",
                  "newName": None
                },
                {
                  "status": False,
                  "actionName": "replace",
                  "replaceTypeList": [
                    {
                      "displayName": "Contains",
                      "name": "contains"
                    },
                    {
                      "displayName": "Equal To",
                      "name": "equals"
                    },
                    {
                      "displayName": "Starts With",
                      "name": "startsWith"
                    },
                    {
                      "displayName": "Ends With",
                      "name": "endsWith"
                    }
                  ],
                  "displayName": "Replace Values",
                  "replacementValues": [

                  ]
                },
                {
                  "status": False,
                  "actionName": "ignore_suggestion",
                  "displayName": "Ignore for Analysis"
                }
              ]
            },
            {
              "slug": "86346dd691a1469b9542091177c26e89",
              "name": "EDUCATION",
              "columnSetting": [
                {
                  "status": False,
                  "actionName": "unique_identifier",
                  "displayName": "Unique Identifier"
                },
                {
                  "status": False,
                  "actionName": "delete",
                  "displayName": "Delete Column"
                },
                {
                  "status": False,
                  "actionName": "rename",
                  "displayName": "Rename Column",
                  "newName": None
                },
                {
                  "status": False,
                  "actionName": "replace",
                  "replaceTypeList": [
                    {
                      "displayName": "Contains",
                      "name": "contains"
                    },
                    {
                      "displayName": "Equal To",
                      "name": "equals"
                    },
                    {
                      "displayName": "Starts With",
                      "name": "startsWith"
                    },
                    {
                      "displayName": "Ends With",
                      "name": "endsWith"
                    }
                  ],
                  "displayName": "Replace Values",
                  "replacementValues": [

                  ]
                },
                {
                  "status": False,
                  "actionName": "ignore_suggestion",
                  "displayName": "Ignore for Analysis"
                }
              ]
            },
            {
              "slug": "9ce9de52c2fa42faa8945235d44509f8",
              "name": "MARRIAGE",
              "columnSetting": [
                {
                  "status": False,
                  "actionName": "unique_identifier",
                  "displayName": "Unique Identifier"
                },
                {
                  "status": False,
                  "actionName": "delete",
                  "displayName": "Delete Column"
                },
                {
                  "status": False,
                  "actionName": "rename",
                  "displayName": "Rename Column",
                  "newName": None
                },
                {
                  "status": False,
                  "actionName": "replace",
                  "replaceTypeList": [
                    {
                      "displayName": "Contains",
                      "name": "contains"
                    },
                    {
                      "displayName": "Equal To",
                      "name": "equals"
                    },
                    {
                      "displayName": "Starts With",
                      "name": "startsWith"
                    },
                    {
                      "displayName": "Ends With",
                      "name": "endsWith"
                    }
                  ],
                  "displayName": "Replace Values",
                  "replacementValues": [

                  ]
                },
                {
                  "status": False,
                  "actionName": "ignore_suggestion",
                  "displayName": "Ignore for Analysis"
                }
              ]
            },
            {
              "slug": "a7cc89c788c346be8bf79cd71d93b329",
              "name": "new_date",
              "columnSetting": [
                {
                  "status": False,
                  "actionName": "unique_identifier",
                  "displayName": "Unique Identifier"
                },
                {
                  "status": False,
                  "actionName": "delete",
                  "displayName": "Delete Column"
                },
                {
                  "status": False,
                  "actionName": "rename",
                  "displayName": "Rename Column",
                  "newName": None
                },
                {
                  "status": False,
                  "actionName": "ignore_suggestion",
                  "displayName": "Ignore for Analysis"
                }
              ]
            },
            {
              "slug": "acfce246d4ed45809fc507a410b05dd1",
              "name": "colToReplace",
              "columnSetting": [
                {
                  "status": False,
                  "actionName": "unique_identifier",
                  "displayName": "Unique Identifier"
                },
                {
                  "status": False,
                  "actionName": "delete",
                  "displayName": "Delete Column"
                },
                {
                  "status": False,
                  "actionName": "rename",
                  "displayName": "Rename Column",
                  "newName": None
                },
                {
                  "status": False,
                  "actionName": "replace",
                  "replaceTypeList": [
                    {
                      "displayName": "Contains",
                      "name": "contains"
                    },
                    {
                      "displayName": "Equal To",
                      "name": "equals"
                    },
                    {
                      "displayName": "Starts With",
                      "name": "startsWith"
                    },
                    {
                      "displayName": "Ends With",
                      "name": "endsWith"
                    }
                  ],
                  "displayName": "Replace Values",
                  "replacementValues": [

                  ]
                },
                {
                  "status": False,
                  "actionName": "ignore_suggestion",
                  "displayName": "Ignore for Analysis"
                }
              ]
            },
            {
              "slug": "4088f715d5c041aeaad8f93d616cb57d",
              "name": "toDelete",
              "columnSetting": [
                {
                  "status": False,
                  "actionName": "unique_identifier",
                  "displayName": "Unique Identifier"
                },
                {
                  "status": False,
                  "actionName": "delete",
                  "displayName": "Delete Column"
                },
                {
                  "status": False,
                  "actionName": "rename",
                  "displayName": "Rename Column",
                  "newName": None
                },
                {
                  "status": False,
                  "actionName": "replace",
                  "replaceTypeList": [
                    {
                      "displayName": "Contains",
                      "name": "contains"
                    },
                    {
                      "displayName": "Equal To",
                      "name": "equals"
                    },
                    {
                      "displayName": "Starts With",
                      "name": "startsWith"
                    },
                    {
                      "displayName": "Ends With",
                      "name": "endsWith"
                    }
                  ],
                  "displayName": "Replace Values",
                  "replacementValues": [

                  ]
                },
                {
                  "status": False,
                  "actionName": "ignore_suggestion",
                  "displayName": "Ignore for Analysis"
                }
              ]
            },
            {
              "slug": "5706f10f70be4158be8d8301e038d121",
              "name": "toReplace",
              "columnSetting": [
                {
                  "status": False,
                  "actionName": "unique_identifier",
                  "displayName": "Unique Identifier"
                },
                {
                  "status": False,
                  "actionName": "delete",
                  "displayName": "Delete Column"
                },
                {
                  "status": False,
                  "actionName": "rename",
                  "displayName": "Rename Column",
                  "newName": None
                },
                {
                  "status": False,
                  "actionName": "replace",
                  "replaceTypeList": [
                    {
                      "displayName": "Contains",
                      "name": "contains"
                    },
                    {
                      "displayName": "Equal To",
                      "name": "equals"
                    },
                    {
                      "displayName": "Starts With",
                      "name": "startsWith"
                    },
                    {
                      "displayName": "Ends With",
                      "name": "endsWith"
                    }
                  ],
                  "displayName": "Replace Values",
                  "replacementValues": [

                  ]
                },
                {
                  "status": True,
                  "actionName": "ignore_suggestion",
                  "displayName": "Consider for Analysis"
                }
              ]
            }
          ]
        },
        "FILE_SETTINGS": {
          "outputfile": [
            "hdfs://ec2-34-205-203-38.compute-1.amazonaws.com:8020/dev/dataset/subset1-0gm5lhts71"
          ],
          "metadata": {
            "url": "34.196.204.54:9012/api/get_metadata_for_mlscripts/",
            "slug_list": [
              "subsetting_testcsv-kbyr49hzml"
            ]
          },
          "inputfile": [
            "file:///home/gulshan/marlabs/datasets/subsetting_test.csv"
          ]
        },
        "DATE_SETTINGS": {

        }
      },
      "job_config": {
        "message_url": "http://34.196.204.54:9012/api/messages/Job_subsetting-subset1-0gm5lhts71-9a3n7yckyl_123/",
        "get_config": {
          "action": "get_config",
          "method": "GET"
        },
        "error_reporting_url": "http://34.196.204.54:9012/api/set_job_report/subsetting-subset1-0gm5lhts71-9a3n7yckyl/",
        "set_result": {
          "action": "result",
          "method": "PUT"
        },
        "job_url": "http://34.196.204.54:9012/api/job/subsetting-subset1-0gm5lhts71-9a3n7yckyl/",
        "job_type": "subSetting",
        "job_name": "subset1",
        "xml_url": "http://34.196.204.54:9012/api/xml/subsetting-subset1-0gm5lhts71-9a3n7yckyl/"
      }
    }
    return subsettingConfig
