# CSP_Solver
To run the program is needed python 3.4 or later, the files search.py, original.py and utils.py have been taken from
https://github.com/aimacode/aima-python as a base solver for general csp.

-The class sudokuCSP creates the objects needed for the general csp solver like neighbor, variables, domain for a sudoku game as a constraint satisfaction problem

-The file csp.py contains code from original.py (csp.py file from https://github.com/aimacode/aima-python) slightly modified, it doesnt use rare functions from other files (like ultis.py), the methods that have been modified are labelled with the comment "@modified"

*Note: the simple backtracking (without inference) from original.py required a lot of time to solve hard sudoku problems, now it requiers only some seconds to solve them.

-The file csp.py contains algorithms to solve csp, like backtracking with the 3 different methods for inference, mrv and some other methods.

-The class in gui.py contains code to create a graphic user interface for the game, allowing the user to choose a level (there are 6 different boards) and an infernet method for backtracking

-The file test.py contains code to execute tests for each inference algorithm on a sudoku board (it is possible to choose which board)

-The file Main.py contains a main method to run the gui program
