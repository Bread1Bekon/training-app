import uuid
from datetime import datetime, timezone
from typing import TypeVar, Generic

from pydantic import BaseModel, Field

T = TypeVar("T")

class KafkaEvent(BaseModel, Generic[T]):
    specversion: str
    type: str
    source: str
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    data: T