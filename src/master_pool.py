from .master import Master


class MasterPool:
    def __init__(self, master_count: int, mean_service_time: float):
        if master_count <= 0:
            raise ValueError("Количество мастеров должно быть положительным")

        self.masters = [
            Master(master_id=i + 1, mean_service_time=mean_service_time)
            for i in range(master_count)
        ]

        self.selection_pointer = 0

    def has_free_master(self) -> bool:
        return any(master.is_free() for master in self.masters)

    def find_free_by_ring(self) -> Master | None:
        for offset in range(len(self.masters)):
            index = (self.selection_pointer + offset) % len(self.masters)

            master = self.masters[index]

            if master.is_free():
                self.selection_pointer = (index + 1) % len(self.masters)
                return master

        return None

    def get_masters(self) -> list[Master]:
        return self.masters

    def get_selection_pointer(self) -> int:
        return self.selection_pointer
