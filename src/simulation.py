from .buffer import Buffer
from .event import Event, EventType
from .event_calendar import EventCalendar
from .master_pool import MasterPool
from .placement_dispatcher import PlacementDispatcher
from .selection_dispatcher import SelectionDispatcher
from .source import Source
from .statistics_collector import StatisticsCollector


class Simulation:
    def __init__(
        self,
        max_requests: int = 10,
        buffer_capacity: int = 2,
        master_count: int = 1,
        min_interval: float = 1.0,
        max_interval: float = 3.0,
        mean_service_time: float = 5.0,
    ):
        if max_requests <= 0:
            raise ValueError("Количество заявок должно быть положительным")

        self.max_requests = max_requests
        self.current_time = 0.0
        self.step_number = 0

        self.sources = [
            Source(1, min_interval, max_interval)
        ]

        self.buffer = Buffer(buffer_capacity)
        self.master_pool = MasterPool(
            master_count, mean_service_time
        )
        self.event_calendar = EventCalendar()
        self.statistics = StatisticsCollector()

        self.selection_dispatcher = SelectionDispatcher(
            self.buffer,
            self.master_pool,
            self.event_calendar,
            self.statistics,
        )

        self.placement_dispatcher = PlacementDispatcher(
            self.buffer,
            self.selection_dispatcher,
            self.statistics,
        )

        self.initialize()

    def initialize(self):
        for source in self.sources:
            self.schedule_next_arrival(source)

    def schedule_next_arrival(self, source):
        if source.generated_count >= self.max_requests:
            return

        interval = source.generate_next_interval()

        self.event_calendar.add_event(
            Event(
                time=self.current_time + interval,
                type=EventType.REQUEST_GENERATED,
            )
        )

    def process_request_generated(self, event):
        source = self.sources[0]

        request = source.generate_request(self.current_time)

        self.statistics.record_generated(request)

        self.placement_dispatcher.handle_request(
            request, self.current_time
        )

        self.schedule_next_arrival(source)

        return f"Поступила заявка №{request.request_number}"

    def process_service_completed(self, event):
        master = event.master

        if master is None:
            raise RuntimeError("У события не указан мастер")

        request = master.finish_service(self.current_time)

        self.statistics.record_service_end(request)

        self.selection_dispatcher.on_master_released(
            master, self.current_time
        )

        return (
            f"Мастер №{master.id} завершил "
            f"заявку №{request.request_number}"
        )

    def process_event(self, event):
        if event.type == EventType.REQUEST_GENERATED:
            return self.process_request_generated(event)

        if event.type == EventType.SERVICE_COMPLETED:
            return self.process_service_completed(event)

        raise ValueError("Неизвестный тип события")

    def step(self):
        if self.event_calendar.is_empty():
            return False

        event = self.event_calendar.get_next_event()

        if event.time < self.current_time:
            raise RuntimeError("Нарушен порядок модельного времени")

        self.current_time = event.time
        self.step_number += 1

        description = self.process_event(event)

        self.show_current_state(description)

        return True

    def show_current_state(self, description):
        print(f"\n{'=' * 45}")
        print(f"ШАГ {self.step_number}")
        print(f"Модельное время: {self.current_time:.2f}")
        print(f"Событие: {description}")

        print("\nИсточник:")
        for source in self.sources:
            print(
                f"  Источник №{source.id}: "
                f"создано {source.generated_count}"
            )

        print("\nБуфер:")
        for index, request in enumerate(self.buffer.slots):
            if request is None:
                value = "пусто"
            else:
                value = f"заявка №{request.request_number}"

            print(f"  Ячейка {index}: {value}")

        print(
            f"  Указатель постановки: "
            f"{self.buffer.get_insertion_pointer()}"
        )

        print("\nМастера:")
        for master in self.master_pool.get_masters():
            if master.is_free():
                print(f"  Мастер №{master.id}: свободен")
            else:
                print(
                    f"  Мастер №{master.id}: занят, "
                    f"заявка №{master.current_request.request_number}"
                )

        print(
            f"  Указатель выбора: "
            f"{self.master_pool.get_selection_pointer()}"
        )

        print("\nСтатистика:")
        print(f"  Создано: {self.statistics.generated_count}")
        print(f"  Обслужено: {self.statistics.completed_count}")
        print(f"  Отказов: {self.statistics.rejected_count}")
        print(
            f"  Вероятность отказа: "
            f"{self.statistics.get_rejection_probability():.2%}"
        )

        print("\nКалендарь событий:")
        events = self.event_calendar.get_events()

        if not events:
            print("  Нет запланированных событий")
        else:
            for event in events:
                print(
                    f"  {event.time:.2f}: "
                    f"{event.type.value}"
                )

    def run_step_mode(self):
        print("=== ПОШАГОВОЕ МОДЕЛИРОВАНИЕ ===")

        while not self.event_calendar.is_empty():
            command = input(
                "\nEnter - следующий шаг, q - выход: "
            ).strip().lower()

            if command == "q":
                print("Моделирование остановлено пользователем.")
                return

            self.step()

        print("\n=== МОДЕЛИРОВАНИЕ ЗАВЕРШЕНО ===")
        print(self.statistics.build_summary())
