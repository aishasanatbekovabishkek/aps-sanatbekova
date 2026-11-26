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
        log=None,
    ):
        self.buffer = buffer
        self.master_pool = master_pool
        self.event_calendar = event_calendar
        self.statistics = statistics
        self.log = log or (lambda message: None)

    def try_start_service(
        self, request: Request, current_time: float
    ) -> bool:
        old_pointer = self.master_pool.get_selection_pointer()

        self.log(
            f"Д2П2: поиск свободного мастера "
            f"по кольцу с позиции {old_pointer}"
        )

        master = self.master_pool.find_free_by_ring()

        if master is None:
            self.log("Д2: все мастера заняты")
            return False

        new_pointer = self.master_pool.get_selection_pointer()

        self.log(f"Д2П2: выбран мастер №{master.id}")

        self.log(
            f"Указатель выбора: "
            f"{old_pointer} -> {new_pointer}"
        )

        finish_time = master.start_service(request, current_time)

        self.log(
            f"Мастер №{master.id} начал обслуживание "
            f"заявки №{request.request_number}"
        )

        self.log(
            f"Время обслуживания: "
            f"{finish_time - current_time:.2f}"
        )

        self.event_calendar.add_event(
            Event(
                time=finish_time,
                type=EventType.SERVICE_COMPLETED,
                request=request,
                master=master,
            )
        )

        self.log(
            f"В календарь добавлено событие "
            f"завершения обслуживания на {finish_time:.2f}"
        )

        self.statistics.record_service_start(request)
        return True

    def on_master_released(
        self, master: Master, current_time: float
    ) -> None:
        self.log(f"Д2: мастер №{master.id} освободился")

        if self.buffer.is_empty():
            self.log("Д2: буфер пуст, нет заявок для обслуживания")
            return

        request = self.buffer.take_lifo()

        if request is not None:
            self.log(
                f"Д2Б2: по LIFO выбрана последняя "
                f"поступившая заявка №{request.request_number}"
            )

            started = self.try_start_service(
                request, current_time
            )

            if not started:
                raise RuntimeError(
                    "После освобождения мастера "
                    "не найден свободный прибор"
                )
