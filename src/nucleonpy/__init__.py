# src/nucleonpy/__init__.py

from .data import get_isotope_info
from .calculus import calculate_remaining_activity, calculate_bateman_chain
from .viz import plot_decay_chain
from .core import Isotope 

__version__ = "0.1.0"