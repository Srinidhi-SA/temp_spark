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
        "file:///home/gulshan/marlabs/datasets/RetailSalesData.csv"
      ]
    }
  },
  "job_config": {
    "message_url": "http://34.196.204.54:9012/api/messages/Job_metadata-retailsalesdatacsv-qxn2cavi2u-twxp7sm89h_123/",
    "get_config": {
      "action": "get_config",
      "method": "GET"
    },
    "error_reporting_url": "http://34.196.204.54:9012/api/set_job_report/metadata-retailsalesdatacsv-qxn2cavi2u-twxp7sm89h/",
    "set_result": {
      "action": "result",
      "method": "PUT"
    },
    "job_url": "http://34.196.204.54:9012/api/job/metadata-retailsalesdatacsv-qxn2cavi2u-twxp7sm89h/",
    "job_type": "metaData",
    "job_name": "RetailSalesData.csv",
    "xml_url": "http://34.196.204.54:9012/api/xml/metadata-retailsalesdatacsv-qxn2cavi2u-twxp7sm89h/"
  }
}
    return metaDataConfig
