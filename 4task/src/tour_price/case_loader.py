"""Load reference price cases independently of the current working directory."""

from __future__ import annotations

import json
from json import JSONDecodeError
from pathlib import Path
from typing import Any

DEFAULT_CASES_PATH = (
    Path(__file__).resolve().parent / "data" / "04_price_calc_cases.json"
)


class PriceCaseDataError(ValueError):
    """Raised when a price-case file cannot be loaded or has an invalid schema."""


def load_price_cases(path: str | Path | None = None) -> list[dict[str, Any]]:
    """Return the ``cases`` array from a UTF-8 JSON fixture."""

    target = Path(path) if path is not None else DEFAULT_CASES_PATH

    try:
        with target.open("r", encoding="utf-8") as source:
            payload = json.load(source)
    except (OSError, JSONDecodeError) as error:
        raise PriceCaseDataError(f"Cannot load price cases from {target}") from error

    if not isinstance(payload, dict) or not isinstance(payload.get("cases"), list):
        raise PriceCaseDataError("Price-case JSON must contain a 'cases' array")

    return payload["cases"]

