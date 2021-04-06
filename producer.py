import re
import json
import requests
import time
from kafka import KafkaProducer

host = '0.0.0.0:9092'
producer = KafkaProducer(bootstrap_servers=host, api_version=(2,0,0))
topic_name = 'test_topic'

input_json = 'https://storage.googleapis.com/datascience-public/data-eng-challenge/MOCK_DATA.json'

with requests.get(input_json) as url:
    raw_data = url.json()

    for row in raw_data:
        st = json.dumps(row, indent=4, sort_keys=True, default=str)

        producer.send('test_topic', st.encode('utf-8'))

        producer.flush()


