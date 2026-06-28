# tests/test_nucleonpy.py
import pytest
from nucleonpy import calculate_remaining_activity

def test_decay_simple():
    # Se tenho 100g e a meia-vida é de 10s, após 10s eu devo ter 50g
    initial = 100.0
    hl = 10.0
    time = 10.0
    
    result = calculate_remaining_activity(initial, hl, time)
    
    # Confiro se o resultado está dentro de uma margem de erro
    assert result == pytest.approx(50.0)

def test_decay_error():
    # Verifica se a biblioteca reclama se alguém colocar meia-vida negativa
    with pytest.raises(ValueError):
        calculate_remaining_activity(100, -5, 10)