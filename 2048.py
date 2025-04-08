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
    rows, cols = len(a), len(a[0])
    return [[a[j][i] for j in range(rows)] for i in range(cols)]

def color(x):
    if x == 0:
        return Fore.RESET + Back.RESET

    # Colores disponibles (pueden rotar en orden cíclico)
    fore_colors = [Fore.WHITE, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    back_colors = [Back.RESET, Back.BLACK]

    # Determinar el índice de la potencia de 2
    power = x.bit_length() - 1  # log2(x)
    
    fore = fore_colors[power % len(fore_colors)]
    back = back_colors[(power // len(fore_colors)) % len(back_colors)]

    return fore + back


def prettyPrint(a, state_number=None):
    max_num = max(max(row) for row in a)
    empty_spaces = sum(row.count(0) for row in a)
    current_sum = sum(sum(row) for row in a)
    if state_number is not None:
        print(Fore.CYAN + f"Step: {state_number}" + Fore.RESET)
    
    for row in a:
        print(" ".join(
            color(num) + (f"{num:4d}" if num != 0 else "   ·") + Fore.RESET + Back.RESET
            for num in row
        ))

    print(Fore.YELLOW + "Highest number: " + Fore.WHITE + f"{max_num}" + Fore.RESET)
    print(Fore.YELLOW + "Empty spaces: " + Fore.WHITE + f"{empty_spaces}" + Fore.RESET)
    print(Fore.YELLOW + "Current sum: " + Fore.WHITE + f"{current_sum}" + Fore.RESET)


def newEmpty(size):
    return [[0] * size for _ in range(size)]

def isWin(a):
    return False

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

def applyMove(board, move):
    if move == "W": return reduceUp(board)
    if move == "A": return reduceLeft(board)
    if move == "S": return reduceDown(board)
    if move == "D": return reduceRight(board)
    return board

def countMissedOpportunities(before, after, move, track_nums):
    missed = 0
    size = len(before)

    for i in range(size):
        for j in range(size - 1):
            # horizontal pair
            if before[i][j] in track_nums and before[i][j] == before[i][j + 1]:
                if move in ["W", "S"]:
                    if not (after[i][j] == before[i][j] * 2 or after[i][j + 1] == before[i][j + 1] * 2):
                        missed += 1
        for j in range(size - 1):
            # vertical pair
            if before[j][i] in track_nums and before[j][i] == before[j + 1][i]:
                if move in ["A", "D"]:
                    if not (after[j][i] == before[j][i] * 2 or after[j + 1][i] == before[j + 1][i] * 2):
                        missed += 1
    return missed

def newGame():
    while True:
        try:
            size = int(input(Fore.CYAN + "\nEnter grid size: " + Fore.RESET))
            if size < 2:
                print(Fore.RED + "Grid size must be at least two" + Fore.RESET)
            else:
                break
        except ValueError:
            print(Fore.RED + "Grid size must be at least two" + Fore.RESET)

    print(Fore.MAGENTA + "Press W to move up, A to move left, S to move down, D to move right.")
    print("Press Q to quit. Press P to simulate. Press R to play randomly." + Fore.RESET)
    print(Fore.WHITE + "\n========================================================================" + Fore.RESET + "\n")
    print(Fore.GREEN + "INITIAL STATE:\n" + Fore.RESET)

    won = False
    moves = 0
    illegal_moves = 0
    a = newEmpty(size)
    randomInit(a)
    randomInit(a)
    state_count = 1
    prettyPrint(a, state_count)

    empty_space_total = sum(row.count(0) for row in a)
    missed_opportunities = 0

    while True:
        print(Fore.BLUE + "---------------------" + Fore.RESET)
        b = copy.deepcopy(a)
        key = input(Fore.BLUE + "Move: " + Fore.RESET).upper()

        if key == "P":
            sequence = input("What sequence of movements would you like to iterate on? ").upper()
            index = 0
            sim_moves = 0  # contador local
            while True:
                move = sequence[index % len(sequence)]
                temp = copy.deepcopy(a)
                reduced = applyMove(a, move)
                print(Fore.BLUE + "---------------------" + Fore.RESET)
                print(Fore.BLUE + f"Move: {move}" + Fore.RESET)
                if reduced == a:
                    print(Fore.RED + "No numbers were reduced. Ending simulation." + Fore.RESET)
                    break
                else:
                    a = reduced
                    randomNum(a)
                    sim_moves += 1
                    moves += 1
                    max_tile = max(max(row) for row in a)
                    if max_tile >= 16:
                        track_nums = [max_tile]
                        temp_val = max_tile
                        for _ in range(2):
                            temp_val //= 2
                            if temp_val >= 16:
                                track_nums.append(temp_val)
                        missed_opportunities += countMissedOpportunities(temp, a, move, track_nums)
                    empty_space_total += sum(row.count(0) for row in a)
                    state_count += 1
                    prettyPrint(a, state_count)
                    if isWin(a) and not won:
                        print("You win!")
                        won = True
                    elif isFail(a):
                        print(Fore.WHITE + "\n============================" + Fore.RESET)
                        print(Fore.RED + "Game over!" + Fore.RESET)
                        break
                index += 1

            print(Fore.CYAN + f"\nSimulation complete." + Fore.RESET)
            print(Fore.GREEN + f"Total simulated moves: " + Fore.WHITE + f"{sim_moves}" + Fore.RESET)
            continue


        if key == "R":
            directions = ["W", "A", "S", "D"]
            while not isFail(a):
                move = random.choice(directions)
                temp = copy.deepcopy(a)
                reduced = applyMove(a, move)
                print(Fore.BLUE + "---------------------" + Fore.RESET)
                print(Fore.BLUE + f"Move: {move}" + Fore.RESET)
                if reduced == a:
                    illegal_moves += 1
                    continue
                a = reduced
                randomNum(a)
                moves += 1
                max_tile = max(max(row) for row in a)
                if max_tile >= 16:
                    track_nums = [max_tile]
                    temp_val = max_tile
                    for _ in range(2):
                        temp_val //= 2
                        if temp_val >= 16:
                            track_nums.append(temp_val)
                    missed_opportunities += countMissedOpportunities(temp, a, move, track_nums)
                empty_space_total += sum(row.count(0) for row in a)
                state_count += 1
                prettyPrint(a, state_count)
                if isWin(a) and not won:
                    print("You win!")
                    won = True
                    break
            print(Fore.WHITE + "\n============================" + Fore.RESET)
            print(Fore.RED + "Game over!" + Fore.RESET)
            break

        if key == "W":   reduced = reduceUp(a)
        elif key == "A": reduced = reduceLeft(a)
        elif key == "S": reduced = reduceDown(a)
        elif key == "D": reduced = reduceRight(a)
        elif key == "Q": break
        else:
            print(Fore.RED + "Invalid move. Use W, A, S, D." + Fore.RESET)
            continue

        if reduced == a:
            print(Fore.RED + "No numbers were reduced." + Fore.RESET)
            illegal_moves += 1
        else:
            prev = copy.deepcopy(a)
            a = reduced
            randomNum(a)
            moves += 1
            max_tile = max(max(row) for row in a)
            if max_tile >= 16:
                track_nums = [max_tile]
                temp_val = max_tile
                for _ in range(2):
                    temp_val //= 2
                    if temp_val >= 16:
                        track_nums.append(temp_val)
                missed_opportunities += countMissedOpportunities(prev, a, key, track_nums)
            empty_space_total += sum(row.count(0) for row in a)
            state_count += 1

        prettyPrint(a, state_count)

        if isWin(a) and not won:
            print("You win!")
            won = True
        elif isFail(a):
            print(Fore.WHITE + "\n============================" + Fore.RESET)
            print(Fore.RED + "Game Over!" + Fore.RESET)
            break

    max_num = max(max(row) for row in a)
    final_sum = sum(sum(row) for row in a)
    mean_empty = empty_space_total / state_count if state_count > 0 else 0

    print(Fore.GREEN + f"Total moves: " + Fore.WHITE + f"{moves}" + Fore.RESET)
    print(Fore.GREEN + "Highest number achieved: " + color(max_num) + f"{max_num}" + Fore.RESET)
    print(Fore.GREEN + "Final sum: " + Fore.WHITE + f"{final_sum}" + Fore.RESET)
    print(Fore.GREEN + f"Average empty spaces: " + Fore.WHITE + f"{mean_empty:.2f}" + Fore.RESET)
    print(Fore.GREEN + f"Missed merge opportunities: " + Fore.WHITE + f"{missed_opportunities}" + Fore.RESET)
    print(Fore.GREEN + f"Illegal moves: " + Fore.WHITE + f"{illegal_moves}" + Fore.RESET)
    
    
    # Final score calculation
    weights = {
        "moves": 0.2,
        "highest": 0.25,
        "avg_empty": 0.05,
        "missed": 0.3,
        "illegal": 0.2
    }

    # Valores esperados dinámicos
    max_expected_sum = (2 ** (3 * size - 2)) * 1.5
    max_expected_moves = max_expected_sum / 2
    max_expected_avgempty = size*size*0.3
    max_expected_missed = 5
    max_expected_illegal = 10

    score = (
        weights["moves"] * min(1, moves / max_expected_moves) +
        weights["highest"] * min(1, final_sum / max_expected_sum) +
        weights["avg_empty"] * min(1, mean_empty / max_expected_avgempty) +
        weights["missed"] * (1 - min(1, missed_opportunities / max_expected_missed)) +
        weights["illegal"] * (1 - min(1, illegal_moves / max_expected_illegal))
    )

    print(Fore.MAGENTA + "FINAL SCORE: " + Fore.YELLOW + f"{score:.3f}" + Fore.RESET)

    
    print(Fore.WHITE + "============================\n" + Fore.RESET)

if __name__ == "__main__":
    newGame()
