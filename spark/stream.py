"""
Find out top heavy heatterss
spark-2.1.0-bin-hadoop2.7/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.1.0 Amy/spark/stream.py
"""
from __future__ import print_function

import os
import json

from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

import redis

def send20(rdd, key):
    # we have only one RDD, so it is OK to create connection in worker
    r = redis.StrictRedis(host=os.environ['REDIS_HOST'],\
         port=os.environ['REDIS_PORT'], db=os.environ['REDIS_DB'])
    list = rdd.sortBy(lambda x: x[1], ascending=False).take(20)
    print(list)
    r.set(key, json.dumps(list))

def createContext():
    sc = SparkContext("local[2]", "NetworkWordCount")
    ssc = StreamingContext(sc, 10)
    ssc.checkpoint('~/sparkCheckpoint/')
 
    kvs = KafkaUtils.createDirectStream(ssc, ['acronyms'], \
        {"metadata.broker.list": os.environ['KAFKA_BOOTSTRAP_SERVERS']})
    searches = kvs.map(lambda a: a[1]).map(lambda a: (a, 1))
    
    countsMin = searches.reduceByKeyAndWindow(lambda a, b: a+b, lambda a, b: a-b, 60, 10)\
        .filter(lambda a: a[1] != 0)
    countsMin.foreachRDD(lambda rdd: send20(rdd, 'topMin'))
    
    countsWeek = searches.reduceByKeyAndWindow(lambda a, b: a+b, lambda a, b: a-b, 604800, 10)\
        .filter(lambda a: a[1] != 0)
    countsWeek.foreachRDD(lambda rdd: send20(rdd, 'topWeek'))
    return ssc

if __name__ == "__main__":
    r = redis.StrictRedis(host=os.environ['REDIS_HOST'],\
         port=os.environ['REDIS_PORT'], db=os.environ['REDIS_DB'])
    ssc = createContext()
    ssc.start()
    ssc.awaitTermination()

