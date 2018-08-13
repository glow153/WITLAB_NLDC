from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql import SQLContext

from pysparkmgr.singleton import Singleton


class PySparkManager(Singleton):
    sc = None

    def __init__(self):
        self.sc = self.getSparkContext('appName', 'local[*]')
        self.sqlContext = self.getSqlContext()
        self.sundf = self.sqlContext.read.parquet("hdfs:///ds/sun.parquet")

    def getSqlContext(self):
        return SQLContext(self.sc)

    def getSparkContext(self, appName, master):
        if self.sc:
            return self.sc

        conf = SparkConf().setAppName(appName)\
                          .setMaster(master)\
                          .set('spark.local.ip', '210.102.142.14')\
                          .set('spark.driver.host', '210.102.142.14')
        return SparkContext(conf=conf)

    def getsrs(self, day):
        rs = self.sundf.select("rise", "set") \
                .where('date = "%s"' % day) \
                .collect()
        return {"rise": str(rs[0][0]),
                "set": str(rs[0][1])}
