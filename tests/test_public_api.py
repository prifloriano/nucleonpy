import nucleonpy


def test_public_api_exports_expected_objects():
    assert hasattr(nucleonpy, "Isotope")
    assert hasattr(nucleonpy, "calculate_remaining_activity")
    assert hasattr(nucleonpy, "calculate_bateman_chain")
    assert hasattr(nucleonpy, "get_isotope_info")
    assert hasattr(nucleonpy, "plot_decay_chain")


def test_version_is_defined():
    assert nucleonpy.__version__ == "0.1.0"


def test_all_exports_are_available():
    for name in nucleonpy.__all__:
        assert hasattr(nucleonpy, name)
