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

get_sudoku("testsudoku")
