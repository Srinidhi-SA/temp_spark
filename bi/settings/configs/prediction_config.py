def get_prediction_config():
    predictionConfig = {
    "job_config": {
      "job_url": "http://34.196.204.54:9012/api/job/score-score-test0-ztgff5jqg0-b0av34gd59/",
      "job_type": "prediction",
      "xml_url": "http://34.196.204.54:9012/api/xml/score-score-test0-ztgff5jqg0-b0av34gd59/",
      "get_config": {
        "action": "get_config",
        "method": "GET"
      },
      "set_result": {
        "action": "result",
        "method": "PUT"
      },
      "message_url": "http://34.196.204.54:9012/api/messages/Score_score-test0-ztgff5jqg0_123/",
      "job_name": "score-test0"
    },
    "config": {
      "COLUMN_SETTINGS": {
        "polarity": [
          "positive"
        ],
        "date_format": None,
        "score_consider_columns_type": [
          "including"
        ],
        "consider_columns_type": [
          "including"
        ],
        "result_column": [
          "class_label"
        ],
        "ignore_column_suggestion": [

        ],
        "app_id": [
          2
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
        "utf8_column_suggestions": [

        ],
        "date_columns": [

        ],
        "dateTimeSuggestions": [
          {

          }
        ],
        "score_consider_columns": [
          "workclass",
          "education",
          "marital-status",
          "occupation",
          "relationship",
          "race",
          "sex",
          "native-country",
          "age",
          "fnlwgt",
          "education-num",
          "Capital-gain",
          "Capital-loss",
          "hours-per-week"
        ]
      },
      "DATA_SOURCE": {
        "datasource_type": "fileUpload",
        "datasource_details": ""
      },
      "FILE_SETTINGS": {
        "metadata": {
          "url": "34.196.204.54:9012/api/get_metadata_for_mlscripts/",
          "slug_list": [
            "adult_testcsv-5a8nb8qti8"
          ]
        },
        "labelMappingDict": [
            {"0": u' <=50K', "1": u' >50K'}
        ],
        "scorepath": [
          "score-test0-ztgff5jqg0"
        ],
        "modelpath": [
          "adult-test0-3wspq2nm3e"
        ],
        "analysis_type": [
          "score"
        ],
        "modelfeatures": [
        'workclass',
        'relationship',
        'age',
        'Capital-gain',
        'sex',
        'hours-per-week',
        'race',
        'native-country',
        'education-num',
        'Capital-loss',
        'education',
        'fnlwgt',
        'marital-status',
        'occupation'
      ],
        "algorithmslug": [
          "f77631ce2ab24cf78c55bb6a5fce4db8rf"
        ],
        "levelcounts": [
          {
            " >50K": 7841,
            " <=50K": 24720
          }
        ],
        "inputfile": [
          "file:///home/gulshan/marlabs/datasets/adult_test.csv"
        ]
      }
    }
  }
    return predictionConfig
