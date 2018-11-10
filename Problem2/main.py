from serial import do_serial
from parallel import do_parallel
from check_solution import do_check
from scipy import random
import numpy as np
import matplotlib.pyplot as plt

#Generate well-conditioned, positive definite matrices
#(all eigenvalues larger than or equal to 0.5)
def create_pos_matrix(size):
	M = 10*random.rand(size,size)
	P = np.matmul(M,M.transpose())
	eigval, eigvec = np.linalg.eig(P)
	while (min(eigval)<0.5):
		M = 10*random.rand(size,size)
		P = np.matmul(M,M.transpose())
		eigval, eigvec = np.linalg.eig(P)
	return P

def create_vect(size):
	M = 10*random.rand(size,1)-5
	return M



if __name__=='__main__':
	# Generate example
	size1 = 10
	size2 = 5
	print("Generating an example problem...")
	A1 = create_pos_matrix(size1)
	A2 = create_pos_matrix(size2)
	b1 = create_vect(size1)
	b2 = create_vect(size2)
	print("Done generating matrices.\n")
	
	# Variable x3 found by minimising cost function without separating
	true_x3,_ = do_check(A1,A2,b1,b2)
	
	# Plot convergence of the shared variable x_3
	max_iter = 1000
	alpha = 0.1
	par_eps1, par_eps2, _ = do_parallel(max_iter,alpha,A1,A2,b1,b2)
	plt.figure(1)
	plt.plot(range(max_iter),par_eps1,label="Found By Agent 1")
	plt.plot(range(max_iter),par_eps2,label="Found By Agent 2")
	plt.plot(range(max_iter),true_x3*np.ones((max_iter,1)),'--',label="Found By Not Separating")
	plt.title("Convergence of shared variable $z$")
	plt.xlabel("Number of iterations")
	plt.ylabel("Value of $z$")
	plt.legend()
	
	
	
	
	# Run tests to compare the completion times of parallel and serial
	# computation for increasing problem size.
	num_tests = 15
	size_problem = [i+13 for i in range(num_tests)]
	time1 = np.zeros((num_tests,1))
	time2 = np.zeros((num_tests,1))
	for i in range(num_tests):
		print(f"Generating a problem of size {size_problem[i]:d}...")
		A1 = create_pos_matrix(size_problem[i])
		A2 = create_pos_matrix(size_problem[i])
		b1 = create_vect(size_problem[i])
		b2 = create_vect(size_problem[i])
		print("Done generating matrices.")
		_, _, time1[i] = do_serial(max_iter,alpha,A1,A2,b1,b2,True)
		_, _, time2[i] = do_parallel(max_iter,alpha,A1,A2,b1,b2,True)
		print("\n")
	
	plt.figure(2)
	plt.plot(size_problem,time1,'bx',label="Serial Execution")
	plt.plot(size_problem,time2,'rx',label="Parallel Execution")
	plt.title("Time trials comparing parallel vs. serial computing")
	plt.xlabel("Dimensions of decomposed problem")
	plt.ylabel("Completion time (s)")
	plt.legend()
	
	plt.show()
	
	
	
	
	plt.show()
	
#	_,_,_ = do_parallel(max_iter,alpha,A1,A2,b1,b2,True)
#	_,_,_ = do_serial(max_iter,alpha,A1,A2,b1,b2,True)
	

