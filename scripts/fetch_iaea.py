# scripts/fetch_iaea.py

from __future__ import annotations

import csv
import json
from datetime import UTC, datetime
from io import StringIO
from pathlib import Path

import requests


IAEA_URL = "https://www-nds.iaea.org/relnsd/v0/data?fields=ground_states&nuclides=all"

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_OUTPUT_PATH = PROJECT_ROOT / "src" / "nucleonpy" / "isotopes.json"
METADATA_OUTPUT_PATH = PROJECT_ROOT / "src" / "nucleonpy" / "isotopes_metadata.json"


def parse_half_life(value: str | None) -> float | None:
    """
    Converte a meia-vida retornada pela IAEA para float.

    Retorna None quando o valor não estiver disponível, vazio ou não for numérico.
    No JSON, None será salvo como null.
    """
    if value is None:
        return None

    value = value.strip()

    if not value:
        return None

    try:
        return float(value)
    except ValueError:
        return None


def build_metadata(total_isotopes: int) -> dict[str, object]:
    """
    Gera metadados sobre a origem da base interna.
    """
    return {
        "source_name": "IAEA LiveChart of Nuclides",
        "source_url": IAEA_URL,
        "fields": "ground_states",
        "nuclides": "all",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "total_isotopes": total_isotopes,
        "half_life_unit": "seconds",
        "stable_or_unknown_half_life_value": None,
        "notes": (
            "Valores null em half_life_seconds representam isótopos estáveis "
            "ou registros sem meia-vida numérica disponível na fonte."
        ),
    }


def fetch_and_build_database() -> None:
    print("Buscando dados na API da IAEA...")

    try:
        response = requests.get(IAEA_URL, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as error:
        print(f"Erro ao buscar dados da IAEA: {error}")
        return

    csv_data = StringIO(response.text)
    reader = csv.DictReader(csv_data)

    isotopes_db: dict[str, dict[str, object]] = {}

    print("Formatando dados nucleares...")

    for row in reader:
        symbol = row.get("symbol")
        z_str = row.get("z")
        n_str = row.get("n")
        half_life_sec = row.get("half_life_sec")
        decay_mode = row.get("decay_1")

        if not symbol or not z_str or not n_str:
            continue

        try:
            atomic_number = int(z_str)
            neutrons = int(n_str)
        except ValueError:
            continue

        symbol = symbol.strip().capitalize()
        mass_number = atomic_number + neutrons
        isotope_name = f"{symbol}-{mass_number}"

        isotopes_db[isotope_name] = {
            "symbol": symbol,
            "atomic_number": atomic_number,
            "neutrons": neutrons,
            "mass_number": mass_number,
            "half_life_seconds": parse_half_life(half_life_sec),
            "decay_mode": decay_mode.strip()
            if decay_mode and decay_mode.strip()
            else "Stable",
        }

    metadata = build_metadata(total_isotopes=len(isotopes_db))

    DATA_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with DATA_OUTPUT_PATH.open("w", encoding="utf-8") as json_file:
        json.dump(
            isotopes_db,
            json_file,
            indent=4,
            ensure_ascii=False,
        )

    with METADATA_OUTPUT_PATH.open("w", encoding="utf-8") as json_file:
        json.dump(
            metadata,
            json_file,
            indent=4,
            ensure_ascii=False,
        )

    print(f"Banco atualizado com {len(isotopes_db)} isótopos.")
    print(f"Dados salvos em: {DATA_OUTPUT_PATH}")
    print(f"Metadados salvos em: {METADATA_OUTPUT_PATH}")


if __name__ == "__main__":
    fetch_and_build_database()
