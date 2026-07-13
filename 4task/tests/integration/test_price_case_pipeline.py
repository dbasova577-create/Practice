import json

import pytest

from tour_price import PriceCaseDataError, evaluate_price_cases


pytestmark = pytest.mark.integration


def test_packaged_reference_cases_pass_from_any_working_directory(
    tmp_path, monkeypatch
):
    monkeypatch.chdir(tmp_path)

    results = evaluate_price_cases()

    assert [result.case_id for result in results] == [1, 2, 3, 4, 5]
    assert [result.actual_total for result in results] == [
        70000,
        90000,
        24000,
        124950,
        103075,
    ]
    assert all(result.passed for result in results)


def test_pipeline_reports_a_business_expectation_mismatch(tmp_path):
    fixture = tmp_path / "custom-cases.json"
    fixture.write_text(
        json.dumps(
            {
                "cases": [
                    {
                        "id": 99,
                        "input": {
                            "nights": 1,
                            "price_per_night_per_person": 1000,
                            "adults": 1,
                            "children": 0,
                            "board": "BB",
                            "discount": 0,
                        },
                        "expected_total": 999,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    [result] = evaluate_price_cases(fixture)

    assert result.actual_total == 1000
    assert result.expected_total == 999
    assert result.passed is False


def test_pipeline_rejects_malformed_case(tmp_path):
    fixture = tmp_path / "malformed-cases.json"
    fixture.write_text(
        json.dumps({"cases": [{"id": 1, "input": {}}]}),
        encoding="utf-8",
    )

    with pytest.raises(PriceCaseDataError, match="Invalid price case"):
        evaluate_price_cases(fixture)

