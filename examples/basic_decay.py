# src/basic_decay.py
import nucleonpy


def run_decay_simulation():
    isotope_name = "Co-60"
    print(f"--- Fetching data for {isotope_name} ---")

    isotope_info = nucleonpy.get_isotope_info(isotope_name)

    if "error" in isotope_info:
        print(f"Error: {isotope_info['error']}")
        return

    half_life = isotope_info["half_life_seconds"]
    decay_mode = isotope_info["decay_mode"]

    print(f"Isotope: {isotope_name}")
    print(f"Half-life: {half_life} seconds")
    print(f"Decay Mode: {decay_mode}")
    print("-" * 30)

    initial_activity = 1000.0
    five_years_in_seconds = 5 * 365 * 24 * 60 * 60

    remaining_activity = nucleonpy.calculate_remaining_activity(
        initial_amount=initial_activity,
        half_life_seconds=half_life,
        time_elapsed_seconds=five_years_in_seconds,
    )

    print("--- Simulation Results after 5 years ---")
    print(f"Initial Activity: {initial_activity:.2f} Bq")
    print(f"Remaining Activity: {remaining_activity:.2f} Bq")


if __name__ == "__main__":
    run_decay_simulation()
