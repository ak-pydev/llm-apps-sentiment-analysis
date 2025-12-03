#!/usr/bin/env python3
import os
import time
import json
from kafka import KafkaProducer

BOOTSTRAP = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
TOPIC = os.environ.get('KAFKA_TOPIC', 'sentiment')

producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

messages = [
    'I love this product',
    'This is terrible, I hate it',
    'Just OK, nothing special',
    'Absolutely amazing experience',
    'Worst purchase ever'
]

try:
    print('Starting producer, sending to', BOOTSTRAP)
    while True:
        for text in messages:
            payload = {'text': text}
            producer.send(TOPIC, payload)
            producer.flush()
            print('sent:', payload)
            time.sleep(1)
except KeyboardInterrupt:
    print('Producer stopped')
