# src/nucleonpy/data.py

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any
import re


DATABASE_PATH = Path(__file__).parent / "isotopes.json"


def _normalize_half_life(value: Any) -> float:
    """
    Normaliza o valor de meia-vida vindo da base interna.

    A base pode representar isótopos estáveis como:
    - Infinity
    - "Infinity"
    - "inf"
    - None
    - "stable"
    """
    if value is None:
        return math.inf

    if isinstance(value, str):
        normalized_value = value.strip().lower()

        if normalized_value in {"infinity", "inf", "stable"}:
            return math.inf

        return float(value)

    if isinstance(value, int | float):
        if math.isinf(value):
            return math.inf

        return float(value)

    raise ValueError(f"Valor inválido de meia-vida: {value!r}")


def _normalize_isotope_data(
    data: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    normalized_data = {}

    for isotope_name, properties in data.items():
        normalized_properties = properties.copy()

        normalized_properties["half_life_seconds"] = _normalize_half_life(
            normalized_properties.get("half_life_seconds")
        )

        normalized_data[isotope_name] = normalized_properties

    return normalized_data


def _load_database() -> dict[str, dict[str, Any]]:
    """Carrega o banco interno de isótopos."""
    try:
        with DATABASE_PATH.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return _normalize_isotope_data(data)

    except FileNotFoundError:
        return {}


ISOTOPE_DATABASE = _load_database()


def get_isotope_info(name: str) -> dict[str, Any]:
    """
    Busca informações básicas de um isótopo na base interna.

    Args:
        name: Nome do isótopo, por exemplo "Co-60".

    Returns:
        Dicionário com meia-vida, modo de decaimento e número atômico.
        Caso o isótopo não exista, retorna um dicionário com a chave "error".
    """
    try:
        isotope_name = normalize_isotope_name(name)
    except ValueError as error:
        return {"error": str(error)}

    return ISOTOPE_DATABASE.get(
        isotope_name,
        {"error": f"Isótopo '{isotope_name}' não encontrado na base de dados."},
    )


def normalize_element_symbol(symbol: str) -> str:
    """
    Normaliza o símbolo químico para o formato usado na base interna.

    Exemplos:
        "co" -> "Co"
        "CO" -> "Co"
        " h " -> "H"
    """
    normalized_symbol = symbol.strip()

    if not normalized_symbol:
        raise ValueError("O símbolo químico não pode ser vazio.")

    if not normalized_symbol.isalpha():
        raise ValueError("O símbolo químico deve conter apenas letras.")

    return normalized_symbol.capitalize()


def list_isotopes() -> list[str]:
    """
    Lista todos os isótopos disponíveis na base interna.
    """
    return sorted(ISOTOPE_DATABASE.keys())


def get_isotopes_by_symbol(symbol: str) -> dict[str, dict[str, Any]]:
    """
    Busca isótopos pelo símbolo químico.

    Exemplo:
        get_isotopes_by_symbol("Co")
    """
    normalized_symbol = normalize_element_symbol(symbol)

    return {
        isotope_name: properties
        for isotope_name, properties in ISOTOPE_DATABASE.items()
        if properties.get("symbol", isotope_name.split("-")[0]) == normalized_symbol
    }


def get_stable_isotopes() -> dict[str, dict[str, Any]]:
    """
    Retorna isótopos estáveis ou sem meia-vida numérica disponível.
    """
    return {
        isotope_name: properties
        for isotope_name, properties in ISOTOPE_DATABASE.items()
        if math.isinf(properties["half_life_seconds"])
    }


def get_radioactive_isotopes() -> dict[str, dict[str, Any]]:
    """
    Retorna isótopos radioativos com meia-vida numérica disponível.
    """
    return {
        isotope_name: properties
        for isotope_name, properties in ISOTOPE_DATABASE.items()
        if not math.isinf(properties["half_life_seconds"])
    }


def get_isotopes_by_decay_mode(decay_mode: str) -> dict[str, dict[str, Any]]:
    """
    Busca isótopos pelo modo de decaimento.

    Exemplo:
        get_isotopes_by_decay_mode("B-")
    """
    normalized_decay_mode = decay_mode.strip().lower()

    if not normalized_decay_mode:
        raise ValueError("O modo de decaimento não pode ser vazio.")

    return {
        isotope_name: properties
        for isotope_name, properties in ISOTOPE_DATABASE.items()
        if str(properties.get("decay_mode", "")).strip().lower()
        == normalized_decay_mode
    }


def normalize_isotope_name(name: str) -> str:
    """
    Normaliza o nome de um isótopo para o formato usado na base interna.

    Exemplos:
        "h-3" -> "H-3"
        " H-3 " -> "H-3"
        "co60" -> "Co-60"
        "CO-60" -> "Co-60"
    """
    normalized_name = name.strip().replace(" ", "")

    if not normalized_name:
        raise ValueError("O nome do isótopo não pode ser vazio.")

    match = re.fullmatch(r"([A-Za-z]+)-?(\d+)", normalized_name)

    if not match:
        raise ValueError(
            "Nome de isótopo inválido. Use formatos como 'H-3', 'Co-60' ou 'U-238'."
        )

    symbol, mass_number = match.groups()
    symbol = symbol.capitalize()

    return f"{symbol}-{mass_number}"
