from pyspark.sql.functions import udf
from pyspark.sql.types import FloatType
from pyspark.sql import functions as F
from pyspark.sql import Window
from pyspark.sql.functions import udf,desc,monotonically_increasing_id
from pyspark.ml.feature import QuantileDiscretizer


class GainLiftKS:
    def __init__(self,df,proba_column,target_column,spark):
        self._df = df
        self._spark = spark
        self._proba_column = proba_column
        self._target_column = target_column

    def Run(self):
        def Lift(cum_resp,decil_no):
            return (cum_resp/float(decil_no+1))
        self._df=self._df.orderBy(self._proba_column,ascending=False)
        self._df = self._df.withColumn("id", monotonically_increasing_id())
        discretizer = QuantileDiscretizer(numBuckets=10, inputCol="id", outputCol="deciles")
        self._df = discretizer.fit(self._df).transform(self._df)
        Rank=self._df.groupby('deciles').agg(F.count(self._df[self._proba_column]).alias('cnt'),F.sum(self._df[self._target_column]).alias('cnt_resp'))
        Rank=Rank.withColumn('cnt_non_resp',Rank['cnt']-Rank['cnt_resp'])
        Rank=Rank.orderBy('deciles',ascending=False)
        cumsum_window = (Window.orderBy(Rank['deciles'].desc()).rangeBetween(Window.unboundedPreceding, Window.currentRow))
        Rank=Rank.withColumn("cum_resp",F.sum('cnt_resp').over(cumsum_window))
        Rank=Rank.withColumn("cum_non_resp",F.sum('cnt_non_resp').over(cumsum_window))
        Rank=Rank.withColumn("cum_resp_pct",F.round(Rank["cum_resp"]*100/Rank.select(F.sum('cnt_resp')).collect()[0][0],2))
        Rank=Rank.withColumn("cum_non_resp_pct",F.round(Rank["cum_non_resp"]*100/Rank.select(F.sum('cnt_non_resp')).collect()[0][0],2))
        Rank=Rank.withColumn("cum_population",F.sum("cnt").over(cumsum_window))
        Rank=Rank.withColumn("pop_pct_per_decile",F.round(Rank["cnt"]*100/Rank.select(F.sum('cnt')).collect()[0][0]))
        Rank=Rank.withColumn("cum_population_pct",F.round(F.sum('pop_pct_per_decile').over(cumsum_window)))
        Rank=Rank.withColumn("KS",F.round(Rank["cum_resp_pct"] - Rank["cum_non_resp_pct"],2))
        Rank=Rank.withColumn("Lift at Decile",F.round(Rank["cnt_resp"]*Rank["pop_pct_per_decile"]*100/Rank.select(F.sum('cnt_resp')).collect()[0][0],2))
        Rank = Rank.withColumn("id", monotonically_increasing_id())
        Lift_udf=udf(lambda x,y:Lift(x,y),FloatType())
        Rank=Rank.withColumn("Total_Lift",F.round(Lift_udf("cum_resp","id"),2)  )
        Rank=Rank.drop('id')
        return(Rank)
