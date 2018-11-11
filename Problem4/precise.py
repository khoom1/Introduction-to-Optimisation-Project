from multiprocessing import Process, Pipe
import time
import numpy as np
from copy import deepcopy
from mygauss import gauss

def quad_cost3(conn1,max_iter,A1,b1):
	coef_vect = deepcopy(b1)
	for i in range(max_iter):
		lamb = conn1.recv()
		coef_vect[-1] = b1[-1] + lamb
		v1 = gauss(np.concatenate((A1,coef_vect),axis=1))
		conn1.send(v1)
		
		
def quad_cost4(conn3,max_iter,A2,b2):
	coef_vect = deepcopy(b2)
	for i in range(max_iter):
		lamb = conn3.recv()
		coef_vect[0] = b2[0] -lamb
		v1 = gauss(np.concatenate((A2,coef_vect),axis=1))
		conn3.send(v1)
		
	
def do_precise(max_iter,alpha,A1,A2,b1,b2,vstar,verbose=False):
	error = np.zeros((max_iter,1))
	lamb = 1.0
	conn1, conn2 = Pipe()
	conn3, conn4 = Pipe()

	begin = time.time()
	d1 = Process(target=quad_cost3,args=(conn1,max_iter,A1,b1))
	d2 = Process(target=quad_cost4,args=(conn3,max_iter,A2,b2))
	d1.start()
	d2.start()
	for i in range(max_iter):
		conn2.send(lamb)
		conn4.send(lamb)
		v1 = conn2.recv()
		v2 = conn4.recv()
		lamb = lamb - alpha*(v1[-1]-v2[0])
		error[i] = np.linalg.norm(np.subtract(v1[:-1]+[v1[-1]/2+v2[0]/2]+v2[1:],vstar))
	d1.join()
	d2.join()
	end = time.time()
	
	if verbose:
		print("Dual decomposition in parallel takes %fs." %(end-begin))
		
	return error
	
	
	
	