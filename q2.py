#!/usr/bin/env python3.7
# You cannot import any other modules. Put all your helper functions in this file
from z3 import *
import itertools


def naive(literals, k):
    """
    Design your naive encoding of the at-most-k constraint.
    You are not allowed to create new variables for this encoding.
    The function returns the list of clauses that encode the at-most-k contraint.
    """
    clauses = []
    cs = list(itertools.combinations(literals, k + 1))
    for c in cs:
        xs = [Not(x) for x in c]
        clauses += [Or(xs)]
    return clauses


def sequential_counter(literals, k):
    """
    Implement the sequential counter encoding of the at-most-k constraint.
    You have to create new variables for this encoding.
    The function returns the list of clauses that encode the at-most-k constraint.
    """
    clauses = []
    # TODO: remove print statement below and implement the encoding.
    print("Sequential counter encoding not implemented.")
    return clauses

# Is the performance difference between the two encodings significant?

# TODO : your response in comments here.

# ================================================================================
#  Do not modify below!
# ================================================================================
import time

def test(encoding, n, k):
    """
    The following test encodes the constraint of having exactly k variables true by
    encoding at-most-k over (X_1, .., X_n) and at-least-k:
    - at-most-k is encoded by the encoding function given as argument.
    - at-least-k is encoded by encoding at-most-(n-k) on the negation of the variables.
    """
    X = []
    for i in range(n):
        X += [Bool("x%d" % i)]
    s = Solver()
    at_most_k = encoding(X, k)
    at_least_k = encoding([Not(x) for x in X], n - k)
    # Add all the clauses to the solver
    for clause in at_most_k + at_least_k:
        s.add(clause)
    # Should print sat
    start = time.time()
    resp = s.check()
    end = time.time()
    if str(resp) == "sat":
        m = s.model()
        count_true = 0
        for x in X:
            try:
                if m.evaluate(x):
                    count_true +=1
            except Z3Exception:
                pass
        if count_true == k:
            print("PASSED in %fs" % (end - start))
        else:
            print("FAILED")
    else:
        print("FAILED")


def usage():
    print("Usage: python q3.py E N K")
    print("      - E is 0 to use naive encoding or 1 to use sequential counter encoding.")
    print("      - K and N two integers such that N >= K > 2.")

if __name__ == '__main__':
    if len(sys.argv) < 4:
        usage()
        exit(1)
    e, n, k = int(sys.argv[1]) == 0, int(sys.argv[2]), int(sys.argv[3])
    if not (n >= k > 2):
        usage()
        exit(1)
    if e:
        test(naive, n, k)
    else:
        test(sequential_counter, n, k)
