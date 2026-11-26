class SummaryReport:
    def __init__(self, summary, masters, total_time, source_id=1):
        self.summary = summary
        self.masters = masters
        self.total_time = total_time
        self.source_id = source_id

    def print_report(self):
        print("\n=== РЕЗУЛЬТАТЫ МОДЕЛИРОВАНИЯ ===")
        print(f"Общее время моделирования: {self.total_time:.2f}")

        self.print_source_table()
        self.print_master_table()

    def print_source_table(self):
        data = self.summary

        print("\nТаблица 1. Характеристики источников")
        print("-" * 100)

        print(
            f"{'Источник':>8} | "
            f"{'N':>8} | "
            f"{'Pотк, %':>8} | "
            f"{'Tпреб':>10} | "
            f"{'TБП':>10} | "
            f"{'Tобсл':>10} | "
            f"{'DБП':>10} | "
            f"{'Dобсл':>10}"
        )

        print("-" * 100)

        print(
            f"{self.source_id:>8} | "
            f"{data['generated']:>8} | "
            f"{data['rejection_probability'] * 100:>8.2f} | "
            f"{data['average_system']:>10.2f} | "
            f"{data['average_waiting']:>10.2f} | "
            f"{data['average_service']:>10.2f} | "
            f"{data['variance_waiting']:>10.2f} | "
            f"{data['variance_service']:>10.2f}"
        )

        print("-" * 100)
        print(f"Обслужено заявок: {data['completed']}")
        print(f"Отказов: {data['rejected']}")

    def print_master_table(self):
        print("\nТаблица 2. Характеристики приборов")
        print("-" * 66)

        print(
            f"{'Мастер':>8} | "
            f"{'Обслужено':>12} | "
            f"{'Время работы':>14} | "
            f"{'Kисп, %':>12}"
        )

        print("-" * 66)

        for master in self.masters:
            utilization = (
                master.busy_time / self.total_time
                if self.total_time > 0
                else 0.0
            )

            print(
                f"{master.id:>8} | "
                f"{master.completed_count:>12} | "
                f"{master.busy_time:>14.2f} | "
                f"{utilization * 100:>12.2f}"
            )

        print("-" * 66)