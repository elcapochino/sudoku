import time
import os


def solve(sudoku, mode=-2, cooldown=0):

    zero_coords = []
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0:
                zero_coords.append((i, j))

    def error():
        os.system('cls')
        print("\n\nERROR: Sudoku has no solution\n")
        input()
        exit()

    def print_live():
        os.system('cls')
        print("\n\nSolving...\n\n")
        for i in range(9):
            line = ""
            for j in range(9):
                if j == 2 or j == 5:
                    if i == zero_coords[c][0] and j == zero_coords[c][1]:
                        line += "|" + str(sudoku[i][j]) + "|| "
                    else:
                        line += " " + str(sudoku[i][j]) + " | "
                else:
                    if i == zero_coords[c][0] and j == zero_coords[c][1]:
                        line += "|" + str(sudoku[i][j]) + "|"
                    else:
                        line += " " + str(sudoku[i][j]) + " "
            print(line)
            if i == 2 or i == 5:
                print("-------------------------------")

        print("\n\nIterations: %d" % depth)
        print("Checking for gap nr.: %d/%d   (row: %d column: %d)" %
              (c + 1, len(zero_coords), zero_coords[c][0]+1, zero_coords[c][1]+1))
        print("Time spent: %d minutes %s seconds" % (t / 60, round(t % 60, 1)))
        if t != 0: print("Speed: %s iterations/s" % round(depth / t, 1))

    def print_cooldown():
        nonlocal last_refresh
        os.system('cls')
        print("\n\nSolving...\n\n")
        print("Iterations:", int(depth / 1000), "thousand       (" + str(round(depth / 1000000, 2)) + " million)")
        print("Time spent:", str(int(t / 60)), "minutes", round(t % 60, 1), "seconds")
        if t != 0: print("Speed:", round(depth / t, 1),
              "iterations/s     (" + str(round(depth / t / 1000, 2)) + " iterations/ms)")
        print("\n\n(refreshing every", cooldown, "seconds)")

    def is_valid(z, s, num):
        for a in range(9):
            if sudoku[a][s] == num or sudoku[z][a] == num:
                return False
        for b in range(z - z % 3, z - z % 3 + 3):
            for c in range(s - s % 3, s - s % 3 + 3):
                if sudoku[b][c] == num:
                    return False
        return True

    def findnum(z, s):
        for num in range(sudoku[z][s] + 1, 10):
            if is_valid(z, s, num):
                sudoku[z][s] = num
                return True
        return False

    global c, depth
    c, depth, last_refresh = 0, 0, -1

    if mode == -1:
        try:
            mode = int(input("\nPlease choose between background-mode (0) and live-mode (1): "))
        except ValueError:
            mode = -2

    if cooldown == -1:
        try:
            cooldown = float(input("\nPlease enter cooldown: "))
        except ValueError:
            cooldown = 0
    if mode == 0 and cooldown == 0:
        cooldown = 5

    global t0
    t0 = time.time()

    while c < len(zero_coords):
        t = time.time()-t0
        if c < 0: error()
        if mode == 1:
            print_live()
            if cooldown > 0: time.sleep(cooldown)
        elif mode == 0 and int(t) % cooldown == 0 and int(t) != last_refresh:
            print_cooldown()
            last_refresh = int(t)
        depth += 1
        row = zero_coords[c][0]
        column = zero_coords[c][1]
        if findnum(row, column):
            c += 1
        else:
            sudoku[row][column] = 0
            c -= 1
    return sudoku


def get_sudoku(p_name="none"):
    if not os.path.exists("sudokus"):
        os.makedirs("sudokus")

    global name
    if p_name == "none":
        while True:
            try:
                os.system("cls")
                name = input("\n\nPlease enter sudoku name: ")
                file = open("sudokus\\"+name+".txt", "r")
                break
            except FileNotFoundError:
                pass
    else:
        name = p_name
        file = open("sudokus\\" + name + ".txt", "r")

    sudoku = []
    for line in file.readlines():
        if "\n" in line:
            sudoku.append(list(map(int, line[:-1].replace(" ", ""))))
        else:
            sudoku.append(list(map(int, line.replace(" ", ""))))
    file.close()
    return sudoku


def print_sudoku(sudoku):
    def print_info(type):
        if type == "its":
            if depth >= 1000000:
                print("\n\nIterations:", depth, "       (" + str(round(depth / 1000, 2)) +
                      " thousand)       (" + str(round(depth / 1000000, 2)) + " million)")
            elif depth >= 1000:
                print("\n\nIterations:", depth, "       (" + str(round(depth / 1000, 2)) + " thousand)")
            else:
                print("\n\nIterations:", depth)

        if type == "gaps":
            print("Gaps filled:", c)

        if type == "time":
            if t >= 60:
                print("Time spent:", str(int(t / 60)), "minutes", round(t % 60, 2), "seconds")
            elif t < 1:
                print("Time spent:", round(t, 2),
                      "seconds        (" + str(round(t * 1000, 2)) + " milliseconds)")
            else:
                print("Time spent:", round(t, 2), "seconds")

        if type == "speed":
            if int(depth / t) >= 1000:
                print("Speed:", round(depth / t, 1),
                      "iterations/s     (" + str(round(depth / t / 1000, 2)) + " iterations/ms)\n\n\n")
            else:
                print("Speed:", round(depth / t, 1), "iterations/s\n\n\n")

    for i in range(9):
        line = ""
        for j in range(9):
            if j == 2 or j == 5:
                line += " " + str(sudoku[i][j]) + " | "
            else:
                line += " " + str(sudoku[i][j]) + " "
        print(line)
        if i == 2 or i == 5:
            print("-------------------------------")
    try:
        t = time.time() - t0
        print_info("its")
        print_info("gaps")
        print_info("time")
        print_info("speed")
    except NameError:
        pass


sudoku_unsolved = get_sudoku()
sudoku_solved = solve(sudoku_unsolved, -1, -1)           # -1: ask; -2 or nothing: do auto (sudoku, mode, cooldown)
os.system("cls")
print("\n\nSudoku \"" + str(name) + "\" successfully solved!\n\n")
print_sudoku(sudoku_solved)

input()
