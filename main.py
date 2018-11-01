from multiprocessing import Process, Value, Array
import time
from serial import perf_serial
from parallel import perf_parallel

max_iter = 100
alpha = 0.1


	

	
if __name__=='__main__':
	perf_serial(max_iter,alpha)
	perf_parallel(max_iter,alpha)

	

