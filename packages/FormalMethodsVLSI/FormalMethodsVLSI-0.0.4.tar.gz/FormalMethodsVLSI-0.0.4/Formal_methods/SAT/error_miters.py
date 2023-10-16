from z3 import *


def comparator(x: BitVecRef,y: BitVecRef):
    # `If` is If-Then-Else(ITE)
    return (If(x>=y,x,y), #max
            If(x<=y,x,y)) #min

def Half_cleaner(b: BitVecRef):
    n = b.size()
    out = BitVec('out',n)
    constraints = []
    for i in range(n//2):
        pass

def Merger(s1: BitVecRef,s2: BitVecRef):
    """merges 2 sorted bit-vectors into 1 sorted bit-vector"""

# TODO
def Sorter(b: BitVecRef):
    ...

# TODO
def Sorting_network(d: BitVecRef):
    """
    Recursively divide bit-vector into 2 halves and sort the 
    top and bottom halves using `Sorter`.Merge both the halves 
    using `Merger`
    """
    n = d.size()
    if n == 1:
        return d
    d_top,d_bottom = Extract(n-1,n//2+1,d),Extract(n//2,0,d)
    Sorter(d_top),Sorter(d_bottom)
    
    ...







if __name__ == "__main__":
    x = BitVec('x',8)
    y = BitVec('y',8)
    s = Solver()
    s.add(x == 8)
    s.add(y == 8)
    s.check()
    print(s.model().eval(*comparator(x,y)))
