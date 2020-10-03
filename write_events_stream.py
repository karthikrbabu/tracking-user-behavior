#!/usr/bin/env python
"""Extract events from kafka and write them to hdfs
"""
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, from_json
from pyspark.sql.types import StructType, StructField, StringType


def purchase_sword_event_schema():
    
    """
    Defining the strucuture of the "purchase_events" store
    
    |-- Accept: string (nullable = true)
    |-- Host: string (nullable = true)
    |-- User-Agent: string (nullable = true)
    |-- event_type: string (nullable = true)
    |-- metal: string (nullable = true)
    |-- power_level: string (nullable = true)
    |-- magical: string (nullable = true)
    |-- remote_addr: string (nullable = true)        
        
    """    
    
    return StructType([
        StructField("Accept", StringType(), True),
        StructField("Host", StringType(), True),
        StructField("User_Agent", StringType(), True),
        StructField("event_type", StringType(), True),        
        StructField('metal', StringType(), True),
        StructField('power_level', StringType(), True),
        StructField('magical', StringType(), True),
        StructField("remote_addr", StringType(), True),
    ])


def join_a_guild_event_schema():
    
    """
    Defining the strucuture of the "join_a_guild" store
    
    |-- Accept: string (nullable = true)
    |-- Host: string (nullable = true)
    |-- User-Agent: string (nullable = true)
    |-- event_type: string (nullable = true)
    |-- timestamp: string (nullable = true)
    |-- region: string (nullable = true)
    |-- remote_addr: string (nullable = true)        
        
    """
    
    return StructType([
        StructField("Accept", StringType(), True),
        StructField("Host", StringType(), True),
        StructField("User_Agent", StringType(), True),
        StructField("event_type", StringType(), True),        
        StructField('region', StringType(), True),
        StructField("remote_addr", StringType(), True),
    ])



@udf('boolean')
def is_sword_purchase(event_as_json):
    """udf for filtering purchase_sword events
    """
    event = json.loads(event_as_json)
    if event['event_type'] == 'purchase_sword':
        return True
    return False


@udf('boolean')
def is_join_a_guild(event_as_json):
    """udf for filtering join_a_guild events
    """
    event = json.loads(event_as_json)
    if event['event_type'] == 'join_a_guild':
        return True
    return False

    
def main():
    """main
    """
    
    #Build the Spark Session 
    spark = SparkSession \
        .builder \
        .appName("ExtractEventsJob") \
        .getOrCreate()

    
    '''
    Connect Spark to Kafka. Set it up in streaming mode to subscribe to the "game_events" 
    topic and read in messages.
    '''    
    raw_events = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:29092") \
        .option("subscribe", "game_events") \
        .load()

    
    '''
    Apply our UDF to only filter for "purchase_sword" events.
    In addition we add two columns, "raw_event" and "timestamp". In addition to all the 
    columns coming form the JSON message. We cast all columns to Strings
    '''
    sword_purchases = raw_events \
        .filter(is_sword_purchase(raw_events.value.cast('string'))) \
        .select(raw_events.value.cast('string').alias('raw_event'),
                raw_events.timestamp.cast('string'),
                from_json(raw_events.value.cast('string'),
                          purchase_sword_event_schema()).alias('json')) \
        .select('raw_event', 'timestamp', 'json.*')
    

    '''
    Apply our UDF to only filter for "join_a_guild" events.
    In addition we add two columns, "raw_event" and "timestamp". In addition to all the 
    columns coming form the JSON message. We cast all columns to Strings
    '''    
    join_a_guild = raw_events \
        .filter(is_join_a_guild(raw_events.value.cast('string'))) \
        .select(raw_events.value.cast('string').alias('raw_event'),
                raw_events.timestamp.cast('string'),
                from_json(raw_events.value.cast('string'),
                          join_a_guild_event_schema()).alias('json')) \
        .select('raw_event', 'timestamp', 'json.*')
    

    
    '''
    Below we setup two sinks, one for each type of event that we are filtering for. Here we indicate
    all the configurations for how and where to write the data. We specife "parquet" as the format. 
    we indicate the directory under the /tmp/* folder in HDFS. Finally we set our trigger processing time 
    to 15 seconds, this means that our stream processing will run ever 15 seconds to pull whatever data 
    that has been put into Kafka and process it.
    '''
    
    sink1 = sword_purchases \
        .writeStream \
        .format("parquet") \
        .option("checkpointLocation", "/tmp/checkpoints_for_purchase_events") \
        .option("path", "/tmp/purchase_events") \
        .trigger(processingTime="15 seconds") \
        .start()
    
    
    sink2 = join_a_guild \
        .writeStream \
        .format("parquet") \
        .option("checkpointLocation", "/tmp/checkpoints_for_join_guild") \
        .option("path", "/tmp/join_a_guild") \
        .trigger(processingTime="15 seconds") \
        .start()

    
    '''
    Using awaitTermination here we do not actually shut down the executor. 
    
    It will block until all tasks have completed execution after a shutdown request, or the timeout occurs, 
    or the current thread is interrupted, whichever happens first.
    '''
    spark.streams.awaitAnyTermination()

    
if __name__ == "__main__":
        main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

if __name__ == "__main__":
    main()
