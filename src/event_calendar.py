import heapq
from itertools import count

from .event import Event


class EventCalendar:
    def __init__(self):
        self.events = []
        self._counter = count()

    def add_event(self, event: Event) -> None:
        heapq.heappush(
            self.events,
            (event.time, next(self._counter), event),
        )

    def get_next_event(self) -> Event:
        if self.is_empty():
            raise ValueError("Календарь событий пуст")

        return heapq.heappop(self.events)[2]

    def is_empty(self) -> bool:
        return len(self.events) == 0

    def get_events(self) -> list[Event]:
        return [
            item[2]
            for item in sorted(self.events)
        ]
