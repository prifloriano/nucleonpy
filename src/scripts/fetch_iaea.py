# scripts/fetch_iaea.py
import requests
import csv
import json
import os
from io import StringIO

def fetch_and_build_database():
    print("Buscando dados na API da IAEA... (Isso pode levar uns segundos...)")
    
    url = "https://www-nds.iaea.org/relnsd/v0/data?fields=ground_states&nuclides=all"
    
    try:
        response = requests.get(url)
        response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        print(f"Deu ruim na conexão, guria: {e}")
        return

    csv_data = StringIO(response.text)
    reader = csv.DictReader(csv_data)

    isotopes_db = {}
    count = 0

    print("Calculando a massa e formatando os dados...")
    for row in reader:
        symbol = row.get("symbol")
        z_str = row.get("z")
        n_str = row.get("n")
        half_life_sec = row.get("half_life_sec")
        decay_mode = row.get("decay_1")

        if symbol and z_str and n_str:
            try:
                atomic_number = int(z_str)
                neutrons = int(n_str)
                mass_number = atomic_number + neutrons
                
                isotope_name = f"{symbol.strip().capitalize()}-{mass_number}"
                
                if half_life_sec and half_life_sec.strip() and half_life_sec.replace('.', '', 1).replace('E', '', 1).isdigit():
                    hl_float = float(half_life_sec)
                else:
                    hl_float = "Infinity" 

                isotopes_db[isotope_name] = {
                    "atomic_number": atomic_number,
                    "half_life_seconds": hl_float,
                    "decay_mode": decay_mode.strip() if decay_mode else "Stable"
                }
                count += 1
            except ValueError:
                continue 

    current_dir = os.getcwd()
    output_path = os.path.join(current_dir, "nucleonpy", "isotopes.json")

    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(isotopes_db, json_file, indent=4)

    print(f"Massa demais! O banco foi atualizado com {count} isótopos reais.")
    print(f"Arquivo salvo em: {output_path}")

if __name__ == "__main__":
    fetch_and_build_database()