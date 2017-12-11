def get_subsetting_config():
    subsettingConfig = {
        "config" : {
                    "COLUMN_SETTINGS" : {
                        "analysis_type" : [
                            "metaData"
                        ]
                    },
                    "DATA_SOURCE" : {
                        "datasource_details" : "",
                        "datasource_type" : "fileUpload"
                    },
                    "DATE_SETTINGS" : {},
                    "FILE_SETTINGS" : {
                        "inputfile" : [
                            # "hdfs://ec2-34-205-203-38.compute-1.amazonaws.com:8020/dev/dataset/subsetting_testcsv-zxhdwhl5u2/subsetting_test_3n3aZh5.csv"
                            "file:///home/gulshan/marlabs/datasets/subsetting_test.csv"
                        ],
                        "outputfile" : [
                            # "hdfs://ec2-34-205-203-38.compute-1.amazonaws.com:8020/dev/dataset/subsetting_test_new-tqj35ger3q"
                            "file:///home/gulshan/marlabs/csvout/data"
                        ]
                    },
                    "FILTER_SETTINGS" : {
                        "dimensionColumnFilters" : [],
                        "measureColumnFilters" : [],
                        "timeDimensionColumnFilters" : []
                    },
                    "TRANSFORMATION_SETTINGS" : {
                        "existingColumns" : [
                            {
                                "columnSetting" : [
                                    {
                                        "actionName" : "delete",
                                        "displayName" : "Delete Column",
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "rename",
                                        "displayName" : "Rename Column",
                                        "newName" : None,
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "replace",
                                        "displayName" : "Replace Values",
                                        "replaceTypeList" : [
                                            {
                                                "displayName" : "Contains",
                                                "name" : "contains"
                                            },
                                            {
                                                "displayName" : "Equal To",
                                                "name" : "equals"
                                            },
                                            {
                                                "displayName" : "Starts With",
                                                "name" : "startsWith"
                                            },
                                            {
                                                "displayName" : "Ends With",
                                                "name" : "endsWith"
                                            }
                                        ],
                                        "replacementValues" : [],
                                        "status" : False
                                    }
                                ],
                                "name" : "CREDIT_BALANCE1",
                                "slug" : "167338ffe707492a9a2f0667ecc26a13"
                            },
                            {
                                "columnSetting" : [
                                    {
                                        "actionName" : "delete",
                                        "displayName" : "Delete Column",
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "rename",
                                        "displayName" : "Rename Column",
                                        "newName" : None,
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "replace",
                                        "displayName" : "Replace Values",
                                        "replaceTypeList" : [
                                            {
                                                "displayName" : "Contains",
                                                "name" : "contains"
                                            },
                                            {
                                                "displayName" : "Equal To",
                                                "name" : "equals"
                                            },
                                            {
                                                "displayName" : "Starts With",
                                                "name" : "startsWith"
                                            },
                                            {
                                                "displayName" : "Ends With",
                                                "name" : "endsWith"
                                            }
                                        ],
                                        "replacementValues" : [],
                                        "status" : False
                                    }
                                ],
                                "name" : "CREDIT_BALANCE2",
                                "slug" : "8b94ae1a2fa54e14b6602ac25344085f"
                            },
                            {
                                "columnSetting" : [
                                    {
                                        "actionName" : "delete",
                                        "displayName" : "Delete Column",
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "rename",
                                        "displayName" : "Rename Column",
                                        "newName" : None,
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "replace",
                                        "displayName" : "Replace Values",
                                        "replaceTypeList" : [
                                            {
                                                "displayName" : "Contains",
                                                "name" : "contains"
                                            },
                                            {
                                                "displayName" : "Equal To",
                                                "name" : "equals"
                                            },
                                            {
                                                "displayName" : "Starts With",
                                                "name" : "startsWith"
                                            },
                                            {
                                                "displayName" : "Ends With",
                                                "name" : "endsWith"
                                            }
                                        ],
                                        "replacementValues" : [],
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "data_type",
                                        "displayName" : "Change Datatype",
                                        "listOfActions" : [
                                            {
                                                "displayName" : "Numeric",
                                                "name" : "numeric",
                                                "status" : True
                                            },
                                            {
                                                "displayName" : "Text",
                                                "name" : "text",
                                                "status" : False
                                            }
                                        ],
                                        "status" : True
                                    }
                                ],
                                "name" : "CREDIT_BALANCE3",
                                "slug" : "684126299d4742c58ca9b460e5ff43a1"
                            },
                            {
                                "columnSetting" : [
                                    {
                                        "actionName" : "delete",
                                        "displayName" : "Delete Column",
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "rename",
                                        "displayName" : "Rename Column",
                                        "newName" : None,
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "replace",
                                        "displayName" : "Replace Values",
                                        "replaceTypeList" : [
                                            {
                                                "displayName" : "Contains",
                                                "name" : "contains"
                                            },
                                            {
                                                "displayName" : "Equal To",
                                                "name" : "equals"
                                            },
                                            {
                                                "displayName" : "Starts With",
                                                "name" : "startsWith"
                                            },
                                            {
                                                "displayName" : "Ends With",
                                                "name" : "endsWith"
                                            }
                                        ],
                                        "replacementValues" : [],
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "data_type",
                                        "displayName" : "Change Datatype",
                                        "listOfActions" : [
                                            {
                                                "displayName" : "Numeric",
                                                "name" : "numeric",
                                                "status" : False
                                            },
                                            {
                                                "displayName" : "Text",
                                                "name" : "text",
                                                "status" : False
                                            }
                                        ],
                                        "status" : False
                                    }
                                ],
                                "name" : "SEX",
                                "slug" : "27aadfb44d8f4fcc837654316e9b1bf4"
                            },
                            {
                                "columnSetting" : [
                                    {
                                        "actionName" : "delete",
                                        "displayName" : "Delete Column",
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "rename",
                                        "displayName" : "Rename Column",
                                        "newName" : None,
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "replace",
                                        "displayName" : "Replace Values",
                                        "replaceTypeList" : [
                                            {
                                                "displayName" : "Contains",
                                                "name" : "contains"
                                            },
                                            {
                                                "displayName" : "Equal To",
                                                "name" : "equals"
                                            },
                                            {
                                                "displayName" : "Starts With",
                                                "name" : "startsWith"
                                            },
                                            {
                                                "displayName" : "Ends With",
                                                "name" : "endsWith"
                                            }
                                        ],
                                        "replacementValues" : [],
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "data_type",
                                        "displayName" : "Change Datatype",
                                        "listOfActions" : [
                                            {
                                                "displayName" : "Numeric",
                                                "name" : "numeric",
                                                "status" : False
                                            },
                                            {
                                                "displayName" : "Text",
                                                "name" : "text",
                                                "status" : False
                                            }
                                        ],
                                        "status" : False
                                    }
                                ],
                                "name" : "EDUCATION",
                                "slug" : "c5c42c0f7b3a4632bd7e0269f998ec30"
                            },
                            {
                                "columnSetting" : [
                                    {
                                        "actionName" : "delete",
                                        "displayName" : "Delete Column",
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "rename",
                                        "displayName" : "Rename Column",
                                        "newName" : None,
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "replace",
                                        "displayName" : "Replace Values",
                                        "replaceTypeList" : [
                                            {
                                                "displayName" : "Contains",
                                                "name" : "contains"
                                            },
                                            {
                                                "displayName" : "Equal To",
                                                "name" : "equals"
                                            },
                                            {
                                                "displayName" : "Starts With",
                                                "name" : "startsWith"
                                            },
                                            {
                                                "displayName" : "Ends With",
                                                "name" : "endsWith"
                                            }
                                        ],
                                        "replacementValues" : [],
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "data_type",
                                        "displayName" : "Change Datatype",
                                        "listOfActions" : [
                                            {
                                                "displayName" : "Numeric",
                                                "name" : "numeric",
                                                "status" : False
                                            },
                                            {
                                                "displayName" : "Text",
                                                "name" : "text",
                                                "status" : False
                                            }
                                        ],
                                        "status" : False
                                    }
                                ],
                                "name" : "MARRIAGE",
                                "slug" : "800b2f543eb5455a8ffcbc48bcdc0abf"
                            },
                            {
                                "columnSetting" : [
                                    {
                                        "actionName" : "delete",
                                        "displayName" : "Delete Column",
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "rename",
                                        "displayName" : "Rename Column",
                                        "newName" : None,
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "replace",
                                        "displayName" : "Replace Values",
                                        "replaceTypeList" : [
                                            {
                                                "displayName" : "Contains",
                                                "name" : "contains"
                                            },
                                            {
                                                "displayName" : "Equal To",
                                                "name" : "equals"
                                            },
                                            {
                                                "displayName" : "Starts With",
                                                "name" : "startsWith"
                                            },
                                            {
                                                "displayName" : "Ends With",
                                                "name" : "endsWith"
                                            }
                                        ],
                                        "replacementValues" : [],
                                        "status" : False
                                    }
                                ],
                                "name" : "new_date",
                                "slug" : "5e1fb20628d04549970d84da96fcb60e"
                            },
                            {
                                "columnSetting" : [
                                    {
                                        "actionName" : "delete",
                                        "displayName" : "Delete Column",
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "rename",
                                        "displayName" : "Rename Column",
                                        "newName" : None,
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "replace",
                                        "displayName" : "Replace Values",
                                        "replaceTypeList" : [
                                            {
                                                "displayName" : "Contains",
                                                "name" : "contains"
                                            },
                                            {
                                                "displayName" : "Equal To",
                                                "name" : "equals"
                                            },
                                            {
                                                "displayName" : "Starts With",
                                                "name" : "startsWith"
                                            },
                                            {
                                                "displayName" : "Ends With",
                                                "name" : "endsWith"
                                            }
                                        ],
                                        "replacementValues" : [],
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "data_type",
                                        "displayName" : "Change Datatype",
                                        "listOfActions" : [
                                            {
                                                "displayName" : "Numeric",
                                                "name" : "numeric",
                                                "status" : False
                                            },
                                            {
                                                "displayName" : "Text",
                                                "name" : "text",
                                                "status" : False
                                            }
                                        ],
                                        "status" : False
                                    }
                                ],
                                "name" : "colToReplace",
                                "slug" : "d8f87c8c454f4aae992a0f05cc9b2edb"
                            },
                            {
                                "columnSetting" : [
                                    {
                                        "actionName" : "delete",
                                        "displayName" : "Delete Column",
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "rename",
                                        "displayName" : "Rename Column",
                                        "newName" : None,
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "replace",
                                        "displayName" : "Replace Values",
                                        "replaceTypeList" : [
                                            {
                                                "displayName" : "Contains",
                                                "name" : "contains"
                                            },
                                            {
                                                "displayName" : "Equal To",
                                                "name" : "equals"
                                            },
                                            {
                                                "displayName" : "Starts With",
                                                "name" : "startsWith"
                                            },
                                            {
                                                "displayName" : "Ends With",
                                                "name" : "endsWith"
                                            }
                                        ],
                                        "replacementValues" : [],
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "data_type",
                                        "displayName" : "Change Datatype",
                                        "listOfActions" : [
                                            {
                                                "displayName" : "Numeric",
                                                "name" : "numeric",
                                                "status" : False
                                            },
                                            {
                                                "displayName" : "Text",
                                                "name" : "text",
                                                "status" : False
                                            }
                                        ],
                                        "status" : False
                                    }
                                ],
                                "name" : "toDelete",
                                "slug" : "28b1ba754bfa4782a644ed93357cf1e9"
                            },
                            {
                                "columnSetting" : [
                                    {
                                        "actionName" : "delete",
                                        "displayName" : "Delete Column",
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "rename",
                                        "displayName" : "Rename Column",
                                        "newName" : None,
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "replace",
                                        "displayName" : "Replace Values",
                                        "replaceTypeList" : [
                                            {
                                                "displayName" : "Contains",
                                                "name" : "contains"
                                            },
                                            {
                                                "displayName" : "Equal To",
                                                "name" : "equals"
                                            },
                                            {
                                                "displayName" : "Starts With",
                                                "name" : "startsWith"
                                            },
                                            {
                                                "displayName" : "Ends With",
                                                "name" : "endsWith"
                                            }
                                        ],
                                        "replacementValues" : [],
                                        "status" : False
                                    },
                                    {
                                        "actionName" : "data_type",
                                        "displayName" : "Change Datatype",
                                        "listOfActions" : [
                                            {
                                                "displayName" : "Numeric",
                                                "name" : "numeric",
                                                "status" : False
                                            },
                                            {
                                                "displayName" : "Text",
                                                "name" : "text",
                                                "status" : False
                                            }
                                        ],
                                        "status" : False
                                    }
                                ],
                                "name" : "toReplace",
                                "slug" : "e628974095ce42de8e5114976979db0e"
                            }
                        ]
                    }
                },
                "job_config" : {
                    "get_config" : {
                        "action" : "get_config",
                        "method" : "GET"
                    },
                    "job_name" : "subsetting_test_new",
                    "job_type" : "subSetting",
                    "job_url" : "http://34.196.204.54:9012/api/job/subsetting-subsetting_test_new-tqj35ger3q-bp9kq1alzn/",
                    "message_url" : "http://34.196.204.54:9012/api/messages/Dataset_subsetting_test_new-tqj35ger3q_123/",
                    "set_result" : {
                        "action" : "result",
                        "method" : "PUT"
                    }
                }
    }
    return subsettingConfig
