from multiprocessing import Process, Pipe
import time
import numpy as np
from copy import deepcopy
	
def quad_cost3(conn1,max_iter,A1,b1):
	coef_vect = deepcopy(b1)
	for i in range(max_iter):
		lamb = conn1.recv()
		coef_vect[-1] = b1[-1] + lamb
		x = np.linalg.solve(A1,coef_vect)
		conn1.send(x[-1])
		
		
def quad_cost4(conn3,max_iter,A2,b2):
	coef_vect = deepcopy(b2)
	for i in range(max_iter):
		lamb = conn3.recv()
		coef_vect[0] = b2[0] -lamb
		x = np.linalg.solve(A2,coef_vect)
		conn3.send(x[0])
		
	
def perf_parallel(max_iter,alpha,A1,A2,b1,b2):
	size1 = len(b1)
	size2 = len(b2)
	
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
		lamb = lamb - alpha*(v1-v2)
	
	d1.join()
	d2.join()
	
	end = time.time()
	print("Dual decomposition in parallel takes %fs." %(end-begin))
	