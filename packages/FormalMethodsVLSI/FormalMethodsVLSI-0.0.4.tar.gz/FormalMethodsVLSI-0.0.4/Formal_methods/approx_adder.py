from z3 import *
from SAT.error_metrics import MAE

a = BitVec('a',9) 
b = BitVec('b',9)
constraints = []
s = Solver()
# Z3 does not support `==` for Bit vectors of 
# different size, so setting MSB bit of a,b 
# to 0
a8 = Extract(8,8,a)
b8 = Extract(8,8,b)
constraints.append(a8 == 0)
constraints.append(b8 == 0)
# exact result
out_exact = BitVec('out_exact',9) 
# constraint for exact addition
constraints.append(out_exact == a + b)


#all_solutions = list(all_models(s,[a,b,out_exact]))
#print(len(all_solutions))

out_approx = BitVec('out_approx',9)

a_3to0 = Extract(3,0,a)
b_3to0 = Extract(3,0,b)
out_approx_3to0 = Extract(3,0,out_approx)
# perform bitwise OR for LSB 4 bits
constraints.append(out_approx_3to0 == a_3to0|b_3to0)

a_8to4 = Extract(8,4,a)
b_8to4 = Extract(8,4,b)
out_approx_8to4 = Extract(8,4,out_approx)
# exact addition for MSB bits
constraints.append(out_approx_8to4 == a_8to4 + b_8to4)
s.add(constraints)


d = BitVec('d',9) # difference in outputs
# subtractor for worst-case error
constraints.append(d == out_exact - out_approx)
print(MAE(d,constraints,a,b,out_exact,out_approx,n=16))
# print(worstcase_error(d,constraints,9,a,b,out_approx,out_exact))
