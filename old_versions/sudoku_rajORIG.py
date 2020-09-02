import numpy as num
import copy

sudoku_answer = []


def SudokuSolve(Sudoku):
    sudoku_flip = 'a'
    global sudoku_answer

    def optimize_sudoku(sudoku):
        global sudoku_flip
        top_left = 0
        top_right = 0
        bottom_left = 0
        bottom_right = 0
        if sudoku[0][0] != 0:
            top_left += 3
        if sudoku[0][8] != 0:
            top_right += 3
        if sudoku[8][0] != 0:
            bottom_left += 3
        if sudoku[8][8] != 0:
            bottom_right += 3
        for i in range(9):
            if sudoku[0][i] != 0:
                top_left += 1
                top_right += 1
            if sudoku[i][0] != 0:
                top_left += 1
                bottom_left += 1
            if sudoku[8][i] != 0:
                bottom_left += 1
                bottom_right += 1
            if sudoku[i][8] != 0:
                top_right += 1
                bottom_right += 1
        dic = {top_left: 'a', top_right: 'b', bottom_left: 'c', bottom_right: 'd'}
        sudoku_flip = dic.get(max(dic))

    def flip_matrix(sudoku):
        optimize_sudoku(sudoku)
        if sudoku_flip == 'b' or sudoku_flip == 'd':  # check again if 0 and 1 are right for flip and if flip is stored or just operation
            sudoku = num.flip(sudoku, 1)
            # flip horizontally
        if sudoku_flip == 'c' or sudoku_flip == 'd':
            sudoku = num.flip(sudoku, 0)
            # flip vertically
        return sudoku

    org_sudoku = Sudoku
    answer_list = []
    is_solved = True

    for i in range(9):  # create list containing the possible answers
        answer_list.append([])
        for j in range(9):
            answer_list[i].append([])

    sudoku = flip_matrix(org_sudoku)  # flip the sudoku for the best starting position

    def check_possible_answers(row, column):  # check the possible answers for each square and save it in answer_list
        valid_values = []
        if sudoku[row][column] == 0:
            for value in range(1, 10):
                valid_value = True
                for counter in range(9):
                    if value == sudoku[row][counter] or value == sudoku[counter][column]:
                        valid_value = False
                        break
                if valid_value:
                    valid_values.append(value)
            if len(
                    valid_values) == 1:  # if there'solved_sudoku only one possible answer for the square, then put it in the sudoku
                sudoku[row][column] = valid_values[0]
        return valid_values

    def conflict(answer, row, column):  # check if answer in answer_list conflicts with numbers in row or column
        for counter in range(9):
            if answer == sudoku[row][counter] or answer == sudoku[counter][column] or answer == \
                    sudoku[row // 3 * 3 + counter // 3][column // 3 * 3 + counter % 3]:
                return True
        return False

    def fill_box(row, column):
        global is_solved
        global sudoku_answer
        if row == 8 and column == 8:  # if at the end of the sudoku
            if sudoku[8][8] != 0:
                is_solved = True
            for answer in answer_list[8][8]:
                if not conflict(answer, 8, 8):
                    sudoku[8][8] = answer
                    is_solved = True
                    break
            if not is_solved:
                return False
            else:
                if sudoku_flip == 'b':
                    solved_sudoku = num.flip(sudoku, 1)
                    # flip horizontally
                elif sudoku_flip == 'd':
                    stemp = num.flip(sudoku, 1)
                    solved_sudoku = num.flip(stemp, 0)
                elif sudoku_flip == 'c':
                    solved_sudoku = num.flip(sudoku, 0)
                else:
                    solved_sudoku = sudoku
                sudoku_answer = copy.deepcopy(solved_sudoku)  # **************************************
        if sudoku[row][column] == 0:  # if block is empty
            for answer in answer_list[row][column]:
                if not conflict(answer, row, column):
                    sudoku[row][column] = answer
                    if column == 8 and row == 8:
                        is_solved = True
                    elif column == 8:
                        fill_box(row + 1, 0)  # *******************
                    else:
                        fill_box(row, column + 1)  # *******************
                sudoku[row][column] = 0
                if answer == answer_list[row][column][-1]:
                    return False
        elif row == 8 and column == 8:
            is_solved = True
        elif column == 8:
            fill_box(row + 1, 0)  # *******************
        else:
            fill_box(row, column + 1)  # *******************

    for row in range(9):
        for column in range(9):
            answer_list[row][column] = check_possible_answers(row, column)
            if answer_list[row][column]:
                is_solved = False
    fill_box(0, 0)
    return sudoku_answer


sudoku = [[0, 0, 0, 2, 6, 0, 7, 0, 1], [6, 8, 0, 0, 7, 0, 0, 9, 0], [1, 9, 0, 0, 0, 4, 5, 0, 0],
          [8, 2, 0, 1, 0, 0, 0, 4, 0], [0, 0, 4, 6, 0, 2, 9, 0, 0], [0, 5, 0, 0, 0, 3, 0, 2, 8],
          [0, 0, 9, 3, 0, 0, 0, 7, 4], [0, 4, 0, 0, 5, 0, 0, 3, 6], [7, 0, 3, 0, 1, 8, 0, 0, 0]]
print(SudokuSolve(sudoku))
