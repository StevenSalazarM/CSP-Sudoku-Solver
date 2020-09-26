# Solver for Sudoku as a Constraint Satisfaction Problem 

This repository provides python scripts that allows to solve the Sudoku Game, show the solution with a Graphical User Interface and models the Sudoku Game as a CSP.

- original.py, utils.py and search.py are python scripts taken from Artificial Intelligence Modern Approach code. Those files have been included in this repository to show the performance obtained with respect to the original version (the results are shown in docs/original_results.txt).

- The file csp.py contains code from original.py (csp.py file from AIMA's code) slightly modified, it doesnt use rare functions from other files (like ultis.py), the methods that have been modified are labelled with the comment "@modified". Furthermore, this file contains algorithms to solve a CSP, like backtracking with the 3 different methods for inference, an heuristic like Most Recent Value, etc.

- sudokucsp.py contains the sudokuCSP class and it creates the objects needed for the general csp solver like neighbor, variables, domain for a sudoku game as a constraint satisfaction problem

- The class in gui.py contains code to create a graphic user interface for the game, allowing the user to choose a level (there are 6 different boards) and an inference method for backtracking

- The file test.py contains code to execute tests for each inference algorithm on a sudoku board (it is possible to choose which board)

- The file Main.py contains a main method to run the gui program

- Docs directory a document explaining the work and two txt files showing the different results obtained from AIMA's code and my code (AIMA's code modified)

- Levels directory contains screenshots showing sample levels used to measure the time of each back-tracking algorithm.

## Usage
The only requirement is to have python 3.4 or later. Then:

1. run Main.py or add your sudoku level to gui.py
<br><br>
<p align="center">
<img align="center" src="https://github.com/StevenSalazarM/CSP-Sudoku-Solver/blob/master/levels/Evil.png"></img>
</p>
<br><br>


If you have any question feel free to contact me at [stevensalazarmolina@gmail.com](mailto:stevensalazarmolina@gmail.com) or open an Issue in this repository.
