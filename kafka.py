from confluent_kafka import Producer
from confluent_kafka.cimpl import Consumer

from config import settings

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def get_kafka_producer():
    kafka_conf = {
        'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
        'client.id': 'training-app-producer'
    }
    producer = Producer(kafka_conf)
    return producer

def get_kafka_consumer(group_id: str):
    conf = {
        'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
        'group.id': group_id,
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False,
    }
    consumer = Consumer(conf)
    return consumer