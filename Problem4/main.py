from multiprocessing import Process, Value, Array
import time
from precise import do_precise
from check_solution import do_check
from imprecise import do_imprecise
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
	max_iter = 1000
	alpha = 0.1
	size1 = 3
	size2 = 5
	binary_frac_bits = 100
	print("Generating an example problem...")
	A1 = create_pos_matrix(size1)
	A2 = create_pos_matrix(size2)
	b1 = create_vect(size1)
	b2 = create_vect(size2)
	print("Done generating matrices.")
	
	xstar = do_check(max_iter,alpha,A1,A2,b1,b2)
	xstar.insert(size1,xstar[size1-1])
	error_from_precise = do_precise(max_iter,alpha,A1,A2,b1,b2,xstar)
	error_from_imprecise = do_imprecise(max_iter,alpha,A1,A2,b1,b2,xstar,binary_frac_bits)
	
	
	plt.plot(range(max_iter),error_from_precise,'b--',range(max_iter),error_from_imprecise,'r--')
	plt.show()