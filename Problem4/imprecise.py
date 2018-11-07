from multiprocessing import Process, Pipe
import time
import numpy as np
from copy import deepcopy
from mygauss import gauss
from conversions import float2bin, bin2float

def quad_cost3(conn1,max_iter,A1,b1,places):
	coef_vect = deepcopy(b1)
	for i in range(max_iter):
		lamb_bin = conn1.recv()
		lamb_float = bin2float(lamb_bin,places)
		coef_vect[-1] = b1[-1] + lamb_float
		x = gauss(np.concatenate((A1,coef_vect),axis=1))
		conn1.send(x)
		
		
def quad_cost4(conn3,max_iter,A2,b2,places):
	coef_vect = deepcopy(b2)
	for i in range(max_iter):
		lamb_bin = conn3.recv()
		lamb_float = bin2float(lamb_bin,places)
		coef_vect[0] = b2[0] -lamb_float
		x = gauss(np.concatenate((A2,coef_vect),axis=1))
		conn3.send(x)
		
	
def do_imprecise(max_iter,alpha,A1,A2,b1,b2,xstar,places):
	size1 = len(b1)
	size2 = len(b2)
	
	error = np.zeros((max_iter,1))
	lamb = 1.0
	conn1, conn2 = Pipe()
	conn3, conn4 = Pipe()

	begin = time.time()
	d1 = Process(target=quad_cost3,args=(conn1,max_iter,A1,b1,places))
	d2 = Process(target=quad_cost4,args=(conn3,max_iter,A2,b2,places))
	
	d1.start()
	d2.start()
	
	for i in range(max_iter):
		lamb_bin = float2bin(lamb,places)
		conn2.send(lamb_bin)
		conn4.send(lamb_bin)
		v1 = conn2.recv()
		v2 = conn4.recv()
		lamb = lamb - alpha*(v1[-1]-v2[0])
		error[i] = np.linalg.norm(np.subtract(v1+v2,xstar))
	d1.join()
	d2.join()
	
	end = time.time()
	print("Dual decomposition in parallel takes %fs." %(end-begin))
	return error
	
	
	
	