from .buffer import Buffer
from .event import Event, EventType
from .event_calendar import EventCalendar
from .master import Master
from .master_pool import MasterPool
from .request import Request
from .statistics_collector import StatisticsCollector


class SelectionDispatcher:
    def __init__(
        self,
        buffer: Buffer,
        master_pool: MasterPool,
        event_calendar: EventCalendar,
        statistics: StatisticsCollector,
    ):
        self.buffer = buffer
        self.master_pool = master_pool
        self.event_calendar = event_calendar
        self.statistics = statistics

    def try_start_service(
        self, request: Request, current_time: float
    ) -> bool:
        master = self.master_pool.find_free_by_ring()

        if master is None:
            return False

        finish_time = master.start_service(request, current_time)

        self.event_calendar.add_event(
            Event(
                time=finish_time,
                type=EventType.SERVICE_COMPLETED,
                request=request,
                master=master,
            )
        )

        self.statistics.record_service_start(request)
        return True

    def on_master_released(
        self, master: Master, current_time: float
    ) -> None:
        if self.buffer.is_empty():
            return

        request = self.buffer.take_lifo()

        if request is not None:
            started = self.try_start_service(request, current_time)

            if not started:
                raise RuntimeError(
                    "После освобождения мастера не найден свободный прибор"
                )
