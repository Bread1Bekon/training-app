from pydantic import BaseModel

from app.events.base import KafkaEvent


class FormStatusUpdateData(BaseModel):
    formid: int
    status: str
    userid: int
    message: str = ""


class FormStatusUpdateEvent(KafkaEvent[FormStatusUpdateData]):
    specversion: str = "v1"
    type: str = "myapp.forms.form.updated"
    source: str = "/services/forms"