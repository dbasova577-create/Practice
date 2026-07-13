"""Core tour price calculation and input validation."""

from decimal import Decimal, ROUND_HALF_UP

Number = int | float | Decimal

CHILD_COEFFICIENT = Decimal("0.5")
ONE_RUBLE = Decimal("1")


def _require_integer(name: str, value: object, minimum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if value < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return value


def _require_finite_number(name: str, value: object) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        raise TypeError(f"{name} must be a number")

    decimal_value = Decimal(str(value))
    if not decimal_value.is_finite():
        raise ValueError(f"{name} must be finite")
    return decimal_value


def calculator_hotel(
    nights: int,
    price_per_night_per_person: Number,
    adults: int,
    children: int,
    board: str,
    discount: Number,
) -> int:
    """Calculate a tour price in whole rubles.

    ``board`` intentionally does not affect the result in the current business
    rule. Monetary halves are rounded away from zero (ROUND_HALF_UP), matching
    the usual expectation for prices.
    """

    validated_nights = _require_integer("nights", nights, 1)
    validated_adults = _require_integer("adults", adults, 1)
    validated_children = _require_integer("children", children, 0)
    price = _require_finite_number(
        "price_per_night_per_person", price_per_night_per_person
    )
    validated_discount = _require_finite_number("discount", discount)

    if price < 0:
        raise ValueError("price_per_night_per_person must not be negative")
    if not Decimal("0") <= validated_discount <= Decimal("1"):
        raise ValueError("discount must be between 0 and 1")

    # Reserved for a future board-specific coefficient.
    _ = board

    guests = Decimal(validated_adults) + (
        Decimal(validated_children) * CHILD_COEFFICIENT
    )
    total = (
        Decimal(validated_nights)
        * price
        * guests
        * (Decimal("1") - validated_discount)
    )
    return int(total.quantize(ONE_RUBLE, rounding=ROUND_HALF_UP))


# Descriptive English alias while preserving the original public function name.
calculate_tour_price = calculator_hotel

