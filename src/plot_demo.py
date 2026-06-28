# src/plot_demo.py
import nucleonpy

nucleonpy.plot_decay_chain(
    initial_amount=100.0, 
    half_lives_seconds=[5.0, 10.0, float('inf')], 
    time_max_seconds=50.0
)