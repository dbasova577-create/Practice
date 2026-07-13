def calculator_hotel(nights,price_per_night_per_person,adults,children,board,discount):
    if nights <= 0:
        raise ValueError('Ошибка валидации: количество ночей должно быть больше 0')
    if adults <= 0:
        raise ValueError('Ошибка валидации: должен быть хотя бы один взрослый')
    if children < 0:
        raise  ValueError('Ошибка валидации: количество детей не может быть отрицательным')
    if price_per_night_per_person < 0:
        raise ValueError('Ошибка валидации: цена за ночь не может быть отрицательной')
    if discount < 0 or discount > 1:
        raise ValueError('Ошибка валидации: скидка должна быть от 0 до 1')
    return round(nights * price_per_night_per_person * (adults + children * 0.5) * (1 - discount))

