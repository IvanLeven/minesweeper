import random
import time
import os


def title():  # Титульник
    print('Ivan Leven Presents: "MineSweeper"')
    time.sleep(4)


def cellPathGenerator():  # Генерация списка значений клеток
    indexCounter = 0
    for i in range(65, 74 + 1):
        for k in range(10):
            s = chr(i) + str(k)
            indexDirectory[s] = indexCounter
            indexCounter += 1


def bombGenerator():  # Генератор бомб
    while len(bombs) != 12:
        number = random.randint(0, 99)
        if number in bombs:
            continue
        else:
            bombs.append(number)


def gameFieldNumbersGenerator():  # Создает вторичное, открытое поле, с отмеченными числами, бомбами
    countBombs = 0  # Счетчик бомб вокруг
    for p in range(100):
        if p not in bombs:
            if p % 10 == 9:
                for i in constantCheck:
                    if p - i in bombs and i != -11 and i != 9 and i != -1:
                        countBombs += 1
            elif p % 10 == 0:
                for i in constantCheck:
                    if p - i in bombs and i != 11 and i != -9 and i != 1:
                        countBombs += 1
            else:
                for i in constantCheck:
                    if p - i in bombs:
                        countBombs += 1
            gameFieldNumbers[p] = countBombs
            countBombs = 0
        else:
            gameFieldNumbers[p] = "*"


def fieldPainter():  # Рисует игровое поле
    os.system("cls")
    lowDigit = 0
    highDigit = 10
    print("      (0)  (1)  (2)  (3)  (4)  (5)  (6)  (7)  (8)  (9)")
    print("      " + "     " * 10)
    for j in range(1, 10 + 1):
        print("(" + chr(64 + j) + ")", end="   ")
        for i in range(lowDigit, highDigit):
            print(gameField[i], end="  ")
        print("\n")
        lowDigit += 10
        highDigit += 10


def checker():  # Элемент алгоритма Null
    if gameFieldNumbers[Null[0] - i] == 0:
        Null.append(Null[0] - i)
        gameFieldNumbers[Null[0] - i] = "_"
    elif gameFieldNumbers[Null[0] - i] == "_":
        if gameField[Null[0] - 1] == "[?]":
            countSafeCell -= 1
        gameField[Null[0] - i] = f" {gameFieldNumbers[Null[0] - i]} "
    else:
        if gameField[Null[0] - 1] == "[?]":
            countSafeCell -= 1
        gameField[Null[0] - i] = f"/{gameFieldNumbers[Null[0] - i]}/"


title()

quitGame = False  # Состояние игры
win = True  # Проверка победы
gameField = []  # Игровое поле
bombs = []  # Проигрышные клетки
gameFieldNumbers = []  # Все номера клеток в начале игры генерируются и попадают сюда
indexDirectory = {}  # Хранилище значений клеток
cell = ""  # Клетка
constantCheck = [-11, -10, -9, -1, 1, 9, 10, 11]  # Проверка клеток вокруг

cellPathGenerator()  # Создаем словарь значений для клеток (A0: 0, A1: 1, и т.д.)

while not quitGame:
    bombs = []
    gameField = ["[ ]"] * 100
    gameFieldNumbers = [0] * 100

    bombGenerator()  # Генератор бомб

    gameFieldNumbersGenerator()  # Поле данных

    countBombCell = 0
    countSafeCell = 0

    while win:  # Основной игровой цикл

        fieldPainter()

        if countBombCell == 12 and countSafeCell == 0 and "[ ]" not in gameField:
            break

        while True:
            print("Текущее количесвто бомб:", 12 - (countBombCell + countSafeCell))
            cell = input(" Введите номер клетки, например - E3\n (Отметить клетку - point, убрать метку - unpoint): ")
            if cell not in indexDirectory:
                if cell[:5] == "point" and cell[5:7] in indexDirectory and gameField[indexDirectory[cell[5:7]]] != "[?]":
                    gameField[indexDirectory[cell[5:7]]] = "[?]"
                    if indexDirectory[cell[5:7]] in bombs:
                        countBombCell += 1
                    else:
                        countSafeCell += 1
                    break
                elif cell[:7] == "unpoint" and cell[7:9] in indexDirectory and gameField[indexDirectory[cell[7:9]]] == "[?]":
                    gameField[indexDirectory[cell[7:9]]] = "[ ]"
                    if indexDirectory[cell[7:9]] in bombs:
                        countBombCell -= 1
                    else:
                        countSafeCell -= 1
                    break
                else:
                    print("Некорректно введен код клетки!")
                    time.sleep(1)
                    fieldPainter()
            elif gameField[indexDirectory[cell]] != "[ ]" and gameField[indexDirectory[cell]] != "[?]":
                print("Эта клетка уже открыта! ")
                time.sleep(1)
                fieldPainter()
            elif indexDirectory[cell] in bombs:
                for bomb in bombs:
                    gameField[bomb] = "[#]"
                    for kaboom in range(1):
                        os.system("color 4F")
                        time.sleep(0.01)
                        os.system("color F0")
                        time.sleep(0.01)
                    os.system("color 0F")
                fieldPainter()
                win = False
                break
            else:
                if gameFieldNumbers[indexDirectory[cell]] > 0:
                    if gameField[indexDirectory[cell]] == "[?]":
                        countSafeCell -= 1
                    gameField[indexDirectory[cell]] = f"/{gameFieldNumbers[indexDirectory[cell]]}/"
                    break
                else:
                    Null = [indexDirectory[cell]]
                    while Null:
                        gameFieldNumbers[indexDirectory[cell]] = "_"
                        if Null[0] % 10 == 9:
                            for i in constantCheck:
                                if i != -11 and i != 9 and i != -1 and 0 <= Null[0] - i < 100:
                                    checker()
                        elif Null[0] % 10 == 0:
                            for i in constantCheck:
                                if i != 11 and i != -9 and i != 1 and 0 <= Null[0] - i < 100:
                                    checker()
                        else:
                            for i in constantCheck:
                                if 0 <= Null[0] - i < 100:
                                    checker()
                        if gameField[Null[0]] == "[?]":
                            countSafeCell -= 1
                        gameField[Null[0]] = " _ "
                        del Null[0]
                    break
    if win:
        print("* * * Congratulations! * * *")
    else:
        print("= = = Game Over = = =")

    while True:
        loop = input("\r  Хотите сыграть еще? (Y/N): ")
        if loop == "Y":
            win = True
            break
        elif loop == "N":
            quitGame = True
            print("Goodbye, Player")
            time.sleep(1)
            break
        else:
            print("Некорректный ввод!")
            time.sleep(1)
