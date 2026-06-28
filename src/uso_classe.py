# src/uso_classe.py
from nucleonpy import Isotope

cobalto = Isotope("Co-60")

print(f"Dados do Isótopo: {cobalto}")
print(f"Número atômico: {cobalto.atomic_number}")

resultado = cobalto.get_remaining_activity(initial_amount=1000, time_elapsed=157680000)

print(f"Atividade após 5 anos: {resultado:.2f} Bq")