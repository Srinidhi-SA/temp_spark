def get_metadata_config():
    # metaDataConfig = {
    #   "config": {
    #     "COLUMN_SETTINGS": {
    #       "analysis_type": [
    #         "metaData"
    #       ]
    #     },
    #     "DATE_SETTINGS": {
    #
    #     },
    #     "DATA_SOURCE": {
    #       "datasource_type": "fileUpload",
    #       "datasource_details": ""
    #     },
    #     "FILE_SETTINGS": {
    #       "inputfile": [
    #         "file:///home/gulshan/marlabs/datasets/sampleDatasets/ecommerce.csv"
    #       ]
    #     }
    #   },
    #   "job_config": {
    #     "message_url": "http://34.196.204.54:9012/api/messages/Job_metadata-retailsalesdatacsv-qxn2cavi2u-twxp7sm89h_123/",
    #     "get_config": {
    #       "action": "get_config",
    #       "method": "GET"
    #     },
    #     "error_reporting_url": "http://34.196.204.54:9012/api/set_job_report/metadata-retailsalesdatacsv-qxn2cavi2u-twxp7sm89h/",
    #     "set_result": {
    #       "action": "result",
    #       "method": "PUT"
    #     },
    #     "job_url": "http://34.196.204.54:9012/api/job/metadata-retailsalesdatacsv-qxn2cavi2u-twxp7sm89h/",
    #     "job_type": "metaData",
    #     "job_name": "RetailSalesData.csv",
    #     "xml_url": "http://34.196.204.54:9012/api/xml/metadata-retailsalesdatacsv-qxn2cavi2u-twxp7sm89h/"
    #   }
    # }
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
            "file:///home/gulshan/marlabs/datasets/Equipment.csv"
          ]
        }
      },
      "job_config": {
        "message_url": "http://34.196.204.54:9012/api/messages/Job_metadata-equipmentcsv-5awj1omo0m-m46od9pzfg_123/",
        "get_config": {
          "action": "get_config",
          "method": "GET"
        },
        "error_reporting_url": "http://34.196.204.54:9012/api/set_job_report/metadata-equipmentcsv-5awj1omo0m-m46od9pzfg/",
        "set_result": {
          "action": "result",
          "method": "PUT"
        },
        "job_url": "http://34.196.204.54:9012/api/job/metadata-equipmentcsv-5awj1omo0m-m46od9pzfg/",
        "job_type": "metaData",
        "job_name": "Equipment.csv",
        "xml_url": "http://34.196.204.54:9012/api/xml/metadata-equipmentcsv-5awj1omo0m-m46od9pzfg/",
        "app_id": None
      }
    }
    return metaDataConfig
