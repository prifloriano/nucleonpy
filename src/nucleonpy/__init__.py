# src/nucleonpy/__init__.py

from .calculus import calculate_bateman_chain, calculate_remaining_activity
from .core import Isotope
from .data import (
    get_isotope_info,
    get_isotopes_by_decay_mode,
    get_isotopes_by_symbol,
    get_radioactive_isotopes,
    get_stable_isotopes,
    list_isotopes,
)
from .export import (
    export_decay_chain_to_csv,
    export_decay_chain_to_json,
    generate_decay_chain_series,
)
from .viz import plot_decay_chain

__version__ = "0.1.0"

__all__ = [
    "Isotope",
    "calculate_bateman_chain",
    "calculate_remaining_activity",
    "export_decay_chain_to_csv",
    "export_decay_chain_to_json",
    "generate_decay_chain_series",
    "get_isotope_info",
    "get_isotopes_by_decay_mode",
    "get_isotopes_by_symbol",
    "get_radioactive_isotopes",
    "get_stable_isotopes",
    "list_isotopes",
    "plot_decay_chain",
    "__version__",
]
