"""Application service that evaluates JSON price cases through the calculator."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .calculator import calculator_hotel
from .case_loader import PriceCaseDataError, load_price_cases


@dataclass(frozen=True, slots=True)
class PriceCaseResult:
    case_id: int
    expected_total: int
    actual_total: int

    @property
    def passed(self) -> bool:
        return self.actual_total == self.expected_total


def _evaluate_case(case: dict[str, Any]) -> PriceCaseResult:
    try:
        case_id = int(case["id"])
        inputs = case["input"]
        expected_total = int(case["expected_total"])
        actual_total = calculator_hotel(
            nights=inputs["nights"],
            price_per_night_per_person=inputs["price_per_night_per_person"],
            adults=inputs["adults"],
            children=inputs["children"],
            board=inputs["board"],
            discount=inputs["discount"],
        )
    except (KeyError, TypeError, ValueError) as error:
        raise PriceCaseDataError("Invalid price case structure or values") from error

    return PriceCaseResult(
        case_id=case_id,
        expected_total=expected_total,
        actual_total=actual_total,
    )


def evaluate_price_cases(path: str | Path | None = None) -> list[PriceCaseResult]:
    """Load and calculate every case from a JSON fixture."""

    return [_evaluate_case(case) for case in load_price_cases(path)]

