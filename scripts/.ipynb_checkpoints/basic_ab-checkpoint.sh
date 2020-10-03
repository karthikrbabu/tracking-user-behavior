#!/bin/sh

#Use Apache Bench to fire sample basic requests to Flask Server    
docker-compose exec mids ab -n 10 -H "Host: user1.comcast.com" 'http://localhost:5000/'
docker-compose exec mids ab -n 10 -H "Host: user1.comcast.com" 'http://localhost:5000/purchase_sword'
docker-compose exec mids ab -n 10 -H "Host: user2.att.com" 'http://localhost:5000/'
docker-compose exec mids ab -n 10 -H "Host: user2.att.com" 'http://localhost:5000/purchase_sword'
docker-compose exec mids ab -n 10 -H "Host: user1.att.com" 'http://localhost:5000/join_a_guild'
docker-compose exec mids ab -n 10 -H "Host: user2.att.com" 'http://localhost:5000/join_a_guild'
