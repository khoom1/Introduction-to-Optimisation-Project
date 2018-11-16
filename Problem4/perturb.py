from multiprocessing import Process, Pipe
import numpy as np
import time
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from conversions import float2bin, bin2float

def agent1(conn1,send_vec1,max_iter,n,xi_word_limit,cost1):
	for i in range(max_iter):
		lamb_bin = conn1.recv()
		lamb_float = bin2float(lamb_bin)
		res = minimize(cost1, np.ones((n+1,1)),args=lamb_float, method='nelder-mead', options={'xtol': 1e-8, 'disp': False})
		conn1.send(float2bin(res.x[-1],xi_word_limit))
		send_vec1.send(res.x)

def agent2(conn3,send_vec2,max_iter,m,xi_word_limit,cost2):
	for i in range(max_iter):
		lamb_bin = conn3.recv()
		lamb_float = bin2float(lamb_bin)
		res = minimize(cost2, np.ones((m+1,1)), args=lamb_float,method='nelder-mead', options={'xtol': 1e-8, 'disp': False})
		conn3.send(float2bin(res.x[0],xi_word_limit))
		send_vec2.send(res.x)
		
def do_general(max_iter,alpha,n,m,lambda_word_limit,xi_word_limit,cost1,cost2,verbose=False):
	conn1, conn2 = Pipe()
	conn3, conn4 = Pipe()
	send_vec1, rec_vec1 = Pipe()
	send_vec2, rec_vec2 = Pipe()
	lamb = np.zeros((max_iter+1,1))
	lamb[0] = 1.0
	lamb_rounded = np.zeros((max_iter,1))
	#xi1 = np.zeros((max_iter,1))
	#xi2 = np.zeros((max_iter,1))
	
	
	begin = time.time()
	d1 = Process(target=agent1,args=(conn1,send_vec1,max_iter,n,xi_word_limit,cost1))
	d2 = Process(target=agent2,args=(conn3,send_vec2,max_iter,m,xi_word_limit,cost2))
	d1.start()
	d2.start()
	for i in range(max_iter):
		lamb_bin = float2bin(lamb[i],lambda_word_limit)
		lamb_rounded[i] = bin2float(lamb_bin)
		conn2.send(lamb_bin)
		conn4.send(lamb_bin)
		xi1 = conn2.recv()
		xi2 = conn4.recv()
		lamb[i+1] = lamb[i] - alpha*(bin2float(xi1)-bin2float(xi2))
		v1 = rec_vec1.recv()
		v2 = rec_vec2.recv()
	d1.join()
	d2.join()
	end = time.time()
	
	if verbose:
		print(f"Size of dummy for-loop is {size_problem:d} iterations.",end=" ")
		print(f"Parallel computing takes {end-begin:f}s.")
	
	return v1,v2,lamb[-1],end-begin
	
def fn1(x,lamb):
	function = 10*abs(x[0]) + x[1]**2 + x[0] + abs(x[1]*x[0])+0.1*x[1]
	return function - lamb*x[1]
	
def fn2(x,lamb):
	function = x[0]**2 + x[1]**2
	return  function + lamb*x[0]
	
if __name__=='__main__':
	max_iter = 100
	alpha = 0.1
	n = 1
	m = 1
	large_limit = 100
	small_word_limit = 6
	exact_v1,exact_v2,exact_lamb,_ = do_general(max_iter,alpha,n,m,large_limit,large_limit,fn1,fn2)
	v1,v2,_,_ = do_general(max_iter,alpha,n,m,large_limit,small_word_limit,fn1,fn2)
	
	print(f"Perturbed primal value = {fn1(v1,0)+fn2(v2,0):f}")
	print(f"Exact primal value = {fn1(exact_v1,0)+fn2(exact_v2,0):f}")
	print(f"Lambda star = {exact_lamb[0]:f}")
	print(f"Perturbation/xi word limit = {small_word_limit:d}")
	
	
	
	