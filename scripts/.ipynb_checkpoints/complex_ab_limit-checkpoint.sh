#!/bin/sh

# We can set a max threshold for the loop to run and stop for testing purposes. This has to come from the command line whatever value we pass for the limit 
# i.e.   sh complex_ab_limit.sh 7



x=1
while [ $((x)) -le $1 ]
    do

    #Based on odd or even we vary the data requests that we make
    if [ $((x%2)) -eq 0 ]:
    
    
    #Use Apache Bench to fire requests to Flask Server
    then
        docker-compose exec mids ab -n 10 -H "Host: user1.att.com" 'http://localhost:5000/purchase_sword?metal=copper&power_level=50&magical=True'
        
        docker-compose exec mids ab -n 10 -H "Host: user2.comcast.com" 'http://localhost:5000/join_a_guild?region=cali'
        
    else
        docker-compose exec mids ab -n 10 -H "Host: user1.att.com" 'http://localhost:5000/purchase_sword?metal=gold&power_level=100&magical=False'
        
        docker-compose exec mids ab -n 10 -H "Host: user2.comcast.com" 'http://localhost:5000/join_a_guild?region=ny'
        
    fi
    
    #Fire loop once every 5 seconds
    sleep 5
    
    #Increment counter for the data variation and for when to stop iteration
    x=$(( $x + 1 ))
    
done