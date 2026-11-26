from .buffer import Buffer, BufferPutResult
from .request import Request
from .selection_dispatcher import SelectionDispatcher
from .statistics_collector import StatisticsCollector


class PlacementDispatcher:
    def __init__(
        self,
        buffer: Buffer,
        selection_dispatcher: SelectionDispatcher,
        statistics: StatisticsCollector,
        log=None,
    ):
        self.buffer = buffer
        self.selection_dispatcher = selection_dispatcher
        self.statistics = statistics
        self.log = log or (lambda message: None)

    def handle_request(
        self, request: Request, current_time: float
    ) -> None:
        self.log(
            f"Д1: принята заявка №{request.request_number}"
        )

        started = self.selection_dispatcher.try_start_service(
            request, current_time
        )

        if started:
            self.log("Д1: заявка передана на обслуживание")
            return

        self.log("Д1: заявка направляется в буфер")

        old_pointer = self.buffer.get_insertion_pointer()

        result = self.buffer.put_by_ring(request, current_time)

        if result == BufferPutResult.STORED:
            self.statistics.record_buffered(request)

            new_pointer = self.buffer.get_insertion_pointer()
            index = (new_pointer - 1) % self.buffer.capacity

            self.log(
                f"Д1ОЗ1: заявка №{request.request_number} "
                f"помещена в ячейку {index}"
            )

            self.log(
                f"Указатель постановки: "
                f"{old_pointer} -> {new_pointer}"
            )
            return

        self.log("Д1: буфер полностью заполнен")

        rejected = self.buffer.replace_oldest(
            request, current_time
        )

        self.statistics.record_rejected(rejected)
        self.statistics.record_buffered(request)

        new_pointer = self.buffer.get_insertion_pointer()
        index = (new_pointer - 1) % self.buffer.capacity

        self.log(
            f"Д1ОО3: самая старая заявка "
            f"№{rejected.request_number} отправлена в отказ"
        )

        self.log(
            f"Заявка №{request.request_number} "
            f"помещена в ячейку {index}"
        )

        self.log(
            f"Указатель постановки: "
            f"{old_pointer} -> {new_pointer}"
        )
