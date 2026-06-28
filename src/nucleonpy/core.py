# src/nucleonpy/core.py
from .data import get_isotope_info
from .calculus import calculate_remaining_activity

class Isotope:
    def __init__(self, name: str):
        self.name = name
        info = get_isotope_info(name)
        
        if "error" in info:
            raise ValueError(info["error"])
            
        self.half_life = info["half_life_seconds"]
        self.decay_mode = info["decay_mode"]
        self.atomic_number = info["atomic_number"]

    def get_remaining_activity(self, initial_amount: float, time_elapsed: float) -> float:
        """Calcula a atividade restante para este isótopo específico."""
        return calculate_remaining_activity(initial_amount, self.half_life, time_elapsed)

    def __repr__(self):
        return f"<Isotope: {self.name} | Half-life: {self.half_life:.2e}s>"