# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: If a naked twin exists (i.e. two boxes in the same unit with the same two remaining potential values), we know that the two potential values have to be in one of the two boxes associated with the naked twin. This constraint introduces a new complementary constraint which tells us that the two values associated with the naked twin cannot be in any of the other boxes in the unit. This allows us to narrow the search space for subsequent iterations.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: In a diagonal sudoku, the two diagonals introduce two new units to the problems. Similar to the row, column, and square units, the diagonal units cannot have repeating numbers. Therefore, the various strategies such as the elimination strategy, only choice strategy, and naked twin strategy have to be applied to the diagonals as well, which further limit the search space at each iteration.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project.
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.
