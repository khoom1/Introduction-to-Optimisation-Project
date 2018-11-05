import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Process, Queue, Pool,Array
import time

def argm(tuple_in):
	col_i = tuple_in[0]
	alpha = tuple_in[1]
	beta = tuple_in[2]
	P_i = (col_i.transpose() @ alpha)[0][0]
	Q_i = (col_i.transpose() @ beta)[0][0]
	x = (1.1*P_i-Q_i)/0.42
	y = (1.1*Q_i-P_i)/0.42
	
	if x<0.0:
		x=0.0
		y = max(Q_i/2.2,0.0)

	if y<0.0:
		y=0.0
		x = max(P_i/2.2,0.0)
	
	return [x,y]
	
def do_parallel(max_iter,step_size,incidence_matrix,s,t):
	num_nodes = len(s)
	num_edges = incidence_matrix.get_shape()[1] #num columns
	alpha = np.zeros((num_nodes,1))
	beta = np.zeros((num_nodes,1))
	residual_x = np.zeros((max_iter,1))
	residual_y = np.zeros((max_iter,1))
	x = np.zeros((num_edges,1))
	y = np.zeros((num_edges,1))

	begin = time.time()
	pool = Pool()
	for k in range(max_iter):
		result = pool.map(argm, [(incidence_matrix.getcol(i),alpha,beta) for i in range(num_edges)])
		#pool.close()
		#pool.join()
		temp = np.array(list(result))
		x = np.reshape(temp[:,0],(num_edges,1))
		y = np.reshape(temp[:,1],(num_edges,1))
		residual_x[k] = np.linalg.norm(incidence_matrix @ x - s,2)
		residual_y[k] = np.linalg.norm(incidence_matrix @ y - t,2)

		alpha = alpha + step_size*(s-incidence_matrix @ x)
		beta = beta + step_size*(t-incidence_matrix @ y)
	end = time.time()
	print("Dual decomposition in parallel takes %fs." %(end-begin))
	plt.plot(range(max_iter),residual_x)
	plt.show()
