import random

from .request import Request


class Source:
    def __init__(
        self,
        source_id: int,
        min_interval: float,
        max_interval: float,
    ):
        if min_interval <= 0 or max_interval < min_interval:
            raise ValueError("Неверные границы интервала")

        self.id = source_id
        self.min_interval = min_interval
        self.max_interval = max_interval
        self.generated_count = 0

    def generate_next_interval(self) -> float:
        return random.uniform(
            self.min_interval,
            self.max_interval,
        )

    def generate_request(self, current_time: float) -> Request:
        self.generated_count += 1

        return Request(
            source_id=self.id,
            request_number=self.generated_count,
            generation_time=current_time,
        )
