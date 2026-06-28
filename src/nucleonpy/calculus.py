# src/nucleonpy/calculus.py
import math

def calculate_remaining_activity(initial_amount: float, half_life_seconds: float, time_elapsed_seconds: float) -> float:
    """
    Calculates the remaining amount or activity of a radioactive isotope after a given time.

    Args:
        initial_amount (float): The initial quantity of the substance (e.g., mass, activity, or number of atoms).
        half_life_seconds (float): The half-life of the isotope in seconds. Must be strictly positive.
        time_elapsed_seconds (float): The time elapsed in seconds.

    Returns:
        float: The remaining amount of the substance after the elapsed time.

    Raises:
        ValueError: If half_life_seconds is less than or equal to zero.
    """
    if half_life_seconds <= 0:
        raise ValueError("Half-life must be a positive, non-zero value.")

    decay_constant = math.log(2) / half_life_seconds
    
    remaining_amount = initial_amount * math.exp(-decay_constant * time_elapsed_seconds)
    
    return remaining_amount

def calculate_bateman_chain(initial_amount: float, half_lives_seconds: list[float], time_elapsed_seconds: float) -> list[float]:
    """
    Solves the Bateman equations for a linear decay chain (A -> B -> C -> ...).

    Args:
        initial_amount (float): Initial quantity of the parent isotope.
        half_lives_seconds (list[float]): A list of half-lives in seconds for each isotope in the chain.
                                          Use float('inf') for the final stable isotope.
        time_elapsed_seconds (float): The time elapsed in seconds.

    Returns:
        list[float]: The remaining amount of each isotope in the chain at the given time.
    """
    lambdas = []
    for hl in half_lives_seconds:
        if hl > 0 and hl != float('inf'):
            lambdas.append(math.log(2) / hl)
        else:
            lambdas.append(0.0) 

    n_elements = len(lambdas)
    results = [0.0] * n_elements

    for n in range(n_elements):
        if n == 0:
            results[n] = initial_amount * math.exp(-lambdas[0] * time_elapsed_seconds)
            continue

        amount_n = 0.0
        for i in range(n + 1):
            denominator = 1.0
            for j in range(n + 1):
                if i != j:
                    denominator *= (lambdas[j] - lambdas[i])

            if denominator != 0: 
                amount_n += math.exp(-lambdas[i] * time_elapsed_seconds) / denominator

        prod_lambdas = 1.0
        for i in range(n):
            prod_lambdas *= lambdas[i]

        results[n] = initial_amount * prod_lambdas * amount_n

    return results