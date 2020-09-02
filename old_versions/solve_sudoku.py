import numpy as np
import copy
import time


def solve_sudoku(sudoku):
    def get_flip(sudoku):
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
        return dic.get(max(dic))

    def flip_matrix(sudoku, flip):
        if flip == 'b' or flip == 'd':
            sudoku = np.flip(sudoku, 1)
            # flip horizontally
        if flip == 'c' or flip == 'd':
            sudoku = np.flip(sudoku, 0)
            # flip vertically
        return sudoku

    def unflip_matrix(sudoku, flip):
        if flip == 'b':
            return np.flip(sudoku, 1)
            # flip horizontally
        elif flip == 'd':
            stemp = np.flip(sudoku, 1)
            return np.flip(stemp, 0)
        elif flip == 'c':
            return np.flip(sudoku, 0)
        return sudoku

    def check_possible_answers(row, column):  # check the possible answers for each square and save it in answer_list
        valid_values = []
        for value in range(1, 10):
            is_valid = True
            for i in range(9):
                if sudoku[i][column] == value or sudoku[row][i] == value:
                    is_valid = False
                if sudoku[row // 3 * 3 + i // 3][column // 3 * 3 + i % 3] == value:
                    is_valid = False
            if is_valid:
                valid_values.append(value)
        return valid_values

    def conflict(answer, row, column):  # check if answer in answer_list conflicts with numbers in row or column
        for counter in range(9):
            if answer == sudoku[row][counter] or answer == sudoku[counter][column]:
                return True
            if answer == sudoku[row // 3 * 3 + counter // 3][column // 3 * 3 + counter % 3]:
                return True
        return False

    def fill_box(c):
        if c == len(zero_list):  # if last field was filled successfully
            return True
        row, column = zero_list[c]
        for answer in answer_list[row][column]:
            if not conflict(answer, row, column):
                sudoku[row][column] = answer
                if fill_box(c + 1):
                    return True
            sudoku[row][column] = 0
        return False

    flip = get_flip(sudoku)
    sudoku = flip_matrix(sudoku, flip)  # flip the sudoku for the best starting position

    answer_list = []
    zero_list = []
    for i in range(9):  # create list containing the possible answers
        answer_list.append([])
        for j in range(9):
            answer_list[i].append(check_possible_answers(i, j))
            if sudoku[i][j] == 0:
                zero_list.append((i, j))

    fill_box(0)
    sudoku = unflip_matrix(sudoku, flip)
    return sudoku


# sudoku_easy = [[0, 0, 0, 2, 6, 0, 7, 0, 1], [6, 8, 0, 0, 7, 0, 0, 9, 0], [1, 9, 0, 0, 0, 4, 5, 0, 0],
#                [8, 2, 0, 1, 0, 0, 0, 4, 0], [0, 0, 4, 6, 0, 2, 9, 0, 0], [0, 5, 0, 0, 0, 3, 0, 2, 8],
#                [0, 0, 9, 3, 0, 0, 0, 7, 4], [0, 4, 0, 0, 5, 0, 0, 3, 6], [7, 0, 3, 0, 1, 8, 0, 0, 0]]
#
# sudoku_ultra = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 3, 0, 8, 5], [0, 0, 1, 0, 2, 0, 0, 0, 0],
#                 [0, 0, 0, 5, 0, 7, 0, 0, 0], [0, 0, 4, 0, 0, 0, 1, 0, 0], [0, 9, 0, 0, 0, 0, 0, 0, 0],
#                 [5, 0, 0, 0, 0, 0, 0, 7, 3], [0, 0, 2, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 4, 0, 0, 0, 9]]
#
# t0 = time.time()
# print(solve_sudoku(sudoku_ultra))
# print("Time:", time.time() - t0)
