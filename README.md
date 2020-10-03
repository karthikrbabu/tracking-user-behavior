# Project 3: Understanding User Behavior

### 07/30/2020 - Shyamkarthik Rameshbabu

# Introduction

- You're a data scientist at a game development company  

- Your latest mobile game has two events you're interested in tracking: `purchase a
  sword` & `join guild`

- Each has metadata characterstic of such events (i.e., sword type, guild name,
  etc)
  
  
Our goal here will be to simulate user interactions with our "mobile game" while tracking and processing events through the entire pipeline end to end. We will take advantage of a variety of tools to achieve each step of this pipeline which will be detailed below.


Below you will find a table of contents in essence for the various stages of this project.


## Preparing the Pipeline

To set up the infrastructure where we will pipe the data through, transform it, and ultimately land it in in a queriable structure, we will need various docker containers to help out.

The `docker-compose.yml` file is the config file that specifies all the details in order to spin up our pipeline. Please refer to this to understand the various containers that are being used. You will also find the setup of the ports that allow us to connect the containers together. Comments are included in the `docker-compose.yml` file.


## Building the Pipeline

`project3_final_report.ipynb` describes all the commands that are required to spin up the pipeline with all the necessary command line options. You will find details of each step, followed at the end by a runnable query engine setup with Presto. Here you will see some simple queries into HDFS.


## Other Files:

* `karthikrbabu-history.txt` includes the complete history of the commands I have run on my console. (It is un-altered!)


* `game_api.py` includes all the setup for our Flask server. This file defines what APIs are supported and handles the logging to our Kafka queue as requests come in.


* `write_events_stream.py` defines the start of our Spark streaming session. The code detailed here kicks off the Spark job, and will continue to listen and process events that stream in from Kafka. The business logic sits here for filtering events of different types and writing them to the respective file storage in HDFS.


* `write_hive_table.py` defines the Spark job that creates "phonebook" for Presto to read from HDFS using Hive as a meta store that points to the right location to query the data from HDFS. The Spark job here will use spark SQL to create external tables that we can use as a pointer and schema definition to then query into HDFS.


* ```scripts/*.sh``` to simulate user interactions with our "mobile app". These generate requests to our Flask server.

    * ```basic_ab.sh```
    * ```complex_ab_limit.sh```
    * ```complex_ab_infinite.sh```
