# you can modify the csp file that you want to extend
# from original import * ... original is the one of AIMA's code
# but this class doesnt do anything different, i mean it will be the same if it
# extends the class on csp.py or original.py since both class are almost the same
from csp import *


class SudokuCSP(CSP):

    def __init__(self, board):

        self.domains = {}
        self.neighbors = {}
        # our variables will be named as "CELL NUMBER"
        for v in range(81):
            self.neighbors.update({'CELL' + str(v): {}})
        for i in range(9):
            for j in range(9):
                name = (i * 9 + j)
                var = "CELL"+str(name)
                self.add_neighbor(var, self.get_row(i) | self.get_column(j) | self.get_square(i, j))
                # if the board has a value in cell[i][j] the domain of this variable will be that number
                if board[i][j] != 0:
                    self.domains.update({var: str(board[i][j])})
                else:
                    self.domains.update({var: '123456789'})

        CSP.__init__(self, None, self.domains, self.neighbors, different_values_constraint)

    # returns the right square box given row and column index
    def get_square(self, i, j):
        if i < 3:
            if j < 3:
                return self.get_square_box(0)
            elif j < 6:
                return self.get_square_box(3)
            else:
                return self.get_square_box(6)
        elif i < 6:
            if j < 3:
                return self.get_square_box(27)
            elif j < 6:
                return self.get_square_box(30)
            else:
                return self.get_square_box(33)
        else:
            if j < 3:
                return self.get_square_box(54)
            elif j < 6:
                return self.get_square_box(57)
            else:
                return self.get_square_box(60)

    # returns the square of the index's variabile, it must be 0, 3, 6, 27, 30, 33, 54, 57 or 60
    def get_square_box(self, index):
        tmp = set()
        tmp.add("CELL"+str(index))
        tmp.add("CELL"+str(index+1))
        tmp.add("CELL"+str(index+2))
        tmp.add("CELL"+str(index+9))
        tmp.add("CELL"+str(index+10))
        tmp.add("CELL"+str(index+11))
        tmp.add("CELL"+str(index+18))
        tmp.add("CELL"+str(index+19))
        tmp.add("CELL"+str(index+20))
        return tmp

    def get_column(self, index):
        return {'CELL'+str(j) for j in range(index, index+81, 9)}

    def get_row(self, index):
            return {('CELL' + str(x + index * 9)) for x in range(9)}

    def add_neighbor(self, var, elements):
        # we dont want to add variable as its self neighbor
        self.neighbors.update({var: {x for x in elements if x != var}})

