import os
from pyspark import SparkContext, SparkConf

conf = SparkConf()
conf.setAppName("application") \
    .set("spark.network.timeout", "300000") \
    .set("spark.executor.heartbeatInterval", "200000")
dirPath = 'hdfs://'+os.getenv('TARGET_HOST')+':9000'
print(dirPath)

sc = SparkContext.getOrCreate(conf)
text_file = sc.textFile(dirPath+"/twitter_sentiments.csv")
counts = text_file.flatMap(lambda line: line.split(" ")).map(
    lambda word: (word, 1)).reduceByKey(lambda a, b: a+b)
print(counts.collect())
