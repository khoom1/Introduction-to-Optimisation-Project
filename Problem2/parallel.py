from multiprocessing import Process, Value, Array, Event
import time
import numpy as np
from scipy import random

#Generate well-conditioned, positive definite matrices
def create_pos_matrix(size):
	M = 10*random.rand(size,size)
	return np.matmul(M,M.transpose())

def create_vect(size):
	M = 10*random.rand(size,1)-5
	return M
	
def quad_cost3(l,vars1,ev1,ev2,max_iter,A1,b1):
	for i in range(max_iter):
		coef_vect = np.append(b1, l.value)
		x = np.linalg.solve(A1,coef_vect)
		for i in range(len(vars1)):
			vars1[i] = x[i]
		ev1.set()
		ev2.wait()
		ev2.clear()
		
def quad_cost4(l,vars2,ev3,ev4,max_iter,A2,b2):
	for i in range(max_iter):
		coef_vect = np.append(b2, -l.value)
		x = np.linalg.solve(A2,coef_vect)
		for i in range(len(vars2)):
			vars2[i] = x[i]
		ev3.set()
		ev4.wait()
		ev4.clear()
	
def combiner(l,alpha,vars1,vars2,ev1,ev2,ev3,ev4,max_iter):
	for i in range(max_iter):
		ev1.wait()
		ev3.wait()
		ev1.clear()
		ev3.clear()
		l.value = l.value - alpha*(vars1[-1]-vars2[-1])
		ev2.set()
		ev4.set()
		
def perf_parallel(max_iter,alpha,size):
	A1 = create_pos_matrix(size)
	A2 = create_pos_matrix(size)
	
	b1 = create_vect(size-1)
	b2 = create_vect(size-1)
	#print(np.append(b1,1.0))
	event1 = Event()
	event2 = Event()
	event3 = Event()
	event4 = Event()
	vars1 = Array('d',range(size))
	vars2 = Array('d',range(size))
	lamb = Value('d',1.0)

	beg = time.time()
	d1 = Process(target=quad_cost3,args=(lamb,vars1,event1,event2,max_iter,A1,b1))
	d2 = Process(target=quad_cost4,args=(lamb,vars2,event3,event4,max_iter,A2,b2))
	d3 = Process(target=combiner,args=(lamb,alpha,vars1,vars2,event1,event2,event3,event4,max_iter))
	
	d1.start()
	d2.start()
	d3.start()
	
	d1.join()
	d2.join()
	d3.join()	
	
	print(vars2[0])
	print(vars1[-1]-vars2[-1])
	end = time.time()
	print(end-beg)