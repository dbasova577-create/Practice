import json
import pytest

from calculator import calculator_hotel

def load_cases():
    with open('../04_price_calc_cases.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data['cases']

@pytest.mark.parametrize('case',load_cases())
def test_calculator_succesful_cases(case):
    inputs = case['input']
    expected = case['expected_total']
    result = calculator_hotel(
        nights=inputs["nights"],
        price_per_night_per_person=inputs["price_per_night_per_person"],
        adults=inputs["adults"],
        children=inputs["children"],
        board=inputs["board"],
        discount=inputs["discount"]
    )
    assert result == expected



def test_night_error():
    with pytest.raises(ValueError):
        calculator_hotel(0,5000,2,0,'AI',0)


def test_adults_error():
    with pytest.raises(ValueError):
        calculator_hotel(4,3000,0,0,'AI',0)


def test_discount():
    with pytest.raises(ValueError):
        calculator_hotel(7, 4000,3,0,'AI',1.2)