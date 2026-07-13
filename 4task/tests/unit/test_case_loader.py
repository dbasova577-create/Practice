import json

import pytest

from tour_price import PriceCaseDataError, load_price_cases


def test_loads_cases_from_explicit_path(tmp_path):
    fixture = tmp_path / "cases.json"
    fixture.write_text(
        json.dumps({"cases": [{"id": 42}]}),
        encoding="utf-8",
    )

    assert load_price_cases(fixture) == [{"id": 42}]


def test_reports_missing_file(tmp_path):
    with pytest.raises(PriceCaseDataError, match="Cannot load price cases"):
        load_price_cases(tmp_path / "missing.json")


def test_reports_invalid_json(tmp_path):
    fixture = tmp_path / "invalid.json"
    fixture.write_text("{not-json", encoding="utf-8")

    with pytest.raises(PriceCaseDataError, match="Cannot load price cases"):
        load_price_cases(fixture)


@pytest.mark.parametrize("payload", [[], {}, {"cases": {}}])
def test_rejects_invalid_schema(tmp_path, payload):
    fixture = tmp_path / "schema.json"
    fixture.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(PriceCaseDataError, match="must contain a 'cases' array"):
        load_price_cases(fixture)

