from multiprocessing import Process, Value, Array
import time
from serial import perf_serial
from parallel import perf_parallel
from check_solution import perf_check
from scipy import random
import numpy as np

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
	max_iter = 1000
	alpha = 0.1
	size1 = 30
	size2 = 30
	print("Generating an example problem...")
	A1 = create_pos_matrix(size1)
	A2 = create_pos_matrix(size2)
	b1 = create_vect(size1)
	b2 = create_vect(size2)
	print("Done generating matrices.")
	
	perf_parallel(max_iter,alpha,A1,A2,b1,b2)
	perf_serial(max_iter,alpha,A1,A2,b1,b2)
	perf_check(max_iter,alpha,A1,A2,b1,b2)

