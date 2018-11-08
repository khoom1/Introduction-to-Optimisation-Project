from multiprocessing import Process, Pipe
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
		
def perf_parallel(max_iter,size_problem,alpha):
	conn1, conn2 = Pipe()
	conn3, conn4 = Pipe()
	lamb = 1.0

	beg = time.time()
	d1 = Process(target=quad_cost1,args=(conn1,max_iter,size_problem))
	d2 = Process(target=quad_cost2,args=(conn3,max_iter,size_problem))
	
	d1.start()
	d2.start()
	
	for i in range(max_iter):
		conn2.send(lamb)
		conn4.send(lamb)
		eps1 = conn2.recv()
		eps2 = conn4.recv()
		lamb = lamb - alpha*(eps1-eps2)
		
	d1.join()
	d2.join()
	

	print(eps1-eps2)
	end = time.time()
	print(end-beg)