from precise import do_precise
from check_solution import do_check
from imprecise import do_imprecise
from scipy import random
import numpy as np
import matplotlib.pyplot as plt

random.seed(55)
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
	# Vary these limits to get different plots
	lambda_word_limit = 3
	xi_word_limit = 100
	
	max_iter = 1000
	alpha = 1
	size1 = 3
	size2 = 3
	print("Generating an example problem...")
	A1 = create_pos_matrix(size1)
	A2 = create_pos_matrix(size2)
	b1 = create_vect(size1)
	b2 = create_vect(size2)
	print("Done generating matrices.")
	
	vstar = do_check(A1,A2,b1,b2)
	error_from_precise,lamb_precise = do_precise(max_iter,alpha,A1,A2,b1,b2,vstar)
	error_from_imprecise,lamb,lamb_rounded = do_imprecise(max_iter,alpha,A1,A2,b1,b2,vstar,lambda_word_limit,xi_word_limit)
	
	plt.figure(1)
	plt.plot(range(max_iter),error_from_precise,'b--',label="No word limit")
	plt.plot(range(max_iter),error_from_imprecise,'r--',label=f"$\lambda$ word limit {lambda_word_limit:d}, $\epsilon$ word limit {xi_word_limit:d}")
	plt.title("Convergence of private and shared variables to their optimal values")
	plt.xlabel("Number of iterations")
	plt.ylabel("$||v_{aug}-v^*||_2$")
	plt.legend()
	
	plt.figure(2)
	plt.plot(range(max_iter-50,max_iter),lamb[max_iter-50:],'b.',label="$\lambda$ imprecise")
	plt.plot(range(max_iter-50,max_iter),lamb_rounded[max_iter-50:],'r.',label="$\lambda$ imprecise rounded")
	plt.plot(range(max_iter-50,max_iter),lamb_precise*np.ones((50,1)),'k--',label="$\lambda$ precise")
	plt.title(f"Different $\lambda$ values, word limit {lambda_word_limit:d}, step size {alpha:.1f}")
	plt.xlabel("Number of iterations")
	plt.ylabel("Values of $\lambda$")
	plt.legend()
	
	plt.show()
	