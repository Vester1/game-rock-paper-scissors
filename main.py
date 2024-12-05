import random
import json

# Чтение json файла
with open('data.json') as f:
    read_json = json.load(f)

# Вероятности для камня и ножниц если пользователь выиграл в прошлой игре
prob_win = {
    'камень': [0.3, 0.15],
    'ножницы': [0.55, 0.3],
    'бумага': [0.15, 0.55]
}

# Вероятности для камня и ножниц если пользователь проиграл в прошлой игре
prob_loss = {
    'камень': [0.55, 0.3],
    'ножницы': [0.15, 0.55],
    'бумага': [0.3, 0.15]
}

# Словарь для обозначения "знак слева бьет знак справа"
win_comb = {
    'камень': 'ножницы',
    'ножницы': 'бумага',
    'бумага': 'камень'
}

game_info = {
    'last': None,  # Последний выбранный знак пользователем
    'win': None,  # Исход прошлой игры(для пользователя)
    'cnt_of_win': 0  # Количество побед игрока
}
# Статистка игр
stat = read_json['stat']
# Ставка (по умолчанию - 10)
bet = 10


def get_info():
    """
    Выводит в консоль список всех команд с описанием
    """

    # Команды игры
    info = (
        '\nСписок команд:\n- "игра <знак>" - начало игры\n- "стат" - вывод статистики игр\n- "баланс" - баланс '
        'хумстеров\n- "ставка <число>" - изменить ставку, если не указывать ставку, то выведет нынешнюю\n'
        '- "заработок" - заработать хумстеры\n- "выход" - выход из игры\n')
    print(info)
    return


def rand_choice(p1, p2):
    """
    Делает случайны выбор из камня, ножницы или бумаги по данным вероятностям
    p1 - вероятность камня, p2 - ножниц
    """
    rand_num = random.random()  # Генерация случайного вещественного числа от 0 до 1
    if 0 <= rand_num <= p1:
        return 'камень'
    elif p1 < rand_num <= p1 + p2:
        return 'ножницы'
    else:
        return 'бумага'


def play(inp):
    translate = {  # Словарь с переводом с русского на английский
        'камень': 'rock',
        'ножницы': 'scissors',
        'бумага': 'paper',
    }
    s = inp.split()[1]  # Знак которой выбрал пользователь
    if s not in ['камень', 'ножницы', 'бумага']:
        print('\nНеправильный знак\n')
        return
    if stat['humsters'] < bet:
        print('\nУ вас слишком большая ставка. У вас нет столько!\n')
        return
    if game_info['last'] is None:  # Если первая игра
        sign = rand_choice(0.25, 0.25)  # Полагаем, что пользователь скорее всего выбрал камень
    elif game_info['cnt_of_win'] > 5:  # Если пользователь слишком часто выигрывает
        sign = rand_choice(0.33, 0.33)
    elif game_info['win'] == 'win':  # Если пользователь выиграл в прошлой игре
        sign = rand_choice(*prob_win[s])
    elif game_info['win'] == 'loss':  # Если пользователь проиграл в прошлой игре
        sign = rand_choice(*prob_loss[s])
    else:  # Если была ничья в прошлой игре
        sign = rand_choice(0.33, 0.33)

    print(f'\nЯ выбрал {sign}, Вы выбрали {s}')
    stat['cnt'] += 1  # Обновление кол-ва игр
    stat[f'cnt_{translate[s]}'] += 1  # Обновление кол-ва выбранных значков
    game_info['last'] = s

    if s == sign:  # Если ничья
        game_info['win'] = 'draw'
        stat['draw'] += 1
        print('НИЧЬЯ, Вам вернулись хумстеры\n')
    elif win_comb[s] == sign:  # Если пользователь выиграл
        game_info['cnt_of_win'] += 1  # Обновление счетчика побед/поражений пользователя
        game_info['win'] = 'win'
        stat['win'] += 1  # Обновление статистики выигрышей
        stat['humsters'] += bet  # Начисление ставки на баланс
        print(f'ВЫ ВЫИГРАЛИ, Вам начислено {bet} хумстеров')
    else:  # Если пользователь проиграл
        game_info['cnt_of_win'] -= 1  # Обновление счетчика побед/поражений пользователя
        game_info['win'] = 'loss'
        stat['loss'] += 1
        stat['humsters'] -= bet  # Списание с баланса ставки
        print(f'ВЫ ПРОИГРАЛИ, с баланса списано {bet} хумстеров')

    print(f'Баланс: {stat["humsters"]} хумстеров\n')


def get_stat():
    """
    Вывод в консоль статистику игры
    """
    total_num = stat['cnt_rock'] + stat['cnt_paper'] + stat['cnt_scissors']
    if total_num == 0:
        total_num = 1
    p_rock = round(stat['cnt_rock'] / total_num * 100, 1)
    p_paper = round(stat['cnt_paper'] / total_num * 100, 1)
    p_scissors = round(stat['cnt_scissors'] / total_num * 100, 1)
    print(f"\nКоличество игр: {stat['cnt']}\nПобед: {stat['win']}   Поражений: {stat['loss']}   Ничьих: {stat['draw']}\n"
          f"Процент выбора:   камня - {p_rock}%   ножниц - {p_scissors}%   бумаги - {p_paper}%\n")

    return


def get_humsters():
    """
    Функция для генерации случайного числа из 15 цифр написанными буквами и проверки введенного числа на правильность
    """
    print("\nЧтобы заработать 100 хумстеров вам нужно ввести данное число цифрами (без пробелов)")
    # Словарь с сопоставлением цифры к слову
    nums = {i: j for i, j in zip(range(0, 10),
                                 ['ноль', 'один', 'два', 'три', 'четыре', 'пять', 'шесть', 'семь', 'восемь', 'девять'])}
    rand_num = random.randint(10**14, 10**15-1)  # Генерация случайного числа
    str_rand_num = ' '.join(nums[int(i)] for i in str(rand_num))  # Строка из цифр, написанными буквами
    print(str_rand_num)
    try:
        s = int(input())
    except ValueError:
        print("\nОШИБКА. Вы ввели что то некорректное\n")
        return
    if s == rand_num:
        print("\nУСПЕШНО. Вам начислено 100 хумстеров\n")
        stat['humsters'] += 100
    else:
        print("\nВ набранном числе есть ошибка\n")

    return


def get_balance():
    """
    Вывод в консоль баланса
    """
    print(f"\nБАЛАНС - {stat['humsters']}\n")
    return


def change_bet(inp):
    """
    Изменяет ставку
    inp - Введенная с консоли команда
    """
    global bet
    lst_inp = list(inp.split())
    if len(lst_inp) == 1:
        print(f"\nСтавка - {bet}\n")
        return

    if len(lst_inp) == 2:
        try:
            new_bet = int(lst_inp[1])
        except ValueError:
            print("\nВведено нечисловое значение\n")
            return
    else:
        print("\nОшибка в записи команды\n")
        return

    if 0 < new_bet <= stat['humsters']:
        bet = new_bet
        print("\nСтавка успешно изменена\n")
    else:
        print("\nНекорректная ставка\n")


def exit_from_game():
    """
    Выход из игры
    """
    print("\nБУДЕМ ЖДАТЬ ВАС СНОВА")
    exit(0)


# Приветствие
print('ВАС ПРИВЕТСТВУЕТ ИГРА КАМЕНЬ-НОЖНИЦЫ-БУМАГА\nЧтобы посмотреть все команды, введи "список"\n')

# Бесконечный цикл игры
while True:
    inp = input()
    if inp:
        command = inp.split()[0]
    else:
        continue
    if command == 'список':
        get_info()
    elif command == 'игра':
        play(inp)
    elif command == 'стат':
        get_stat()
    elif command == 'заработок':
        get_humsters()
    elif command == 'ставка':
        change_bet(inp)
    elif command == 'баланс':
        get_balance()
    elif command == 'выход':
        exit_from_game()
    else:
        print("\nЧто вы имели ввиду?\n")

    # Обновление json файла
    to_write = {'stat': stat}
    with open('data.json', 'w') as f:
        json.dump(to_write, f, indent=2)
