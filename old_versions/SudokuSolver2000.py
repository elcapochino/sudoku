import time
import os

sudoku = []

if not os.path.exists("sudokus"):
    os.makedirs("sudokus")

os.system("cls")
name = input("\n\nPlease enter sudoku name: ")
file = open("sudokus\\" + name + ".txt", "r")
for line in file.readlines():
    if "\n" in line:
        sudoku.append(list(map(int, line[:-1].replace(" ", ""))))
    else:
        sudoku.append(list(map(int, line.replace(" ", ""))))
file.close()

livemode = bool(int(input("\nPlease choose between background-mode (0) and live-mode (1): ")))

zero_coords = []
for i in range(9):
    for j in range(9):
        if sudoku[i][j] == 0:
            zero_coords_temp = [i, j]
            zero_coords.append(zero_coords_temp)


def findnum(z, s, start):
    for num in range(start + 1, 10):
        if is_valid(z, s, num):
            sudoku[z][s] = num
            # print(num, "fits!")
            return True
    return False


def is_valid(z, s, num):
    for a in range(9):
        if sudoku[a][s] == num or sudoku[z][a] == num:
            return False
    for b in range(z - z % 3, z - z % 3 + 3):
        for c in range(s - s % 3, s - s % 3 + 3):
            if sudoku[b][c] == num:
                return False
    return True


def solve(c):
    if findnum(zero_coords[c][0], zero_coords[c][1], sudoku[zero_coords[c][0]][zero_coords[c][1]]):
        # print("set zero nr.", c, "to", sudoku[zero_coords[c][0]][zero_coords[c][1]], ", moving on to next zero")
        c += 1
    else:
        # print("Nothing found to fill zero nr.", c, ":(. Set to 0 (initially",
        #      sudoku[zero_coords[c][0]][zero_coords[c][1]], ") and went back one zero")
        sudoku[zero_coords[c][0]][zero_coords[c][1]] = 0
        c -= 1
    return c


c, depth, last_refresh = 0, 0, -1
starttime = time.time()
# livemode = 1                # Switch between livemode (slower) and cooldown-mode (faster)
delay = 0  # Delay per iteration (in seconds)
cooldown = 3  # Cooldown for refreshing in cooldown-mode (in seconds, no fractions)

os.system('cls')

while c != len(zero_coords):
    dt = time.time() - starttime
    if livemode:
        os.system('cls')
        print("\n\nSolving...\n\n")

        for i in range(9):  # Printing the sudoku
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

        # Printing extra infos
        print("\n\nIterations:", depth)
        print("Checking for gap nr.: " + str(c + 1) + "/" + str(len(zero_coords)) +
              "     (row", str(zero_coords[c][0] + 1) + ",", "column", str(zero_coords[c][1] + 1) + ")")
        print("Time spent:", str(int(dt / 60)), "minutes", round(dt % 60, 1), "seconds")
        print("Speed:", round(depth / dt, 1), "iterations/s")

    elif int(dt) % cooldown == 0 and int(dt) != last_refresh:
        # cooldown-mode
        os.system('cls')
        print("\n\nSolving...\n\n")
        print("Iterations:", int(depth / 1000), "thousand       (" + str(round(depth / 1000000, 2)) + " million)")
        print("Time spent:", str(int(dt / 60)), "minutes", round(dt % 60, 1), "seconds")
        print("Speed:", round(depth / dt, 1),
              "iterations/s     (" + str(round(depth / dt / 1000, 2)) + " iterations/ms)")
        print("\n\n(refreshing every", cooldown, "seconds)")
        last_refresh = int(dt)

    if delay > 0:  # delay
        time.sleep(delay)
    if c < 0:  # error-message
        os.system('cls')
        print("\n\nERROR: Sudoku has no solution\n")
        exit()
    depth += 1
    c = solve(c)

# final screen
dt = time.time() - starttime
os.system('cls')
print("\n\nSudoku \"" + str(name) + "\" successfully solved!\n\n")
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

if depth >= 1000000:
    print("\n\nIterations:", depth, "       (" + str(round(depth / 1000, 2)) +
          " thousand)       (" + str(round(depth / 1000000, 2)) + " million)")
elif depth >= 1000:
    print("\n\nIterations:", depth, "       (" + str(round(depth / 1000, 2)) + " thousand)")
else:
    print("\n\nIterations:", depth)

print("Gaps filled:", c)

if dt >= 60:
    print("Time spent:", str(int(dt / 60)), "minutes", round(dt % 60, 2), "seconds")
elif dt < 1:
    print("Time spent:", round(dt, 2),
          "seconds        (" + str(round(dt * 1000, 2)) + " milliseconds)")
else:
    print("Time spent:", round(dt, 2), "seconds")

if int(depth / dt) >= 1000:
    print("Speed:", round(depth / dt, 1),
          "iterations/s     (" + str(round(depth / dt / 1000, 2)) + " iterations/ms)\n\n\n")
else:
    print("Speed:", round(depth / dt, 1), "iterations/s\n\n\n")

input()
