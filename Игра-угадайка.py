import random
num = random.randint(1,20)
flag = True
guess = 0

print('Отгадай число от 1 до 20: ', end='')

while flag:
    guess = input()
    if not guess.isdigit():
        print('Ошибка, введите число от 1 до 20')
        break
    elif int(guess) < num:
        print('Слишком мало, попробуйте ещё раз:')
    elif int(guess) > num:
        print('Слишком много, попробуйте ещё раз:')
    else:
        print(f'Правильно, моё число: {guess}')
        flag = False