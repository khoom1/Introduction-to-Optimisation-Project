import time
import numpy as np
from copy import deepcopy

def quad_cost1(lamb,A1,b1):
	coef_vect = deepcopy(b1)
	
	coef_vect[-1] = b1[-1] + lamb
	x = np.linalg.solve(A1,coef_vect)
	return x[-1]

def quad_cost2(lamb,A2,b2):
	coef_vect = deepcopy(b2)
	coef_vect[0] = b2[0] - lamb
	x = np.linalg.solve(A2,coef_vect)
	return x[0]
	
def perf_serial(max_iter,alpha,A1,A2,b1,b2):
	lamb = 1.0
	begin = time.time()
	
	for i in range(max_iter):
		eps1 = quad_cost1(lamb,A1,b1)
		eps2 = quad_cost2(lamb,A2,b2)
		lamb = lamb - alpha*(eps1-eps2)	
		
	
	end = time.time()
	print("Dual decomposition in series takes %fs." %(end-begin))