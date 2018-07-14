import os
import time


class Player:
    def __init__(self):
        self.name = ''
        self.n, self.m = 10, 10
        self.hits = [[0 for _ in range(self.m)] for _ in range(self.n)]
        self.ships = [[0 for _ in range(self.m)] for _ in range(self.n)]
        self.storage = []

    def print_field(self, paint=True):  # рисует поле. Если идет игра, то корабли не отображаются
        os.system('cls')
        print(' ', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        for i in range(self.m):
            print(i, end=' ')
            for j in range(self.n):
                if self.ships[i][j] == 0:  # Пусто
                    print('.', end=' ')
                elif self.ships[i][j] == 1:  # Корабль
                    print('@', end=' ') if paint else print('.', end=' ')
                elif self.ships[i][j] == 2:  # Мимо
                    print('*', end=' ')
                elif self.ships[i][j] == 3:  # Ранен
                    print('x', end=' ')
                elif self.ships[i][j] == 4:  # Убит
                    print('@', end=' ')
            print()

    def check_ship(self, deck, s, c, orient=1):  # Проверка, можно ли поместить корабль в данном месте
        if (orient == 2 and (s + deck - 1) >= self.n) or (orient == 1 and (c + deck -1) >= self.n):
            print('Не лезет!!!')
            return False
        if orient == 1:
            for i in range(s-1, s+2):
                for j in range(c-1, c + deck + 1):
                    if 0 <= i <= 9 and 0 <= j <= 9 and self.ships[i][j]:
                        print('Касается другого корабля!')
                        return False
            return True
        if orient == 2:
            for i in range(c-1, c+2):
                for j in range(s-1, s + deck + 1):
                    if 0 <= i <= 9 and 0 <= j <= 9 and self.ships[j][i]:
                        print('Касается другого корабля!')
                        return False
            return True

    def place_ship(self, deck, s, c, orient=1):  # сохраняет корабль
        spisok = []
        if orient == 1:
            for _ in range(deck):
                self.ships[s][c] = 1
                spisok.append([s, c])
                c += 1
        if orient == 2:
            for _ in range(deck):
                self.ships[s][c] = 1
                spisok.append([s, c])
                s += 1
        self.storage.append(spisok)

    def input_coord(self):  # ввод координат кораблей
        for i in [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]:
            check = False
            orient = 1
            while not check:
                orient = 1
                if i == 1:
                    print('Введите координату {}-палубного корабля'.format(i))
                else:
                    print('Введите координату {}-палубного корабля,'.format(i),
                          'введите направление: 1 - горизонтально, 2 - вертикально')
                try:
                    new_str = input().split()
                    s = int(new_str[0])
                    c = int(new_str[1])
                    if len(new_str) > 2:
                        orient = int(new_str[3])
                    if orient not in [1, 2]:
                        raise ValueError
                    check = self.check_ship(i, s, c, orient)
                except ValueError:
                    print('Введите корректное значение!')
                    time.sleep(0.5)
                except IndexError:
                    print('Введите корректное значение!')
                    time.sleep(0.5)
            self.place_ship(i, s, c, orient)
            self.print_field()

    def check_win(self):  # проверка выигрыша
        dead = 0
        for i in range(self.m):
            for j in range(self.n):
                if self.ships[i][j] == 4:
                    dead += 1
        return True if dead == 20 else False


class Game:
    def __init__(self):
        self.player1 = Player()
        self.player2 = Player()
        self.player1.name = input('Введите имя первого игрока: ')
        self.player1.print_field()
        self.player1.input_coord()
        self.player2.print_field()
        self.player2.name = input('Введите имя второго игрока: ')
        self.player2.input_coord()
        print(self.player1.storage)
        os.system('cls')
        self.shot()

    def shot(self):  # Принимает координаты выстрела
        flag = True
        player = self.player1 if flag else self.player2
        while not player.check_win():
            try:
                player.print_field(False)
                print('Ход игрока', player.name)
                s, c = list(map(int, input().split()))
                while player.hits[s][c]:
                    print('Вы уже сюда стреляли! Попробуйте снова!')
                    s, c = list(map(int, input().split()))
                player.hits[s][c] = 1
                flag = self.check_shot(player, s, c, flag)
                player = self.player1 if flag else self.player2
            except ValueError:
                print('Введите корректное значение!')
                time.sleep(0.5)
        print('Вы выиграли!')

    def check_shot(self, player, s, c, flag):  # Проверяет, чему соответствует выстрел: мимо, убит, ранен
        if player.ships[s][c] == 0:
            player.ships[s][c] = 2
            player.print_field(False)
            print('мимо')
            time.sleep(0.8)
            return not flag
        elif player.ships[s][c] == 1:
            player.ships[s][c] = 3
            if self.check_dead(player, s, c):
                print('Убит')
            else:
                player.print_field(False)
                print('ранен')
            time.sleep(0.5)
            return flag

    @staticmethod
    def check_dead(player, s, c):  # Проверяет, убит ли корабль
        for i in range(10):
            if [s, c] in player.storage[i]:
                for j in player.storage[i]:
                    k, m = j
                    if player.ships[k][m] != 3:
                        return False
                for j in player.storage[i]:
                    k, m = j
                    player.ships[k][m] = 4
                Game.mimo(player, i)
                return True

    @staticmethod
    def mimo(player, m):  # Расставляет мимо вокруг потонувшего корабля
        s, c = player.storage[m][0]
        deck = len(player.storage[m])
        if deck > 1 and player.storage[m][0][1] == player.storage[m][1][1]:
            orient = 2
        else:
            orient = 1
        if orient == 1:
            for i in range(s-1, s+2):
                for j in range(c-1, c + deck + 1):
                    if 0 <= i <= 9 and 0 <= j <= 9 and not player.ships[i][j]:
                        player.ships[i][j] = 2
                        player.hits[i][j] = 1
        if orient == 2:
            for i in range(c-1, c+2):
                for j in range(s-1, s + deck + 1):
                    if 0 <= i <= 9 and 0 <= j <= 9 and not player.ships[j][i]:
                        player.ships[j][i] = 2
                        player.hits[j][i] = 1


os.system('cls')
game = Game()


