# src/nucleonpy/viz.py

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from .calculus import calculate_bateman_chain


def plot_decay_chain(
    initial_amount: float,
    half_lives_seconds: list[float],
    time_max_seconds: float,
    num_points: int = 500,
    show: bool = False,
) -> tuple[Figure, Axes]:
    """
    Gera um gráfico para uma cadeia de decaimento radioativo.

    Args:
        initial_amount: Quantidade, atividade ou número inicial de átomos.
        half_lives_seconds: Meias-vidas em segundos para cada isótopo da cadeia.
            Use float("inf") para isótopos estáveis.
        time_max_seconds: Tempo máximo da simulação, em segundos.
        num_points: Número de pontos usados no gráfico.
        show: Define se o gráfico deve ser exibido imediatamente.

    Returns:
        Uma tupla contendo a figura e os eixos do Matplotlib.
    """
    if initial_amount < 0:
        raise ValueError("A quantidade inicial deve ser maior ou igual a zero.")

    if time_max_seconds <= 0:
        raise ValueError("O tempo máximo deve ser maior que zero.")

    if num_points < 2:
        raise ValueError("O número de pontos deve ser pelo menos 2.")

    if not half_lives_seconds:
        raise ValueError("Informe pelo menos uma meia-vida.")

    t_array = np.linspace(0, time_max_seconds, num_points)

    num_isotopes = len(half_lives_seconds)
    results_matrix = np.zeros((num_isotopes, num_points))

    for i, tempo in enumerate(t_array):
        resultados = calculate_bateman_chain(
            initial_amount=initial_amount,
            half_lives_seconds=half_lives_seconds,
            time_elapsed_seconds=float(tempo),
        )

        for j, quantidade in enumerate(resultados):
            results_matrix[j, i] = quantidade

    fig, ax = plt.subplots(figsize=(10, 6))

    labels = [f"Geração {i + 1}" for i in range(num_isotopes)]

    if half_lives_seconds[-1] == float("inf"):
        labels[-1] = "Produto final estável"

    for j, label in enumerate(labels):
        ax.plot(
            t_array,
            results_matrix[j, :],
            linewidth=2.5,
            label=label,
        )

    ax.set_xlabel("Tempo (segundos)", fontsize=12, fontweight="bold")
    ax.set_ylabel("Quantidade / Atividade", fontsize=12, fontweight="bold")
    ax.set_title(
        "Evolução da cadeia de decaimento radioativo",
        fontsize=14,
        fontweight="bold",
    )
    ax.grid(True, linestyle="--", alpha=0.7)
    ax.legend(fontsize=11)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()

    if show:
        plt.show()

    return fig, ax