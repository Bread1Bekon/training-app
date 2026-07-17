from app.producers.base import BaseKafkaProducer
from app.events.form_status_update import FormStatusUpdateEvent

class FormProducer(BaseKafkaProducer[FormStatusUpdateEvent]):
    def __init__(self, topic: str = "form-status-updates"):
        super().__init__(topic=topic)