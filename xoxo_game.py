print("xoxoxoxoxoxoxoxoxoxoxox")
print("o        Игра         o")
print("x   крестики-нолики   x")
print("o     v0.123 beta     o")
print("x=====================x")
print("o  Введите два числа: o")
print("x         X Y         x")
print("o  X - номер строки   o")
print("x  Y - номер столбца  x")
print("oxoxxooxoxoxoxoxoxoxoxo")


def cells_display():       # Функция вывода таблицы с крестиками-нолмками на экран.
    print("  0 1 2")
    print("0", cells[0], cells[1], cells[2])
    print("1", cells[3], cells[4], cells[5])
    print("2", cells[6], cells[7], cells[8])


def player_input():         # Функция обработки ввода координат от игроков.
    while True:
        player_in = input("Выберите клеточку (ваш ход): ").split()

        if len(player_in) != 2:
            print("Введите два числа 0-2 (через пробел): ")
            continue

        x, y = player_in

        if not (x.isdigit()) or not (y.isdigit()):
            print("Введите два числа 0-2 (через пробел): ")
            continue

        x, y = int(x), int(y)

        if not (0 <= x <= 2) or not (0 <= y <= 2):
            print("Введите два числа 0-2 (через пробел): ")
            continue

        if cells[x*3 + y] != "-":
            print("Клеточка занята! ")
            continue

        return x, y


def victory_check():        # Функция проверки наличия выиграшной комбинации.
    victory = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                (0, 4, 8), (2, 4, 6))
    for combo in victory:
        player_set = []
        for i in combo:
            player_set.append(cells[i])
        if player_set == ["x", "x", "x"]:
            print()
            print("==================")
            print("Выиграли Крестики!")
            return True
        if player_set == ["o", "o", "o"]:
            print()
            print("==================")
            print("Выиграли Нолики!")
            return True
    return False

# Основное тело игры.


cells = ['-', '-', '-', '-', '-', '-', '-', '-', '-']
turns = 0
while True:
    turns += 1
    cells_display()
    if turns % 2 == 1:
        print("Ходят Крестики!")
    else:
        print("Ходят Нолики!")

    x, y = player_input()

    if turns % 2 == 1:
        cells[x*3 + y] = "x"
    else:
        cells[x*3 + y] = "o"

    if victory_check():
        break

    if turns == 9:
        print("Победила Дружба!")
        break
cells_display()
