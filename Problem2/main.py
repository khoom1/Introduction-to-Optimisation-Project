from multiprocessing import Process, Value, Array
import time
from serial import perf_serial
from parallel import perf_parallel

max_iter = 1000
alpha = 0.1
size = 30

	

	
if __name__=='__main__':
	#perf_serial(max_iter,size_problem,alpha)
	perf_parallel(max_iter,alpha,size)

	

