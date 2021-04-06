from kafka import KafkaConsumer
import json
import hashlib
from datetime import datetime, date
from collections import defaultdict

host = '0.0.0.0:9092'
kafka_topic = 'test_topic'

consumer = KafkaConsumer(kafka_topic, bootstrap_servers=host, api_version=(2,0,0))

insert_dict = {}
stats_dict = defaultdict(dict)

counter = 0

max_people_from = ''
max_count = 1

max_date_on = date.min
max_date_traffic = 0


for msg in consumer:
    #print('message consumed by kafka !!!')
    #print(msg)
    raw = json.loads(msg.value)
    if len(raw['country']) > 256:
        print('increase the column size!!!')

    # for GDPR reasons, we have to hide the names    
    raw['first_name'] = 'HIDDEN'    
    raw['last_name'] = 'HIDDEN'    
    
    hash_object = hashlib.md5(raw['email'].encode())
    raw['email'] = hash_object.hexdigest()

    d = datetime.strptime(raw['date'], '%d/%m/%Y')
    raw['date'] = d.strftime('%Y-%m-%d')

    # people from which countries
    try:
        stats_dict['country'][raw['country']] +=1
        print('total countries:',len(stats_dict['country']))
        if stats_dict['country'][raw['country']] > max_count:
            max_people_from = raw['country']
            max_count = stats_dict['country'][raw['country']] 
        print('max traffic from:',max_people_from, ':',max_count,'/',counter)
        #break    
    except:
        stats_dict['country'][raw['country']] = 1

     # male-female ratio
    try:
        stats_dict['gender'][raw['gender']] +=1
        print('male-female ratio?',stats_dict['gender']['Male'],':',stats_dict['gender']['Female'])
    except:
        stats_dict['gender'][raw['gender']] = 1

    #date of maximum traffic
    try:
        stats_dict['date'][raw['date']] +=1
        #print('total dates?',len(stats_dict['date']))
        if stats_dict['date'][raw['date']] > max_date_traffic:
            max_date_on = raw['date']
            max_date_traffic = stats_dict['date'][raw['date']] 
        print('max traffic on',max_date_on, ':',max_date_traffic,'/',counter)
        #break    
    except Exception as e:
        stats_dict['date'][raw['date']] = 1



    counter+=1


    #print('TOTAL:',counter)
