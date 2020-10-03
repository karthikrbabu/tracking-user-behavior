#!/bin/sh

# To simulate streaming, we have an infinite loop to request data. 

x=1
while true
    do

    #Based on odd or even we vary the data requests that we make
    if [ $((x%2)) -eq 0 ]:
    
    #Use Apache Bench to fire requests to Flask Server    
    then
        docker-compose exec mids ab -n 10 -H "Host: user1.att.com" 'http://localhost:5000/purchase_sword?metal=copper&power_level=50&magical=True'
        
        docker-compose exec mids ab -n 10 -H "Host: user2.comcast.com" 'http://localhost:5000/join_a_guild?region=cali'
        
    else
    
        #Use Apache Bench to fire requests 
        docker-compose exec mids ab -n 10 -H "Host: user1.att.com" 'http://localhost:5000/purchase_sword?metal=gold&power_level=100&magical=False'
        
        docker-compose exec mids ab -n 10 -H "Host: user2.comcast.com" 'http://localhost:5000/join_a_guild?region=ny'
        
    fi
    
    #Fire loop once every 10 seconds
    sleep 10
    
    #Increment counter for the data variation    
    x=$(( $x + 1 ))
    
done