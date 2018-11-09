import numpy as np
from serial import do_serial
from parallel import do_parallel
import matplotlib.pyplot as plt

if __name__=='__main__':
	# Plot convergence of the shared variable x_3
	max_iter = 100
	alpha = 0.1
	par_eps1, par_eps2, time2 = do_parallel(max_iter,alpha)
	plt.figure(1)
	plt.plot(range(max_iter),par_eps1,label="Found By Agent 1")
	plt.plot(range(max_iter),par_eps2,label="Found By Agent 2")
	plt.title("Convergence of shared variable $x_3$")
	plt.xlabel("Number of iterations")
	plt.ylabel("Value of $x_3$")
	plt.legend()
	
	# Run tests to compare the completion times of parallel and serial
	# computation for increasing problem size.
	num_tests = 14
	size_problem = [2**(i+7) for i in range(num_tests)]
	time1 = np.zeros((num_tests,1))
	time2 = np.zeros((num_tests,1))
	for i in range(num_tests):
		_, _, time1[i] = do_serial(max_iter,alpha,size_problem[i],True)
		_, _, time2[i] = do_parallel(max_iter,alpha,size_problem[i],True)
		print("\n")
	
	plt.figure(2)
	plt.plot(size_problem,time1,'bx',label="Serial Execution")
	plt.plot(size_problem,time2,'rx',label="Parallel Execution")
	plt.title("Time trials comparing parallel vs. serial computing")
	plt.xlabel("Number of iterations in dummy for-loop")
	plt.ylabel("Completion time (s)")
	plt.legend()
	
	plt.show()
	
	

