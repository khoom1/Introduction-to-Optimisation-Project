from multiprocessing import Process, Pipe
import time
import numpy as np
from copy import deepcopy
from mygauss import gauss
from conversions import float2bin, bin2float

def quad_cost1(conn1,send_vec1,max_iter,A1,b1,xi_word_limit):
	coef_vect = deepcopy(b1)
	for i in range(max_iter):
		lamb_bin = conn1.recv()
		lamb_float = bin2float(lamb_bin)
		coef_vect[-1] = b1[-1] + lamb_float
		v1 = gauss(np.concatenate((A1,coef_vect),axis=1))
		# Simulate word limit on message send by Agent 2
		conn1.send(float2bin(v1[-1],xi_word_limit))
		send_vec1.send(v1)
		
		
def quad_cost2(conn3,send_vec2,max_iter,A2,b2,xi_word_limit):
	coef_vect = deepcopy(b2)
	for i in range(max_iter):
		lamb_bin = conn3.recv()
		lamb_float = bin2float(lamb_bin)
		coef_vect[0] = b2[0] -lamb_float
		v2 = gauss(np.concatenate((A2,coef_vect),axis=1))
		# Simulate word limit on message send by Agent 2
		conn3.send(float2bin(v2[0],xi_word_limit))
		send_vec2.send(v2)
	
def do_imprecise(max_iter,alpha,A1,A2,b1,b2,vstar,lambda_word_limit,xi_word_limit,verbose=False):
	error = np.zeros((max_iter,1))
	lamb = 1.0
	conn1, conn2 = Pipe()
	conn3, conn4 = Pipe()
	send_vec1, rec_vec1 = Pipe()
	send_vec2, rec_vec2 = Pipe()
	
	begin = time.time()
	d1 = Process(target=quad_cost1,args=(conn1,send_vec1,max_iter,A1,b1,xi_word_limit))
	d2 = Process(target=quad_cost2,args=(conn3,send_vec2,max_iter,A2,b2,xi_word_limit))
	d1.start()
	d2.start()
	for i in range(max_iter):
		# Simulate word limit on message sent to Agents 1 and 2
		lamb_bin = float2bin(lamb,lambda_word_limit)
		conn2.send(lamb_bin)
		conn4.send(lamb_bin)
		xi1 = conn2.recv()
		xi2 = conn4.recv()
		lamb = lamb - alpha*(bin2float(xi1)-bin2float(xi2))
		
		v1 = rec_vec1.recv()
		v2 = rec_vec2.recv()
		error[i] = np.linalg.norm(np.subtract(v1[:-1]+[v1[-1]/2+v2[0]/2]+v2[1:],vstar))
	d1.join()
	d2.join()
	end = time.time()
	
	if verbose:
		print("Dual decomposition in parallel takes %fs." %(end-begin))
	
	return error
	
	
	
	