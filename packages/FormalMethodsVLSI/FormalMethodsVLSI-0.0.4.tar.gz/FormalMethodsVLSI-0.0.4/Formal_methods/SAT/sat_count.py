from z3 import *
from typing import Iterable,Union
#import pdb
#import sys
#sys.setrecursionlimit(1000000)
T = Union[BitVecRef,BoolRef,ArithRef]
#`set_param("parallel.enable",True)

def model_count(solver: Solver,terms: Iterable[T])->int: 
    def count_rec(solver: Solver,terms: Iterable[T],
                  start: int,count: int)->int:
        """see https://theory.stanford.edu/%7Enikolaj/programmingz3.html#sec-blocking-evaluations"""
        if solver.check() == sat:
            m = solver.model()
            count += 1
            for i in range(start,len(terms)):
                solver.push()
                solver.add(terms[i] != m.eval(terms[i],True))   
                for j in range(start,i):
                    solver.add(terms[j] == m.eval(terms[j],True))
                count = count_rec(solver,terms,i,count)
                solver.pop()
        return count
    return count_rec(solver,terms,0,0)

def all_models(solver: Solver,terms: Iterable[T]): 
    def all_models_rec(solver: Solver,terms: Iterable[T],start):
        if solver.check() == sat:
            m = solver.model()
            yield m
            for i in range(start,len(terms)):
                solver.push()
                solver.add(terms[i] != m.eval(terms[i],True))
                for j in range(start,i):
                    solver.add(terms[j] == m.eval(terms[j],True))
                yield from all_models_rec(solver,terms,i)
                solver.pop()
    yield from all_models_rec(solver,terms,0)
