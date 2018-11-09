import time
import numpy as np
from copy import deepcopy
from mygauss import gauss

def quad_cost1(lamb,A1,b1):
	coef_vect = deepcopy(b1)
	coef_vect[-1] = b1[-1] + lamb
	x = gauss(np.concatenate((A1,coef_vect),axis=1))
	return x[-1]

def quad_cost2(lamb,A2,b2):
	coef_vect = deepcopy(b2)
	coef_vect[0] = b2[0] - lamb
	x = gauss(np.concatenate((A2,coef_vect),axis=1))
	return x[0]
	
def do_serial(max_iter,alpha,A1,A2,b1,b2,verbose=False):
	lamb = 1.0
	eps1 = np.zeros((max_iter,1))
	eps2 = np.zeros((max_iter,1))
	
	begin = time.time()
	for i in range(max_iter):
		eps1[i] = quad_cost1(lamb,A1,b1)
		eps2[i] = quad_cost2(lamb,A2,b2)
		lamb = lamb - alpha*(eps1[i]-eps2[i])
	end = time.time()
	
	if verbose:
		print("Dual decomposition in series takes %fs." %(end-begin))
	
	return eps1,eps2,end-begin