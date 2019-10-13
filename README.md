# CSP_Solver
In order to run the program you should have installed python 3.4 or later, the files search.py, original.py and utils.py have been taken from AIMA's code (
https://github.com/aimacode/aima-python) as a base solver for general csp.

- original.py, utils.py and search.py arent needed to run main.py or test.py, those have been added just to show its performance on docs/original_results.txt

- The class sudokuCSP creates the objects needed for the general csp solver like neighbor, variables, domain for a sudoku game as a constraint satisfaction problem

- The file csp.py contains code from original.py (csp.py file from AIMA's code) slightly modified, it doesnt use rare functions from other files (like ultis.py), the methods that have been modified are labelled with the comment "@modified"

*Note: the simple backtracking (without inference) from original.py required a lot of time to solve hard sudoku problems, now it requiers only some seconds to solve them.

- The file csp.py contains algorithms to solve csp, like backtracking with the 3 different methods for inference, mrv and some other methods.

- The class in gui.py contains code to create a graphic user interface for the game, allowing the user to choose a level (there are 6 different boards) and an infernet method for backtracking

- The file test.py contains code to execute tests for each inference algorithm on a sudoku board (it is possible to choose which board)

- The file Main.py contains a main method to run the gui program



Two files have been added showing the difference between the original csp.py file from AIMA's code and this one modified. (check modified_results.txt and original_results.txt)

A pdf explaining the work (how to model the sudoku problem and tests) have been added, at the moment it is in italian but it may be traslated in future, if you have any question feel free to contact me at steven.salazar@stud.unifi.it 
