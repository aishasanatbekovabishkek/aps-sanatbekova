import math

from .simulation import Simulation


def calculate_required_requests(probability):
    if probability <= 0:
        return None

    t_alpha = 1.643
    delta = 0.1

    required = (
        t_alpha ** 2 * (1 - probability)
        / (probability * delta ** 2)
    )

    return max(1, math.ceil(required))


def run_with_accuracy(
    buffer_capacity=2,
    master_count=2,
    min_interval=1.0,
    max_interval=3.0,
    mean_service_time=5.0,
    initial_requests=100,
    request_limit=200000,
):
    request_count = initial_requests
    previous_probability = None
    iteration = 1

    print("\n=== ПОДБОР КОЛИЧЕСТВА ЗАЯВОК ===")
    print("Относительная точность: 10%")
    print("Доверительная вероятность: 0.9")

    while True:
        simulation = Simulation(
            max_requests=request_count,
            buffer_capacity=buffer_capacity,
            master_count=master_count,
            min_interval=min_interval,
            max_interval=max_interval,
            mean_service_time=mean_service_time,
        )

        summary = simulation.run_automatic_mode()

        probability = summary["rejection_probability"]

        required = calculate_required_requests(probability)

        print(f"\nИтерация {iteration}")
        print(f"Количество заявок: {request_count}")
        print(f"Вероятность отказа: {probability:.4%}")

        if required is not None:
            print(f"Необходимое количество заявок: {required}")
        else:
            print("Отказов нет. Увеличиваем количество заявок.")

        if (
            previous_probability is not None
            and previous_probability > 0
            and probability > 0
        ):
            relative_difference = (
                abs(probability - previous_probability)
                / previous_probability
            )

            print(
                f"Относительное изменение: "
                f"{relative_difference:.2%}"
            )

            if (
                relative_difference <= 0.1
                and request_count >= required
            ):
                print("\nУсловия расчёта выполнены.")
                return simulation

        if request_count >= request_limit:
            print(
                "\nДостигнут предел количества заявок. "
                "Требуемая точность не подтверждена."
            )
            return simulation

        previous_probability = probability

        if required is None:
            request_count *= 2
        else:
            request_count = max(
                required,
                request_count * 2,
            )

        request_count = min(request_count, request_limit)

        iteration += 1
