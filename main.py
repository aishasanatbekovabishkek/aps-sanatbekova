
from src.simulation import Simulation


def main():
    simulation = Simulation(
        max_requests=10,
        buffer_capacity=2,
        master_count=1,
        min_interval=1.0,
        max_interval=3.0,
        mean_service_time=5.0,
    )

    simulation.run_step_mode()


if __name__ == "__main__":
    main()
