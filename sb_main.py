from random import randint

# Классы исключений, которые обрабатывает наша программа.

class BoardError(Exception):
    pass

class BoardOutsideException(BoardError):
    def __str__(self):
        return "Выстрел за пределы доски!"

class BoardOldTargetException(BoardError):
    def __str__(self):
        return "В эту клетку уже стреляли!"

class BoardShipOccupiedException(BoardError):
    pass

# Класс координат игрового поля.

class Dots:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, another):
        return self.x == another.x and self.y == another.y

    def __repr__(self):
        return f"({self.x}, {self.y})"

# Класс кораблей.

class Ship:
    def __init__(self, front, length, orient):
        self.front = front
        self.length = length
        self.orient = orient
        self.decks = length

    @property
    def coords(self):
        ship_coords = []
        for i in range(self.length):
            current_x = self.front.x
            current_y = self.front.y
            if self.orient == 0:
                current_x += i
            elif self.orient == 1:
                current_y += i
            ship_coords.append(Dots(current_x, current_y))
        return ship_coords

# Класс игрового поля.

class Board:
    def __init__(self, hide=False, size=6):
        self.size = size
        self.hide = hide
        self.count = 0
        self.field = [["O"] * size for _ in range(size)]
        self.occupied = []
        self.ships = []

    def add_ship(self, ship):
        for d in ship.coords:
            if self.outside(d) or d in self.occupied:
                raise BoardShipOccupiedException()
        for d in ship.coords:
            self.field[d.x][d.y] = "■"
            self.occupied.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.coords:
            for dx, dy in near:
                current = Dots(d.x + dx, d.y + dy)
                if not (self.outside(current)) and current not in self.occupied:
                    if verb:
                        self.field[current.x][current.y] = "."
                    self.occupied.append(current)

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hide:
            res = res.replace("■", "O")
        return res

    def outside(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):
        if self.outside(d):
            raise BoardOutsideException()

        if d in self.occupied:
            raise BoardOldTargetException()

        self.occupied.append(d)

        for ship in self.ships:
            if d in ship.coords:
                ship.decks -= 1
                self.field[d.x][d.y] = "X"
                if ship.decks == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль потоплен!")
                    return False
                else:
                    print("Корабль подбит (ещё на плаву)!")
                    return True

        self.field[d.x][d.y] = "T"
        print("Промах!")
        return False

    def begin(self):
        self.occupied = []

# Класс игроков.

class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardError as e:
                print(e)

# Класс игрока "Компьютер".

class Computer(Player):
    def ask(self):
        d = Dots(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d

# Класс игрока "Человек".

class Human(Player):
    def ask(self):
        while True:
            target = input("Ваш ход: ").split()

            if len(target) != 2:
                print(" Введите координаты X и Y! ")
                continue

            x, y = target

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите два числа от 1 до 6! ")
                continue

            x, y = int(x), int(y)

            return Dots(x - 1, y - 1)

# Класс "Игра".

class Game:
    def __init__(self, size=6):
        self.size = size
        h_board = self.random_board()
        c_board = self.random_board()
        c_board.hide = True

        self.comptr = Computer(c_board, h_board)
        self.humn = Human(h_board, c_board)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        fleet = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for f in fleet:
            while True:
                attempts += 1
                if attempts > 9000:
                    return None
                ship = Ship(Dots(randint(0, self.size), randint(0, self.size)), f, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardShipOccupiedException:
                    pass
        board.begin()
        return board

    def greetings(self):
        print("_______________________")
        print("|        Игра         |")
        print("|     МОРСКОЙ БОЙ     |")
        print("|     v0.123 beta     |")
        print("|=====================|")
        print("|  Введите два числа: |")
        print("|        X   Y        |")
        print("|  X - номер строки   |")
        print("|  Y - номер столбца  |")
        print("|_____________________|")

    def gaming(self):
        num = 0
        while True:
            print("-" * 27)
            print("Ваша доска:")
            print(self.humn.board)
            print("-" * 27)
            print("Доска компьютера:")
            print(self.comptr.board)
            if num % 2 == 0:
                print("-" * 27)
                print("Ходит человек!")
                repeat = self.humn.move()
            else:
                print("-" * 27)
                print("Ходит компьютер!")
                repeat = self.comptr.move()
            if repeat:
                num -= 1

            if self.comptr.board.count == 7:
                print("-" * 27)
                print("Выиграл Человек!")
                break

            if self.humn.board.count == 7:
                print("-" * 27)
                print("Выиграл компьютер!")
                break
            num += 1

    def start(self):
        self.greetings()
        self.gaming()


go = Game()
go.start()
