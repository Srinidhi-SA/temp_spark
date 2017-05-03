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
import pandas as pd
import random
from pyspark.sql.functions import col,udf
from pyspark.sql.types import FloatType


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
    ip = dff_context.get_input_file()
    dummy_ip = ip+str(random.random())
    df = DataLoader.load_csv_file(spark, ip)
    print "FILE LOADED: ", ip
    dff_helper = DataFilterHelper(df, dff_context)
    dff_helper.set_params()
    df = dff_helper.get_data_frame()

    meta_helper = MetaDataHelper(df)
    CSV_FILE = dff_context.get_input_file()
    print "File loaded: ", CSV_FILE
    meta_data = utils.as_dict(meta_helper)
    print "Metadata: ", meta_data
    print '-'*20
    RESULT_FILE = dff_context.get_result_file()
    DataWriter.write_dict_as_json(spark, meta_data, RESULT_FILE)
    #df.write.csv('hdfs://localhost:9000/input/created_by_spark.csv')
    df.coalesce(1).write.format('csv').save(dummy_ip, header = True)
    files = commands.getoutput('hadoop fs -ls '+dummy_ip).splitlines()[-1]
    files = files.split()[-1]
    #commands.getoutput('hadoop fs -rm '+CSV_FILE)
    print '*'*20 + 'hadoop fs -distcp '+files+' /input/spark_created_' + '*'*20
    #commands.getoutput('hadoop distcp '+files+' /input/spark_created_'+str(random.random()))
    commands.getoutput('hadoop fs -rm '+CSV_FILE)
    commands.getoutput('hadoop fs -cp '+files+' '+CSV_FILE)
    commands.getoutput('hadoop fs -rm -r '+dummy_ip)

    spark.stop()
