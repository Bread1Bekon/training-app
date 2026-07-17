import json
from kafka import get_kafka_consumer
from app.events.form_status_update import FormStatusUpdateEvent


class FormNotificationConsumer:
    def __init__(self):
        self.topic = "form-notifications"
        self.consumer = get_kafka_consumer(group_id="notification-service-group")

    def start(self):
        try:
            self.consumer.subscribe([self.topic])
            print(f"[*] Waiting for messages in '{self.topic}'. To exit press CTRL+C")

            while True:
                msg = self.consumer.poll(timeout=1.0)

                if msg is None:
                    continue
                if msg.error():
                    print(f"Consumer error: {msg.error()}")
                    continue

                data = json.loads(msg.value().decode('utf-8'))

                event = FormStatusUpdateEvent(**data)

                print("\n" + "=" * 50)
                print("RECEIVED KAFKA EVENT: Form Status Updated")
                print(f"Form ID:    {event.form_id}")
                print(f"New Status: {event.status}")
                print(f"To User ID: {event.user_id}")
                print(f"Moderator:  {event.moderator_name}")
                print(f"Message:    {event.message}")
                print("=" * 50 + "\n")

                self.consumer.commit(asynchronous=False)

        finally:
            self.consumer.close()


if __name__ == "__main__":
    consumer = FormNotificationConsumer()
    consumer.start()