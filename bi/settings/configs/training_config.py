def get_training_config():
    trainingConfig = {
    "job_config": {
      "job_url": "http://34.196.204.54:9012/api/job/model-adult-test0-3wspq2nm3e-rjc9lg9jcd/",
      "job_type": "training",
      "xml_url": "http://34.196.204.54:9012/api/xml/model-adult-test0-3wspq2nm3e-rjc9lg9jcd/",
      "get_config": {
        "action": "get_config",
        "method": "GET"
      },
      "set_result": {
        "action": "result",
        "method": "PUT"
      },
      "message_url": "http://34.196.204.54:9012/api/messages/Trainer_adult-test0-3wspq2nm3e_123/",
      "job_name": "adult-test0"
    },
    "config": {
      "COLUMN_SETTINGS": {
        "polarity": [
          "positive"
        ],
        "date_format": None,
        "utf8_column_suggestions": [

        ],
        "date_columns": [

        ],
        "consider_columns_type": [
          "including"
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
        "result_column": [
          "class_label"
        ],
        "ignore_column_suggestion": [

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
      "FILE_SETTINGS": {
        "analysis_type": [
          "training"
        ],
        "modelpath": [
          "adult-test0-3wspq2nm3e"
        ],
        "train_test_split": [
          0.71
        ],
        "metadata": {
          "url": "34.196.204.54:9012/api/get_metadata_for_mlscripts/",
          "slug_list": [
            "adultcsv-cjzdoqhdcg"
          ]
        },
        "inputfile": [
          "file:///home/gulshan/marlabs/datasets/sampleDatasets/demography.csv"
        ]
      }
    }
  }



    return trainingConfig
