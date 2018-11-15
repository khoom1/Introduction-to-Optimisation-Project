import time
import numpy as np
from copy import deepcopy
from mygauss import gauss

def agent1(lamb,A1,b1):
	coef_vect = deepcopy(b1)
	coef_vect[-1] = b1[-1] + lamb
	v1 = gauss(np.concatenate((A1,coef_vect),axis=1))
	return v1[-1]

def agent2(lamb,A2,b2):
	coef_vect = deepcopy(b2)
	coef_vect[0] = b2[0] - lamb
	v2 = gauss(np.concatenate((A2,coef_vect),axis=1))
	return v2[0]
	
def do_serial(max_iter,alpha,A1,A2,b1,b2,verbose=False):
	lamb = 1.0
	xi1 = np.zeros((max_iter,1))
	xi2 = np.zeros((max_iter,1))
	
	begin = time.time()
	for i in range(max_iter):
		xi1[i] = agent1(lamb,A1,b1)
		xi2[i] = agent2(lamb,A2,b2)
		lamb = lamb - alpha*(xi1[i]-xi2[i])
	end = time.time()
	
	if verbose:
		print("Dual decomposition in series takes %fs." %(end-begin))
	
	return xi1,xi2,end-begin