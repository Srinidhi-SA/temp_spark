def get_metadata_config():
    metaDataConfig = {
        "job_config": {
          "message_url": "http://34.196.204.54:9012/api/messages/Job_metadata-auditcsv-87bqhohk96-rjvr5kwk4i_123/",
          "get_config": {
            "action": "get_config",
            "method": "GET"
          },
          "error_reporting_url": "http://34.196.204.54:9012/api/set_job_report/metadata-auditcsv-87bqhohk96-rjvr5kwk4i/",
          "set_result": {
            "action": "result",
            "method": "PUT"
          },
          "job_url": "http://34.196.204.54:9012/api/job/metadata-auditcsv-87bqhohk96-rjvr5kwk4i/",
          "job_type": "metaData",
          "job_name": "audit.csv",
          "xml_url": "http://34.196.204.54:9012/api/xml/metadata-auditcsv-87bqhohk96-rjvr5kwk4i/"
        },
        "config": {
          "COLUMN_SETTINGS": {
            "analysis_type": [
              "metaData"
            ]
          },
          "DATE_SETTINGS": {

          },
          "DATA_SOURCE": {
            "datasource_type": "fileUpload",
            "datasource_details": ""
          },
          "FILE_SETTINGS": {
            "inputfile": [
              "/home/marlabs/Documents/mAdvisor/Datasets/audit.csv"
            ]
          }
        }
    }
    return metaDataConfig
