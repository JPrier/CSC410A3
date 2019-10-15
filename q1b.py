#!/usr/bin/env python3.7
# You cannot import any other modules. Put all your helper functions in this file.
from z3 import *
import itertools

def adjacent(r, n):
    """
    Takes a room number j and returns a list of all adjacent rooms numbers.
    """
    adj = []
    row = r // n
    col = r % n
    if row > 0: #Up
        adj.append(r - n)
    if row < n - 1: #Down
        adj.append(r + n)
    if col > 0: #Left
        adj.append(r - 1)
    if col < n - 1: #Right
        adj.append(r + 1)

    return adj

def coordinates(r, n):
    """
    Takes a room number r and returns the room's coordinates
    """
    row = r // n
    col = r % n

    return [col, row]

def decode(model, vars, n):
    """
    This function is only a helper suggestion to transform a model (the output of
    the solver) to a list of moves.
    To decode the model, you can query the values of the variables you defined.
    For this example, all_my_vars is a dictionnary of the solver variables used
    in the encoding.
    """
    moves = []
    path = [0] * (len(vars) + 1)

    for i in range(len(vars)):
        for j in range(len(vars[i])):
            if model.evaluate(vars[i][j]):
                # then var has been assigned to true,
                path[i + 1] = j

    for i in range(len(path) - 1):
        moves.append([coordinates(path[i], n), coordinates(path[i + 1], n)])

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
    # TODO : implement this function.
    # Suggestion: implement a decode function to decode the model returned by the solver.
    vars = []
    clauses = []

    rooms = n ** 2
    if n % 2: #If n is odd
        rooms -= 1

    #Create the variables
    for i in range(rooms):
        vars.append([])
        for j in range(n ** 2):
            vars[i].append(Bool("x_%i_%i" % (i,j)))

    #Add starting clauses
    clauses.append([vars[0][1], vars[0][n]]) #Move left or down from the starting room
    clauses.append(vars[rooms - 1][n ** 2 - 1]) #The bottom-right is the last room in the path

    #Every non-starting room appears at least once, every room appears at most once
    for j in range(n ** 2):
        clause1 = []
        for i in range(rooms):
            clause1.append(vars[i][j])

        if j:
            clauses.append(clause1)
        for pair in itertools.combinations(clause1, 2):
            clauses.append([Not(pair[0]), Not(pair[1])])

    #Each step on the path has at least one room, and at most one room
    for i in range(rooms):
        clause2 = []
        for j in range(n ** 2):
            clause2.append(vars[i][j])

        clauses.append(clause2)
        for pair in itertools.combinations(clause2, 2):
            clauses.append([Not(pair[0]), Not(pair[1])])

    #Consecutive steps have adjacent rooms
    for j in range(n ** 2):
        for i in range(rooms - 1):
            clause3 = [Not(vars[i][j])]
            for adj in adjacent(j, n):
                clause3.append(vars[i + 1][adj])
            clauses.append(clause3)

    #Create solver, add clauses and check
    s = Solver()

    for clause in clauses:
        s.add(Or(clause))

    if str(s.check()) == 'sat':
        return decode(s.model(), vars, n)
    else:
        return []

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
