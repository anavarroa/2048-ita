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

def prettyPrint(a):
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
    for row in a:
        print(" ".join(color(num) + f"{num:4d}" + Fore.RESET + Back.RESET for num in row))
    print()

def newEmpty(size):
    return [[0] * size for _ in range(size)]

def isWin(a):
    return any(2048 in row for row in a)

def isFail(a):
    for row in a:
        for x, y in zip(row, row[1:]):
            if x == 0 or y == 0 or x == y:
                return False
    return all(isFail(list(col)) for col in zip(*a))

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

def newGame(size):
    print("Press w to move up, a to move left, s to move down, d to move right.")
    print("Press q to quit.")
    won = False
    a = newEmpty(size)
    randomInit(a)
    randomInit(a)
    prettyPrint(a)
    while True:
        b = copy.deepcopy(a)
        key = input("Move: ")
        if key == "w":   a = reduceUp(a)
        elif key == "a": a = reduceLeft(a)
        elif key == "s": a = reduceDown(a)
        elif key == "d": a = reduceRight(a)
        elif key == "q": break
        if a == b: 
            print("No numbers were reduced.")
        else:
            randomNum(a)
        prettyPrint(a)
        if isWin(a) and not won:
            print("You win!")
            won = True
        elif isFail(a):
            print("You lose!")
            break

def test():
    assert reduceLineLeft([4, 4, 4, 4]) == [8, 8, 0, 0]
    assert reduceLineLeft([0, 0, 0, 0]) == [0, 0, 0, 0]
    assert reduceLineLeft([2, 0, 2, 0]) == [4, 0, 0, 0]
    assert reduceLineLeft([2, 0, 0, 2]) == [4, 0, 0, 0]
    assert reduceLineLeft([2, 2, 0, 2]) == [4, 2, 0, 0]
    assert reduceLineLeft([4, 0, 2, 2]) == [4, 4, 0, 0]
    assert reduceLineLeft([2, 0, 2, 2]) == [4, 2, 0, 0]
    assert reduceLineLeft([2, 2, 8, 8]) == [4, 16, 0, 0]
    assert reduceLineRight([2, 2, 0, 2]) == [0, 0, 2, 4]
    assert reduceLineRight([0, 0, 0, 2]) == [0, 0, 0, 2]
    assert reduceLineRight([2, 0, 0, 2]) == [0, 0, 0, 4]
    assert reduceLineRight([4, 4, 2, 2]) == [0, 0, 8, 4]
    assert reduceLineRight([2, 4, 4, 2]) == [0, 2, 8, 2]
    print("All tests passed!")

if __name__ == "__main__":
    newGame(4)
