import json
from pyspark.sql import SQLContext
import pandas as pd
import numpy as np
import scipy.stats as scs
import urllib2
import random

from collections import Counter
from bi.stats.chisquare import ChiSquare
from bi.common import utils as CommonUtils


class StockAdvisor:
    # BASE_DIR = "/home/marlabs/codebase/stock-advisor/data/"
    BASE_DIR = "file:///home/gulshan/marlabs/datasets/"

    def __init__(self, spark, file_names,dataframe_context,result_setter):
        self._spark = spark
        self._file_names = file_names
        self._sqlContext = SQLContext(self._spark)
        self._dataAPI = dataframe_context.get_stock_data_api()
        self.dataFilePath = self._dataAPI+"?stockDataType={}&stockName={}"
        self._runEnv = dataframe_context.get_environement()


    def read_csv(self, file_name):
        sql = SQLContext(self._spark)
        print "-"*50
        print "Reading File : ", file_name + ".csv"
        name = self.BASE_DIR + file_name + ".csv"
        df = (sql.read
         .format("com.databricks.spark.csv")
         .option("header", "true")
         .load(name))
        return df

    def read_json(self, filepath):
        df = self._spark.read.json(filepath)
        return df

    def read_ankush_json(self,url):
        req = urllib2.urlopen(url)
        req_data = req.read()
        randNO = str(int(random.random()*10000000))
        tempFileName = "/tmp/temp{}.csv".format(randNO)
        tf = open(tempFileName,"w")
        tf.write(req_data)
        tf.close()
        df = self._spark.read.json("file:///"+tempFileName)
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
        return return_dict

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
        return (end_price-start_price, ((end_price-start_price)*100.0)/start_price )

    def identify_concepts(self, df):
        from pyspark.sql.functions import udf, col
        from pyspark.sql.types import ArrayType

        # temp_fun = udf( lambda x: self.get_concepts_for_item(x), ArrayType)
        # new_df = df.withColumn("concepts", temp_fun(col("keywords")))
        # new_df.printSchema()
        return df

    def load_concepts_from_json(self):
        concepts = {}
        for item in self._spark.read.json(self.BASE_DIR + "concepts.json").rdd.collect():
            cur_dict = item.asDict()
            for k in cur_dict:
                concepts[k] = cur_dict[k]
        return concepts

    def get_concepts_for_item(self, item):
        print "="*20
        print item
        cur_keywords = [item["text"].lower() for item in item["keywords"]]
        cur_concepts = []
        # print set(keywords)
        for key in self.concepts:
            if set(self.concepts[key]).intersection(set(cur_keywords)):
                cur_concepts.append(key)
        return cur_concepts

    def initialize_overall_dict(self):
        data_dict_overall = {}
        data_dict_overall["number_articles"] = 0
        data_dict_overall["number_sources"] = 0
        data_dict_overall["avg_sentiment_score"] = 0
        data_dict_overall["stock_value_change"] = 0
        data_dict_overall["stock_percent_change"] = 0
        data_dict_overall["max_value_change"] = {}
        data_dict_overall["max_sentiment_change"] = {}
        data_dict_overall["number_articles_by_stock"] = {}
        data_dict_overall["number_articles_per_source"] = {}
        data_dict_overall["stocks_by_sentiment"] = {}
        data_dict_overall["top_keywords"] = {}
        return data_dict_overall

    def identify_concepts_python(self,df):
        pandasDf = df.toPandas()
        pandasDf["concepts"] = pandasDf["keywords"].apply(self.get_concepts_for_item_python)
        return pandasDf

    def get_concepts_for_item_python(self, item):
        cur_keywords = [k["text"].lower() for k in item]
        cur_concepts = {"conceptList":[],"conceptKeywordDict":{}}
        for key in self.concepts:
            keywordIntersection = list(set(self.concepts[key]).intersection(set(cur_keywords)))
            if len(keywordIntersection) > 0:
                cur_concepts["conceptList"].append(key)
                cur_concepts["conceptKeywordDict"][key] = keywordIntersection
        return cur_concepts

    def get_number_articles_and_sentiments_per_concept(self,pandasDf):
        conceptNames = self.concepts.keys()
        valArray = []
        for val in conceptNames:
            valArray.append({"articlesCount":0,"posArticles":0,"negArticles":0,"totalSentiment":0})
        conceptNameDict = dict(zip(conceptNames,valArray))
        for index, dfRow in pandasDf.iterrows():
            conceptNameDict = self.update_article_count_and_sentiment_score(conceptNameDict,dfRow)

        outputDict = {}
        for key,value in conceptNameDict.items():
            value["avgSentiment"] = round(float(value["totalSentiment"])/value["articlesCount"],2)
            outputDict[key] = value
        return outputDict


    def update_article_count_and_sentiment_score(self,counterDict,dfRow):
        for concept in dfRow["concepts"]["conceptList"]:
            counterDict[concept]["articlesCount"] += 1
            counterDict[concept]["totalSentiment"] += dfRow["sentiment"]["document"]["score"]
            if self.check_an_article_is_positive_or_not(dfRow["keywords"]) == True:
                counterDict[concept]["posArticles"] += 1
            else:
                counterDict[concept]["negArticles"] += 1
        return counterDict

    def check_an_article_is_positive_or_not(self,keyWordArray):
        nPositive = []
        nNegative = []
        [nPositive.append(1) if obj["sentiment"]["label"] == "positive" else nNegative.append(1) for obj in keyWordArray]
        return True if sum(nPositive) > sum(nNegative) else False

    def create_chi_square_df(self,pandasDf,dfHistoric):
        conceptList = self.concepts.keys()
        conceptsData = pandasDf[["time","concepts"]]
        stockPriceData = dfHistoric.select(["date","close","open"]).toPandas()
        stockPriceData["close"] = stockPriceData["close"].apply(float)
        stockPriceData["open"] = stockPriceData["open"].apply(float)
        stockPriceData["dayPriceDiff"] = stockPriceData["close"] - stockPriceData["open"]
        conceptCountDict = {}
        for val in conceptList:
            conceptCountDict[val] = []
        map(lambda x: self.get_chisquare_concept_columns(conceptCountDict,x),conceptsData["concepts"])
        conceptCountDf = pd.DataFrame(conceptCountDict,index=conceptsData.index)
        conceptsDF = pd.concat([conceptsData["time"], conceptCountDf], axis=1).groupby("time").sum().reset_index()
        chiSquareDf = pd.concat([conceptsDF, stockPriceData["dayPriceDiff"]], axis=1, join='inner')
        chiSquareDf.drop(['time'], axis=1, inplace=True)
        return chiSquareDf

    def get_chisquare_concept_columns(self,conceptCountDict,dfRow):
        for concept in conceptCountDict.keys():
            if concept in dfRow["conceptList"]:
                conceptCountDict[concept].append(1)
            else:
                conceptCountDict[concept].append(0)

    def get_splits(self,pandasDf,colname,n_split):
        splits  = CommonUtils.frange(min(pandasDf[colname])-1,max(pandasDf[colname])+1,num_steps=n_split)
        splits = sorted(splits)
        splits_range = [(splits[idx],splits[idx+1]) for idx in range(len(splits)-1)]
        splits_data = {"splits":splits,"splits_range":splits_range}
        return splits_data

    def cramers_stat(self,confusion_matrix):
        n = confusion_matrix.sum().sum()
        # print n
        chi2 = scs.chi2_contingency(confusion_matrix)[0]
        return np.sqrt(chi2 / (n*(min(confusion_matrix.shape)-1)))

    def calculate_chiSquare(self,df,targetCol):
        cramerStat = {}
        colsToIterate = [x for x in df.columns if x!=targetCol]
        targetColSplits = self.get_splits(df,targetCol,3)["splits"]
        targetColGroupNames = ["grp"+str(idx) for idx in range(1,len(targetColSplits))]
        df["targetColBins"] = pd.cut(df[targetCol], targetColSplits, labels=targetColGroupNames)
        for col in colsToIterate:
            colSplits = self.get_splits(df,col,3)["splits"]
            colGroupNames = ["grp"+str(idx) for idx in range(1,len(colSplits))]
            df[col+"_bin_"] = pd.cut(df[col], colSplits, labels=colGroupNames)
            confusionMatrix = pd.crosstab(df["targetColBins"], df[col+"_bin_"])
            # Dropping rows and columns with zero sum
            confusionMatrix = confusionMatrix.loc[(confusionMatrix.sum(axis=1) != 0), (confusionMatrix.sum(axis=0) != 0)]
            cramerStat[col] = self.cramers_stat(confusionMatrix)
        return cramerStat


    def Run(self):
        print "In stockAdvisor"
        data_dict_stocks = {}
        data_dict_overall = self.initialize_overall_dict()
        if self._runEnv == "debugMode":
            self.concepts = self.load_concepts_from_json()
        else:
            self.concepts = self.read_ankush_json(self.dataFilePath.format("concepts",""))
        for stock_symbol in self._file_names:
            #-------------- Read Operations ----------------
            if self._runEnv == "debugMode":
                df = self.read_json(self.BASE_DIR+stock_symbol+".json")
                df_historic = self.read_json(self.BASE_DIR+stock_symbol+"_historic.json")
            else:
                df = self.read_ankush_json(self.dataFilePath.format("bluemix",stock_symbol))
                df_historic = self.read_ankush_json(self.dataFilePath.format("historical",stock_symbol))
            self.pandasDf = self.identify_concepts_python(df)
            nArticlesAndSentimentsPerConcept = self.get_number_articles_and_sentiments_per_concept(self.pandasDf)
            print nArticlesAndSentimentsPerConcept
            self.chiSquarePandasDf = self.create_chi_square_df(self.pandasDf,df_historic)
            # self.chiSquareDf = self._sqlContext.createDataFrame(self.chiSquarePandasDf)
            self.chiSquareDict = self.calculate_chiSquare(self.chiSquarePandasDf,"dayPriceDiff")
            #-------------- Start Calculations ----------------
            number_articles = self.get_stock_articles(df)
            data_dict_overall["number_articles"] += number_articles
            data_dict_overall["number_articles_by_stock"][stock_symbol] = number_articles
            print "number_articles : ", number_articles

            number_sources = self.get_stock_sources(df)
            data_dict_overall["number_sources"] += number_sources
            print "number_sources : ", number_sources

            avg_sentiment_score = self.get_stock_sentiment(df)
            data_dict_overall["avg_sentiment_score"] += avg_sentiment_score
            data_dict_overall["stocks_by_sentiment"][stock_symbol] = avg_sentiment_score
            # print "avg_sentiment_score : ", avg_sentiment_score

            sentiment_change = self.get_sentiment_change(df)
            data_dict_overall["max_sentiment_change"][stock_symbol]=sentiment_change
            # print "sentiment_change : ", sentiment_change

            (stock_value_change, stock_percent_change) = self.get_stock_change(df_historic)
            data_dict_overall["stock_value_change"] += stock_value_change
            data_dict_overall["stock_percent_change"] += stock_percent_change
            data_dict_overall["max_value_change"][stock_symbol]=stock_value_change
            # print "stock_value_change : ", stock_value_change
            # print "stock_percent_change : ", stock_percent_change

            number_articles_per_source = self.get_number_articles_per_source(df)
            # print "number_articles_per_source : ", number_articles_per_source
            data_dict_overall["number_articles_per_source"] = dict(Counter(number_articles_per_source) + Counter(data_dict_overall["number_articles_per_source"]))


            average_sentiment_per_source = self.get_average_sentiment_per_source(df, number_articles_per_source)
            # print "average_sentiment_per_source : ", average_sentiment_per_source
            #

            # # number_articles_per_concept = self.get_number_articles_per_concept(unpacked_df)
            # # average_sentiment_per_concept = self.get_average_sentiment_per_concept(unpacked_df)
            #

            top_keywords = self.get_top_keywords(df)
            # print "top_keywords : ", top_keywords
            data_dict_overall["top_keywords"] = dict(Counter(top_keywords) + Counter(data_dict_overall["top_keywords"]))

            # average_stock_per_date = self.get_average_stock_per_date(unpacked_df)

            average_sentiment_per_date = self.get_average_sentiment_per_date(df)
            # print "average_sentiment_per_date : ", average_sentiment_per_date

            (top_events_positive, top_events_negative) = self.get_top_events(df)
            # print "top events positive : ", top_events_positive
            # print "top events negative : ", top_events_negative

            # top_days = self.get_top_days(unpacked_df)

            # sentiment_by_concept_by_keyword = self.get_sentiment_by_concept_by_keyword(unpacked_df)

            # statistical_significance_keywords = self.get_statistical_significance_keywords(unpacked_df)

            # key_parameters_impacting_stock = self.get_key_parameters_impacting_stock(unpacked_df)

        print "_"*50
        number_stocks = len(self._file_names)
        data_dict_overall["avg_sentiment_score"] = data_dict_overall["avg_sentiment_score"]/number_stocks

        data_dict_overall["stock_value_change"] = data_dict_overall["stock_value_change"]/number_stocks

        data_dict_overall["stock_percent_change"] = data_dict_overall["stock_percent_change"]/number_stocks

        key, value = max(data_dict_overall["max_value_change"].iteritems(), key = lambda p: p[1])
        data_dict_overall["max_value_change"] = {key:value}

        key,value = max(data_dict_overall["max_sentiment_change"].iteritems(), key = lambda p: p[1])
        data_dict_overall["max_sentiment_change"] = {key:value}

        # print data_dict_overall
        sampleOutput ={
        "name": "Overview card",
        "slug": "fdfdfd_overview",
        "listOfNodes" : [],
        "listOfCards" : [

                {
                        "cardType": "normal",
                        "name": "Test",
                        "slug": "sdfasjfaskdjf",
                        "cardData": [
                            {
                                "dataType": "html",
                                "data": '<p><h2>{}</h2>{}</p>'.format("Test", "Test content")
                            }
                        ]
                    }
                ]
        }
        return sampleOutput
