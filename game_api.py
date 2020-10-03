#!/usr/bin/env python
import json
from kafka import KafkaProducer
from flask import Flask, request

app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers='kafka:29092')

    
# * Adds metadata such as Host/IP address, User-Agent to all generated events
# * Encodes it (default: encoding='utf-8', #errors='strict')
# * Produces event to Kafka
def log_to_kafka(topic, event):
        
    event.update(request.headers)
    #Adding remote header in case IP addresses outside of my environment make requests to our server
    event.update({'remote_addr': request.remote_addr}) 
    producer.send(topic, json.dumps(event).encode())
    
    
@app.route("/")
def default_response():
    """
    * Default response if no specific API route is hit
    """
    default_event = {'event_type': 'default'}
    log_to_kafka('game_events', default_event)
    return "This is the default response!\n"


@app.route("/purchase_sword")
def purchase_sword():
    """
    * GET message here can either be a default purchase_sword or pass query params
    * Both options get processed through via the log_to_kafka function while return back to the user the information of their purchase.
    """
    
    #Data is passed via qury parameters, add the arguments to our JSON logged to Kafka    
    result = {}
    for key, value in request.args.items():
        result[key] = value
        
        
    #Condition to check if params were specified in request
    if len(result) == 0:
        sword_event = {'event_type': 'purchase_sword'}
        log_to_kafka('game_events', sword_event)
        return "Sword Purchased\n"
    else:
        sword_event = {'event_type': 'purchase_sword'}
        sword_event.update(result)
        log_to_kafka('game_events', sword_event)
        return "Sword Purchased: " + json.dumps(result) + "\n"



@app.route("/join_a_guild")
def join_a_guild():
    """
    * GET message here can either be a default join_a_guild or pass query params
    * Both options get processed through via the log_to_kafka function while return back to the user the information of their purchase.
    
    """
    
    
    #Data is passed via qury parameters, add the arguments to our JSON logged to Kafka
    result = {}
    for key, value in request.args.items():
        result[key] = value
    
    
    #Condition to check if params were specified in request    
    if len(result) == 0:
        join_a_guild_event = {'event_type': 'join_a_guild'}
        log_to_kafka('game_events', join_a_guild_event)
        return "Joined a Guild!\n"
    else:
        join_a_guild_event = {'event_type': 'join_a_guild'}
        join_a_guild_event.update(result)
        log_to_kafka('game_events', join_a_guild_event)
        return "Joined a guild! " + json.dumps(result) + "\n"