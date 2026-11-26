import math
import random

from src.simulation import Simulation
from src.automatic_runner import run_with_accuracy


def read_int(message, default, minimum=1):
    while True:
        value = input(f"{message} [{default}]: ").strip()

        try:
            result = int(value) if value else default

            if result >= minimum:
                return result

            print(f"Значение должно быть не меньше {minimum}.")

        except ValueError:
            print("Введите целое число.")


def read_float(message, default):
    while True:
        value = input(f"{message} [{default}]: ").strip()

        try:
            result = float(value.replace(",", ".")) if value else default

            if math.isfinite(result) and result > 0:
                return result

            print("Введите положительное конечное число.")

        except ValueError:
            print("Введите число.")


def read_seed():
    while True:
        value = input("Seed (Enter - случайный): ").strip()

        if not value:
            return None

        try:
            return int(value)
        except ValueError:
            print("Seed должен быть целым числом.")


def main():
    while True:
        print("\n=== СМО. СЕРВИСНЫЙ ЦЕНТР ===")
        print("Вариант №16")
        print("\n1 - Пошаговый режим (ОД1)")
        print("2 - Автоматический режим (ОР1)")
        print("0 - Выход")

        mode = input("\nВыберите режим: ").strip()

        if mode == "0":
            print("Программа завершена.")
            break

        if mode not in ("1", "2"):
            print("Некорректный режим.")
            continue

        print("\n=== ВХОДНЫЕ ПАРАМЕТРЫ ===")

        master_count = read_int(
            "Количество мастеров", 2
        )

        buffer_capacity = read_int(
            "Размер буфера", 2
        )

        while True:
            min_interval = read_float(
                "Минимальный интервал", 1.0
            )

            max_interval = read_float(
                "Максимальный интервал", 3.0
            )

            if min_interval <= max_interval:
                break

            print(
                "Максимальный интервал не может "
                "быть меньше минимального."
            )

        mean_service_time = read_float(
            "Среднее время ремонта", 5.0
        )

        if mode == "1":
            max_requests = read_int(
                "Количество заявок", 10
            )
        else:
            initial_requests = read_int(
                "Начальное количество заявок", 100
            )

        seed = read_seed()
        random.seed(seed)

        if mode == "1":
            simulation = Simulation(
                max_requests=max_requests,
                buffer_capacity=buffer_capacity,
                master_count=master_count,
                min_interval=min_interval,
                max_interval=max_interval,
                mean_service_time=mean_service_time,
            )

            simulation.run_step_mode()

        else:
            simulation = run_with_accuracy(
                buffer_capacity=buffer_capacity,
                master_count=master_count,
                min_interval=min_interval,
                max_interval=max_interval,
                mean_service_time=mean_service_time,
                initial_requests=initial_requests,
            )

            simulation.show_summary()


if __name__ == "__main__":
    main()
