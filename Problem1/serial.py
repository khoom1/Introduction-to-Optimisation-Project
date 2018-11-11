import numpy as np
import time

def quad_cost1(lamb,size_problem):
	for i in range(size_problem):
		a=1
	return lamb/2

def quad_cost2(lamb,size_problem):
	for i in range(size_problem):
		a=1
	return -lamb/2
	
def do_serial(max_iter,alpha,size_problem=0,verbose=False):
	lamb = 1.0
	xi1 = np.zeros((max_iter,1))
	xi2 = np.zeros((max_iter,1))
	
	begin = time.time()
	for i in range(max_iter):
		xi1[i] = quad_cost1(lamb,size_problem)
		xi2[i] = quad_cost2(lamb,size_problem)
		lamb = lamb - alpha*(xi1[i]-xi2[i])
	end = time.time()
	
	if verbose:
		print(f"Size of dummy for-loop is {size_problem:d} iterations.",end=" ")
		print(f"Serial computing takes {end-begin:f}s.")
	
	return xi1,xi2,end-begin