import math

import pytest

from nucleonpy.data import (
    get_isotope_info,
    get_isotopes_by_decay_mode,
    get_isotopes_by_symbol,
    get_radioactive_isotopes,
    get_stable_isotopes,
    list_isotopes,
    normalize_element_symbol,
    normalize_isotope_name,
)


def test_normalize_isotope_name_with_lowercase():
    assert normalize_isotope_name("h-3") == "H-3"


def test_normalize_isotope_name_with_spaces():
    assert normalize_isotope_name(" H-3 ") == "H-3"


def test_normalize_isotope_name_without_hyphen():
    assert normalize_isotope_name("co60") == "Co-60"


def test_normalize_isotope_name_with_uppercase_symbol():
    assert normalize_isotope_name("CO-60") == "Co-60"


def test_normalize_isotope_name_rejects_empty_string():
    with pytest.raises(ValueError):
        normalize_isotope_name("")


def test_get_isotope_info_accepts_normalized_variations():
    isotope = get_isotope_info("h3")

    assert isotope["atomic_number"] == 1
    assert isotope["decay_mode"] == "B-"
    assert isotope["half_life_seconds"] > 0
    assert not math.isinf(isotope["half_life_seconds"])


def test_normalize_element_symbol():
    assert normalize_element_symbol("co") == "Co"
    assert normalize_element_symbol(" CO ") == "Co"
    assert normalize_element_symbol("h") == "H"


def test_normalize_element_symbol_rejects_empty_value():
    with pytest.raises(ValueError):
        normalize_element_symbol("")


def test_list_isotopes_returns_known_isotope():
    isotopes = list_isotopes()

    assert "H-3" in isotopes


def test_get_isotopes_by_symbol_returns_hydrogen_isotopes():
    isotopes = get_isotopes_by_symbol("h")

    assert "H-1" in isotopes
    assert "H-3" in isotopes


def test_get_stable_isotopes_returns_known_stable_isotope():
    isotopes = get_stable_isotopes()

    assert "H-1" in isotopes


def test_get_radioactive_isotopes_returns_known_radioactive_isotope():
    isotopes = get_radioactive_isotopes()

    assert "H-3" in isotopes


def test_get_isotopes_by_decay_mode_returns_beta_minus_isotopes():
    isotopes = get_isotopes_by_decay_mode("B-")

    assert "H-3" in isotopes
