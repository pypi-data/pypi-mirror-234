from typing import Iterable
from z3 import *
from .sat_count import model_count
from multiprocessing.pool import ThreadPool

__all__ = ["worstcase_error","worstcase_HD",
           "MSE","MAE"]

def worstcase_error(d: BitVecRef,constraints: Iterable[BoolRef],
                    *inputs: BitVecRef) -> int:
    """

    1. For each i from m-1 down to 0 checkif there is a 
    satisfying assignment for d which makes di(ith bit) 
    active
    2. If there is a satisfying assignment di add 2^i to 
    error.
    3. Use current satisfying assignment to reduce the no.
    of calls to SMT solver.
    4. If current satisfying assignment makes dj(jth bit of
    d) 0<=j<=i-1 active, no need to check for other 
    satisfying assignment for dj, add 2^j to error for each 
    such j from i-1 downto 0. Break if dj is not active for 
    current satisfying assignment
    """
    error = 0
    u = 1
    s = Solver() 
    s.add(constraints)
    m = d.size()
    i = m-1
    while i > 0:
        di = Extract(i,i,d) #ith bit of d
        # AND `di` with `u` as we need a satisfying 
        # assignment(if any) to make di active 
        # `s.push()` is to enable popping if 
        # ANDing `di` makes `u` unsatisfiable
        s.push()
        s.add((u & di) == 1)
        if s.check() == sat:
            u &= di
            error += 2**i
            solution = s.model().eval  
            block = Extract(i-1,0,d)
            bits = solution(block).as_binary_string()
            for bit in bits:
                if bit == '1':
                    i -= 1
                    di = Extract(i,i,d)
                    u &= di
                    error += 2**i
                else:
                    break
        else:
            s.pop()
        i -= 1
    # handle LSB bit separately
    d0 = Extract(0,0,d)
    s.add(u & d0 == 1)
    error += (s.check()==sat)
    return error

#worst-case hamming distance
def worstcase_HD(s: BitVecRef,constraints: Iterable[BoolRef],
                 *inputs: BitVecRef) -> int:
    """
    Count no.of 1's before the first occurence of 0 of the 
    sorted output using Binary search.
    """
    m = s.size()
    l,r = 0,m-1
    solver = Solver()
    while l<=r:
        # mid = ceil((l+r)/2)
        mid = ((l^r) >>1) + (l&r)
        s_mid = Extract(mid,mid,s)
        solver.push() #backtracking point
        solver.add(s_mid == 1)
        if solver.check() == sat:
            solution = solver.model().eval
            l = mid+1
            block = Extract(r,l,s)
            bits = solution(block).as_binary_string()
            # current assignment may be used to reduce
            # the calls to the SMT solver
            for bit in reversed(bits):
                if bit == '1':
                    l += 1
                else:
                    break
        else:
            solver.pop()
            r = mid-1
    # after first occurence of 0 is found, remaining bits are
    # all 0's as the output s is sorted in descending order
    return l

# TODO
def MSE(e: BitVecRef,constraints: Iterable[BoolRef],
        *inputs: BitVecRef,n = None) -> float:
    error = 0
    m = e.size()
    n = m if not n else n
    s = Solver()
    s.add(constraints)
    c = model_count(s,*inputs)


# Mean Absolute Error
def MAE(e: BitVecRef,constraints: Iterable[BoolRef],
        *inputs: BitVecRef,n = None) -> float:
    pool = ThreadPool(8) 
    error = 0
    m = e.size()
    # default input size is same as output size 
    # if input size is not specified
    n = n if n else m
    s = Solver() # solver with main context
    s.add(constraints)
    for i in range(m):
        error += pool.apply(contribution,(e,i,s,inputs))
    # close and sync the threads
    pool.close()
    pool.join() 
    error /= 2**n
    return error

def contribution(e: BitVecRef,i: int,s: Solver,
                 inputs: Iterable[BoolRef])->int:
    ''' 
    contribution of ei to Mean Absolute error,create new 
    context and copies of e,s for each thread to avoid 
    segmentation fault
    '''
    ctx = Context() # define a new context
    # solver and bit-vector copies with new context
    s_copy = s.translate(ctx) 
    inputs_copy = [var.translate(ctx) for var in inputs]
    e_copy = e.translate(ctx)
    ei = Extract(i,i,e_copy)
    s_copy.add(ei==1)
    SAT_count = model_count(s_copy,inputs_copy)
    error = SAT_count*2**i
    return error
