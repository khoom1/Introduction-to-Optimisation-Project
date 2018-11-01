from multiprocessing import Process, Value, Array, Event
import time
import numpy as np


coef_matrix1 = np.array([[2,0],[0,1.5]])
coef_matrix2 = np.array([[2,0],[0,0.25]])

def quad_cost3(l,vars1,ev1,ev2,max_iter):
	for i in range(max_iter):
		coef_vect = [0, l.value]
		x = np.linalg.solve(coef_matrix1,coef_vect)
		for i in range(len(vars1)):
			vars1[i] = x[i]
		ev1.set()
		ev2.wait()
		ev2.clear()
		
	

def quad_cost4(l,vars2,ev3,ev4,max_iter):
	for i in range(max_iter):
		coef_vect = [0, -l.value]
		x = np.linalg.solve(coef_matrix2,coef_vect)
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
		l.value = l.value - alpha*(vars1[1]-vars2[1])
		#print(vars1[:])
		ev2.set()
		ev4.set()
		
def perf_parallel(max_iter,alpha):
	event1 = Event()
	event2 = Event()
	event3 = Event()
	event4 = Event()
	vars1 = Array('d',range(2))
	vars2 = Array('d',range(2))
	lamb = Value('d',1.0)

	beg = time.time()
	d1 = Process(target=quad_cost3,args=(lamb,vars1,event1,event2,max_iter))
	d2 = Process(target=quad_cost4,args=(lamb,vars2,event3,event4,max_iter))
	d3 = Process(target=combiner,args=(lamb,alpha,vars1,vars2,event1,event2,event3,event4,max_iter))
	
	d1.start()
	d2.start()
	d3.start()
	
	d1.join()
	d2.join()
	d3.join()	
	

	print(vars1[1]-vars2[1])
	end = time.time()
	print(end-beg)