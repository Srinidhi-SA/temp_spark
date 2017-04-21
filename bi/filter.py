import sys
import ConfigParser
import json
from bi.common import utils
from bi.common import DataLoader
from bi.common import DataWriter
from bi.common import DataFilterHelper
from bi.common import FilterContextSetter
from bi.common import BIException
from parser import configparser
from bi.common import MetaDataHelper
import commands


'''
def get_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, help='HDFS location of input csv file')
    parser.add_argument('--result', type=str, help='HDFS output location to store descriptive stats')
    return parser
'''

if __name__ == '__main__':
    APP_NAME = 'mAdvisor-Filterer'
    spark = utils.get_spark_session(app_name=APP_NAME)
    spark.sparkContext.setLogLevel("ERROR")

    config_file = sys.argv[1]
    config = ConfigParser.ConfigParser()
    config.optionxform=str
    config.read(config_file)
    config_obj = configparser.ParserConfig(config)
    config_obj.set_params()

    dff_context = FilterContextSetter(config_obj)
    dff_context.set_params()

    df = DataLoader.load_csv_file(spark, dff_context.get_input_file())
    print "FILE LOADED: ", dff_context.get_input_file()
    dff_helper = DataFilterHelper(df, dff_context)
    dff_helper.set_params()
    df = dff_helper.get_data_frame()

    meta_helper = MetaDataHelper(df)
    #meta_helper.get_datetime_suggestions()
    if meta_helper.has_date_suggestions():
        meta_helper.get_formats()
    CSV_FILE = dff_context.get_input_file()
    print "File loaded: ", CSV_FILE
    meta_data = utils.as_dict(meta_helper)
    print "Metadata: ", meta_data
    print '-'*20
    RESULT_FILE = dff_context.get_result_file()
    #DataWriter.write_dict_as_json(spark, meta_data, RESULT_FILE)
    #df.write.csv('hdfs://localhost:9000/input/created_by_spark.csv')
    df.coalesce(1).write.format('csv').save('hdfs://localhost:9000/input/created_by_spark1')
    files = commands.getoutput('hadoop fs -ls hdfs://localhost:9000/input/created_by_spark1').splitlines()[-1]
    files = files.split()[-1]
    #commands.getoutput('hadoop fs -rm '+CSV_FILE)
    import random
    print '*'*20 + 'hadoop fs -distcp '+files+' /input/spark_created_' + '*'*20
    commands.getoutput('hadoop distcp '+files+' /input/spark_created_'+str(random.random()))
    commands.getoutput('hadoop fs -rm -r hdfs://localhost:9000/input/created_by_spark1')
    spark.stop()
