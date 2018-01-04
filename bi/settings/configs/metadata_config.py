def get_metadata_config():
    metaDataConfig = {
        "job_config":{
         "message_url":"http://34.196.204.54:9012/api/messages/Job_metadata-adult_newcsv-j0ak4a53pp-4d5byu0tqd_123/",
         "get_config":{
            "action":"get_config",
            "method":"GET"
         },
         "error_reporting_url":"http://34.196.204.54:9012/api/set_job_report/metadata-adult_newcsv-j0ak4a53pp-4d5byu0tqd/",
         "set_result":{
            "action":"result",
            "method":"PUT"
         },
         "job_url":"http://34.196.204.54:9012/api/job/metadata-adult_newcsv-j0ak4a53pp-4d5byu0tqd/",
         "job_type":"metaData",
         "job_name":"adult_new.csv",
         "xml_url":"http://34.196.204.54:9012/api/xml/metadata-adult_newcsv-j0ak4a53pp-4d5byu0tqd/"
      },
      "config":{
         "COLUMN_SETTINGS":{
            "analysis_type":[
               "metaData"
            ]
         },
         "DATE_SETTINGS":{

         },
         "DATA_SOURCE":{
            "datasource_type":"fileUpload",
            "datasource_details":""
         },
         "FILE_SETTINGS":{
            "inputfile":[
               "/home/marlabs/Documents/mAdvisor/Datasets/adult_new.csv"
            ]
         }
      }
    }
    return metaDataConfig
