# src/nucleonpy/core.py

from __future__ import annotations

import math
from typing import Any

from .calculus import calculate_remaining_activity
from .data import get_isotope_info, normalize_isotope_name


class Isotope:
    """
    Representa um isótopo carregado a partir da base interna do nucleonpy.
    """

    def __init__(self, name: str):
        normalized_name = normalize_isotope_name(name)
        info = get_isotope_info(normalized_name)

        if "error" in info:
            raise ValueError(info["error"])

        self.name = normalized_name
        self.symbol = self._get_optional_value(info, "symbol")
        self.atomic_number = int(info["atomic_number"])
        self.neutrons = self._get_optional_value(info, "neutrons")
        self.mass_number = self._get_optional_value(info, "mass_number")
        self.half_life = float(info["half_life_seconds"])
        self.decay_mode = str(info["decay_mode"])

    @staticmethod
    def _get_optional_value(info: dict[str, Any], key: str) -> Any:
        return info.get(key)

    @property
    def is_stable(self) -> bool:
        """
        Indica se o isótopo é estável.
        """
        return math.isinf(self.half_life) or self.decay_mode.lower() == "stable"

    @property
    def decay_constant(self) -> float:
        """
        Retorna a constante de decaimento do isótopo.

        Para isótopos estáveis, retorna 0.0.
        """
        if self.is_stable:
            return 0.0

        return math.log(2) / self.half_life

    def get_remaining_activity(
        self,
        initial_amount: float,
        time_elapsed: float,
    ) -> float:
        """
        Calcula a quantidade ou atividade restante para este isótopo.
        """
        return calculate_remaining_activity(
            initial_amount=initial_amount,
            half_life_seconds=self.half_life,
            time_elapsed_seconds=time_elapsed,
        )

    def __repr__(self) -> str:
        stability = "estável" if self.is_stable else f"meia-vida={self.half_life:.2e}s"

        return f"<Isotope {self.name}: Z={self.atomic_number}, {stability}>"
