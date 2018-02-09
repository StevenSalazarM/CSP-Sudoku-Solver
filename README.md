# CSP_Solver
To run the program is needed python 3.4 or later, the files search.py, original.py and utils.py have been taken from
https://github.com/aimacode/aima-python as a base solver for general csp.

-The class sudokuCSP creates the objects needed for the general csp solver like neighbor, variables, domain for a sudoku game as a CSP problem

-The class in gui.py contains code to create a graphic user interface for the game, allowing the user to choose a level (there are 6 different boards) and an infernet method for backtracking

-The file test.py contains code to execute tests for each inference algorithm on a sudoku board (it is possible to choose which board)

-The file Main.py contains a main method to run the gui program
