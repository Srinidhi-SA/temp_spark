import random
import urllib2
from collections import Counter

import numpy as np
import pandas as pd
import scipy.stats as scs
from pyspark.sql import SQLContext
from statsmodels.formula.api import ols

from bi.common import utils as CommonUtils
from bi.algorithms import utils as MLUtils
from bi.common import NormalCard, NarrativesTree, HtmlData, C3ChartData, TableData, ModelSummary,PopupData,NormalCard,ParallelCoordinateData,DataBox,WordCloud
from bi.common import NormalChartData, ChartJson

class StockAdvisor:
    # BASE_DIR = "/home/marlabs/codebase/stock-advisor/data/"
    BASE_DIR = "file:///home/gulshan/marlabs/datasets/"

    def __init__(self, spark, stockNameList,dataframe_context,result_setter):
        self._spark = spark
        self._stockNameList = stockNameList
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
        tempFileName = "/tmp/temp{}.json".format(randNO)
        tf = open(tempFileName,"w")
        tf.write(req_data)
        tf.close()
        df = self._spark.read.json("file:///"+tempFileName)
        return df

    def unpack_df(self, df):
        print "Unpacking the dataframe"
        old = df.toPandas()
        new_pd = old[['stock','source','final_url','time','title','short_desc','google_url','content']].copy()
        new = self._spark.createDataFrame(new_pd)

    def get_stock_articles(self, df):
        return df.count()

    def get_stock_sources(self, df):
        return df.select("source").distinct().count()

    def get_stock_sentiment(self, df):
        sentiment = 0
        for row in df.rdd.collect():
            sentimentLabel = row['sentiment']['document']['label']
            if sentimentLabel in ["positive","neutral"]:
                sentiment += row['sentiment']['document']['score']
            else:
                sentiment += -(row['sentiment']['document']['score'])
        return sentiment/float(df.count())

    def get_sentiment_change(self, df):
        change = list((x["time"], x["sentiment"]["document"]["score"]) for x in df.rdd.sortBy(lambda x : x["time"], ascending=True).collect())
        return change[len(change)-1][1] - change[0][1]

    def get_number_articles_per_source(self, df):
        output = dict(df.groupby('source').count().rdd.collect())
        print "*"*50
        print output
        print "*"*50

        return output

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

    def get_capitalized_name(self,word):
        capWord = ""
        for letter in word:
            capWord += letter.capitalize()
        return capWord

    def identify_concepts(self, df):

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
        data_dict_overall["nArticlesAndSentimentsPerConcept"] = {}

        return data_dict_overall

    def identify_concepts_python(self,df):
        pandasDf = df.toPandas()
        print type(pandasDf["keywords"])
        print pandasDf["keywords"][:3]
        pandasDf["concepts"] = pandasDf["keywords"].apply(self.get_concepts_for_item_python)
        return pandasDf

    def get_concepts_for_item_python(self, item):
        cur_keywords = [k["text"].lower() for k in item]
        cur_sentiments = [k["sentiment"]["score"] if True in [k["sentiment"]["label"] == "positive",k["sentiment"]["label"] == "neutral"]  else -k["sentiment"]["score"] for k in item]
        sentimentsDict = dict(zip(cur_keywords,cur_sentiments))
        cur_concepts = {"conceptList":[],"conceptKeywordDict":{},"conceptAvgSentimentDict":{}}
        for key in self.concepts:
            keywordIntersection = list(set(self.concepts[key]).intersection(set(cur_keywords)))
            if len(keywordIntersection) > 0:
                cur_concepts["conceptList"].append(key)
                cur_concepts["conceptKeywordDict"][key] = keywordIntersection
                cur_concepts["conceptAvgSentimentDict"][key] = np.mean(np.array([sentimentsDict[x]  for x in keywordIntersection]))
        return cur_concepts

    def get_number_articles_and_sentiments_per_concept(self,pandasDf):
        conceptNames = self.concepts.keys()
        valArray = []
        for val in conceptNames:
            valArray.append({"articlesCount":0,"posArticles":0,"negArticles":0,"totalSentiment":0})
        conceptNameDict = dict(zip(conceptNames,valArray))
        conceptCountArray = []
        sentimentArray = []
        for index, dfRow in pandasDf.iterrows():
            conceptNameDict = self.update_article_count_and_sentiment_score(conceptNameDict,dfRow)
            rowConceptArray = [1 if x in dfRow["concepts"]["conceptList"] else 0 for x in self.concepts.keys()]
            rowConceptArray.append(np.sum(np.array(rowConceptArray)))
            conceptCountArray.append(rowConceptArray)
            sentimentArray.append([dfRow["concepts"]["conceptAvgSentimentDict"][x] if x in dfRow["concepts"]["conceptAvgSentimentDict"] else 0 for x in self.concepts.keys()])
        outputDict = {}
        for key,value in conceptNameDict.items():
            value["avgSentiment"] = round(float(value["totalSentiment"])/value["articlesCount"],2)
            outputDict[key] = value
        conceptCounterDf = pd.DataFrame(np.array(conceptCountArray),columns=[x+"_count" for x in self.concepts.keys()]+["totalCount"])
        sentimentCounterDf = pd.DataFrame(np.array(sentimentArray),columns=[x+"_sentiment" for x in self.concepts.keys()])
        self.pandasDf = pd.concat([pandasDf,conceptCounterDf,sentimentCounterDf], axis=1)
        self.pandasDf["overallSentiment"] = self.pandasDf["sentiment"].apply(lambda x:x["document"]["score"] if x["document"]["label"] == "positive" else -x["document"]["score"])
        # print "*"*50
        # print outputDict
        # print "*"*50
        return outputDict

    def get_number_articles_per_concept(self,stockConceptsData):
        """
        aggregate results of get_number_articles_and_sentiments_per_concept method
        """
        outputDict = dict(zip(self.concepts.keys(),[0]*len(self.concepts.keys())))
        for stock,conceptDict in stockConceptsData.items():
            for k,v in conceptDict.items():
                outputDict[k] += v["articlesCount"]
        return outputDict


    def update_article_count_and_sentiment_score(self,counterDict,dfRow):
        for concept in dfRow["concepts"]["conceptList"]:
            counterDict[concept]["articlesCount"] += 1
            absSentimentScore = dfRow["sentiment"]["document"]["score"]
            label = dfRow["sentiment"]["document"]["label"]
            sentimentScore = absSentimentScore if label == "positive" else -absSentimentScore
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

    def create_chi_square_df(self,pandasDf,stockPriceData):
        conceptList = self.concepts.keys()
        conceptsData = pandasDf[["time"]+[x+"_count" for x in self.concepts.keys()]]
        # conceptCountDict = {}
        # for val in conceptList:
        #     conceptCountDict[val] = []
        # map(lambda x: self.get_chisquare_concept_columns(conceptCountDict,x),conceptsData["concepts"])
        # conceptCountDf = pd.DataFrame(conceptCountDict,index=conceptsData.index)
        # conceptsDF = pd.concat([conceptsData["time"], conceptCountDf], axis=1).groupby("time").sum().reset_index()
        conceptsDF = conceptsData.groupby("time").sum().reset_index()
        conceptsDF.index = conceptsDF["time"]
        stockDf = stockPriceData[["date","dayPriceDiff"]]
        stockDf.index = stockDf["date"]
        chiSquareDf = pd.concat([conceptsDF, stockDf], axis=1, join='inner')
        print chiSquareDf.columns
        chiSquareDf.drop(['time','date'], axis=1, inplace=True)
        print chiSquareDf.columns
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
        chi2 = scs.chi2_contingency(confusion_matrix)[0]
        return np.sqrt(chi2 / (n*(min(confusion_matrix.shape)-1)))

    def calculate_chiSquare(self,df,targetCol):
        cramerStat = {}
        colsToIterate = [x for x in df.columns if x != targetCol]
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

    def run_regression(self,df,targetCol):

        colMaps = ["c"+str(idx) if x != targetCol else x for idx,x in enumerate(df.columns)]
        print colMaps
        reverseMap = dict(zip(colMaps,df.columns))
        df.columns = colMaps
        reg_model = ols("{} ~ ".format(targetCol) +"+".join(list(set(df.columns) - {targetCol})), data=df).fit()
        # summarize our model
        model_summary = reg_model.summary()
        modelParams = reg_model.params
        modelParamsDf = pd.DataFrame({'id':modelParams.index, 'value':modelParams.values})
        print modelParamsDf
        coeffDict = modelParamsDf.set_index('id').to_dict()["value"]
        reverseMappedCoef = {}
        for k,v in coeffDict.items():
            if k != "Intercept":
                reverseMappedCoef[reverseMap[k]] = coeffDict[k]
            else:
                reverseMappedCoef[k] = coeffDict[k]
        print reverseMappedCoef
        print model_summary
        return reverseMappedCoef




    def Run(self):
        print "In stockAdvisor"
        data_dict_stocks = {}
        data_dict_overall = self.initialize_overall_dict()
        if self._runEnv == "debugMode":
            self.concepts = self.load_concepts_from_json()
        else:
            self.concepts = self.read_ankush_json(self.dataFilePath.format("concepts",""))

        masterDfDict = {}
        stockPriceTrendDict = {}
        for stock_symbol in self._stockNameList:
            #-------------- Read Operations ----------------
            if self._runEnv == "debugMode":
                df = self.read_json(self.BASE_DIR+stock_symbol+".json")
                df_historic = self.read_json(self.BASE_DIR+stock_symbol+"_historic.json")
            else:
                df = self.read_ankush_json(self.dataFilePath.format("bluemix",stock_symbol))
                df_historic = self.read_ankush_json(self.dataFilePath.format("historical",stock_symbol))

            stockPriceData = df_historic.select(["date","close","open"]).toPandas()
            stockPriceData["close"] = stockPriceData["close"].apply(float)
            stockPriceData["open"] = stockPriceData["open"].apply(float)
            stockPriceData["dayPriceDiff"] = stockPriceData["close"] - stockPriceData["open"]

            self.pandasDf = self.identify_concepts_python(df)

            # overall Distribution of articles and sentiments by concecpts
            # needs final presentation
            nArticlesAndSentimentsPerConcept = self.get_number_articles_and_sentiments_per_concept(self.pandasDf)
            # print nArticlesAndSentimentsPerConcept
            # print self.pandasDf.shape
            regDf = self.pandasDf[["time","overallSentiment","totalCount"]+[x+"_count" for x in self.concepts.keys()]]
            regDfgrouped = regDf.groupby("time").sum().reset_index()
            regDfgrouped.index = regDfgrouped["time"]
            stockDf  = stockPriceData[["close","date"]]
            stockDf.index = stockDf["date"]
            priceTrendDict = stockDf.to_dict()["close"]
            stockPriceTrendDict[stock_symbol] = priceTrendDict
            regDfFinal =  pd.concat([regDfgrouped, stockDf], axis=1, join='inner')
            regDfFinal.drop(["date"],axis = 1,inplace=True)
            # regDfFinal.columns = ["time","overallSentiment"+"_"+stock_symbol,"totalCount"+"_"+stock_symbol]+[x+"_count" for x in self.concepts.keys()]+["close"+"_"+stock_symbol]
            masterDfDict[stock_symbol] = regDfFinal
            self.chiSquarePandasDf = self.create_chi_square_df(self.pandasDf,stockPriceData)
            # self.chiSquareDf = self._sqlContext.createDataFrame(self.chiSquarePandasDf)
            self.chiSquareDict = self.calculate_chiSquare(self.chiSquarePandasDf,"dayPriceDiff")
            #-------------- Start Calculations ----------------
            number_articles = self.get_stock_articles(df)
            data_dict_overall["number_articles"] += number_articles
            data_dict_overall["number_articles_by_stock"][stock_symbol] = number_articles  #used for bar plot

            data_dict_overall["nArticlesAndSentimentsPerConcept"][stock_symbol] = nArticlesAndSentimentsPerConcept

            number_sources = self.get_stock_sources(df)
            data_dict_overall["number_sources"] += number_sources

            avg_sentiment_score = self.get_stock_sentiment(df)
            data_dict_overall["avg_sentiment_score"] += avg_sentiment_score
            data_dict_overall["stocks_by_sentiment"][stock_symbol] = avg_sentiment_score #used for bar plot

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
            # data_dict_overall["number_articles_per_source"][stock_symbol]=number_articles_per_source
            data_dict_overall["number_articles_per_source"]= dict(Counter(number_articles_per_source) + Counter(data_dict_overall["number_articles_per_source"]))
            average_sentiment_per_source = self.get_average_sentiment_per_source(df, number_articles_per_source)
            # print "average_sentiment_per_source : ", average_sentiment_per_source


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

        print "_"*50+"REGRESSIONDATA"+"_"*50
        self.regressionResultDict = {}
        for current_stock in self._stockNameList:
            regressionDf = masterDfDict[current_stock]
            regressionDf.index = regressionDf["time"]
            remaining_stocks = list(set(self._stockNameList) - {current_stock})
            if len(remaining_stocks) > 0:
                for other_stock in remaining_stocks:
                    colsToConsider = ["time","overallSentiment","close"]
                    otherStockDf = masterDfDict[other_stock][colsToConsider]
                    otherStockDf.columns = [x+"_"+other_stock for x in colsToConsider]
                    otherStockDf.index = otherStockDf["time"+"_"+other_stock]
                    regressionDf = pd.concat([regressionDf,otherStockDf], axis=1, join='inner')
                    regressionDf.drop(["time","time"+"_"+other_stock],axis=1,inplace=True)
            # print regressionDf.columns
            # Run linear regression on the regressionDf dataframe
            regressionCoeff = self.run_regression(regressionDf,"close")
            self.regressionResultDict[current_stock] = regressionCoeff

        print "#"*110
        number_stocks = len(self._stockNameList)

        stockPriceTrendArray = []
        dateList = stockPriceTrendDict[self._stockNameList[0]].keys()
        stockPriceTrendArray = stockPriceTrendDict[self._stockNameList[0]].items()
        capNameList = [self.get_capitalized_name(x) for x in self._stockNameList]
        capNameDict = dict(zip(self._stockNameList,capNameList))
        stockPriceTrendArray = [{"date":obj[0],capNameList[0]:obj[1]} for obj in stockPriceTrendArray]
        for obj in stockPriceTrendArray:
            for stockName in self._stockNameList[1:]:
                obj.update({capNameDict[stockName]:stockPriceTrendDict[stockName][obj["date"]]})

        data_dict_overall["price_trend"] = stockPriceTrendArray

        data_dict_overall["avg_sentiment_score"] = data_dict_overall["avg_sentiment_score"]/number_stocks
        data_dict_overall["stock_value_change"] = data_dict_overall["stock_value_change"]/number_stocks
        data_dict_overall["stock_percent_change"] = data_dict_overall["stock_percent_change"]/number_stocks

        data_dict_overall["number_articles_by_concept"] = self.get_number_articles_per_concept(data_dict_overall["nArticlesAndSentimentsPerConcept"])

        key, value = max(data_dict_overall["max_value_change"].iteritems(), key = lambda p: p[1])
        data_dict_overall["max_value_change_overall"] = (self.get_capitalized_name(key),value)
        key, value = min(data_dict_overall["max_value_change"].iteritems(), key = lambda p: p[1])
        data_dict_overall["min_value_change_overall"] = (self.get_capitalized_name(key),value)

        key,value = max(data_dict_overall["max_sentiment_change"].iteritems(), key = lambda p: p[1])
        data_dict_overall["max_sentiment_change_overall"] = (self.get_capitalized_name(key),value)

        # print data_dict_overall
        finalResult = NarrativesTree()
        overviewNode = NarrativesTree()
        stockNode = NarrativesTree()

        overviewCard = MLUtils.stock_sense_overviewCard(data_dict_overall)
        overviewNode.add_a_card(overviewCard)
        finalResult.add_a_node(overviewNode)


        return finalResult


    def __generate_normal_card(self, name, html):
        return {
                "cardType": "normal",
                "name": name,
                "slug": self.genarate_slug(name),
                "cardData": [
                    {
                        "dataType": "html",
                        "data": '<p><h2>{}</h2>{}</p>'.format(name, html)
                    }
                ]
            }

    def __generate_react_gauge_chart_card(self, name, score):
        score = round(score, 2)
        gauge_c3_chart_data = {
            "dataType": "gauge",
            "data": {
                    "min" : -1,
                    "max" : 1,
                    "value" : score,
                    "segments" : 2
                }

        }

        return gauge_c3_chart_data

    def __generate_c3_gauge_chart_card(self, name, score):

        score = round(score, 2)
        gauge_c3_chart_data = {
            "dataType": "c3Chart",
            "data": {
                "chart_c3": {
                    "color": {
                        "threshold": {
                            "values": [
                                -1,
                                0,
                                0.5,
                                1
                            ],
                            "unit": "value"
                        },
                        "pattern": [
                            '#0fc4b5',
                            '#005662',
                            '#148071',
                            '#6cba86'
                        ]
                    },
                    "data": {
                        "type": "gauge",
                        "columns": [
                            [
                                "data",
                                score
                            ]
                        ]
                    },
                    "gauge": {
                        "label": {
                            "format" : ""
                        },
                        "max": 1,
                        "min": -1,
                        "width": 39
                    },
                    "size": {
                        "height": 180
                    }
                },
                "gauge_format": True,
                # "xdata":["score"],
                # "table_c3": [
                #     ['score', score]
                # ]
            }
        }

        return gauge_c3_chart_data

    def generate_para_html(self):
        emotions_sorted = sorted(self.nl_understanding.get("emotion").get("document").get("emotion").items(),
                                 key=lambda (key, val): val, reverse=True)
        (best_emotion, best_value) = emotions_sorted[0]
        (second_best_emotion, second_best_value) = emotions_sorted[1]
        keywords = self.nl_understanding.get("keywords")
        keywords_html = " and ".join(
            ["<strong>{} ({})</strong>".format(item.get("text"), round(item.get("relevance"), 2)) for item in keywords[:2]])

        categories_html = " and ".join(["<strong>{}</strong>".format(item.get("label").split("/")[-1]) for item in
                                    self.nl_understanding.get("categories")[:2]])

        return """<p>The overall sentiment in the speech seems to be <strong>{} {}</strong>.
            The most predominant emotion is <strong>{}</strong> at around <strong>{}%</strong>.
            Another important emotion identified is  <strong>{}</strong> at <strong>{}%</strong>.
           mAdvisor identified <strong>{} keywords</strong> in the speech,
            {}
            having the highest relevance.
           The major categories are {}.</p>
             """.format(self.nl_understanding.get("sentiment").get("document").get("label"),
                        round(self.nl_understanding.get("sentiment").get("document").get("score"), 2),
                        best_emotion, int(best_value * 100),
                        second_best_emotion, int(second_best_value * 100),
                        len(keywords),
                        keywords_html,
                        categories_html
                        )


    def get_bar_chart(self, data, rotate=False, x="label", y="score", label_text=None):

        c3 = C3chart_ML(
            axes={
                "x": x,
                "y": y
            },
            label_text=label_text,
            data=data,
            axisRotation=rotate
        )
        details = c3.get_details()

        # decoded_chart =  decode_and_convert_chart_raw_data(details)

        # del decoded_chart['chart_c3']['axis']['x']['tick']['format']
        # del decoded_chart['chart_c3']['axis']['y']['tick']['format']
        # del decoded_chart['yformat']

        return {
            "dataType": "c3Chart",
            "data": details
        }


    def get_categories_bar(self, categories):

        data = categories
        return self.get_bar_chart(
            data=data,
            label_text={
                "x": "category",
                "y": "score"
            }
        )

    def get_keywords_bar(self, keywords):

        data = []

        for d in keywords:
            temp = {}
            temp['text'] = d.get('text')
            temp['score'] = d.get('relevance')
            data.append(temp)

        return self.get_bar_chart(
            data=data,
            x='text',
            y='score',
            label_text={
                "x": "keyword",
                "y": "score"
            }
        )

    def get_entities_bar(self, entities):

        data = []

        for d in entities:
            temp = {}
            temp['type'] = d.get('type')
            temp['relevance'] = d.get('relevance')
            data.append(temp)

        return self.get_bar_chart(
            data=data,
            x='type',
            y='relevance',
            label_text={
                "x": "entity",
                "y": "relevance"
            }
        )


class C3chart_ML(object):

    def __init__(self, **kwrgs):
        self.chart_type = kwrgs.get('chart_type', 'bar')
        self.axes = kwrgs.get('axes', {})
        self.label_text = kwrgs.get('label_text', {})
        self.types = kwrgs.get('types')
        self.axisRotation = kwrgs.get('axisRotation', False)
        self.yAxisNumberFormat = kwrgs.get('yAxisNumberFormat', ".2f")
        # self.y2AxisNumberFormat = kwrgs.get('y2AxisNumberFormat', False)
        self.showLegend = kwrgs.get('showLegend', False)
        self.hide_xtick = kwrgs.get('hide_xtick', False)
        self.subchart = kwrgs.get('subchart', False)
        self.rotate = kwrgs.get('rotate', False)
        self.data = kwrgs.get('data')
        self.legend = {}

    def get_details(self):

        return {
            'chart_type': self.chart_type,
            'axes': self.axes,
            'label_text': self.label_text,
            'types': self.types,
            'axisRotation': self.axisRotation,
            'yAxisNumberFormat': self.yAxisNumberFormat,
            'showLegend': self.showLegend,
            'hide_xtick': self.hide_xtick,
            'subchart': self.subchart,
            'rotate': self.rotate,
            'data': self.data,
            'legend': self.legend
        }

    def update_data(self, data):
        self.data = data

    def rotate_axis(self):
        self.axisRotation = True

    def update_axes(self, axes):
        self.axes = axes
