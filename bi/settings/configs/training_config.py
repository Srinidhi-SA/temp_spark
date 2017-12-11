def get_training_config():
    # trainingConfig = {
    #     "config":{
    #         'FILE_SETTINGS': {
    #             'inputfile': ['file:///home/gulshan/marlabs/datasets/adult.csv'],
    #             # Model Slug will go instead of model path
    #             'modelpath': ["ANKUSH"],
    #             'train_test_split' : [0.8],
    #             'analysis_type' : ['training']
    #         },
    #         'COLUMN_SETTINGS': {
    #             'analysis_type': ['training'],
    #             'result_column': ['class_label'],
    #             'consider_columns_type': ['excluding'],
    #             'consider_columns':[],
    #             'polarity': ['positive'],
    #             'date_format': None,
    #             # 'date_columns':["new_date","Month","Order Date"],
    #             'date_columns':[],
    #             'ignore_column_suggestions': [],
    #             # 'ignore_column_suggestions': ["Outlet ID","Visibility to Cosumer","Cleanliness","Days to Resolve","Heineken Lager Share %","Issue Category","Outlet","Accessible_to_consumer","Resultion Status"],
    #             'dateTimeSuggestions' : [],
    #             'utf8ColumnSuggestion':[],
    #             'consider_columns':[],
    #         },
    #         "DATA_SOURCE" : {
    #             "datasource_details" : "",
    #             "datasource_type" : "fileUpload"
    #         }
    #     },
    #     "job_config":{
    #         "get_config" : {
    #             "action" : "get_config",
    #             "method" : "GET"
    #         },
    #         "job_name" : "Sample1.csv",
    #         "job_type":"training",
    #         "message_url" : "http://34.196.204.54:9012/api/messages/Dataset_trend_gulshancsv-h85lh79ybd_123/",
    #         # "job_url": "http://localhost:8000/api/job/dataset-iriscsv-qpmercq3r8-2fjupdcwdu/",
    #         "job_url": "http://localhost:8000/api/job/dataset-iriscsv-qpmercq3r8-2fjupdcwdu/",
    #         "set_result": {
    #             "method": "PUT",
    #             "action": "result"
    #           },
    #     }
    # }
    trainingConfig = {
        "config" : {
            "COLUMN_SETTINGS" : {
                "consider_columns" : [
                    "Channel",
                    "MTO_MTS",
                    "City",
                    "State",
                    "Source_Facility",
                    "Payment_Method",
                    "Customer_Type",
                    "order_month",
                    "order_day",
                    "Order_Item_Status_String",
                    "BEDS",
                    "OUTDOOR",
                    "MATTRESS",
                    "DINING - OTHERS",
                    "LIVING SEATING",
                    "DECOR",
                    "DINING",
                    "LIVING ESSENTIALS",
                    "STUDY",
                    "WARDROBES",
                    "BEDROOM - OTHERS",
                    "KIDS",
                    "Sales Amount"
                ],
                "consider_columns_type" : [
                    "including"
                ],
                "dateTimeSuggestions" : [
                    {}
                ],
                "date_columns" : [],
                "date_format" : None,
                "ignore_column_suggestion" : [
                ],
                "polarity" : [
                    "positive"
                ],
                "result_column" : [
                    "Order_Item_Status_String"
                ],
                "utf8_column_suggestions" : []
            },
            "DATA_SOURCE" : {
                "datasource_details" : "",
                "datasource_type" : "fileUpload"
            },
            "FILE_SETTINGS" : {
                "analysis_type" : [
                    "training"
                ],
                "inputfile" : [
                    "file:///home/gulshan/marlabs/datasets/ul_5050.csv"
                ],
                "modelpath" : [
                    "ggop-4b7ztc3rmn"
                ],
                "train_test_split" : [
                    0.71
                ]
            }
        },
        "job_config" : {
            "get_config" : {
                "action" : "get_config",
                "method" : "GET"
            },
            "job_name" : "ggop",
            "job_type" : "training",
            "job_url" : "http://34.196.204.54:9012/api/job/model-ggop-4b7ztc3rmn-9tesfpqui8/",
            "message_url" : "http://34.196.204.54:9012/api/messages/Trainer_ggop-4b7ztc3rmn_123/",
            "set_result" : {
                "action" : "result",
                "method" : "PUT"
            }
        }
    }
    return trainingConfig
