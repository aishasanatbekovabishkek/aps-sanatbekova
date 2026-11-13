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
    ):
        self.buffer = buffer
        self.selection_dispatcher = selection_dispatcher
        self.statistics = statistics

    def handle_request(
        self, request: Request, current_time: float
    ) -> None:
        started = self.selection_dispatcher.try_start_service(
            request, current_time
        )

        if started:
            return

        result = self.buffer.put_by_ring(request, current_time)

        if result == BufferPutResult.STORED:
            self.statistics.record_buffered(request)
            return

        rejected = self.buffer.replace_oldest(request, current_time)

        self.statistics.record_rejected(rejected)
        self.statistics.record_buffered(request)
