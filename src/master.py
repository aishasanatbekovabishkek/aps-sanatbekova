import random

from .request import Request, RequestStatus


class Master:
    def __init__(self, master_id: int, mean_service_time: float):
        if mean_service_time <= 0:
            raise ValueError("Среднее время обслуживания должно быть положительным")

        self.id = master_id
        self.mean_service_time = mean_service_time
        self.busy = False
        self.current_request: Request | None = None
        self.busy_time = 0.0
        self.completed_count = 0

    def is_free(self) -> bool:
        return not self.busy

    def generate_service_time(self) -> float:
        return random.expovariate(1.0 / self.mean_service_time)

    def start_service(self, request: Request, current_time: float) -> float:
        if self.busy:
            raise ValueError("Мастер уже занят")

        service_time = self.generate_service_time()

        self.busy = True
        self.current_request = request

        request.service_start_time = current_time
        request.status = RequestStatus.IN_SERVICE

        return current_time + service_time

    def finish_service(self, current_time: float) -> Request:
        if not self.busy or self.current_request is None:
            raise ValueError("У мастера нет заявки для завершения")

        request = self.current_request
        request.service_end_time = current_time
        request.status = RequestStatus.COMPLETED

        self.busy_time += current_time - request.service_start_time
        self.completed_count += 1

        self.busy = False
        self.current_request = None

        return request
