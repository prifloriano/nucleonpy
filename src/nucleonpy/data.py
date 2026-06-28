# src/nucleonpy/data.py
import json
import os

def _load_database() -> dict:
    """Carrega o banco de dados de isótopos a partir do arquivo JSON interno."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, "isotopes.json")
    
    try:
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            
            for isotope, properties in data.items():
                if properties.get("half_life_seconds") == "Infinity":
                    properties["half_life_seconds"] = float('inf')
                    
            return data
    except FileNotFoundError:
        return {}

ISOTOPE_DATABASE = _load_database()

def get_isotope_info(name: str) -> dict:
    """
    Fetches basic properties of an isotope from the internal database.

    Args:
        name (str): The common name of the isotope (e.g., 'Co-60').

    Returns:
        dict: A dictionary containing half-life, decay mode, etc. 
              Returns an error dictionary if the isotope is not found.
    """
    return ISOTOPE_DATABASE.get(name, {"error": f"Isotope '{name}' not found in the database."})