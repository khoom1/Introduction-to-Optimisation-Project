import time

def quad_cost1(lamb,size_problem):
	for i in range(size_problem):
		a=1
	return lamb/2

def quad_cost2(lamb,size_problem):
	for i in range(size_problem):
		a=1
	return -lamb/2
	
def perf_serial(max_iter,size_problem,alpha):
	lamb = 1.0
	start = time.time()
	for i in range(max_iter):
		eps1 = quad_cost1(lamb,size_problem)
		eps2 = quad_cost2(lamb,size_problem)
		lamb = lamb - alpha*(eps1-eps2)

	print(eps1-eps2)
	end = time.time()
	print(end-start)