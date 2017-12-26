def get_subsetting_config():
    subsettingConfig = {
        "job_config": {
          "job_url": "http://34.196.204.54:9012/api/job/subsetting-subset-gul-rdixv7igls-q1768cgtjh/",
          "job_type": "subSetting",
          "xml_url": "http://34.196.204.54:9012/api/xml/subsetting-subset-gul-rdixv7igls-q1768cgtjh/",
          "get_config": {
            "action": "get_config",
            "method": "GET"
          },
          "set_result": {
            "action": "result",
            "method": "PUT"
          },
          "message_url": "http://34.196.204.54:9012/api/messages/Dataset_subset-gul-rdixv7igls_123/",
          "job_name": "subset-gul"
        },
        "config": {
          "FILTER_SETTINGS": {
            "measureColumnFilters": [
              {
                "filterType": "valueRange",
                "lowerBound": 10701,
                "colname": "CREDIT_BALANCE1",
                "upperBound": 21600
              }
            ],
            "dimensionColumnFilters": [
              {
                "filterType": "valueIn",
                "values": [
                  "High School",
                  "Graduate School",
                  "Others"
                ],
                "colname": "EDUCATION"
              }
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
                "slug": "e68463a473d644bfb70020f554b58c00",
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
                  }
                ]
              },
              {
                "slug": "0c32c0443898415799869dede76c5b0d",
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
                  }
                ]
              },
              {
                "slug": "f203f443307e4e2a9e80401d84852bcf",
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
                  }
                ]
              },
              {
                "slug": "470bcc2e31764c41904195f2ea83037f",
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
                  }
                ]
              },
              {
                "slug": "114c83f54efb4382950a0f815a2a4a29",
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
                  }
                ]
              },
              {
                "slug": "93d8b1002b85442392c3c83bd8c1e79b",
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
                  }
                ]
              },
              {
                "slug": "7c2aa0071e964a9dac11b411f1d9eab6",
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
                  }
                ]
              },
              {
                "slug": "5f3a3b72d3324cc8b66169e07356c834",
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
                  }
                ]
              },
              {
                "slug": "b1f65a708db74d6598c68881a6eb86af",
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
                  }
                ]
              },
              {
                "slug": "b25433efbc9a472ca9d19194c97eb4a6",
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
                  }
                ]
              }
            ]
          },
          "FILE_SETTINGS": {
            "outputfile": [
              "file:///home/gulshan/marlabs/csvout/data"
            ],
            "inputfile": [
              "file:///home/gulshan/marlabs/datasets/subsetting_test.csv"
            ]
          },
          "DATE_SETTINGS": {

          }
        }
    }
    return subsettingConfig
