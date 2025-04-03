# coding=utf8
# Wei Guannan <kiss.kraks@gmail.com>

import copy
import random
from colorama import Fore, Back
from functools import reduce

def reduceLineLeft(xs): 
    def aux(acc, y):
        if len(acc) == 0:
            acc.append(y)
        elif acc[-1] == y:
            acc[-1] = y * 2
            acc.append(0)
        else:
            acc.append(y)
        return acc
    res = list(filter(lambda x: x != 0, reduce(aux, filter(lambda x: x != 0, xs), [])))
    res.extend([0] * (len(xs) - len(res)))
    return res

def reduceLineRight(xs):
    return reduceLineLeft(xs[::-1])[::-1]

def reduceLeft(a):
    return [reduceLineLeft(row) for row in a]

def reduceRight(a):
    return [reduceLineRight(row) for row in a]

def reduceUp(a):
    return rotate(reduceLeft(rotate(a)))

def reduceDown(a):
    return rotate(reduceRight(rotate(a)))

def rotate(a):
    size = len(a)
    return [[a[j][i] for j in range(size)] for i in range(size)]

def color(x):
    colors = {
        0: Fore.RESET + Back.RESET,
        2: Fore.RED + Back.RESET,
        4: Fore.GREEN + Back.RESET,
        8: Fore.YELLOW + Back.RESET,
        16: Fore.BLUE + Back.RESET,
        32: Fore.MAGENTA + Back.RESET,
        64: Fore.CYAN + Back.RESET,
        128: Fore.RED + Back.BLACK,
        256: Fore.GREEN + Back.BLACK,
        512: Fore.YELLOW + Back.BLACK,
        1024: Fore.BLUE + Back.BLACK,
        2048: Fore.MAGENTA + Back.BLACK,
        4096: Fore.CYAN + Back.BLACK,
        8192: Fore.WHITE + Back.BLACK
    }
    return colors.get(x, Fore.RESET + Back.RESET)

def prettyPrint(a):
    max_num = max(max(row) for row in a)
    empty_spaces = sum(row.count(0) for row in a)
    for row in a:
        print(" ".join(color(num) + f"{num:4d}" + Fore.RESET + Back.RESET for num in row))
    print(Fore.YELLOW + "Highest number: " + Fore.WHITE + f"{max_num}" + Fore.RESET)
    print(Fore.YELLOW + "Empty spaces: " + Fore.WHITE + f"{empty_spaces}" + Fore.RESET)

def newEmpty(size):
    return [[0] * size for _ in range(size)]

def isWin(a):
    return any(2048 in row for row in a)

def isFail(a):
    for row in a:
        for x, y in zip(row, row[1:]):
            if x == 0 or y == 0 or x == y:
                return False
    for col in zip(*a):
        for x, y in zip(col, col[1:]):
            if x == 0 or y == 0 or x == y:
                return False
    return True

def randomPoint(size):
    return random.randint(0, size - 1), random.randint(0, size - 1)

def randomInit(a):
    seed = [2, 2, 2, 4]
    x, y = randomPoint(len(a))
    while a[x][y] != 0:
        x, y = randomPoint(len(a))
    a[x][y] = random.choice(seed)

def randomNum(a):
    randomInit(a)

def newGame():
    size = int(input("\n" + Fore.CYAN + "Enter grid size: " + Fore.RESET))
    print(Fore.MAGENTA + "Press W to move up, A to move left, S to move down, D to move right.")
    print("Press Q to quit." + Fore.RESET)
    print(Fore.WHITE + "\n========================================================================" + Fore.RESET + "\n")
    print(Fore.GREEN + "INITIAL STATE:\n" + Fore.RESET)

    won = False
    moves = 0
    a = newEmpty(size)
    randomInit(a)
    randomInit(a)
    prettyPrint(a)
    while True:
        print(Fore.BLUE + "---------------------" + Fore.RESET)
        b = copy.deepcopy(a)
        key = input(Fore.BLUE + "Move: " + Fore.RESET).upper()
        if key == "W":   a = reduceUp(a)
        elif key == "A": a = reduceLeft(a)
        elif key == "S": a = reduceDown(a)
        elif key == "D": a = reduceRight(a)
        elif key == "Q":
            break
        else:
            print(Fore.RED + "Invalid move. Use W, A, S, D." + Fore.RESET)
            continue
        if a == b: 
            print(Fore.RED + "No numbers were reduced." + Fore.RESET)
        else:
            randomNum(a)
            moves += 1
        prettyPrint(a)
        if isWin(a) and not won:
            print("You win!")
            won = True
        elif isFail(a):
            print(Fore.WHITE + "\n============================" + Fore.RESET)
            print(Fore.RED + "You lose!" + Fore.RESET)
            break
    max_num = max(max(row) for row in a)
    print(Fore.GREEN + f"Total moves: " + Fore.WHITE + f"{moves}\n" + Fore.GREEN + "Highest number achieved: " + color(max_num) + f"{max_num}" + Fore.RESET)
    print(Fore.WHITE + "============================\n" + Fore.RESET)

if __name__ == "__main__":
    newGame()