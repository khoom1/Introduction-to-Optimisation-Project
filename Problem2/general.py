from multiprocessing import Process, Pipe
import numpy as np
import time
from scipy.optimize import minimize
import matplotlib.pyplot as plt

def agent1(conn1,max_iter,n,cost1):
	for i in range(max_iter):
		lamb = conn1.recv()
		res = minimize(cost1, np.ones((n+1,1)),args=lamb, method='nelder-mead', options={'xtol': 1e-8, 'disp': False})
		conn1.send(res.x[-1])
	

def agent2(conn3,max_iter,m,cost2):
	for i in range(max_iter):
		lamb = conn3.recv()
		res = minimize(cost2, np.ones((m+1,1)), args=lamb,method='nelder-mead', options={'xtol': 1e-8, 'disp': False})
		conn3.send(res.x[0])	
		
def do_general(max_iter,alpha,n,m,cost1,cost2,verbose=False):
	conn1, conn2 = Pipe()
	conn3, conn4 = Pipe()
	lamb = 1.0
	xi1 = np.zeros((max_iter,1))
	xi2 = np.zeros((max_iter,1))
	
	
	begin = time.time()
	d1 = Process(target=agent1,args=(conn1,max_iter,n,cost1))
	d2 = Process(target=agent2,args=(conn3,max_iter,m,cost2))
	d1.start()
	d2.start()
	for i in range(max_iter):
		conn2.send(lamb)
		conn4.send(lamb)
		xi1[i] = conn2.recv()
		xi2[i] = conn4.recv()
		lamb = lamb - alpha*(xi1[i]-xi2[i])
	d1.join()
	d2.join()
	end = time.time()
	
	if verbose:
		print(f"Size of dummy for-loop is {size_problem:d} iterations.",end=" ")
		print(f"Parallel computing takes {end-begin:f}s.")
	
	return xi1,xi2,end-begin
	
def fn1(x,lamb):
	function = 10*abs(x[0]) + x[1]**2 + x[0] + abs(x[1]*x[0])+x[1]
	return function - lamb*x[1]
	
def fn2(x,lamb):
	function = x[0]**2 + x[1]**2
	return  function + lamb*x[0]
	
if __name__=='__main__':
	max_iter = 100
	alpha = 0.1
	n = 1
	m = 1
	xi1,xi2,_ = do_general(max_iter,alpha,n,m,fn1,fn2)
	plt.figure(1)
	plt.plot(range(max_iter),xi1,label="Found By Agent 1")
	plt.plot(range(max_iter),xi2,label="Found By Agent 2")
	plt.title("Convergence of shared variable $x_3$")
	plt.xlabel("Number of iterations")
	plt.ylabel("Value of $x_3$")
	plt.legend()
	plt.show()
	