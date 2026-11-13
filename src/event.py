from dataclasses import dataclass
from enum import Enum
from typing import Optional

from .request import Request
from .master import Master


class EventType(Enum):
    REQUEST_GENERATED = "request_generated"
    SERVICE_COMPLETED = "service_completed"


@dataclass
class Event:
    time: float
    type: EventType
    request: Optional[Request] = None
    master: Optional[Master] = None
