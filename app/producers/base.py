from abc import abstractmethod
from typing import TypeVar, Generic, Any
from kafka import get_kafka_producer, delivery_report

T = TypeVar('T')

class BaseKafkaProducer(Generic[T]):
    def __init__(self, topic: str):
        self.producer = get_kafka_producer()
        self.topic = topic

    def _send_to_kafka(self, key: str, value: str):
        self.producer.produce(
            topic=self.topic,
            key=key,
            value=value,
            callback=delivery_report
        )

        self.producer.poll(0)

    def publish(self, key: str, event: T):

        self._send_to_kafka(
            key=str(key),
            value=str(event.model_dump_json())
        )

        self.producer.flush()