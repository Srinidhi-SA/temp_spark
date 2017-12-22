def get_prediction_config():
    predictionConfig = {

            "job_config": {
              "job_url": "http://34.196.204.54:9012/api/job/score-kkkk_score_rf-31fm2m25bj-3ajz9wkx4l/",
              "job_type": "prediction",
              "set_result": {
                "action": "result",
                "method": "PUT"
              },
              "get_config": {
                "action": "get_config",
                "method": "GET"
              },
              "message_url": "http://34.196.204.54:9012/api/messages/Score_kkkk_score_rf-31fm2m25bj_123/",
              "job_name": "kkkk_score_rf",
              "xml_url": "http://34.196.204.54:9012/api/xml/model-somerandommkdela-ys05d31fzi-8w81aqsa2q_pmml/"
            },
            "config": {
              "COLUMN_SETTINGS": {
                "uidColumn" : {"colName":"workclass","colSlug":""},
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
                    "adult_testcsv-yzl7qkfbj4"
                  ]
                },
                "scorepath": [
                  "kkkk_score_rf-31fm2m25bj"
                ],
                "modelpath": [
                  "kkkk-9sldrt5c8z"
                ],
                "analysis_type": [
                  "score"
                ],
                "modelfeatures": ['age','workclass','fnlwgt','education','education-num','marital-status','occupation','relationship','race','sex','Capital-gain','Capital-loss','hours-per-week','native-country'
                ],
                # 'modelfeatures':[u'workclass', u'relationship', u'age', u'Capital-gain', u'sex', u'hours-per-week', u'race', u'native-country', u'education-num', u'Capital-loss', u'education', u'fnlwgt', u'marital-status', u'occupation'],
                "algorithmslug": [
                  "f77631ce2ab24cf78c55bb6a5fce4db8rf"
                ],
                "levelcounts": [
                    {' >50K': 7841, ' <=50K': 24720}
                ],
                "inputfile": [
                  "file:///home/gulshan/marlabs/datasets/adult_test.csv"
                ]
              }
            }
    }
    return predictionConfig
