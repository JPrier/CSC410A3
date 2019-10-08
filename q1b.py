#!/usr/bin/env python3.7
# You cannot import any other modules. Put all your helper functions in this file.
from z3 import *
import itertools


def decode(model, all_my_vars):
    """
    This function is only a helper suggestion to transform a model (the output of
    the solver) to a list of moves.
    To decode the model, you can query the values of the variables you defined.
    For this example, all_my_vars is a dictionnary of the solver variables used
    in the encoding.
    """
    moves = []
    for k, my_var in all_my_vars.items():
        if model.evaluate(my_var):
            # then my_var has been assigned to true,
            moves = []
        else:
            # then my_var has been assigned to false,
            moves = []

    return moves

def encoding(n):
    """
    encoding takes an integer n > 0 and returns a list of moves. A move is a pair
    of cells (rooms) in the grid, for example [0,0],[1,0] is a move from cell (0,0) to cell
    (1,0).
    - If the killer cannot take a path from cell (0,0) to cell (n,n), return an
    empty list.
    - If the killer can find a path, return a list of moves, for example:
      [[[0,0],[1,0]],[[1,0],[2,0]], ...]
    - The moves do not have to be sorted in the right order, but they have to define a path
    that the "killer" can follow.
    """
    all_my_vars = {}
    # TODO : implement this function.
    # Suggestion: implement a decode function to decode the model returned by the solver.
    model = None
    return decode(model, all_my_vars)

# ================================================================================
#  Do not modify below!
# ================================================================================
if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Usage: python q1b.py GRID_SIZE\n\tWhere GRID_SIZE >= 2 is the size of the grid.")
        exit(1)

    N = int(sys.argv[1])
    if N < 2:
        print("Grid size should be at least 2.")
        exit(1)
    solution = encoding(N)
    if solution:
        print(solution)
    else:
        print("No solution.")
