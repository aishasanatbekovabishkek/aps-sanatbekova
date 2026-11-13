from .request import Request


class StatisticsCollector:
    def __init__(self):
        self.generated_count = 0
        self.rejected_count = 0
        self.completed_count = 0

        self.total_waiting_time = 0.0
        self.total_service_time = 0.0
        self.total_system_time = 0.0

    def record_generated(self, request: Request) -> None:
        self.generated_count += 1

    def record_buffered(self, request: Request) -> None:
        pass

    def record_rejected(self, request: Request) -> None:
        self.rejected_count += 1

    def record_service_start(self, request: Request) -> None:
        pass

    def record_service_end(self, request: Request) -> None:
        self.completed_count += 1

        self.total_waiting_time += request.get_waiting_time()
        self.total_service_time += request.get_service_time()
        self.total_system_time += request.get_system_time()

    def get_rejection_probability(self) -> float:
        if self.generated_count == 0:
            return 0.0

        return self.rejected_count / self.generated_count

    def build_summary(self) -> dict:
        if self.completed_count == 0:
            average_waiting = 0.0
            average_service = 0.0
            average_system = 0.0
        else:
            average_waiting = self.total_waiting_time / self.completed_count
            average_service = self.total_service_time / self.completed_count
            average_system = self.total_system_time / self.completed_count

        return {
            "generated": self.generated_count,
            "completed": self.completed_count,
            "rejected": self.rejected_count,
            "rejection_probability": self.get_rejection_probability(),
            "average_waiting": average_waiting,
            "average_service": average_service,
            "average_system": average_system,
        }
