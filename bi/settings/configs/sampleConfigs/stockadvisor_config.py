def get_stockadvisor_config():
    stockConfig = {
          "config": {
            "COLUMN_SETTINGS": {
              "analysis_type": [
                "metaData"
              ]
            },
            "DATE_SETTINGS": {

            },
            "DATA_SOURCE": {
              "datasource_type": "",
              "datasource_details": ""
            },
            "STOCK_SETTINGS": {
              "stockSymbolList": [
                "googl",
                "amzn"
              ],
              "dataAPI": "http://madvisordev.marlabsai.com:80/api/stockdatasetfiles/asd23-xu1c13hebr/"
            },
            "FILE_SETTINGS": {
              "inputfile": [
                ""
              ]
            }
          },
          "job_config": {
            "message_url": "http://madvisordev.marlabsai.com:80/api/messages/Job_stockadvisor-asd23-xu1c13hebr-zkkkkf2ljl_123/",
            "get_config": {
              "action": "get_config",
              "method": "GET"
            },
            "error_reporting_url": "http://madvisordev.marlabsai.com:80/api/set_job_report/stockadvisor-asd23-xu1c13hebr-zkkkkf2ljl/",
            "set_result": {
              "action": "result",
              "method": "PUT"
            },
            "job_url": "http://madvisordev.marlabsai.com:80/api/job/stockadvisor-asd23-xu1c13hebr-zkkkkf2ljl/",
            "job_type": "stockAdvisor",
            "job_name": "asd23",
            "xml_url": "http://madvisordev.marlabsai.com:80/api/xml/stockadvisor-asd23-xu1c13hebr-zkkkkf2ljl/",
            "app_id": None
          }
    }
    return stockConfig
