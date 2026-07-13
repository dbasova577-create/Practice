from decimal import Decimal

import pytest

from tour_price import calculate_tour_price, calculator_hotel


@pytest.mark.parametrize(
    ("nights", "price", "adults", "children", "board", "discount", "expected"),
    [
        (7, 5000, 2, 0, "AI", 0, 70000),
        (10, 4000, 2, 1, "UAI", Decimal("0.1"), 90000),
        (1, 1, 1, 0, "BB", Decimal("0.5"), 1),
        (2, 1000, 1, 0, "BB", 1, 0),
    ],
)
def test_calculates_expected_total(
    nights, price, adults, children, board, discount, expected
):
    assert (
        calculator_hotel(nights, price, adults, children, board, discount)
        == expected
    )


def test_board_does_not_change_total():
    totals = {
        calculator_hotel(7, 5000, 2, 1, board, 0.1)
        for board in ("AI", "UAI", "BB", "unexpected")
    }
    assert totals == {78750}


@pytest.mark.parametrize("nights", [0, -1, -10])
def test_rejects_non_positive_nights(nights):
    with pytest.raises(ValueError, match="nights must be at least 1"):
        calculator_hotel(nights, 5000, 2, 0, "AI", 0)


@pytest.mark.parametrize("adults", [0, -1])
def test_rejects_non_positive_adults(adults):
    with pytest.raises(ValueError, match="adults must be at least 1"):
        calculator_hotel(4, 3000, adults, 0, "AI", 0)


def test_rejects_negative_children():
    with pytest.raises(ValueError, match="children must be at least 0"):
        calculator_hotel(4, 3000, 2, -1, "AI", 0)


def test_rejects_negative_price():
    with pytest.raises(ValueError, match="must not be negative"):
        calculator_hotel(4, -1, 2, 0, "AI", 0)


@pytest.mark.parametrize("discount", [-0.1, 1.1, 2])
def test_rejects_discount_outside_closed_interval(discount):
    with pytest.raises(ValueError, match="between 0 and 1"):
        calculator_hotel(7, 4000, 3, 0, "AI", discount)


@pytest.mark.parametrize(
    ("arguments", "message"),
    [
        ((1.5, 1000, 1, 0, "AI", 0), "nights must be an integer"),
        ((1, 1000, True, 0, "AI", 0), "adults must be an integer"),
        ((1, 1000, 1, 0.5, "AI", 0), "children must be an integer"),
        ((1, "1000", 1, 0, "AI", 0), "price_per_night_per_person must be a number"),
        ((1, 1000, 1, 0, "AI", False), "discount must be a number"),
    ],
)
def test_rejects_invalid_types(arguments, message):
    with pytest.raises(TypeError, match=message):
        calculator_hotel(*arguments)


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_rejects_non_finite_numbers(value):
    with pytest.raises(ValueError, match="must be finite"):
        calculator_hotel(1, value, 1, 0, "AI", 0)


def test_descriptive_alias_keeps_public_contract():
    assert calculate_tour_price is calculator_hotel

