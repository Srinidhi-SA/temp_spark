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
              "slug": "45acf251d8fb4a64a574213211fff4fe",
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
              "slug": "cc1e8369051a4b41b8450fa0c31bbfa8",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": True
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "measure",
              "name": "fnlwgt",
              "selected": True,
              "slug": "612c305f7ed44751bddd2b03aed0de76",
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
              "slug": "f47d64a311fc458db253871a8bd0b0be",
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
              "slug": "00869a1a210644738cbf3b64b37541ba",
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
              "slug": "b0293b6b22614f7389d51ea261b88917",
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
              "slug": "814936b0fd8b47fcafeb13fd17d933a1",
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
              "slug": "e8484b368b674748ad69f23aac7fa1ba",
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
              "slug": "9a028a747e46455f9d637a2124c1fd01",
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
              "slug": "e5cadb3e61534d7d80d7c2ff80ee2096",
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
              "slug": "c553feb40fb542dc86d68e91854c1c34",
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
              "slug": "cfa46535fb844c4a97242128b29bcc1c",
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
              "slug": "e20604526aec42b080ee56971a9961e3",
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
              "slug": "71daec723ab4416ebd8ade9918a73dd3",
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
              "slug": "c57340ebbb594658915782c01b66a804",
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
            "dkk-5ohvqqbssx"
          ],
          "train_test_split": [
            0.66
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
        "message_url": "http://34.196.204.54:9012/api/messages/Job_model-dkk-5ohvqqbssx-mvj5k0nz59_123/",
        "get_config": {
          "action": "get_config",
          "method": "GET"
        },
        "error_reporting_url": "http://34.196.204.54:9012/api/set_job_report/model-dkk-5ohvqqbssx-mvj5k0nz59/",
        "set_result": {
          "action": "result",
          "method": "PUT"
        },
        "job_url": "http://34.196.204.54:9012/api/job/model-dkk-5ohvqqbssx-mvj5k0nz59/",
        "job_type": "training",
        "job_name": "dkk",
        "xml_url": "http://34.196.204.54:9012/api/xml/model-dkk-5ohvqqbssx-mvj5k0nz59/",
        "app_id": 2
      }
    }



    return trainingConfig
