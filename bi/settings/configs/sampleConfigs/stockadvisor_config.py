def get_stockadvisor_config():
    stockAdvisorConfig = {
        'job_config': {
          'job_url': 'http://34.196.204.54:9012/api/job/stockadvisor-stocking_is_what_i_do-6ryt9x72e8-ynolqb82hb/',
          'job_type': 'stockAdvisor',
          'set_result': {
            'action': 'result',
            'method': 'PUT'
          },
          'get_config': {
            'action': 'get_config',
            'method': 'GET'
          },
          'message_url': 'http://34.196.204.54:9012/api/messages/StockDataset_stocking_is_what_i_do-6ryt9x72e8_123/',
          'job_name': u'stocking_is_what_i_do'
        },
        u'config': {
          u'COLUMN_SETTINGS': {
            u'analysis_type': [
              u'metaData'
            ]
          },
          u'DATE_SETTINGS': {

          },
          u'DATA_SOURCE': {
            u'datasource_details': u''
          },
          u'STOCK_SETTINGS': {
            u'stockSymbolList': [
              'googl','appl'
            ],
            u'dataAPI': 'http://34.196.204.54:9012/api/stockdatasetfiles/stocking_is_what_i_do-imlizu9xul/',
          },
          u'FILE_SETTINGS': {
            u'inputfile': [
              u''
            ]
          }
        }
      }
    return stockAdvisorConfig
