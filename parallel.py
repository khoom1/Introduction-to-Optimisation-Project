from multiprocessing import Process, Value, Array, Event
import time

size_problem = 1000000

def quad_cost3(l,e,ev1,ev2,max_iter):
	for i in range(max_iter):
		for i in range(size_problem):
			a=1
		e.value = l.value/2
		ev1.set()
		ev2.wait()
		ev2.clear()
		
	

def quad_cost4(l,e,ev3,ev4,max_iter):
	for i in range(max_iter):
		for i in range(size_problem):
			a=1
		e.value = -l.value/2
		ev3.set()
		ev4.wait()
		ev4.clear()
	
def combiner(l,alpha,ep1,ep2,ev1,ev2,ev3,ev4,max_iter):
	for i in range(max_iter):
		ev1.wait()
		ev3.wait()
		ev1.clear()
		ev3.clear()
		l.value = l.value - alpha*(ep1.value-ep2.value)
		ev2.set()
		ev4.set()
		
def perf_parallel(max_iter,alpha):
	event1 = Event()
	event2 = Event()
	event3 = Event()
	event4 = Event()
	eps1 = Value('d',0.0)
	eps2 = Value('d',0.0)
	lamb = Value('d',1.0)

	beg = time.time()
	d1 = Process(target=quad_cost3,args=(lamb,eps1,event1,event2,max_iter))
	d2 = Process(target=quad_cost4,args=(lamb,eps2,event3,event4,max_iter))
	d3 = Process(target=combiner,args=(lamb,alpha,eps1,eps2,event1,event2,event3,event4,max_iter))
	
	d1.start()
	d2.start()
	d3.start()
	
	d1.join()
	d2.join()
	d3.join()	
	

	print(eps1.value-eps2.value)
	end = time.time()
	print(end-beg)