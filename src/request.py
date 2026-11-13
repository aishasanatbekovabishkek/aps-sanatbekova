from dataclasses import dataclass
from enum import Enum
from typing import Optional


class RequestStatus(Enum):
    CREATED = "created"
    BUFFERED = "buffered"
    IN_SERVICE = "in_service"
    COMPLETED = "completed"
    REJECTED = "rejected"


@dataclass
class Request:
    source_id: int
    request_number: int
    generation_time: float
    buffer_entry_time: Optional[float] = None
    service_start_time: Optional[float] = None
    service_end_time: Optional[float] = None
    status: RequestStatus = RequestStatus.CREATED

    def get_waiting_time(self) -> float:
        if self.service_start_time is None:
            return 0.0

        return self.service_start_time - self.generation_time

    def get_service_time(self) -> float:
        if self.service_start_time is None or self.service_end_time is None:
            return 0.0

        return self.service_end_time - self.service_start_time

    def get_system_time(self) -> float:
        if self.service_end_time is None:
            return 0.0

        return self.service_end_time - self.generation_time
