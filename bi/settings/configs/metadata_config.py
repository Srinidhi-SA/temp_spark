def get_metadata_config():
    metaDataConfig = {
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
                    "file:///home/gulshan/marlabs/datasets/sigma/ignoreTest.csv"
                ]
            }
        },
        "job_config" : {
            "get_config" : {
                "action" : "get_config",
                "method" : "GET"
            },
            "job_name" : "Sample1.csv",
            "job_type" : "metaData",
            "message_url" : "http://34.196.204.54:9012/api/messages/Dataset_trend_gulshancsv-h85lh79ybd_123/",
            "job_url" : "http://34.196.204.54:9012/api/job/metadata-sample1csv-e2za8z9u26-o1f6wicswc/",
            "set_result" : {
                "action" : "result",
                "method" : "PUT"
            }
        }
    }
    return metaDataConfig
