#!/usr/bin/env python3.7
# You cannot import any other modules. Put all your helper functions in this file
from z3 import *
import itertools
import sys #python complained about sys not being defined


def encoding(pt_from, pt_to, grid):
    """
    The encoding function encodes the reachability problem in SAT and uses a solver to
    answer True if there is a path from pt_from to pt_to in grid, and False otherwise.
    pt_from -- a list of two integers, pt_from[0] is the row number of the starting point
               and pt_from[1] the column number.
    pt_to   -- a list of two integers, pt_to[0] is the row number of the end point, and
               and pt_to[1] the column number.
    grid    -- a list of lists of zeroes and ones, representing the grid, given row by row.
    """

    # You can assume that well_formed_problem(pt_from, pt_to, grid) returns True (see below)

    clauses = []

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 1:
                clauses += [Not(Bool("b_%i_%i" % (i,j)))]
            else:
                if [i,j] == pt_to:
                    clauses += [Bool("b_%i_%i" % (i,j))]
                    #add previous
                elif [i,j] == pt_from:
                    clauses += [Bool("b_%i_%i" % (i,j))]
                    #clauses += [Xor(get_possible(i,j,grid))] #next
                else:
                    #either not this move or next (previous covered by always getting next)
                    temp = get_possible(i,j,grid)
                    temp_xor = [Not(Bool("b_%i_%i" % (i,j)))]

                    if len(temp) > 0:
                        temp_xor = [Xor(temp_xor[0], temp[0])]
                    for i in range(len(temp) - 1):
                        temp_xor = [Xor(temp[i+1], temp_xor[0])]
                    clauses += temp_xor

    s = Solver()

    for clause in clauses:
        s.add(And(clause))

    print(str(s.check()))
    print(s.model())

    return False


def get_possible(i,j,grid):
    possible = []
    if i < len(grid) - 1 and grid[i+1][j] == 0:
        possible.append(Bool("b_%i_%i" % (i+1, j)))
    if i > 0 and grid[i-1][j] == 0:
        possible.append(Bool("b_%i_%i" % (i-1, j)))
    if j < len(grid[i]) - 1 and grid[i][j+1] == 0:
        possible.append(Bool("b_%i_%i" % (i, j+1)))
    if j > 0 and grid[i][j-1] == 0:
        possible.append(Bool("b_%i_%i" % (i, j-1)))
    return possible

# ================================================================================
#  Do not modify below!
# ================================================================================
def well_formed_problem(pt_from, pt_to, grid):
    """
    Check if the problem defined by (pt_from, pt_to, grid) is a well formed problem:
    - the grid is not empty and every row has the same length,
    - starting and end points are different and both are in the grid.
    """
    n = len(grid[1])
    if n < 1:
        return False
    m = len(grid[0])
    for line in grid:
        if len(line) != m:
            return False
    i0, j0 = pt_from[0], pt_from[1]
    iEnd, jEnd = pt_to[0], pt_to[1]

    if i0 == iEnd and j0 == jEnd:
        return False

    return (0 <= i0 < n) and (0 <= iEnd < n) and (0 <= j0 < m) and (0 <= jEnd < m)


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Usage: python q1a.py INPUT_FILE\n\tHint: test_input contains two valid input files.")
        exit(1)

    _grid = []
    with open(sys.argv[1], 'r') as input_grid:
        # The first line contains 4 ints separeted by spaces,
        _pts = [int(x) for x in input_grid.readline().strip().split(" ")]
        # the first two ints are the coordinates of the starting point,
        _pt_from = _pts[:2]
        # and the last to are the coordinates of the end point.
        _pt_to = _pts[2:]
        # Then, each new line is a line of the grid, starting from line 0.
        for line in input_grid.readlines():
            _grid.append([int(x) for x in line.split(" ")])

        if well_formed_problem(_pt_from, _pt_to, _grid):
            # Call the encoding function on the input.
            print(encoding(_pt_from, _pt_to, _grid))
            exit(0)
        else:
            print("The input file does not define a valid problem.")
            exit(1)
