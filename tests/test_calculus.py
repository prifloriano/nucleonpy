import math

import pytest

from nucleonpy import (
    Isotope,
    calculate_bateman_chain,
    calculate_remaining_activity,
)


def test_remaining_activity_after_one_half_life():
    result = calculate_remaining_activity(
        initial_amount=100.0,
        half_life_seconds=10.0,
        time_elapsed_seconds=10.0,
    )

    assert result == pytest.approx(50.0)


def test_remaining_activity_after_zero_time():
    result = calculate_remaining_activity(
        initial_amount=100.0,
        half_life_seconds=10.0,
        time_elapsed_seconds=0.0,
    )

    assert result == pytest.approx(100.0)


def test_remaining_activity_rejects_zero_half_life():
    with pytest.raises(ValueError):
        calculate_remaining_activity(
            initial_amount=100.0,
            half_life_seconds=0.0,
            time_elapsed_seconds=10.0,
        )


def test_remaining_activity_handles_stable_isotope():
    result = calculate_remaining_activity(
        initial_amount=100.0,
        half_life_seconds=math.inf,
        time_elapsed_seconds=1000.0,
    )

    assert result == pytest.approx(100.0)


def test_bateman_chain_initial_state():
    result = calculate_bateman_chain(
        initial_amount=100.0,
        half_lives_seconds=[5.0, 10.0, math.inf],
        time_elapsed_seconds=0.0,
    )

    assert result == pytest.approx([100.0, 0.0, 0.0])


def test_bateman_chain_conserves_total_amount():
    result = calculate_bateman_chain(
        initial_amount=100.0,
        half_lives_seconds=[5.0, 10.0, math.inf],
        time_elapsed_seconds=20.0,
    )

    assert sum(result) == pytest.approx(100.0)


def test_isotope_loads_known_isotope():
    isotope = Isotope("H-3")

    assert isotope.name == "H-3"
    assert isotope.atomic_number == 1
    assert isotope.decay_mode == "B-"
    assert isotope.half_life > 0


def test_remaining_activity_rejects_negative_initial_amount():
    with pytest.raises(ValueError):
        calculate_remaining_activity(
            initial_amount=-1.0,
            half_life_seconds=10.0,
            time_elapsed_seconds=5.0,
        )


def test_remaining_activity_rejects_negative_elapsed_time():
    with pytest.raises(ValueError):
        calculate_remaining_activity(
            initial_amount=100.0,
            half_life_seconds=10.0,
            time_elapsed_seconds=-5.0,
        )


def test_bateman_chain_rejects_empty_half_lives():
    with pytest.raises(ValueError):
        calculate_bateman_chain(
            initial_amount=100.0,
            half_lives_seconds=[],
            time_elapsed_seconds=10.0,
        )


def test_bateman_chain_rejects_stable_isotope_before_end():
    with pytest.raises(ValueError):
        calculate_bateman_chain(
            initial_amount=100.0,
            half_lives_seconds=[math.inf, 10.0],
            time_elapsed_seconds=10.0,
        )


def test_bateman_chain_rejects_equal_half_lives():
    with pytest.raises(ValueError):
        calculate_bateman_chain(
            initial_amount=100.0,
            half_lives_seconds=[10.0, 10.0, math.inf],
            time_elapsed_seconds=10.0,
        )
