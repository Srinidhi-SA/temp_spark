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

    @staticmethod
    @accepts(SparkSession, basestring, basestring, basestring, basestring, basestring)
    def create_dataframe_from_jdbc_connector(spark_session, jdbc_url, db_schema, table_name, user, password):
        df = None
        try:
            df = spark_session.read.format("jdbc").option(
                "url", "{}/{}".format(jdbc_url, db_schema)).option(
                "dbtable", "{}".format(table_name)).option(
                "user", user).option("password", password).load()
        except Exception as e:
            print("couldn't connect to database")
        return df

    
    
    @staticmethod
    @accepts(SparkSession, basestring, basestring, basestring, basestring, basestring)
    def create_dataframe_from_hana_connector(spark_session, jdbc_url, db_schema, table_name, user, password):
        df = None
        try:
            df = spark_session.read.format("jdbc").option(
                "url", jdbc_url).option("driver", "com.sap.db.jdbc.Driver").option(
                "dbtable", table_name).option("user", user).option("password", password).load()
        except Exception as e:
            print("couldn't connect to hana")
            raise e 
        return df

    
    
