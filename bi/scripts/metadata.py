# -*- coding: utf-8 -*-
"""Gathers descriptive stats for all columns in a dataframe"""

import argparse
import json
import sys

from bi.common import DataLoader
from bi.common import DataWriter
from bi.common import MetaDataHelper
from bi.common import utils as CommonUtils


# from bi.common import ContextSetter

def get_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, help='HDFS location of input csv file')
    parser.add_argument('--result', type=str, help='HDFS output location to store descriptive stats')
    return parser


#if __name__ == '__main__':
def main(inputPath,resultPath):
    APP_NAME = "DataFrame Metadata"
    spark = CommonUtils.get_spark_session(app_name=APP_NAME)
    spark.sparkContext.setLogLevel("ERROR")
    CSV_FILE = inputPath #arguments.input
    RESULT_FILE = resultPath#arguments.result
    df = DataLoader.load_csv_file(spark, CSV_FILE)
    # df_context = ContextSetter(df)
    meta_helper = MetaDataHelper(df, transform = 1)
    #meta_helper.get_datetime_suggestions()
    if meta_helper.has_date_suggestions():
        meta_helper.get_formats()
    print "File loaded: ", CSV_FILE
    meta_data = CommonUtils.as_dict(meta_helper)
    meta_data = json.dumps(meta_data)
    # print  meta_data
    print '-'*20
    DataWriter.write_dict_as_json(spark, {'Metadata':meta_data}, RESULT_FILE)
     #spark.stop()

if __name__ == '__main__':
    argument_parser = get_argument_parser()
    arguments = argument_parser.parse_args()
    if arguments.input is None \
            or arguments.result is None:
        print 'One of the aguments --input / --result is missing'
        sys.exit(-1)
    main(arguments.input,arguments.result)
