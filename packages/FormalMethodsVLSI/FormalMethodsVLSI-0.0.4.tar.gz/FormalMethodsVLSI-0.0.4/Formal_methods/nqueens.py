from z3 import *
from SAT import all_models
import matplotlib.pyplot as plt
# import sys

def Nqueens(n):
    # qi represents variable for row i to represent 
    # column in which a queen is present
    q = [Int(f"q{i}") for i in range(n)]
    #print(q)
    s = Solver()
    # columns should be between 1 and n
    constraints = [And(q[i] >= 0,q[i] <= n-1) for i in range(n)]
    # no 2 queens in the same column
    constraints.append(Distinct(q))
    # constraints.extend(q[i] != q[j] for i in range(n)
    #                    for j in range(i+1,n))
    # no 2 queens along the same diagonal
    constraints.extend(Abs(q[i] - q[j]) != abs(i - j)
                       for i in range(n) for j in range(i+1,n))
    s.add(constraints)
    return s,q

if __name__ == "__main__":
    n = int(input("Board size: "))
    s,q = Nqueens(n)
    solution = None
    for model in all_models(s,q):
        solution = map(model.eval,q)
        break
    if solution:
        # for i in range(n):
        #     for j in range(n):
        #         print(" Q " if solution[i]==j else " . ",end = '')
        #     print()
        for pos in solution:
            pos = pos.as_long()
            # print(type(pos))
            print(" . "*pos + " Q " + " . "*(n-1-pos))
    else:
        print(f"No solutions possible for Board size={n}") 
