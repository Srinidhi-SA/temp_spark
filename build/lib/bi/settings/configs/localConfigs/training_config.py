def get_training_config():
    trainConfigClassification = {
  "job_config": {
    "message_url": "https://madvisor-dev.marlabsai.com/api/messages/Job_model-security-finance-0xn9ykzfy3-k5ftzql0me_123/",
    "config_url": "https://madvisor-dev.marlabsai.com/api/job/model-security-finance-0xn9ykzfy3-k5ftzql0me/get_config",
    "initial_messages": "https://madvisor-dev.marlabsai.com/api/job/model-security-finance-0xn9ykzfy3-k5ftzql0me/dump_complete_messages/",
    "get_config": {
      "action": "get_config",
      "method": "GET"
    },
    "xml_url": "https://madvisor-dev.marlabsai.com/api/xml/model-security-finance-0xn9ykzfy3-k5ftzql0me/",
    "error_reporting_url": "https://madvisor-dev.marlabsai.com/api/set_job_report/model-security-finance-0xn9ykzfy3-k5ftzql0me/",
    "set_result": {
      "action": "result",
      "method": "PUT"
    },
    "job_type": "training",
    "job_url": "https://madvisor-dev.marlabsai.com/api/job/model-security-finance-0xn9ykzfy3-k5ftzql0me/",
    "job_name": "security finance",
    "app_id": 2,
    "kill_url": "https://madvisor-dev.marlabsai.com/api/job/model-security-finance-0xn9ykzfy3-k5ftzql0me/rest_in_peace/"
  },
  "config": {
    "FILE_SETTINGS": {
      "inputfile": [
        "https://madvisor-dev.marlabsai.com/media/datasets/security_finance_new_columns_dzzFVnk.csv"
      ],
      "validationTechnique": [
        {
          "value": 2,
          "displayName": "K Fold Validation",
          "name": "kFold"
        }
      ],
      "analysis_type": [
        "training"
      ],
      "app_type": "classification",
      "modelpath": [
        "security-finance-0xn9ykzfy3"
      ],
      "metadata": {
        "url": "https://madvisor-dev.marlabsai.com/api/get_metadata_for_mlscripts/",
        "slug_list": [
          "security_finance_new_columns-cuvvi5t0wx"
        ]
      },
      "targetLevel": "Yes"
    },
    "FEATURE_SETTINGS": {
      "DATA_CLEANSING": {
        "columns_wise_settings": {
          "missing_value_treatment": {
            "selected": True,
            "displayName": "Missing value treatment",
            "name": "missing_value_treatment",
            "operations": [
              {
                "columns": [

                ],
                "selected": False,
                "displayName": "Mean Imputation",
                "name": "mean_imputation",
                "slug": "MT0cf0H3rNXyaVhXHtiP43"
              },
              {
                "columns": [

                ],
                "selected": False,
                "displayName": "Mode Imputation",
                "name": "mode_imputation",
                "slug": "mZbFlJkOkeKsneDHDqNIXE"
              },
              {
                "columns": [

                ],
                "selected": False,
                "displayName": "Median Imputation",
                "name": "median_imputation",
                "slug": "ToO7vD2uKTyHMBjLs26dgU"
              },
              {
                "columns": [

                ],
                "selected": False,
                "displayName": "Backward Filling",
                "name": "backward_filling",
                "slug": "cFruIkyFXLbarvFeObC1Rx"
              },
              {
                "columns": [

                ],
                "selected": False,
                "displayName": "Forward Filling",
                "name": "forward_filling",
                "slug": "zu5VKiX2n5MqEP0jge9TSJ"
              },
              {
                "columns": [

                ],
                "selected": False,
                "displayName": "Regression Imputation",
                "name": "regression_imputation",
                "slug": "cpDLZigzHSekw7y90kioQn"
              },
              {
                "columns": [

                ],
                "selected": False,
                "displayName": "Stocastic Imputation",
                "name": "stocastic_imputation",
                "slug": "Tm4E16v15xUF7BZznuYpOs"
              },
              {
                "columns": [

                ],
                "selected": False,
                "displayName": "Logistic regression imputation",
                "name": "logistic_regression_imputation",
                "slug": "phPtnl4Dt6Dcdy5erCINXI"
              },
              {
                "columns": [

                ],
                "selected": False,
                "displayName": "Discriminant analysis imputation",
                "name": "discriminant_analysis_imputation",
                "slug": "tbeVfqh4GYxoSivkKiTMoy"
              },
              {
                "columns": [

                ],
                "selected": False,
                "displayName": "KNN imputation",
                "name": "knn_imputation",
                "slug": "x5FU8rJgsgrJDNPsZUaQ7F"
              },
              {
                "columns": [

                ],
                "selected": False,
                "displayName": "None",
                "name": "none",
                "slug": "ggususBEm6Uhj7zDMKGUrN"
              }
            ]
          },
          "outlier_removal": {
            "selected": True,
            "displayName": "Outlier treatment",
            "name": "outlier_treatment",
            "operations": [
              {
                "columns": [

                ],
                "selected": False,
                "displayName": "Cap Outliers",
                "name": "cap_outliers",
                "slug": "J47WSI7DgZDx4ROTBNahp"
              },
              {
                "columns": [

                ],
                "selected": False,
                "displayName": "Replace with Mean",
                "name": "replace_with_mean",
                "slug": "RMN20VRhZBrIoI3M41UF8D"
              },
              {
                "columns": [

                ],
                "selected": False,
                "displayName": "Replace with Median",
                "name": "replace_with_median",
                "slug": "2MWuRulQahdbkD66y3R0b0"
              }
            ]
          }
        },
        "slug": "",
        "name": "data_cleansing",
        "selected": False,
        "displayName": "Data Cleansing",
        "overall_settings": [
          {
            "selected": False,
            "displayName": "Do you want to remove duplicate attributes/columns in the dataset?",
            "name": "duplicate_column",
            "slug": "vjYloNUHxUqjPFTC9Oc8nm"
          },
          {
            "selected": False,
            "displayName": "Do you want to remove duplicate observations  in the dataset?",
            "name": "duplicate_row",
            "slug": "4e0mzsNOeiVG4SzRFu1mpp"
          }
        ]
      },
      "FEATURE_ENGINEERING": {
        "slug": "",
        "name": "feature_engineering",
        "column_wise_settings": {
          "transformation_settings": {
            "selected": False,
            "displayName": "Transform Variables",
            "name": "transformation_settings",
            "operations": [
              {
                "name": "replace_values_with",
                "selected": False,
                "displayName": "Replace Values With",
                "columns": [

                ]
              },
              {
                "name": "add_value_to",
                "selected": False,
                "displayName": "Add Specific value",
                "columns": [

                ]
              },
              {
                "name": "subtract_value_from",
                "selected": False,
                "displayName": "Subtract Specific value",
                "columns": [

                ]
              },
              {
                "name": "multiply_by_value",
                "selected": False,
                "displayName": "Multiply by Specific value",
                "columns": [

                ]
              },
              {
                "name": "divide_by_value",
                "selected": False,
                "displayName": "Divide by Specific value",
                "columns": [

                ]
              },
              {
                "name": "perform_standardization",
                "selected": False,
                "displayName": "Perform Standardization",
                "columns": [

                ]
              },
              {
                "name": "variable_transformation",
                "selected": False,
                "displayName": "Variable Transformation",
                "columns": [

                ]
              },
              {
                "name": "encoding_dimensions",
                "selected": False,
                "displayName": "Perform Encoding",
                "columns": [

                ]
              },
              {
                "name": "return_character_count",
                "selected": False,
                "displayName": "return Character Count",
                "columns": [

                ]
              },
              {
                "name": "is_custom_string_in",
                "selected": False,
                "displayName": "Is custom string in",
                "columns": [

                ]
              },
              {
                "name": "is_date_weekend",
                "selected": False,
                "displayName": "Is Date Weekend",
                "columns": [

                ]
              },
              {
                "name": "extract_time_feature",
                "selected": False,
                "displayName": "Extract Time Feature",
                "columns": [

                ]
              },
              {
                "name": "time_since",
                "selected": False,
                "displayName": "Time Since Some Event",
                "columns": [

                ]
              }
            ]
          },
          "level_creation_settings": {
            "selected": False,
            "displayName": "Create Bins Or Levels",
            "name": "creating_new_bins_or_levels",
            "operations": [
              {
                "name": "create_equal_sized_bins",
                "selected": False,
                "displayName": "Create Equal Sized Bins",
                "columns": [

                ]
              },
              {
                "name": "create_custom_bins",
                "selected": False,
                "displayName": "Create Custom Bins",
                "columns": [

                ]
              },
              {
                "name": "create_new_levels",
                "selected": False,
                "displayName": "Create Levels",
                "columns": [

                ]
              },
              {
                "name": "create_new_datetime_levels",
                "selected": False,
                "displayName": "Create Datetime Levels",
                "columns": [

                ]
              }
            ]
          }
        },
        "selected": False,
        "displayName": "Feature Engineering",
        "overall_settings": [
          {
            "number_of_bins": 10,
            "selected": False,
            "displayName": "Bin all Measures",
            "name": "binning_all_measures",
            "slug": ""
          }
        ]
      }
    },
    "ALGORITHM_SETTING": [

    ],
    "COLUMN_SETTINGS": {
      "variableSelection": [
        {
          "targetColumn": False,
          "actualColumnType": "dimension",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "a050b4c097274455aae397c5b31f21d5",
          "name": "ACCOUNT_CLASS",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "dimension",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "dimension",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "a7c23dcc89754773bfc1511c11a325b0",
          "name": "ACCOUNT_STATUS",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "dimension",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "dimension",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "b0c445c36114412a9b67f33c25e67c34",
          "name": "ALLOW_SOLICITATION",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "dimension",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "measure",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "003b1b2f5d4346af891f88aba758b7fb",
          "name": "AMOUNT_PAID",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "measure",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "measure",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "ba243abbda52475b8499cb437a6af737",
          "name": "APPROVED_AMOUNT",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "measure",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "measure",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "351dac3728844e6b82dd61c7b614baa1",
          "name": "CURRENT_PRINCIPLE_AMOUNT",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "measure",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "dimension",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "c7aab8668c114d90a48210e849d1d84e",
          "name": "CUSTOMER_STATUS",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "dimension",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "dimension",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "8e0915358d4444efb5435cf90c0bfdd1",
          "name": "DELINQUENCY_STATUS",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "dimension",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "datetime",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "69d7d771fe7f420aba671afe9f9ab601",
          "name": "ENTRY_DATETIME",
          "polarity": None,
          "uidCol": False,
          "selected": False,
          "columnType": "datetime",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "measure",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "01d9cb5ae9fc40f3a427692a345e0324",
          "name": "HIGHEST_ACCOUNT",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "measure",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "dimension",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "3f9cbd6acd4d40539e9a131285cde893",
          "name": "MARITAL_STATUS",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "dimension",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "dimension",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "4ce85149a344438d9a86eba2a3e8873a",
          "name": "MI",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "dimension",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "measure",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "e81a6a42c8a44234a03c1b8e033b4308",
          "name": "NUMBER_OF_ACCOUNTS",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "measure",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "measure",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "9c181422e19a4465aa85db276f1fb023",
          "name": "ORIGINAL_PRINCIPLE_AMOUNT",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "measure",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "measure",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "baf303b5987144b89cdcba7560c3ab91",
          "name": "ORIG_FINANCE_CHRGE_AMT",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "measure",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "dimension",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "b5e53885132f4622bf4b524700a91d8e",
          "name": "PAY_OPT_PERSONAL_CHK",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "dimension",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "measure",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "a750b4fae4c04456bbf89084fbc4c9ad",
          "name": "SALARY",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "measure",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "dimension",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "2d10fcc6b10043da872677de7ae1824d",
          "name": "SALARY_PERIOD_TYPE",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "dimension",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "dimension",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "05a39d9beff44d3ba3d8df6e6216cc14",
          "name": "ability",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "dimension",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "dimension",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "d448412c9ffb4acbb49db6b4aeddef2e",
          "name": "account_status_class",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "dimension",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "dimension",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "3dfb655cc8584eeba10fba30c553a5d5",
          "name": "allow_allotment",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "dimension",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "measure",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "2319481665694a91a02921b40ad1e63a",
          "name": "apr_rate",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "measure",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "dimension",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "f4b25817d12c4e139932ed370e6cbb2d",
          "name": "auto",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "dimension",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "measure",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "22c92bf139524075973e8924e90eed38",
          "name": "auto1payment",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "measure",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "dimension",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "80c444f1c1b740329c02dc1f1fb48704",
          "name": "auto1title",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "dimension",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "dimension",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "5964fa813ecc4e66932bf18b7bf10770",
          "name": "bankrupt",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "dimension",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "measure",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "87f7e5fe5f4e4b629a10cfb83e952229",
          "name": "contractual_payments_made",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "measure",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "measure",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "bc0a8ffa92424915aecc9bd9d6ad7cb1",
          "name": "credit_limit",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "measure",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "measure",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "fb934202af984c539ec1fe9d89470408",
          "name": "credit_limt_diff",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "measure",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "measure",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "faef966d74af4c67ba514a4c3c6c10cd",
          "name": "current_other_charge_amt",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "measure",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "measure",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "8f2b2cf0f3384e17af006b885c822bee",
          "name": "del_1_count",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "measure",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "measure",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "55767b7c6890487fa5b55bcd87e6cb52",
          "name": "del_2_count",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "measure",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "measure",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "a0a5cae91a074aee9a9ee4dc419aeed4",
          "name": "del_3_count",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "measure",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "measure",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "32fa3a2a2a7b4b2cb561e2c934c1d313",
          "name": "del_p_count",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "measure",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": True,
          "actualColumnType": "dimension",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "6e87ae00f82949bead3bf04b58871720",
          "name": "denied",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "dimension",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "measure",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "3c3fdaf6abfa498bbe0993bd1bc48760",
          "name": "dependents",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "measure",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "dimension",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "3ae7562873c146b68f02ce358ec0d01c",
          "name": "employment_verified",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "dimension",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "dimension",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "b38d705330af43799f9d30b0e90d6720",
          "name": "hardship_status",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "dimension",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "dimension",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "2774c0cd014f46bab2a69b94ed3d68f5",
          "name": "hometown_state",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "dimension",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "dimension",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "362bb4ca9efb466d9eb14b7c07bfc14e",
          "name": "is_reffered",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "dimension",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "measure",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "adfa1fd6622845f4ae33337c451767fa",
          "name": "landlord_amt",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "measure",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "measure",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "2b1aa7c7cd0643d6af2e9aebfbbf9eb3",
          "name": "last_charg_diff",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "measure",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "dimension",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "a8ab1ac5220f4a6786b4b31917ffd54f",
          "name": "opted_out",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "dimension",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "measure",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "adcd7ed62b214f93a22e9e2085bc2549",
          "name": "original_other_charge_amt",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "measure",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "dimension",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "0982cadf01ba42fd8d2329ba7a40dbfa",
          "name": "personal",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "dimension",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "dimension",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "484405b4c38e42338a602d3613901177",
          "name": "phoneapp",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "dimension",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "dimension",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "218262143d544ef080eb2b3e9ca27234",
          "name": "purpose",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "dimension",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "measure",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "8e48bd6af6a044c69e177807e35509aa",
          "name": "renewal_payoff_prior_account",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "measure",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "measure",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "f559050d5bd146ac98c19b2a60d55a47",
          "name": "requested_amount",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "measure",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "dimension",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "76c91ee072b244dc8e640313c182d2ed",
          "name": "residence_verified",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "dimension",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "dimension",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "bb17328afe8d43b196ba4742d558dd66",
          "name": "stability_emp",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "dimension",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "dimension",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "c9d27f6c646045f6863a5b27612657fc",
          "name": "stability_res",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "dimension",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "measure",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "28c16aa28c734cd4b2df3f197f6776ac",
          "name": "total_length",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "measure",
          "targetColSetVarAs": None
        },
        {
          "targetColumn": False,
          "actualColumnType": "dimension",
          "setVarAs": None,
          "dateSuggestionFlag": False,
          "slug": "8dd9f8a423d7472082e444eaa6ff89ec",
          "name": "willingness",
          "polarity": None,
          "uidCol": False,
          "selected": True,
          "columnType": "dimension",
          "targetColSetVarAs": None
        }
      ]
    },
    "DATA_SOURCE": {
      "datasource_type": "fileUpload",
      "datasource_details": ""
    },
    "TRAINER_MODE": "autoML"
  }
}
    trainingConfigRegression = {
      "config": {
        "COLUMN_SETTINGS": {
          "variableSelection": [
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "measure",
              "name": "age",
              "selected": True,
              "actualColumnType": "measure",
              "slug": "4027162c25bc426791ad5ea5b86f66c4",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": True,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "workclass",
              "selected": True,
              "actualColumnType": "dimension",
              "slug": "360fae82dac34befaef1959cbc48f958",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "measure",
              "name": "fnlwgt",
              "selected": True,
              "actualColumnType": "measure",
              "slug": "9a63bb9fe2fa4cfea24680e9285230d5",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "education",
              "selected": True,
              "actualColumnType": "dimension",
              "slug": "ffad161b78434353917c7af7baaf714c",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "measure",
              "name": "education-num",
              "selected": True,
              "actualColumnType": "measure",
              "slug": "1f3a3cecacb14ff3bdcb6a19dfa3ec5e",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "marital-status",
              "selected": True,
              "actualColumnType": "dimension",
              "slug": "88dc82c43a234afaa13c79c0b75b4a6d",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "occupation",
              "selected": True,
              "actualColumnType": "dimension",
              "slug": "867e002a86424293a1bdedd5d1842258",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "relationship",
              "selected": True,
              "actualColumnType": "dimension",
              "slug": "9f56667995ef4d069faf5c7dc73a36a2",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "race",
              "selected": True,
              "actualColumnType": "dimension",
              "slug": "57922dd2d8174751ac4ec2b038c5b249",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "sex",
              "selected": True,
              "actualColumnType": "dimension",
              "slug": "ffa0bb5e67c04111b60cfdb307b31246",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "measure",
              "name": "Capital-gain",
              "selected": True,
              "actualColumnType": "measure",
              "slug": "a0a5e768300249cdb71a783703bad23c",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "measure",
              "name": "Capital-loss",
              "selected": True,
              "actualColumnType": "measure",
              "slug": "f53b09062c3c4ba1a8529c8a0ab3c545",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "measure",
              "name": "hours-per-week",
              "selected": True,
              "actualColumnType": "measure",
              "slug": "410e68f42c5d4c1782aa4664e471d546",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "native-country",
              "selected": True,
              "actualColumnType": "dimension",
              "slug": "2274768114cd49fbb4dabb5a88668d34",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "class_label",
              "selected": True,
              "actualColumnType": "dimension",
              "slug": "1e829e7c75ec4bffbe4ab9c0b3fbbf76",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            }
          ]
        },
        "ALGORITHM_SETTING": [
          {
            "description": "fill in the blanks",
            "parameters": [
              {
                "expectedDataType": [
                  "int"
                ],
                "displayName": "No Of Jobs",
                "description": "Number of CPU cores used when parallelizing over classes",
                "paramType": "number",
                "acceptedValue": None,
                "valueRange": [
                  -1,
                  4
                ],
                "hyperpatameterTuningCandidate": False,
                "uiElemType": "slider",
                "allowedDataType": [
                  "int"
                ],
                "display": True,
                "name": "n_jobs"
              },
              {
                "expectedDataType": [
                  "bool"
                ],
                "displayName": "Fit Intercept",
                "name": "fit_intercept",
                "paramType": "list",
                "defaultValue": [
                  {
                    "selected": False,
                    "displayName": "False",
                    "name": "False"
                  },
                  {
                    "selected": True,
                    "displayName": "True",
                    "name": "True"
                  }
                ],
                "hyperpatameterTuningCandidate": True,
                "uiElemType": "checkbox",
                "description": "It specifies whether to calculate the intercept for this model. If set to False, no intercept will be used in calculations",
                "display": True,
                "allowedDataType": [
                  "bool"
                ]
              },
              {
                "expectedDataType": [
                  "bool"
                ],
                "displayName": "Normalize",
                "name": "normalize",
                "paramType": "list",
                "defaultValue": [
                  {
                    "selected": True,
                    "displayName": "False",
                    "name": "False"
                  },
                  {
                    "selected": False,
                    "displayName": "True",
                    "name": "True"
                  }
                ],
                "hyperpatameterTuningCandidate": True,
                "uiElemType": "checkbox",
                "description": "If True, the regressors X will be normalized before regression",
                "display": True,
                "allowedDataType": [
                  "bool"
                ]
              },
              {
                "expectedDataType": [
                  "bool"
                ],
                "displayName": "Copy X",
                "name": "copy_X",
                "paramType": "list",
                "defaultValue": [
                  {
                    "selected": False,
                    "displayName": "False",
                    "name": "False"
                  },
                  {
                    "selected": True,
                    "displayName": "True",
                    "name": "True"
                  }
                ],
                "hyperpatameterTuningCandidate": True,
                "uiElemType": "checkbox",
                "description": "If True, X will be copied; else, it may be overwritten",
                "display": True,
                "allowedDataType": [
                  "bool"
                ]
              }
            ],
            "selected": True,
            "algorithmSlug": "f77631ce2ab24cf78c55bb6a5fce4db8linr",
            "algorithmName": "Linear Regression",
            "hyperParameterSetting": [
              {
                "displayName": "Grid Search",
                "selected": False,
                "params": [
                  {
                    "expectedDataType": [
                      None,
                      "string"
                    ],
                    "displayName": "Metric Used for Optimization",
                    "name": "evaluationMetric",
                    "paramType": "list",
                    "display": True,
                    "uiElemType": "dropDown",
                    "defaultValue": [
                      {
                        "selected": True,
                        "displayName": "R-Squared",
                        "name": "r2"
                      },
                      {
                        "selected": False,
                        "displayName": "MAE",
                        "name": "neg_mean_absolute_error"
                      },
                      {
                        "selected": False,
                        "displayName": "MSE",
                        "name": "neg_mean_squared_error"
                      },
                      {
                        "selected": False,
                        "displayName": "MSE(log)",
                        "name": "neg_mean_squared_log_error"
                      }
                    ]
                  },
                  {
                    "expectedDataType": [
                      None,
                      "int"
                    ],
                    "displayName": "No Of Folds to Use",
                    "name": "kFold",
                    "display": True,
                    "paramType": "number",
                    "acceptedValue": None,
                    "valueRange": [
                      2,
                      10
                    ],
                    "uiElemType": "slider",
                    "defaultValue": 3
                  }
                ],
                "name": "gridsearchcv"
              },
              {
                "displayName": "None",
                "selected": True,
                "params": None,
                "name": "none"
              }
            ]
          },
          {
            "description": "fill in the blanks",
            "parameters": [
              {
                "expectedDataType": [
                  "string"
                ],
                "displayName": "Loss Function",
                "name": "loss",
                "paramType": "list",
                "defaultValue": [
                  {
                    "selected": True,
                    "displayName": "Least Squares Regression",
                    "name": "ls"
                  },
                  {
                    "selected": False,
                    "displayName": "Least Absolute Deviation",
                    "name": "lad"
                  },
                  {
                    "selected": False,
                    "displayName": "Huber",
                    "name": "huber"
                  },
                  {
                    "selected": False,
                    "displayName": "Quantile Regression",
                    "name": "quantile"
                  }
                ],
                "hyperpatameterTuningCandidate": True,
                "uiElemType": "checkbox",
                "description": "It is the loss function to be optimized",
                "display": True,
                "allowedDataType": [
                  "string"
                ]
              },
              {
                "expectedDataType": [
                  "float"
                ],
                "displayName": "Alpha-Quantile",
                "description": "The alpha-quantile of the huber loss function and the quantile loss function",
                "display": False,
                "paramType": "number",
                "acceptedValue": None,
                "valueRange": [
                  0.1,
                  1
                ],
                "hyperpatameterTuningCandidate": False,
                "uiElemType": "slider",
                "dependentOnDict": {
                  "loss": [
                    "huber",
                    "quantile"
                  ]
                },
                "allowedDataType": [
                  "float"
                ],
                "defaultValue": 0.9,
                "name": "alpha"
              },
              {
                "expectedDataType": [
                  "float"
                ],
                "displayName": "Learning Rate",
                "description": "It shrinks the contribution of each tree by learning_rate",
                "display": True,
                "paramType": "number",
                "acceptedValue": None,
                "valueRange": [
                  0.1,
                  1
                ],
                "hyperpatameterTuningCandidate": True,
                "uiElemType": "slider",
                "allowedDataType": [
                  "float"
                ],
                "defaultValue": 0.1,
                "name": "learning_rate"
              },
              {
                "expectedDataType": [
                  "bool"
                ],
                "displayName": "Warm Start",
                "name": "warm_start",
                "paramType": "list",
                "defaultValue": [
                  {
                    "selected": True,
                    "displayName": "False",
                    "name": "False"
                  },
                  {
                    "selected": False,
                    "displayName": "True",
                    "name": "True"
                  }
                ],
                "hyperpatameterTuningCandidate": False,
                "uiElemType": "checkbox",
                "description": "When set to True, reuse the solution of the previous call to fit as initialization",
                "display": True,
                "allowedDataType": [
                  "bool"
                ]
              }
            ],
            "selected": True,
            "algorithmSlug": "f77631ce2ab24cf78c55bb6a5fce4db8gbtr",
            "algorithmName": "Gradient Boosted Tree Regression",
            "hyperParameterSetting": [
              {
                "displayName": "Grid Search",
                "selected": False,
                "params": [
                  {
                    "expectedDataType": [
                      None,
                      "string"
                    ],
                    "displayName": "Metric Used for Optimization",
                    "name": "evaluationMetric",
                    "paramType": "list",
                    "display": True,
                    "uiElemType": "dropDown",
                    "defaultValue": [
                      {
                        "selected": True,
                        "displayName": "R-Squared",
                        "name": "r2"
                      },
                      {
                        "selected": False,
                        "displayName": "MAE",
                        "name": "neg_mean_absolute_error"
                      },
                      {
                        "selected": False,
                        "displayName": "MSE",
                        "name": "neg_mean_squared_error"
                      },
                      {
                        "selected": False,
                        "displayName": "MSE(log)",
                        "name": "neg_mean_squared_log_error"
                      }
                    ]
                  },
                  {
                    "expectedDataType": [
                      None,
                      "int"
                    ],
                    "displayName": "No Of Folds to Use",
                    "name": "kFold",
                    "display": True,
                    "paramType": "number",
                    "acceptedValue": None,
                    "valueRange": [
                      2,
                      10
                    ],
                    "uiElemType": "slider",
                    "defaultValue": 3
                  }
                ],
                "name": "gridsearchcv"
              },
              {
                "displayName": "None",
                "selected": True,
                "params": None,
                "name": "none"
              }
            ]
          },
          {
            "description": "fill in the blanks",
            "parameters": [
              {
                "expectedDataType": [
                  "int"
                ],
                "displayName": "No. Of Estimators",
                "description": "The number of trees in the forest",
                "display": True,
                "paramType": "number",
                "acceptedValue": None,
                "valueRange": [
                  10,
                  1000
                ],
                "hyperpatameterTuningCandidate": True,
                "uiElemType": "slider",
                "allowedDataType": [
                  "int"
                ],
                "defaultValue": 10,
                "name": "n_estimators"
              },
              {
                "expectedDataType": [
                  "int",
                  None
                ],
                "displayName": "Max Depth Of Trees",
                "description": "The maximum depth of the tree",
                "display": True,
                "paramType": "number",
                "acceptedValue": None,
                "valueRange": [
                  2,
                  20
                ],
                "hyperpatameterTuningCandidate": True,
                "uiElemType": "slider",
                "allowedDataType": [
                  "int",
                  None
                ],
                "defaultValue": 3,
                "name": "max_depth"
              },
              {
                "expectedDataType": [
                  "string"
                ],
                "displayName": "Measure For quality of a split",
                "name": "criterion",
                "paramType": "list",
                "defaultValue": [
                  {
                    "selected": True,
                    "displayName": "Friedman Mse",
                    "name": "friedman_mse"
                  },
                  {
                    "selected": False,
                    "displayName": "Mean Squared Error",
                    "name": "mse"
                  },
                  {
                    "selected": False,
                    "displayName": "Mean Absolute Error",
                    "name": "mae"
                  }
                ],
                "hyperpatameterTuningCandidate": True,
                "uiElemType": "checkbox",
                "description": "The function to measure the quality of a split",
                "display": True,
                "allowedDataType": [
                  "string"
                ]
              },
              {
                "expectedDataType": [
                  "int"
                ],
                "displayName": "Minimum Instances For Split",
                "description": "The minimum number of samples required to split an internal node",
                "display": True,
                "paramType": "number",
                "acceptedValue": None,
                "valueRange": [
                  2,
                  10
                ],
                "hyperpatameterTuningCandidate": True,
                "uiElemType": "slider",
                "allowedDataType": [
                  "int",
                  "float"
                ],
                "defaultValue": 2,
                "name": "min_samples_split"
              },
              {
                "expectedDataType": [
                  "int"
                ],
                "displayName": "Minimum Instances For Leaf Node",
                "description": "The minimum number of samples required to be at a leaf node",
                "display": True,
                "paramType": "number",
                "acceptedValue": None,
                "valueRange": [
                  1,
                  100
                ],
                "hyperpatameterTuningCandidate": True,
                "uiElemType": "slider",
                "allowedDataType": [
                  "int",
                  "float"
                ],
                "defaultValue": 1,
                "name": "min_samples_leaf"
              },
              {
                "expectedDataType": [
                  "float"
                ],
                "displayName": "Sub Sampling Rate",
                "description": "It is the subsample ratio of the training instance",
                "display": True,
                "paramType": "number",
                "acceptedValue": None,
                "valueRange": [
                  0.1,
                  1
                ],
                "hyperpatameterTuningCandidate": True,
                "uiElemType": "slider",
                "allowedDataType": [
                  "float"
                ],
                "defaultValue": 1,
                "name": "subsample"
              },
              {
                "expectedDataType": [
                  "float"
                ],
                "displayName": "Maximum Features for Split",
                "description": "The number of features to consider when looking for the best split",
                "display": True,
                "paramType": "number",
                "acceptedValue": None,
                "valueRange": [
                  0.1,
                  1
                ],
                "hyperpatameterTuningCandidate": True,
                "uiElemType": "slider",
                "allowedDataType": [
                  "float",
                  "int",
                  "string",
                  None
                ],
                "defaultValue": None,
                "name": "max_features"
              },
              {
                "expectedDataType": [
                  "int",
                  None
                ],
                "displayName": "Maximum Number of Leaf Nodes",
                "description": "The maximum of number of leaf nodes",
                "display": True,
                "paramType": "number",
                "acceptedValue": None,
                "valueRange": [

                ],
                "hyperpatameterTuningCandidate": False,
                "uiElemType": "textBox",
                "allowedDataType": [
                  "int",
                  None
                ],
                "defaultValue": None,
                "name": "max_leaf_nodes"
              },
              {
                "expectedDataType": [
                  "float"
                ],
                "displayName": "Impurity Decrease cutoff for Split",
                "description": "A node will be split if this split induces a decrease of the impurity greater than or equal to this value",
                "display": True,
                "paramType": "number",
                "acceptedValue": None,
                "valueRange": [
                  0,
                  1
                ],
                "hyperpatameterTuningCandidate": False,
                "uiElemType": "slider",
                "allowedDataType": [
                  "float"
                ],
                "defaultValue": 0,
                "name": "min_impurity_decrease"
              },
              {
                "expectedDataType": [
                  "int",
                  None
                ],
                "displayName": "Random Seed",
                "description": "The seed of the pseudo random number generator to use when shuffling the data",
                "display": True,
                "paramType": "number",
                "acceptedValue": None,
                "valueRange": [
                  1,
                  100
                ],
                "hyperpatameterTuningCandidate": False,
                "uiElemType": "textBox",
                "allowedDataType": [
                  "int",
                  None
                ],
                "defaultValue": None,
                "name": "random_state"
              },
              {
                "expectedDataType": [
                  "string"
                ],
                "displayName": "Node Split Strategy",
                "name": "splitter",
                "paramType": "list",
                "defaultValue": [
                  {
                    "selected": False,
                    "displayName": "Best split",
                    "name": "best"
                  },
                  {
                    "selected": True,
                    "displayName": "Best random split",
                    "name": "random"
                  }
                ],
                "hyperpatameterTuningCandidate": True,
                "uiElemType": "checkbox",
                "description": "The strategy used to choose the split at each node",
                "display": True,
                "allowedDataType": [
                  "string"
                ]
              }
            ],
            "selected": True,
            "algorithmSlug": "f77631ce2ab24cf78c55bb6a5fce4db8dtreer",
            "algorithmName": "Decision Tree Regression",
            "hyperParameterSetting": [
              {
                "displayName": "Grid Search",
                "selected": False,
                "params": [
                  {
                    "expectedDataType": [
                      None,
                      "string"
                    ],
                    "displayName": "Metric Used for Optimization",
                    "name": "evaluationMetric",
                    "paramType": "list",
                    "display": True,
                    "uiElemType": "dropDown",
                    "defaultValue": [
                      {
                        "selected": True,
                        "displayName": "R-Squared",
                        "name": "r2"
                      },
                      {
                        "selected": False,
                        "displayName": "MAE",
                        "name": "neg_mean_absolute_error"
                      },
                      {
                        "selected": False,
                        "displayName": "MSE",
                        "name": "neg_mean_squared_error"
                      },
                      {
                        "selected": False,
                        "displayName": "MSE(log)",
                        "name": "neg_mean_squared_log_error"
                      }
                    ]
                  },
                  {
                    "expectedDataType": [
                      None,
                      "int"
                    ],
                    "displayName": "No Of Folds to Use",
                    "name": "kFold",
                    "display": True,
                    "paramType": "number",
                    "acceptedValue": None,
                    "valueRange": [
                      2,
                      10
                    ],
                    "uiElemType": "slider",
                    "defaultValue": 3
                  }
                ],
                "name": "gridsearchcv"
              },
              {
                "displayName": "None",
                "selected": True,
                "params": None,
                "name": "none"
              }
            ]
          },
          {
            "description": "fill in the blanks",
            "parameters": [
              {
                "expectedDataType": [
                  "int"
                ],
                "displayName": "No. Of Estimators",
                "description": "The number of trees in the forest",
                "display": True,
                "paramType": "number",
                "acceptedValue": None,
                "valueRange": [
                  10,
                  1000
                ],
                "hyperpatameterTuningCandidate": True,
                "uiElemType": "slider",
                "allowedDataType": [
                  "int"
                ],
                "defaultValue": 10,
                "name": "n_estimators"
              },
              {
                "expectedDataType": [
                  "int",
                  None
                ],
                "displayName": "Max Depth Of Trees",
                "description": "The maximum depth of the tree",
                "display": True,
                "paramType": "number",
                "acceptedValue": None,
                "valueRange": [
                  2,
                  20
                ],
                "hyperpatameterTuningCandidate": True,
                "uiElemType": "slider",
                "allowedDataType": [
                  "int",
                  None
                ],
                "defaultValue": 3,
                "name": "max_depth"
              },
              {
                "expectedDataType": [
                  "string"
                ],
                "displayName": "Measure For quality of a split",
                "name": "criterion",
                "paramType": "list",
                "defaultValue": [
                  {
                    "selected": True,
                    "displayName": "Friedman Mse",
                    "name": "friedman_mse"
                  },
                  {
                    "selected": False,
                    "displayName": "Mean Squared Error",
                    "name": "mse"
                  },
                  {
                    "selected": False,
                    "displayName": "Mean Absolute Error",
                    "name": "mae"
                  }
                ],
                "hyperpatameterTuningCandidate": True,
                "uiElemType": "checkbox",
                "description": "The function to measure the quality of a split",
                "display": True,
                "allowedDataType": [
                  "string"
                ]
              },
              {
                "expectedDataType": [
                  "int"
                ],
                "displayName": "Minimum Instances For Split",
                "description": "The minimum number of samples required to split an internal node",
                "display": True,
                "paramType": "number",
                "acceptedValue": None,
                "valueRange": [
                  2,
                  10
                ],
                "hyperpatameterTuningCandidate": True,
                "uiElemType": "slider",
                "allowedDataType": [
                  "int",
                  "float"
                ],
                "defaultValue": 2,
                "name": "min_samples_split"
              },
              {
                "expectedDataType": [
                  "int"
                ],
                "displayName": "Minimum Instances For Leaf Node",
                "description": "The minimum number of samples required to be at a leaf node",
                "display": True,
                "paramType": "number",
                "acceptedValue": None,
                "valueRange": [
                  1,
                  100
                ],
                "hyperpatameterTuningCandidate": True,
                "uiElemType": "slider",
                "allowedDataType": [
                  "int",
                  "float"
                ],
                "defaultValue": 1,
                "name": "min_samples_leaf"
              },
              {
                "expectedDataType": [
                  "float"
                ],
                "displayName": "Sub Sampling Rate",
                "description": "It is the subsample ratio of the training instance",
                "display": True,
                "paramType": "number",
                "acceptedValue": None,
                "valueRange": [
                  0.1,
                  1
                ],
                "hyperpatameterTuningCandidate": True,
                "uiElemType": "slider",
                "allowedDataType": [
                  "float"
                ],
                "defaultValue": 1,
                "name": "subsample"
              },
              {
                "expectedDataType": [
                  "float"
                ],
                "displayName": "Maximum Features for Split",
                "description": "The number of features to consider when looking for the best split",
                "display": True,
                "paramType": "number",
                "acceptedValue": None,
                "valueRange": [
                  0.1,
                  1
                ],
                "hyperpatameterTuningCandidate": True,
                "uiElemType": "slider",
                "allowedDataType": [
                  "float",
                  "int",
                  "string",
                  None
                ],
                "defaultValue": None,
                "name": "max_features"
              },
              {
                "expectedDataType": [
                  "int",
                  None
                ],
                "displayName": "Maximum Number of Leaf Nodes",
                "description": "The maximum of number of leaf nodes",
                "display": True,
                "paramType": "number",
                "acceptedValue": None,
                "valueRange": [

                ],
                "hyperpatameterTuningCandidate": False,
                "uiElemType": "textBox",
                "allowedDataType": [
                  "int",
                  None
                ],
                "defaultValue": None,
                "name": "max_leaf_nodes"
              },
              {
                "expectedDataType": [
                  "float"
                ],
                "displayName": "Impurity Decrease cutoff for Split",
                "description": "A node will be split if this split induces a decrease of the impurity greater than or equal to this value",
                "display": True,
                "paramType": "number",
                "acceptedValue": None,
                "valueRange": [
                  0,
                  1
                ],
                "hyperpatameterTuningCandidate": False,
                "uiElemType": "slider",
                "allowedDataType": [
                  "float"
                ],
                "defaultValue": 0,
                "name": "min_impurity_decrease"
              },
              {
                "expectedDataType": [
                  "int",
                  None
                ],
                "displayName": "Random Seed",
                "description": "The seed of the pseudo random number generator to use when shuffling the data",
                "display": True,
                "paramType": "number",
                "acceptedValue": None,
                "valueRange": [
                  1,
                  100
                ],
                "hyperpatameterTuningCandidate": False,
                "uiElemType": "textBox",
                "allowedDataType": [
                  "int",
                  None
                ],
                "defaultValue": None,
                "name": "random_state"
              },
              {
                "expectedDataType": [
                  "bool"
                ],
                "displayName": "Bootstrap Sampling",
                "name": "bootstrap",
                "paramType": "list",
                "defaultValue": [
                  {
                    "selected": False,
                    "displayName": "False",
                    "name": "False"
                  },
                  {
                    "selected": True,
                    "displayName": "True",
                    "name": "True"
                  }
                ],
                "hyperpatameterTuningCandidate": True,
                "uiElemType": "checkbox",
                "description": "It defines whether bootstrap samples are used when building trees",
                "display": True,
                "allowedDataType": [
                  "bool"
                ]
              },
              {
                "expectedDataType": [
                  "bool"
                ],
                "displayName": "use out-of-bag samples",
                "name": "oob_score",
                "paramType": "list",
                "defaultValue": [
                  {
                    "selected": False,
                    "displayName": "False",
                    "name": "False"
                  },
                  {
                    "selected": True,
                    "displayName": "True",
                    "name": "True"
                  }
                ],
                "hyperpatameterTuningCandidate": False,
                "uiElemType": "checkbox",
                "description": "It defines whether to use out-of-bag samples to estimate the R^2 on unseen data",
                "display": False,
                "allowedDataType": [
                  "bool"
                ]
              },
              {
                "expectedDataType": [
                  "int"
                ],
                "displayName": "No Of Jobs",
                "description": "The number of jobs to run in parallel for both fit and predict",
                "display": True,
                "paramType": "number",
                "acceptedValue": None,
                "valueRange": [
                  -1,
                  4
                ],
                "hyperpatameterTuningCandidate": False,
                "uiElemType": "slider",
                "allowedDataType": [
                  "int"
                ],
                "defaultValue": 1,
                "name": "n_jobs"
              },
              {
                "expectedDataType": [
                  "bool"
                ],
                "displayName": "Warm Start",
                "name": "warm_start",
                "paramType": "list",
                "defaultValue": [
                  {
                    "selected": True,
                    "displayName": "False",
                    "name": "False"
                  },
                  {
                    "selected": False,
                    "displayName": "True",
                    "name": "True"
                  }
                ],
                "hyperpatameterTuningCandidate": False,
                "uiElemType": "checkbox",
                "description": "When set to True, reuse the solution of the previous call to fit as initialization",
                "display": True,
                "allowedDataType": [
                  "bool"
                ]
              }
            ],
            "selected": True,
            "algorithmSlug": "f77631ce2ab24cf78c55bb6a5fce4db8rfr",
            "algorithmName": "Random Forest Regression",
            "hyperParameterSetting": [
              {
                "displayName": "Grid Search",
                "selected": False,
                "params": [
                  {
                    "expectedDataType": [
                      None,
                      "string"
                    ],
                    "displayName": "Metric Used for Optimization",
                    "name": "evaluationMetric",
                    "paramType": "list",
                    "display": True,
                    "uiElemType": "dropDown",
                    "defaultValue": [
                      {
                        "selected": True,
                        "displayName": "R-Squared",
                        "name": "r2"
                      },
                      {
                        "selected": False,
                        "displayName": "MAE",
                        "name": "neg_mean_absolute_error"
                      },
                      {
                        "selected": False,
                        "displayName": "MSE",
                        "name": "neg_mean_squared_error"
                      },
                      {
                        "selected": False,
                        "displayName": "MSE(log)",
                        "name": "neg_mean_squared_log_error"
                      }
                    ]
                  },
                  {
                    "expectedDataType": [
                      None,
                      "int"
                    ],
                    "displayName": "No Of Folds to Use",
                    "name": "kFold",
                    "display": True,
                    "paramType": "number",
                    "acceptedValue": None,
                    "valueRange": [
                      2,
                      10
                    ],
                    "uiElemType": "slider",
                    "defaultValue": 3
                  }
                ],
                "name": "gridsearchcv"
              },
              {
                "displayName": "None",
                "selected": True,
                "params": None,
                "name": "none"
              }
            ]
          }
        ],
        "DATA_SOURCE": {
          "datasource_type": "fileUpload",
          "datasource_details": ""
        },
        "FILE_SETTINGS": {
          "app_type": "regression",
          "validationTechnique": [
            {
              "displayName": "K Fold Validation",
              "name": "kFold",
              "value": 2
            }
          ],
          "targetLevel": None,
          "modelpath": [
            "nmm-qjvzzooq5k"
          ],
          "analysis_type": [
            "training"
          ],
          "inputfile": [
            "file:///home/gulshan/marlabs/datasets/sampleDatasets/demography.csv"
          ],
          "metadata": {
            "url": "madvisor2.marlabsai.com:80/api/get_metadata_for_mlscripts/",
            "slug_list": [
              "demographycsv-ffxzl7yc2u"
            ]
          }
        }
      },
      "job_config": {
        "message_url": "http://madvisor2.marlabsai.com:80/api/messages/Job_model-nmm-qjvzzooq5k-3pc9nk4a8u_123/",
        "get_config": {
          "action": "get_config",
          "method": "GET"
        },
        "error_reporting_url": "http://madvisor2.marlabsai.com:80/api/set_job_report/model-nmm-qjvzzooq5k-3pc9nk4a8u/",
        "set_result": {
          "action": "result",
          "method": "PUT"
        },
        "job_url": "http://madvisor2.marlabsai.com:80/api/job/model-nmm-qjvzzooq5k-3pc9nk4a8u/",
        "job_type": "training",
        "job_name": "nmm",
        "xml_url": "http://madvisor2.marlabsai.com:80/api/xml/model-nmm-qjvzzooq5k-3pc9nk4a8u/",
        "app_id": 13
      }
    }
    return trainConfigClassification
