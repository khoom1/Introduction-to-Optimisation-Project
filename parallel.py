from multiprocessing import Process, Value, Array
import time


max_iter = 100
alpha = 0.1

def quad_cost1(lamb):
	for i in range(10000000):
		a=1
	return [0,lamb/2]

def quad_cost2(lamb):
	for i in range(10000000):
		a=1
	return [0,-lamb/2]
	
def quad_cost3(l,e):
	for i in range(10000000):
		a=1
	e.value = l/2

def quad_cost4(l,e):
	for i in range(10000000):
		a=1
	e.value = -l/2
	
if __name__=='__main__':
	lamb = 1.0
	start = time.time()
	for i in range(max_iter):
		eps11 = quad_cost1(lamb)
		eps22 = quad_cost2(lamb)
		
		lamb = lamb - alpha*(eps11[1]-eps22[1])

	print(eps11[1]-eps22[1])
	end = time.time()
	print(end-start)

	eps1 = Value('d',0.0)
	eps2 = Value('d',0.0)
	lamb = 1.0
	beg = time.time()
	for i in range(max_iter):
	
		d1 = Process(target=quad_cost3,args=(lamb,eps1))
		d2 = Process(target=quad_cost4,args=(lamb,eps2))
		
		d1.start()
		d2.start()
		
		d1.join()
		d2.join()
		
		lamb = lamb - alpha*(eps1.value-eps2.value)

	print(eps1.value-eps2.value)
	end = time.time()
	print(end-beg)

