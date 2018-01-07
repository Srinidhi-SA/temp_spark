def get_metadata_config():
    metaDataConfig = {
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
        "file:///home/gulshan/marlabs/datasets/sampleDatasets/audit.csv"
      ]
    }
  },
  "job_config": {
    "message_url": "http://34.196.204.54:9012/api/messages/Job_metadata-auditcsv-k0ird5loop-f9eug0wvqo_123/",
    "get_config": {
      "action": "get_config",
      "method": "GET"
    },
    "error_reporting_url": "http://34.196.204.54:9012/api/set_job_report/metadata-auditcsv-k0ird5loop-f9eug0wvqo/",
    "set_result": {
      "action": "result",
      "method": "PUT"
    },
    "job_url": "http://34.196.204.54:9012/api/job/metadata-auditcsv-k0ird5loop-f9eug0wvqo/",
    "job_type": "metaData",
    "job_name": "audit.csv",
    "xml_url": "http://34.196.204.54:9012/api/xml/metadata-auditcsv-k0ird5loop-f9eug0wvqo/"
  }
}
    return metaDataConfig
