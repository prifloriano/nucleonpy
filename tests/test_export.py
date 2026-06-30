import csv
import json

from nucleonpy import (
    export_decay_chain_to_csv,
    export_decay_chain_to_json,
    generate_decay_chain_series,
)


def test_generate_decay_chain_series_returns_expected_points():
    series = generate_decay_chain_series(
        initial_amount=100.0,
        half_lives_seconds=[5.0, 10.0, float("inf")],
        time_max_seconds=10.0,
        num_points=3,
    )

    assert len(series) == 3
    assert series[0]["time_seconds"] == 0.0
    assert "isotope_1" in series[0]
    assert "isotope_2" in series[0]
    assert "isotope_3" in series[0]


def test_export_decay_chain_to_csv(tmp_path):
    output_path = tmp_path / "decay_chain.csv"

    result_path = export_decay_chain_to_csv(
        path=output_path,
        initial_amount=100.0,
        half_lives_seconds=[5.0, 10.0, float("inf")],
        time_max_seconds=10.0,
        num_points=3,
    )

    assert result_path == output_path
    assert output_path.exists()

    with output_path.open("r", encoding="utf-8") as csv_file:
        rows = list(csv.DictReader(csv_file))

    assert len(rows) == 3
    assert "time_seconds" in rows[0]
    assert "isotope_1" in rows[0]


def test_export_decay_chain_to_json(tmp_path):
    output_path = tmp_path / "decay_chain.json"

    result_path = export_decay_chain_to_json(
        path=output_path,
        initial_amount=100.0,
        half_lives_seconds=[5.0, 10.0, float("inf")],
        time_max_seconds=10.0,
        num_points=3,
    )

    assert result_path == output_path
    assert output_path.exists()

    with output_path.open("r", encoding="utf-8") as json_file:
        payload = json.load(json_file)

    assert payload["initial_amount"] == 100.0
    assert payload["num_points"] == 3
    assert len(payload["series"]) == 3
