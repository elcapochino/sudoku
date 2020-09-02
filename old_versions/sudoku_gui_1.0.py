from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import numpy as num
import time
from solve_sudoku import solve_sudoku

root = Tk()
root.title("Sudoku Solver")
bg = root['bg']
font = ('Verdana', 20)


def error(msg):
    messagebox.showerror("Error", msg)
    print("ERROR:", msg)


def solve():
    sudoku = []
    for i in range(9):
        sudoku.append([])
        for j in range(9):
            value = list_input[i][j]['text']
            if value == "":
                value = 0
            try:
                value = int(value)
            except ValueError:
                error("Invalid input in row %d column %d" % (i + 1, j + 1))
                return
            sudoku[i].append(value)
    insert_sudoku(solve_sudoku(sudoku))


def reset():
    global sel
    for i in list_input:
        for j in i:
            j.config(text="")
    sel = None
    update_sel()


def insert_sudoku(sudoku):
    for i in range(9):
        for j in range(9):
            value = sudoku[i][j]
            if value == 0:
                value = ""
            list_input[i][j].config(text=str(value))


def import_sudoku():
    filename = filedialog.askopenfilename(initialdir="/", title="Sudoku auswählen",
                                          filetypes=(("sudoku-files", "*.sd"), ("all files", "*.*")))
    if filename == "":
        return

    sudoku = []
    file = open(filename, "r")
    for line in file.readlines():
        if "\n" in line:
            sudoku.append(list(map(int, line[:-1].replace(" ", ""))))
        else:
            sudoku.append(list(map(int, line.replace(" ", ""))))
    file.close()

    insert_sudoku(sudoku)


def move_left():
    global sel
    if sel is None:
        return
    if sel[0] == 0 and sel[1] == 0:
        sel = (8, 8)
    elif sel[1] > 0:
        sel = (sel[0], sel[1] - 1)
    else:
        sel = (sel[0] - 1, 8)
    update_sel()


def move_right():
    global sel
    if sel is None:
        return
    if sel[0] == 8 and sel[1] == 8:
        sel = (0, 0)
    elif sel[1] < 8:
        sel = (sel[0], sel[1] + 1)
    else:
        sel = (sel[0] + 1, 0)
    update_sel()


def move_up():
    global sel
    if sel is None:
        return
    if sel[0] == 0:
        pass
    else:
        sel = (sel[0] - 1, sel[1])
    update_sel()


def move_down():
    global sel
    if sel is None:
        return
    if sel[0] == 8:
        pass
    else:
        sel = (sel[0] + 1, sel[1])
    update_sel()


def update_sel():
    for i in list_frame_input:  # reset all highlightings
        for j in i:
            j.config(highlightcolor="grey", highlightbackground="grey")
    if sel is not None:
        list_frame_input[sel[0]][sel[1]].config(highlightcolor="red", highlightbackground="red")


def click(event):
    global sel
    print("clicked")
    for i in range(9):  # get selection coords
        for j in range(9):
            if list_input[i][j] == event.widget:
                sel = (i, j)
    print(sel)
    update_sel()


def key_press(event):
    if event.char in map(str, list(range(1, 10))):
        list_input[sel[0]][sel[1]].config(text=event.char)


sel = None
frame_sudoku = Frame(root, highlightcolor="black", highlightbackground="black", highlightthickness=1)
frame_sudoku.pack(padx=20, pady=20)

list_input = []
list_frame_input = []
list_frame_block = []

for i in range(3):
    list_frame_block.append([])
    for j in range(3):
        frame = Frame(frame_sudoku, highlightcolor="black", highlightbackground="black", highlightthickness=1)
        list_frame_block[i].append(frame)
        frame.grid(row=i, column=j)

for i in range(9):
    list_input.append([])
    list_frame_input.append([])
    for j in range(9):
        frame = Frame(list_frame_block[i // 3][j // 3], highlightthickness=2)
        list_frame_input[i].append(frame)
        frame.grid(row=i % 3, column=j % 3)
        entry = Label(frame, width=2, font=font, justify=CENTER, text="")
        list_input[i].append(entry)
        entry.pack()

update_sel()

frame_btn = Frame(root, pady=15)
frame_btn.pack()
btn_solve = Button(frame_btn, padx=15, pady=5, text="Solve", command=solve)
btn_solve.pack(side=LEFT, padx=10)
btn_reset = Button(frame_btn, padx=15, pady=5, text="Reset", command=reset)
btn_reset.pack(side=LEFT, padx=10)
btn_import = Button(frame_btn, padx=15, pady=5, text="Open", command=import_sudoku)
btn_import.pack(side=LEFT, padx=10)

root.bind('<Up>', lambda x: move_up())
root.bind('<Down>', lambda x: move_down())
root.bind('<Left>', lambda x: move_left())
root.bind('<Right>', lambda x: move_right())
root.bind("<Button-1>", click)
root.bind('<Return>', lambda x: solve())
root.bind('<BackSpace>', lambda x: list_input[sel[0]][sel[1]].config(text=""))
root.bind('<Delete>', lambda x: list_input[sel[0]][sel[1]].config(text=""))
root.bind('<KeyPress>', key_press)
root.mainloop()
