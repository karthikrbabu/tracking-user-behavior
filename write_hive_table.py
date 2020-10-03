#!/usr/bin/env python
"""Extract events from kafka and write them to hdfs
"""
import json
from pyspark.sql import SparkSession, Row

# READ DIRECTLY FROM HDFS
def main():
    """main
    """
    
    
    '''
    Create a Spark job here to create an external table into our Hive metastore. We specify the schema
    needed for the table with the reference name of "sword_purchases"
    '''
    spark = SparkSession \
        .builder \
        .appName("WriteHiveTables") \
        .enableHiveSupport() \
        .getOrCreate()
    
    query_sword_purchases = """
    
        create external table if not exists sword_purchases(
        raw_event STRING, timestamp STRING, Accept STRING, Host STRING, User_Agent STRING,
        event_type STRING, metal STRING, power_level STRING, magical STRING, remote_addr STRING)
        stored as parquet
        location '/tmp/purchase_events'
    """
    
    spark.sql(query_sword_purchases)
    
    
    '''
    Create a Spark job here to create an external table into our Hive metastore. We specify the schema
    needed for the table with the reference name of "guild_joins"
    '''    
    query_guild_joins = """
        create external table if not exists guild_joins(
        raw_event STRING, timestamp STRING, Accept STRING, Host STRING, User_Agent STRING,
        event_type STRING, region STRING, remote_addr STRING)
        stored as parquet
        location '/tmp/join_a_guild'
    """
        
    spark.sql(query_guild_joins)

    
if __name__ == "__main__":
    main()
