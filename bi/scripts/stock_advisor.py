import json
from pyspark.sql import SQLContext

class stockAdvisor:
    def __init__(self, spark, file_names):
        self._spark = spark
        self._file_names = file_names

    def read_csv(self):
        sql = SQLContext(self._spark)
        print "In Read CSV"
        df = (sql.read
         .format("com.databricks.spark.csv")
         .option("header", "true")
         .load("/home/marlabs/Documents/stock-advisor/nl_understanding.csv"))
        print type(df)
        print df.columns
        return df

    def get_file_sentiment(df):
        print

    def Run(self):
        print "In stockAdvisor"
        data_dict_files = {}
        for files in self._file_names:
            df = self.read_csv(self)
            unpacked_df = self.unpack_df(self)
            unpacked_df.cache()
            '''
            Start of Single Stock Analysis
            '''
            number_articles = self.get_stock_articles(unpacked_df)
            number_sources = self.get_stock_sources(unpacked_df)
            avg_sentiment_score = self.get_stock_sentiment(unpacked_df)
            sentiment_change = self.get_sentiment_change(unpacked_df)

            #stock_value_change = self.get_stock_value_change(unpacked_df)

            number_articles_per_source = self.get_number_articles_per_source(unpacked_df)
            average_sentiment_per_source = self.get_average_sentiment_per_source(unpacked_df)

            # number_articles_per_concept = self.get_number_articles_per_concept(unpacked_df)
            # average_sentiment_per_concept = self.get_average_sentiment_per_concept(unpacked_df)

            top_keywords = self.get_top_keywords(unpacked_df)
            average_stock_per_date = self.get_average_stock_per_date(unpacked_df)
            average_sentiment_per_date = self.get_average_sentiment_per_date(unpacked_df)
            top_events = self.get_top_events(unpacked_df)
            top_days = self.get_top_days(unpacked_df)
            '''
            # "Each concept has multiple keywords. Each keyword will be involved in multiple articles of varying sentiment.
            Calculate average sentiment for each keyword.
            3 Values Required: Concept, keyword, Average sentiment score for keyword
            *The color coding should be based on the absolute value of the sentiment score. ie. Darkest green should be applicable for values close to both +1 and -1
            '''
            sentiment_by_concept_by_keyword = self.get_sentiment_by_concept_by_keyword(unpacked_df)

            '''
            "
            Statistical Significance of Keywords (Chi-Square):
            Target variable is stock performance (High Medium Low) vs No of mentions of Keyword ( Positive or Negative Mentions)
            x-axis - Keyword
            y-axis - Effect Size
            Limit - Top 10"
            '''
            statistical_significance_keywords = self.get_statistical_significance_keywords(unpacked_df)
            '''
            "Regression:
            Stock Price vs Overall Sentiment/ No of Articles/ No of Articles by Concepts/ Sentiment Score by Concepts/ Sentiment Score by Keywords/ Sentiment Score of Competition/ Stock Price of Competition/ Competition's Mentions
            x-axis - Regression Coeff
            y-axis - Independant Variables"
            '''
            key_parameters_impacting_stock = self.get_key_parameters_impacting_stock(unpacked_df)
