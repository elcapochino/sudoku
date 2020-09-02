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
            value = input_list[i][j]['text']
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
    for i in input_list:
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
            input_list[i][j].config(text=str(value))


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

    print("Eingelesenes Sudoku:")
    print(sudoku)
    insert_sudoku(sudoku)


def key_left(x):
    return


def key_right(x):
    return


def key_up(x):
    return


def key_down(x):
    return


def update_sel():
    for i in frame_list:  # reset all highlightings
        for j in i:
            j.config(highlightcolor="grey", highlightbackground="grey")
    if sel is None:
        return
    frame_list[sel[0]][sel[1]].config(highlightcolor="red", highlightbackground="red")


def click(event):
    global sel
    print("clicked")
    for i in range(9):  # get selection coords
        for j in range(9):
            if input_list[i][j] == event.widget:
                sel = (i, j)
    print(sel)
    update_sel()


def press_num(event):
    if event.char in map(str, list(range(1, 10))):
        input_list[sel[0]][sel[1]].config(text=event.char)


sel = None
frame_sudoku = Frame(root, highlightcolor="black", highlightbackground="black", highlightthickness=1)

input_list = []
frame_list = []
for i in range(9):
    input_list.append([])
    frame_list.append([])
    frame_block = Frame(frame_sudoku, highlightcolor="black", highlightbackground="black", highlightthickness=1)
    frame_block.grid(row=i // 3, column=i % 3)
    for j in range(9):
        frame = Frame(frame_block, highlightcolor="red", highlightthickness=1)
        frame_list[i].append(frame)
        frame.grid(row=j // 3, column=j % 3)
        entry = Label(frame, width=2, font=font, justify=CENTER, highlightcolor="red", text="")
        input_list[i].append(entry)
        entry.pack()
update_sel()

frame_sudoku.pack(padx=20, pady=20)
frame_btn = Frame(root, pady=15)
frame_btn.pack()
btn_solve = Button(frame_btn, padx=15, pady=5, text="Solve", command=solve)
btn_solve.pack(side=LEFT, padx=10)
btn_reset = Button(frame_btn, padx=15, pady=5, text="Reset", command=reset)
btn_reset.pack(side=LEFT, padx=10)
btn_import = Button(frame_btn, padx=15, pady=5, text="Open", command=import_sudoku)
btn_import.pack(side=LEFT, padx=10)

root.bind("<Button-1>", click)
root.bind('<Left>', key_left)
root.bind('<Right>', key_right)
root.bind('<Up>', key_up)
root.bind('<Down>', key_down)
root.bind('<Return>', lambda x: solve())
root.bind('<BackSpace>', lambda x: input_list[sel[0]][sel[1]].config(text=""))
root.bind('<Delete>', lambda x: input_list[sel[0]][sel[1]].config(text=""))
root.bind('<KeyPress>', press_num)
root.mainloop()
