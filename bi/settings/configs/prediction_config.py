def get_prediction_config():
    predictionConfig = {
        "config":{
            'FILE_SETTINGS': {
                'inputfile': ['file:///home/gulshan/marlabs/datasets/adult_test.csv'],
                'modelpath': ["ANKUSH"],
                'scorepath': ["DDDDD"],
                # 'train_test_split' : [0.8],
                'levelcounts' : [],
                'modelfeatures' : [],
                "algorithmslug":["f77631ce2ab24cf78c55bb6a5fce4db8rf"],
            },
            'COLUMN_SETTINGS': {
                'analysis_type': ['Dimension'],
                'result_column': ['class_label'],
                # 'consider_columns_type': ['excluding'],
                # 'consider_columns':[],
                # 'date_columns':['Date'],
                'score_consider_columns_type': ['excluding'],
                'score_consider_columns':[],
                "app_id":[2]

            },
            "DATA_SOURCE" : {
                "datasource_details" : "",
                "datasource_type" : "fileUpload"
            },
        },
        "job_config":{
            "get_config" : {
                "action" : "get_config",
                "method" : "GET"
            },
            "job_name" : "Sample1",
            "job_type":"prediction",
            "job_url": "http://34.196.204.54:9012/api/job/score-hiohoyuo-bn1ofiupv0-j0irk37cob/set_result/",
            "message_url" : "http://34.196.204.54:9012/api/messages/Dataset_trend_gulshancsv-h85lh79ybd_123/",
            "set_result": {
                "method": "PUT",
                "action": "result"
              },
        }
    }
    return predictionConfig
