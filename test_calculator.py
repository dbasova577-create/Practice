import json
import pytest

from calculator import calculator_hotel

def load_cases():
    with open('04_price_calc_cases.json', 'r', encoding='utf-8') as file:
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

@pytest.mark.parametrize('invalid_nights', [0,-1,-10])

def test_night_error(invalid_nights):
    with pytest.raises(ValueError, match='количество ночей должно быть больше 0'):
        calculator_hotel(invalid_nights,5000,2,0,'AI',0)


@pytest.mark.parametrize('invalid_adults',[0,-1])

def test_adults_error(invalid_adults):
    with pytest.raises(ValueError, match='должен быть хотя бы один взрослый'):
        calculator_hotel(4,3000,invalid_adults,0,'AI',0)


@pytest.mark.parametrize('invalid_discount',[-0.1,1.1,2.0])

def test_discount(invalid_discount):
    with pytest.raises(ValueError, match='скидка должна быть от 0 до 1'):
        calculator_hotel(7, 4000,3,0,'AI',invalid_discount)