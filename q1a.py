#!/usr/bin/env python3.7
# You cannot import any other modules. Put all your helper functions in this file
from z3 import *
import itertools

def empty_cells(grid):
    """
    Takes a grid and returns the number of empty cells (cells that contain 0).
    """
    count = 0

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 0:
                count += 1

    return count

def adjacent(i, j, n, m):
    """
    Takes coordinates i, j and returns a list of all adjacent cell coordinates.
    """
    adj = []

    if i > 0: #Up
        adj.append([i - 1, j])
    if i < n - 1: #Down
        adj.append([i + 1, j])
    if j > 0: #Left
        adj.append([i, j - 1])
    if j < m - 1: #Right
        adj.append([i, j + 1])

    return adj

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

    # TODO : implement this function!
    if grid[pt_from[0]][pt_from[1]] or grid[pt_to[0]][pt_to[1]]:
        return False

    n = len(grid)
    m = len(grid[0])
    cells = empty_cells(grid)

    vars = []
    clauses = []

    #Create the variables
    for i in range(n):
        vars.append([])
        for j in range(m):
            vars[i].append([])
            if grid[i][j] == 0:
                for k in range(cells):
                    vars[i][j].append(Bool("x_%i_%i_%i" % (i,j,k)))

    #Path starts with pt_from and contains pt_to
    clauses.append([vars[pt_from[0]][pt_from[1]][0]])
    clauses.append(vars[pt_to[0]][pt_to[1]])

    #Every room appears at most once
    for i in range(n):
        for j in range(m):
            for pair in itertools.combinations(vars[i][j], 2):
                clauses.append([Not(pair[0]), Not(pair[1])])

    #Each step on the path has at most one room
    for k in range(cells):
        clause2 = []
        for i in range(n):
            for j in range(m):
                if grid[i][j] == 0:
                    clause2.append(vars[i][j][k])

        for pair in itertools.combinations(clause2, 2):
            clauses.append([Not(pair[0]), Not(pair[1])])

    #Consecutive steps have adjacent rooms
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 0 and (i != pt_to[0] or j != pt_to[1]):
                adj = adjacent(i, j, n, m)
                for k in range(cells - 1):
                    clause3 = [Not(vars[i][j][k])]
                    for r, c in adj:
                        if grid[r][c] == 0:
                            clause3.append(vars[r][c][k + 1])
                    clauses.append(clause3)

    #Create solver, add clauses and check
    s = Solver()
    for clause in clauses:
        s.add(Or(clause))
        
    return str(s.check()) == 'sat'

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
