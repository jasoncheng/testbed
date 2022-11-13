from pyspark import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.streaming import StreamingContext
import pyspark.sql.types as tp
from pyspark.ml import Pipeline
from pyspark import StorageLevel
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler
from pyspark.ml.feature import StopWordsRemover, Word2Vec, RegexTokenizer
from pyspark.ml.classification import LogisticRegression
from pyspark.sql import Row, Column
import sys
import numpy

def get_prediction(tweet_text):
    try:
        # remove blank line
        tweet_text = tweet_text.filter(lambda x: len(x) > 0)
        # create dataframe for each row contains a tweet text
        rowRdd = tweet_text.map(lambda w: Row(tweet=w))
        wordsDataFrame = spark.createDataFrame(rowRdd)
        # get the sentiments for each row
        #pipelineFit.transform(wordsDataFrame).select("tweet", "prediction").show()
        pipelineFit.transform(wordsDataFrame).select('tweet','prediction').show()

    except:
        pass

sc = SparkContext(appName="PySparkShell")
spark = SparkSession(sc)

my_schema = tp.StructType([
    tp.StructField(name='id', dataType=tp.IntegerType(), nullable=True),
    tp.StructField(name='label', dataType=tp.IntegerType(), nullable=True),
    tp.StructField(name='tweet', dataType=tp.StringType(), nullable=True),
        ])

print('\n\nReading the dataset\n')
my_data = spark.read.csv('hdfs://bd2:9000/twitter_sentiments.csv', schema=my_schema, header=True)
my_data.show(2)
my_data.printSchema()

print('\n\nDefining the pipeline stages\m')
stage_1 = RegexTokenizer(inputCol = 'tweet', outputCol = 'tokens', pattern = '\\W')
stage_2 = StopWordsRemover(inputCol = 'tokens', outputCol = 'filtered_words')
stage_3 = Word2Vec(inputCol = 'filtered_words', outputCol = 'vector', vectorSize = 100)
model = LogisticRegression(featuresCol = 'vector', labelCol = 'label')

print('\n\nStages Defined.....\n')
pipeline = Pipeline(stages = [stage_1, stage_2, stage_3, model])

print('\n\nFit the pipeline with the training data....\n')
pipelineFie = pipeline.fit(my_data)

print('\n\nModel Trained...Waiting for the Data!!!!\n')
ssc = StreamingContext(sc, batchDuration=3)
lines = ssc.socketTextStream(sys.argv[1], int(sys.argv[2]), StorageLevel.MEMORY_AND_DISK)
words = lines.flatMap(lambda line: line.split('TWEET_APP'))
words.foreachRDD(get_prediction)
ssc.start()
ssc.awaitTermination()