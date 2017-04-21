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
import argparse
import pandas as pd
import random
from pyspark.sql.functions import col,udf
from pyspark.sql.types import FloatType
'''
Filter Arguments Format:
--inputfile "" --consider_columns [] --dimension_filter {} --measure_filter {}

Example:
Format1:
spark-submit --master spark://localhost.localdomain:7077 /home/yasar/marlabs/marlabs-bi/bi/filter_cl.py
    --input hdfs://localhost:9000/input/data_test1.csv --result hdfs://localhost:9000/meta_result
    --consider_columns 'EDUCATION' 'MARRIAGE' 'AGE_CATEGORY' 'PAYMENT_DECEMBER' 'PAYMENT_NOVEMBER' 'BILL_AMOUNT_DECEMBER' 'AMOUNT_PAID_DECEMBER' 'STATUS' 'AVERAGE_BALANCE' 'RATING' 'DEFAULT_PERCENT' 'DATE_JOIN' 'CREDIT_BALANCE' 'AMOUNT' 'TOTAL' 'NUMBER' 'RANDOM'
    --dimension_filter '{"AGE_CATEGORY":["31-40","21-30","41-50","Above 50"]}'
    --measure_filter  '{"CREDIT_BALANCE":[100,1000]}'

Format2:
spark-submit --master spark://localhost.localdomain:7077 /home/yasar/marlabs/marlabs-bi/bi/filter_cl.py
    --input hdfs://localhost:9000/input/data_test1.csv
    --result hdfs://localhost:9000/meta_result
    --consider_columns '{"consider_columns": ["EDUCATION", "MARRIAGE", "AGE_CATEGORY", "PAYMENT_DECEMBER", "PAYMENT_NOVEMBER", "BILL_AMOUNT_DECEMBER", "AMOUNT_PAID_DECEMBER", "STATUS", "AVERAGE_BALANCE", "RATING", "DEFAULT_PERCENT", "DATE_JOIN", "CREDIT_BALANCE", "AMOUNT", "TOTAL", "NUMBER", "RANDOM"]}'
    --dimension_filter '{"AGE_CATEGORY":["31-40","21-30","41-50","Above 50"]}'
    --measure_filter  '{"CREDIT_BALANCE":[100,1000]}'

'''

def get_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, help='HDFS location of input csv file')
    #parser.add_argument('--consider_columns', type=str, help='List of columns', nargs='+')
    parser.add_argument('--consider_columns', type=str, help='Dictionary with consider_columns as key')
    parser.add_argument('--measure_filter', type=str, help='Dictionary with measure filter criteria')
    parser.add_argument('--dimension_filter', type=str, help='Dictionary with dimension filter criteria')
    parser.add_argument('--result', type=str, help='HDFS output location to store descriptive stats')
    return parser

if __name__ == '__main__':
    APP_NAME = 'mAdvisor-Filterer'
    argument_parser = get_argument_parser()
    arguments = argument_parser.parse_args()
    if arguments.input is None or arguments.consider_columns is None or arguments.measure_filter is None \
            or arguments.result is None or arguments.dimension_filter is None:
        # print 'One of the aguments --input / --consider_columns / --measure_filter / --consider_columns is missing'
        sys.exit(-1)
    ip = arguments.input
    dummy_ip = ip+str(random.random())
    result = arguments.result
    cc = arguments.consider_columns
    mf = arguments.measure_filter
    df = arguments.dimension_filter
    spark = utils.get_spark_session(app_name=APP_NAME)
    spark.sparkContext.setLogLevel("ERROR")
    cc = json.loads(cc)['consider_columns']
    df = json.loads(df)
    mf = json.loads(mf)
    #config_file = sys.argv[1]
    #config = ConfigParser.ConfigParser()
    #config.optionxform=str
    #config.read(config_file)
    #config_obj = configparser.ParserConfig(config)
    #config_obj.set_params()

    dff_context = FilterContextSetter('')
    dff_context.set_params_cl(ip,result,cc,df,mf)

    df = DataLoader.load_csv_file(spark, dff_context.get_input_file())
    print "FILE LOADED: ", dff_context.get_input_file()
    dff_helper = DataFilterHelper(df, dff_context)
    dff_helper.set_params()
    df = dff_helper.get_data_frame()
    sample_rows = min(100.0, float(df.count()*0.8))
    sample_df = df.sample(False, sample_rows/df.count(), seed = 120)
    sample_df = sample_df.toPandas()
    updated_col_names = utils.get_updated_colnames(sample_df)
    changed_columns = updated_col_names['c']
    updated_col_names = updated_col_names['f']
    mapping = dict(zip(sample_df.columns, updated_col_names))
    from re import sub
    func = udf(lambda x: float(sub('[^0-9.a-zA-Z/-]','',x)), FloatType())
    #func = udf(lambda x: dt.datetime.strptime(x,'%d-%m-%Y'), DateType())
    #df = df.select(*[func(c).alias(mapping.get(c)) if c in changed_columns else c for c in df.columns])
    #df = df.select([col(c).alias(mapping.get(c)) for c in sample_df.columns])
    df = df.select(*[func(c).alias(c) if c in changed_columns else c for c in df.columns])

    meta_helper = MetaDataHelper(df)
    df = df.select(*[col(c).alias(mapping.get(c)) if c in changed_columns else c for c in df.columns])
    #meta_helper.get_datetime_suggestions()
    if meta_helper.has_date_suggestions():
        meta_helper.get_formats()
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
