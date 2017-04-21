"""
functions to load data from various sources to create a dataframe
"""

from pyspark.sql import SparkSession

from decorators import accepts

class DataLoader:
    @staticmethod
    @accepts(SparkSession, basestring, has_header=bool, interpret_data_schema=bool)
    def load_csv_file(spark_session, csv_file_path, has_header=True, interpret_data_schema=True):
        return spark_session.read.csv(csv_file_path, header=has_header, inferSchema=interpret_data_schema)
