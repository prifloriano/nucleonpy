import math

import pytest

from nucleonpy import Isotope


def test_isotope_loads_known_radioactive_isotope():
    isotope = Isotope("H-3")

    assert isotope.name == "H-3"
    assert isotope.atomic_number == 1
    assert isotope.decay_mode == "B-"
    assert isotope.half_life > 0
    assert not isotope.is_stable
    assert isotope.decay_constant > 0


def test_isotope_loads_known_stable_isotope():
    isotope = Isotope("H-1")

    assert isotope.name == "H-1"
    assert isotope.atomic_number == 1
    assert isotope.is_stable
    assert math.isinf(isotope.half_life)
    assert isotope.decay_constant == 0.0


def test_isotope_rejects_unknown_isotope():
    with pytest.raises(ValueError):
        Isotope("Xx-999")


def test_isotope_rejects_empty_name():
    with pytest.raises(ValueError):
        Isotope("")


def test_isotope_calculates_remaining_activity():
    isotope = Isotope("H-3")

    result = isotope.get_remaining_activity(
        initial_amount=100.0,
        time_elapsed=0.0,
    )

    assert result == pytest.approx(100.0)


def test_isotope_accepts_lowercase_name():
    isotope = Isotope("h-3")

    assert isotope.name == "H-3"


def test_isotope_accepts_name_without_hyphen():
    isotope = Isotope("co60")

    assert isotope.name == "Co-60"
