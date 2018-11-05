import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Process, Queue, Pool,Array
import time

def argm(incidence_col,alpha,beta,x,y):
	
	P_i = (incidence_col.transpose() @ alpha)[0][0]
	Q_i = (incidence_col.transpose() @ beta)[0][0]
	x = (1.1*P_i-Q_i)/0.42
	y = (1.1*Q_i-P_i)/0.42
	
	if x<0.0:
		x=0.0
		y = max(Q_i/2.2,0.0)

	if y<0.0:
		y=0.0
		x = max(P_i/2.2,0.0)

	
def do_p2(max_iter,step_size,incidence_matrix,s,t):
	num_nodes = len(s)
	num_edges = incidence_matrix.get_shape()[1] #num columns
	alpha = np.zeros((num_nodes,1))
	beta = np.zeros((num_nodes,1))
	residual_x = np.zeros((max_iter,1))
	residual_y = np.zeros((max_iter,1))
	#x = np.zeros((num_edges,1))
	#y = np.zeros((num_edges,1))
	
	x = Array('d',range(num_edges))
	y = Array('d',range(num_edges))
	
	begin = time.time()
	pool = Process()
	for k in range(max_iter):
		for i in range(num_edges):
			d[i] = Process(target=argm, args=(incidence_matrix.getcol(i),alpha,beta,x,y))
			d[i].start()
		for i in range(num_edges):
			d[i].join()

			
		residual_x[k] = np.linalg.norm(incidence_matrix @ x - s,2)
		residual_y[k] = np.linalg.norm(incidence_matrix @ y - t,2)

		alpha = alpha + step_size*(s-incidence_matrix @ x)
		beta = beta + step_size*(t-incidence_matrix @ y)
	end = time.time()
	print("Dual decomposition in parallel takes %fs." %(end-begin))
	plt.plot(range(max_iter),residual_x)
	plt.show()