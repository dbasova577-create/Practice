def calculator_hotel(nights,price_per_night_per_person,adults,children,board,discount):
    if nights <= 0:
        raise ValueError('Ощибка валидации: количество ночей должно быть больше 0')
    if adults == 0:
        raise ValueError('Ошибка валидации: должен быть хотя бы один взрослый')
    if discount < 0 or discount > 1:
        raise ValueError('Ошибка валидации: скидка должна быть от 0 до 1')
    return round(nights * price_per_night_per_person * (adults + children * 0.5) * (1 - discount))

nights = 7
price_per_night_per_person = 5000
adults = 2
children = 0
board = 'AI'
discount = 0.0
total = calculator_hotel(nights,price_per_night_per_person,adults,children,board,discount)
print(total)
