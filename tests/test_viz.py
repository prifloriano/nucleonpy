import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from nucleonpy import plot_decay_chain


def test_plot_decay_chain_returns_figure_and_axes():
    fig, ax = plot_decay_chain(
        initial_amount=100.0,
        half_lives_seconds=[5.0, 10.0, float("inf")],
        time_max_seconds=50.0,
    )

    assert isinstance(fig, Figure)
    assert isinstance(ax, Axes)
    assert len(ax.lines) == 3

    plt.close(fig)


def test_plot_decay_chain_rejects_negative_initial_amount():
    with pytest.raises(ValueError):
        plot_decay_chain(
            initial_amount=-1.0,
            half_lives_seconds=[5.0, 10.0, float("inf")],
            time_max_seconds=50.0,
        )


def test_plot_decay_chain_rejects_invalid_time_max():
    with pytest.raises(ValueError):
        plot_decay_chain(
            initial_amount=100.0,
            half_lives_seconds=[5.0, 10.0, float("inf")],
            time_max_seconds=0.0,
        )


def test_plot_decay_chain_rejects_invalid_num_points():
    with pytest.raises(ValueError):
        plot_decay_chain(
            initial_amount=100.0,
            half_lives_seconds=[5.0, 10.0, float("inf")],
            time_max_seconds=50.0,
            num_points=1,
        )


def test_plot_decay_chain_rejects_empty_half_lives():
    with pytest.raises(ValueError):
        plot_decay_chain(
            initial_amount=100.0,
            half_lives_seconds=[],
            time_max_seconds=50.0,
        )
