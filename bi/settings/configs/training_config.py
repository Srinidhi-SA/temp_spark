def get_training_config():
    trainingConfig = {
        "job_config": {
          "job_url": "http://34.196.204.54:9012/api/job/model-kkkk-9sldrt5c8z-9gb7xd99xn/",
          "job_type": "training",
          "set_result": {
            "action": "result",
            "method": "PUT"
          },
          "get_config": {
            "action": "get_config",
            "method": "GET"
          },
          "message_url": "http://34.196.204.54:9012/api/messages/Trainer_kkkk-9sldrt5c8z_123/",
          "job_name": "kkkk",
          "xml_url": "http://34.196.204.54:9012/api/xml/model-kkkk-9sldrt5c8z-9gb7xd99xn_pmml/"

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
              "kkkk-9sldrt5c8z"
            ],
            "train_test_split": [
              0.73
            ],
            "metadata": {
              "url": "34.196.204.54:9012/api/get_metadata_for_mlscripts/",
              "slug_list": [
                "adultcsv-jwl8oc17hw"
              ]
            },
            "inputfile": [
              "file:///home/gulshan/marlabs/datasets/adult.csv"
            ]
          }
        }
    }

    return trainingConfig
