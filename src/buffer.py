from enum import Enum

from .request import Request, RequestStatus


class BufferPutResult(Enum):
    STORED = "stored"
    FULL = "full"


class Buffer:
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Размер буфера должен быть положительным")

        self.capacity = capacity
        self.slots: list[Request | None] = [None] * capacity
        self.insertion_pointer = 0
        self._entry_counter = 0
        self._entry_order: dict[int, int] = {}

    def is_empty(self) -> bool:
        return all(request is None for request in self.slots)

    def is_full(self) -> bool:
        return all(request is not None for request in self.slots)

    def _store(self, index: int, request: Request, current_time: float):
        request.buffer_entry_time = current_time
        request.status = RequestStatus.BUFFERED

        self._entry_counter += 1
        self._entry_order[id(request)] = self._entry_counter
        self.slots[index] = request

    def put_by_ring(
        self, request: Request, current_time: float
    ) -> BufferPutResult:
        for offset in range(self.capacity):
            index = (self.insertion_pointer + offset) % self.capacity

            if self.slots[index] is None:
                self._store(index, request, current_time)
                self.insertion_pointer = (index + 1) % self.capacity
                return BufferPutResult.STORED

        return BufferPutResult.FULL

    def replace_oldest(
        self, request: Request, current_time: float
    ) -> Request:
        if not self.is_full():
            raise ValueError("Буфер ещё не заполнен")

        oldest_index = min(
            range(self.capacity),
            key=lambda i: self._entry_order[id(self.slots[i])],
        )

        rejected = self.slots[oldest_index]
        rejected.status = RequestStatus.REJECTED
        self._entry_order.pop(id(rejected))

        self._store(oldest_index, request, current_time)
        self.insertion_pointer = (oldest_index + 1) % self.capacity

        return rejected

    def take_lifo(self) -> Request | None:
        occupied = [
            (index, request)
            for index, request in enumerate(self.slots)
            if request is not None
        ]

        if not occupied:
            return None

        index, request = max(
            occupied,
            key=lambda item: self._entry_order[id(item[1])],
        )

        self.slots[index] = None
        self._entry_order.pop(id(request))

        return request

    def get_requests(self) -> list[Request]:
        return [
            request
            for request in self.slots
            if request is not None
        ]

    def get_insertion_pointer(self) -> int:
        return self.insertion_pointer
