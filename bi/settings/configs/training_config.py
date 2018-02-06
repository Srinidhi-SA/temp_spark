def get_training_config():
    trainingConfig = {
      "config": {
        "COLUMN_SETTINGS": {
          "variableSelection": [
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "measure",
              "name": "age",
              "selected": True,
              "slug": "556652df46d14a68ac6b2fafa8363afb",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "workclass",
              "selected": True,
              "slug": "db3f94d81b37429c9a2783306e5da9f2",
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
              "slug": "c10dc58069ea441d94e48e36d04d0bf2",
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
              "slug": "edab205bf35e4d929022201ec6f30e31",
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
              "slug": "0e95bba63c274898889e43e642d8d503",
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
              "slug": "9c4a6d087f424689bbc8bcf3bd98974d",
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
              "slug": "8639e3277cad4d1a95ffd8c75e32e2ca",
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
              "slug": "473b745f23fa44c894d4a59abe4bed4c",
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
              "slug": "50636b13c97d47acb279604f14739950",
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
              "slug": "a066f47a3d8c4997b0790120feecda5a",
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
              "slug": "b3784bf061ff4e088c90a5f7decb38a4",
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
              "slug": "fa1ac039d3bc48d5b9b87d507db8ac8b",
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
              "slug": "bbedc95901a34b71bbc2158278d6514e",
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
              "slug": "2da496d30203414fb00201c5a644c56e",
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
              "slug": "a7724c2c0fa647e7b3a31c0d289fc5b0",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": True,
              "uidCol": False
            }
          ]
        },
        "DATA_SOURCE": {
          "datasource_type": "fileUpload",
          "datasource_details": ""
        },
        "FILE_SETTINGS": {
          "analysis_type": [
            "training"
          ],
          "modelpath": [
            "model-1-8utf3z5bo3"
          ],
          "train_test_split": [
            0.7
          ],
          "metadata": {
            "url": "34.196.204.54:9012/api/get_metadata_for_mlscripts/",
            "slug_list": [
              "demographycsv-0t82v0amim"
            ]
          },
          "inputfile": [
            "file:///home/gulshan/marlabs/datasets/sampleDatasets/demography.csv"
          ]
        }
      },
      "job_config": {
        "message_url": "http://34.196.204.54:9012/api/messages/Job_model-model-1-8utf3z5bo3-lw97yj8yb9_123/",
        "get_config": {
          "action": "get_config",
          "method": "GET"
        },
        "error_reporting_url": "http://34.196.204.54:9012/api/set_job_report/model-model-1-8utf3z5bo3-lw97yj8yb9/",
        "set_result": {
          "action": "result",
          "method": "PUT"
        },
        "job_url": "http://34.196.204.54:9012/api/job/model-model-1-8utf3z5bo3-lw97yj8yb9/",
        "job_type": "training",
        "job_name": "model-1",
        "xml_url": "http://34.196.204.54:9012/api/xml/model-model-1-8utf3z5bo3-lw97yj8yb9/",
        "app_id": 2
      }
    }



    return trainingConfig
