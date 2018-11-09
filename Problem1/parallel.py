from multiprocessing import Process, Pipe
import numpy as np
import time

def quad_cost1(conn1,max_iter,size_problem):
	for i in range(max_iter):
		lamb = conn1.recv()
		for i in range(size_problem):
			a=1
		eps1 = lamb/2
		conn1.send(eps1)
	

def quad_cost2(conn3,max_iter,size_problem):
	for i in range(max_iter):
		lamb = conn3.recv()
		for i in range(size_problem):
			a=1
		eps2 = -lamb/2
		conn3.send(eps2)	
		
def do_parallel(max_iter,alpha,size_problem=0,verbose=False):
	conn1, conn2 = Pipe()
	conn3, conn4 = Pipe()
	lamb = 1.0
	eps1 = np.zeros((max_iter,1))
	eps2 = np.zeros((max_iter,1))
	
	begin = time.time()
	d1 = Process(target=quad_cost1,args=(conn1,max_iter,size_problem))
	d2 = Process(target=quad_cost2,args=(conn3,max_iter,size_problem))
	d1.start()
	d2.start()
	for i in range(max_iter):
		conn2.send(lamb)
		conn4.send(lamb)
		eps1[i] = conn2.recv()
		eps2[i] = conn4.recv()
		lamb = lamb - alpha*(eps1[i]-eps2[i])
	d1.join()
	d2.join()
	end = time.time()
	
	if verbose:
		print(f"Size of dummy for-loop is {size_problem:d} iterations.",end=" ")
		print(f"Parallel computing takes {end-begin:f}s.")
	
	return eps1,eps2,end-begin