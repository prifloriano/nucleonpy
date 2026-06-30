# src/nucleonpy/export.py

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from .calculus import calculate_bateman_chain


def generate_decay_chain_series(
    initial_amount: float,
    half_lives_seconds: list[float],
    time_max_seconds: float,
    num_points: int = 500,
) -> list[dict[str, float]]:
    """
    Gera uma série temporal para uma cadeia de decaimento radioativo.
    """
    if time_max_seconds <= 0:
        raise ValueError("O tempo máximo deve ser maior que zero.")

    if num_points < 2:
        raise ValueError("O número de pontos deve ser pelo menos 2.")

    step = time_max_seconds / (num_points - 1)
    series = []

    for index in range(num_points):
        time_seconds = step * index
        amounts = calculate_bateman_chain(
            initial_amount=initial_amount,
            half_lives_seconds=half_lives_seconds,
            time_elapsed_seconds=time_seconds,
        )

        row = {"time_seconds": time_seconds}

        for isotope_index, amount in enumerate(amounts, start=1):
            row[f"isotope_{isotope_index}"] = amount

        series.append(row)

    return series


def export_decay_chain_to_csv(
    path: str | Path,
    initial_amount: float,
    half_lives_seconds: list[float],
    time_max_seconds: float,
    num_points: int = 500,
) -> Path:
    """
    Exporta uma cadeia de decaimento para CSV.
    """
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    series = generate_decay_chain_series(
        initial_amount=initial_amount,
        half_lives_seconds=half_lives_seconds,
        time_max_seconds=time_max_seconds,
        num_points=num_points,
    )

    fieldnames = list(series[0].keys())

    with output_path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(series)

    return output_path


def export_decay_chain_to_json(
    path: str | Path,
    initial_amount: float,
    half_lives_seconds: list[float],
    time_max_seconds: float,
    num_points: int = 500,
) -> Path:
    """
    Exporta uma cadeia de decaimento para JSON.
    """
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    payload: dict[str, Any] = {
        "initial_amount": initial_amount,
        "half_lives_seconds": half_lives_seconds,
        "time_max_seconds": time_max_seconds,
        "num_points": num_points,
        "series": generate_decay_chain_series(
            initial_amount=initial_amount,
            half_lives_seconds=half_lives_seconds,
            time_max_seconds=time_max_seconds,
            num_points=num_points,
        ),
    }

    with output_path.open("w", encoding="utf-8") as json_file:
        json.dump(payload, json_file, indent=4, ensure_ascii=False)

    return output_path
