from tkinter import *
from timeit import default_timer as timer
from tkinter import messagebox
import threading
import copy

from sudokucsp import SudokuCSP
# if you want to verify that my csp.py does a better job just change
# from csp import ... to from original import ...  , original is the csp.py file from AIMA code
from csp import backtracking_search, mrv, unordered_domain_values, forward_checking, mac, no_inference
MARGIN = 20  # Pixels around the board
SIDE = 50  # Width of every board cell
WIDTH_B = HEIGHT_B = MARGIN * 2 + SIDE * 9  # Width and height of the whole board
WIDTH = WIDTH_B + 180  # Width of board and buttons solve and reset


class SudokuUI(Frame):

    def __init__(self, parent):
        self.parent = parent
        # we start with a blank board
        self.original_board = [[0 for j in range(9)] for i in range(9)]
        # ofc we should have another board in which we will show solution
        self.current_board = copy.deepcopy(self.original_board)
        Frame.__init__(self, parent)
        self.row, self.col = 0, 0
        self.__initUI()

    def __initUI(self):
        # we will initializate stuff that will be shown in the gui
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self, width=WIDTH_B, height=HEIGHT_B)
        self.canvas.pack(fill=BOTH, side=TOP)
        self.canvas.grid(row=0, column=0, rowspan=30, columnspan=60)

        # level will be used to select the lvl of the board, 1 means easy and 2 hard
        self.level = IntVar(value=1)
        # which will be used to select which board at which lvl, there are 3 for each level
        self.which = 0

        # we will need a StringVar so that the client can see the time used by an algorithm
        self.time = StringVar()
        self.time.set("Time:                    ")
        # same for number of backtracks
        self.n_bt = StringVar()
        self.n_bt.set("N. BT:   ")

        self.make_menu()

        # the default will be the board of lvl 1 and which 1
        self.__change_level()

        self.clear_button = Button(self, text="Reset", command=self.__clear_board, width=15, height=5)
        self.clear_button.grid(row=10, column=61, padx=20, columnspan=3)
        self.solve_button = Button(self, text="Solve", command=self.solve_clicked, width=15, height=5)
        self.solve_button.grid(row=13, column=61, padx=20, columnspan=3)

        lbltime = Label(self, textvariable=self.time)
        lblBT = Label(self, textvariable=self.n_bt)

        Label(self, text="Inference:               ").grid(row=14, column=61)
        lbltime.grid(row=30, column=0)

        lblBT.grid(row=32, column=0)
        self.inference = StringVar()
        self.radio = []
        self.radio.append(Radiobutton(self, text="No Inference", variable=self.inference, value="NO_INFERENCE"))
        self.radio[0].grid(row=15, column=62, padx=2)
        self.radio.append(Radiobutton(self, text="FC                  ", variable=self.inference, value="FC"))
        self.radio[1].grid(row=16, column=62)
        self.radio.append(Radiobutton(self, text="MAC              ", variable=self.inference, value="MAC"))
        self.radio[2].grid(row=17, column=62)
        self.inference.set("NO_INFERENCE")

        Label(self, text="Variable to choose:").grid(row=18, column=61)
        lbltime.grid(row=30, column=0)

        lblBT.grid(row=32, column=0)

        self.var_to_choose = StringVar()
        self.radio.append(Radiobutton(self, text="MRV", variable=self.var_to_choose, value="MRV"))
        self.radio[3].grid(row=20, column=62)

        self.var_to_choose.set("MRV")

        self.__draw_grid()
        self.__draw_puzzle()

    def solve_clicked(self):

        # we are searching for a solution so it is good to disable buttons
        for rb in self.radio:
            rb.config(state=DISABLED)
        self.clear_button.config(state=DISABLED)
        self.solve_button.config(state=DISABLED)
        self.menu_bar.entryconfig("Level", state="disabled")
        p = threading.Thread(target=self.solve_sudoku)
        p.start()
        messagebox.showinfo("Working", "We are looking for a solution, please wait some seconds ...")

    def solve_sudoku(self):

        s = SudokuCSP(self.current_board)
        inf, dv, suv = None, None, None

        if self.inference.get() == "NO_INFERENCE":
            inf = no_inference
        elif self.inference.get() == "FC":
            inf = forward_checking
        elif self.inference.get() == "MAC":
            inf = mac

        if self.var_to_choose.get() == "MRV":
            suv = mrv

        start = timer()
        a = backtracking_search(s, select_unassigned_variable=suv, order_domain_values=unordered_domain_values,
                                inference=inf)
        end = timer()
        # if a isn't null we found a solution so we will show it in the current board
        # if a is null then we send a message to the user that the initial board
        # breaks some constraints
        if a:
            for i in range(9):
                for j in range(9):
                    index = i * 9 + j
                    self.current_board[i][j] = a.get("CELL" + str(index))
        else:
            messagebox.showerror("Error", "Invalid sudoku puzzle, please check the initial state")

        # showing solution
        self.__draw_puzzle()
        self.time.set("Time: "+str(round(end-start, 5))+" seconds")
        self.n_bt.set("N. BR: "+str(s.n_bt))

        # re-enabling buttons for search a new solution
        for rb in self.radio:
            rb.config(state=NORMAL)
        self.clear_button.config(state=NORMAL)
        self.solve_button.config(state=NORMAL)
        self.menu_bar.entryconfig("Level", state="normal")

    def make_menu(self):
        # creating menu with level Easy and Hard
        self.menu_bar = Menu(self.parent)
        self.parent.configure(menu=self.menu_bar)
        level_menu = Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="Level", menu=level_menu)
        level_menu.add_radiobutton(label="Easy", variable=self.level, value=1, command=self.__change_level)
        level_menu.add_radiobutton(label="Hard", variable=self.level, value=2, command=self.__change_level)

    def __change_level(self):
        # to add a new board, you just have to change %3 to %4 and then add another
        # clause elif like "elif self.which == 3:"
        self.which = (self.which+1) % 3
        if self.level.get() == 1:
            if self.which == 0:
                self.original_board[0] = [0, 6, 0, 3, 0, 0, 8, 0, 4]
                self.original_board[1] = [5, 3, 7, 0, 9, 0, 0, 0, 0]
                self.original_board[2] = [0, 4, 0, 0, 0, 6, 0, 0, 7]
                self.original_board[3] = [0, 9, 0, 0, 5, 0, 0, 0, 0]
                self.original_board[4] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                self.original_board[5] = [7, 1, 3, 0, 2, 0, 0, 4, 0]
                self.original_board[6] = [3, 0, 6, 4, 0, 0, 0, 1, 0]
                self.original_board[7] = [0, 0, 0, 0, 6, 0, 5, 2, 3]
                self.original_board[8] = [1, 0, 2, 0, 0, 9, 0, 8, 0]
            elif self.which == 1:
                self.original_board[0] = [7, 9, 0, 4, 0, 2, 3, 8, 1]
                self.original_board[1] = [5, 0, 3, 0, 0, 0, 9, 0, 0]
                self.original_board[2] = [0, 0, 0, 0, 3, 0, 0, 7, 0]
                self.original_board[3] = [0, 0, 0, 0, 0, 5, 0, 0, 2]
                self.original_board[4] = [9, 2, 0, 8, 1, 0, 7, 0, 0]
                self.original_board[5] = [4, 6, 0, 0, 0, 0, 5, 1, 9]
                self.original_board[6] = [0, 1, 0, 0, 0, 0, 2, 3, 8]
                self.original_board[7] = [8, 0, 0, 0, 4, 1, 0, 0, 0]
                self.original_board[8] = [0, 0, 9, 0, 8, 0, 1, 0, 4]
            elif self.which == 2:
                self.original_board[0] = [0, 3, 0, 5, 0, 6, 2, 0, 0]
                self.original_board[1] = [8, 2, 0, 0, 0, 1, 0, 0, 4]
                self.original_board[2] = [6, 0, 7, 8, 3, 0, 0, 9, 1]
                self.original_board[3] = [0, 0, 0, 0, 0, 0, 0, 2, 9]
                self.original_board[4] = [5, 0, 0, 6, 0, 7, 0, 0, 3]
                self.original_board[5] = [3, 9, 0, 0, 0, 0, 0, 0, 0]
                self.original_board[6] = [4, 5, 0, 0, 8, 9, 1, 0, 2]
                self.original_board[7] = [9, 0, 0, 1, 0, 0, 0, 4, 6]
                self.original_board[8] = [0, 0, 3, 7, 0, 4, 0, 5, 0]

        elif self.level.get() == 2:
            if self.which == 0:
                self.original_board[0] = [8, 0, 0, 0, 0, 0, 0, 0, 0]
                self.original_board[1] = [0, 0, 3, 6, 0, 0, 0, 0, 0]
                self.original_board[2] = [0, 7, 0, 0, 9, 0, 2, 0, 0]
                self.original_board[3] = [0, 5, 0, 0, 0, 7, 0, 0, 0]
                self.original_board[4] = [0, 0, 0, 0, 4, 5, 7, 0, 0]
                self.original_board[5] = [0, 0, 0, 1, 0, 0, 0, 3, 0]
                self.original_board[6] = [0, 0, 1, 0, 0, 0, 0, 6, 8]
                self.original_board[7] = [0, 0, 8, 5, 0, 0, 0, 1, 0]
                self.original_board[8] = [0, 9, 0, 0, 0, 0, 4, 0, 0]
            elif self.which == 1:
                self.original_board[0] = [2, 0, 0, 0, 0, 0, 0, 4, 3]
                self.original_board[1] = [1, 9, 0, 0, 3, 0, 0, 0, 0]
                self.original_board[2] = [0, 6, 0, 0, 0, 5, 0, 0, 0]
                self.original_board[3] = [0, 5, 0, 2, 6, 0, 0, 0, 8]
                self.original_board[4] = [0, 0, 0, 0, 7, 0, 0, 0, 0]
                self.original_board[5] = [6, 0, 0, 0, 5, 3, 0, 1, 0]
                self.original_board[6] = [0, 0, 0, 6, 0, 0, 0, 2, 0]
                self.original_board[7] = [0, 0, 0, 0, 8, 0, 0, 3, 4]
                self.original_board[8] = [9, 1, 0, 0, 0, 0, 0, 0, 6]
            elif self.which == 2:
                self.original_board[0] = [0, 0, 0, 0, 2, 0, 0, 0, 5]
                self.original_board[1] = [0, 0, 1, 6, 0, 0, 0, 0, 0]
                self.original_board[2] = [0, 6, 0, 7, 0, 0, 0, 8, 1]
                self.original_board[3] = [0, 0, 0, 3, 0, 0, 5, 0, 0]
                self.original_board[4] = [3, 0, 8, 5, 0, 6, 2, 0, 9]
                self.original_board[5] = [0, 0, 4, 0, 0, 7, 0, 0, 0]
                self.original_board[6] = [7, 4, 0, 0, 0, 9, 0, 1, 0]
                self.original_board[7] = [0, 0, 0, 0, 0, 5, 9, 0, 0]
                self.original_board[8] = [8, 0, 0, 0, 7, 0, 0, 0, 0]

        self.current_board = copy.deepcopy(self.original_board)

        self.__draw_puzzle()

    def __draw_grid(self):

        for i in range(10):
            if i % 3 == 0:
                color = "black"
            else:
                color = "gray"
            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT_B - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)
            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH_B - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def __draw_puzzle(self):
        self.canvas.delete("numbers")
        self.time.set("Time:                  ")
        self.n_bt.set("N. BT:   ")
        for i in range(9):
            for j in range(9):
                cell = self.current_board[i][j]
                if cell != 0:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2
                    if str(cell) == str(self.original_board[i][j]):
                        self.canvas.create_text(x, y, text=cell, tags="numbers", fill="black")
                    else:
                        self.canvas.create_text(x, y, text=cell, tags="numbers", fill="red")

    def __clear_board(self):
        self.current_board = copy.deepcopy(self.original_board)
        self.__draw_puzzle()




