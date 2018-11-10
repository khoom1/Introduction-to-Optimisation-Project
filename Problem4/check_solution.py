import time
import numpy as np
from mygauss import gauss

def augment_matrices(A1,A2):
	size1 = len(A1)
	size2 = len(A2)
	A = np.zeros((size1+size2-1,size1+size2-1))
	for i in range(size1):
		for j in range(size1):
			A[i][j]=A1[i][j]
	for i in range(size1-1,size1+size2-1):
		for j in range(size1-1,size1+size2-1):
			A[i][j]=A2[i-size1+1][j-size1+1]
	A[size1-1][size1-1]=A1[size1-1][size1-1]+A2[0][0]
	return A
	
def augment_vect(b1,b2):
	size1 = len(b1)
	size2 = len(b2)
	b = np.zeros((size1+size2-1,1))
	for i in range(size1):
		b[i]=b1[i]
	for i in range(size1-1,size1+size2-1):
		b[i]=b2[i-size1+1]
	b[size1-1]=b1[size1-1]+b2[0]

	return b

def do_check(A1,A2,b1,b2,verbose=False):
	A = augment_matrices(A1,A2)
	b = augment_vect(b1,b2)

	begin = time.time()
	x = gauss(np.concatenate((A,b),axis=1))
	end = time.time()
	
	if verbose:
		print("No decomposition takes %fs." %(end-begin))
	
	return x