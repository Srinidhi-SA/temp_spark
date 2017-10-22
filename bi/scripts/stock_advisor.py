import json
from pyspark.sql import SQLContext
import pandas as pd

class stockAdvisor:
    def __init__(self, spark, file_names):
        self._spark = spark
        self._file_names = file_names

    def read_csv(self, file_name):
        sql = SQLContext(self._spark)
        print "-"*50
        print "Reading File : ", file_name + ".csv"
        name = "/home/marlabs/Documents/stock-advisor/data/" + file_name + ".csv"
        df = (sql.read
         .format("com.databricks.spark.csv")
         .option("header", "true")
         .load(name))
        return df

    def read_json(self, file_name):
        # sql = SQLContext(self._spark)
        name = "/home/marlabs/codebase/stock-advisor/data/" + file_name + ".json"
        # df = sql.jsonFile(name)
        # content = json.loads(open(name).read())
        df = self._spark.read.json(name)
        return df

    def unpack_df(self, df):
        print "Unpacking the dataframe"
        old = df.toPandas()
        new_pd = old[['stock','source','final_url','time','title','short_desc','google_url','content']].copy()
        print new_pd
        new = self._spark.createDataFrame(new_pd)
        print new.columns

    def get_stock_articles(self, df):
        return df.count()

    def get_stock_sources(self, df):
        return df.select("source").distinct().count()

    def get_stock_sentiment(self, df):
        sentiment = 0
        for row in df.rdd.collect():
            sentiment += row['sentiment']['document']['score']
        return sentiment/df.count()

    def get_sentiment_change(self, df):
        change = list((x["time"], x["sentiment"]["document"]["score"]) for x in df.rdd.sortBy(lambda x : x["time"], ascending=True).collect())
        return change[len(change)-1][1] - change[0][1]

    def get_number_articles_per_source(self, df):
        return dict(df.groupby('source').count().rdd.collect())

    def get_average_sentiment_per_source(self, df, number_articles_per_source):
        return_dict = {}
        for item in number_articles_per_source.keys():
            return_dict[item] = df.filter(df.source == item).groupBy(df.sentiment.document.score).avg().collect()[0].asDict().values()[0]
        return return_dict

    def get_average_sentiment_per_date(self, df):
        return_dict = {}
        for item in dict(df.groupby('time').count().rdd.collect()):
            return_dict[item] = df.filter(df.time == item).groupBy(df.sentiment.document.score).avg().collect()[0].asDict().values()[0]

    def get_top_keywords(self, df):
        return dict((x['text'], x['relevance']) for x in df.select('keywords').rdd.flatMap(lambda x: x).flatMap(lambda x: x).sortBy(lambda x: x['relevance'], ascending=False).collect())

    def get_top_events(self, df):
        positive_articles = list((x['title'], x['sentiment']['document']['score']) for x in df.rdd.sortBy(lambda x: x['sentiment']['document']['score'], ascending=False).filter(lambda x : x['sentiment']['document']['score'] > 0).collect())
        negative_articles = list((x['title'], x['sentiment']['document']['score']) for x in df.rdd.sortBy(lambda x: x['sentiment']['document']['score'], ascending=False).filter(lambda x : x['sentiment']['document']['score'] < 0).collect())

        return (positive_articles, negative_articles)

    def get_stock_change(self, df_historic):
        sorted_list = df_historic.rdd.sortBy(lambda x: x['date'], ascending=True).collect()
        start_price = float(sorted_list[-1]['close'])
        end_price = float(sorted_list[0]['close'])
        print "start_price", start_price
        print "end_price" , end_price

        return (end_price-start_price, ((end_price-start_price)*100.0)/start_price )

    def Run(self):
        print "In stockAdvisor"
        data_dict_files = {}
        for stock_symbol in self._file_names:
            # df = self.read_csv(file_name)
            df = self.read_json(stock_symbol)
            df_historic = self.read_json(stock_symbol+"_historic")

            # unpacked_df = self.unpack_df(df)
            # unpacked_df.cache()

            # '''
            # Start of Single Stock Analysis
            # '''
            number_articles = self.get_stock_articles(df)
            print "number_articles : ", number_articles
            number_sources = self.get_stock_sources(df)
            print "number_sources : ", number_sources
            avg_sentiment_score = self.get_stock_sentiment(df)
            print "avg_sentiment_score : ", avg_sentiment_score

            sentiment_change = self.get_sentiment_change(df)
            print "sentiment_change : ", sentiment_change
            # stock_value_change = self.get_stock_value_change(unpacked_df)
            # sentiment_change = self.get_sentiment_change(df)
            (stock_value_change, stock_percent_change) = self.get_stock_change(df_historic)
            print "stock_value_change : ", stock_value_change
            print "stock_percent_change : ", stock_percent_change

            number_articles_per_source = self.get_number_articles_per_source(df)
            print "number_articles_per_source : ", number_articles_per_source
            average_sentiment_per_source = self.get_average_sentiment_per_source(df, number_articles_per_source)
            print "average_sentiment_per_source : ", average_sentiment_per_source
            #
            # # number_articles_per_concept = self.get_number_articles_per_concept(unpacked_df)
            # # average_sentiment_per_concept = self.get_average_sentiment_per_concept(unpacked_df)
            #
            top_keywords = self.get_top_keywords(df)
            print "top_keywords : ", top_keywords
            # average_stock_per_date = self.get_average_stock_per_date(unpacked_df)
            average_sentiment_per_date = self.get_average_sentiment_per_date(df)
            print "average_sentiment_per_date : ", average_sentiment_per_date

            (top_events_positive, top_events_negative) = self.get_top_events(df)
            print "top events positive : ", top_events_positive
            print "top events negative : ", top_events_negative

            # top_days = self.get_top_days(unpacked_df)
            # '''
            # # "Each concept has multiple keywords. Each keyword will be involved in multiple articles of varying sentiment.
            # Calculate average sentiment for each keyword.
            # 3 Values Required: Concept, keyword, Average sentiment score for keyword
            # *The color coding should be based on the absolute value of the sentiment score. ie. Darkest green should be applicable for values close to both +1 and -1
            # '''
            # sentiment_by_concept_by_keyword = self.get_sentiment_by_concept_by_keyword(unpacked_df)
            #
            # '''
            # "
            # Statistical Significance of Keywords (Chi-Square):
            # Target variable is stock performance (High Medium Low) vs No of mentions of Keyword ( Positive or Negative Mentions)
            # x-axis - Keyword
            # y-axis - Effect Size
            # Limit - Top 10"
            # '''
            # statistical_significance_keywords = self.get_statistical_significance_keywords(unpacked_df)
            # '''
            # "Regression:
            # Stock Price vs Overall Sentiment/ No of Articles/ No of Articles by Concepts/ Sentiment Score by Concepts/ Sentiment Score by Keywords/ Sentiment Score of Competition/ Stock Price of Competition/ Competition's Mentions
            # x-axis - Regression Coeff
            # y-axis - Independant Variables"
            # '''
            # key_parameters_impacting_stock = self.get_key_parameters_impacting_stock(unpacked_df)
            