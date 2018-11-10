import numpy as np
import time

def argm(col_i, alpha, beta):
	P_i = col_i.transpose() @ alpha
	Q_i = col_i.transpose() @ beta
	x = (1.1*P_i-Q_i)/0.42
	y = (1.1*Q_i-P_i)/0.42
	
	if x<0.0:
		x=0.0
		y = max(Q_i/2.2,0.0)

	if y<0.0:
		y=0.0
		x = max(P_i/2.2,0.0)
	
	return x,y
	
def do_serial(max_iter,step_size,incidence_matrix,s,t,verbose=False):
	num_nodes = len(s)
	num_edges = incidence_matrix.get_shape()[1] #num columns
	alpha = np.zeros((num_nodes,1))
	beta = np.zeros((num_nodes,1))
	residual_x = np.zeros((max_iter,1))
	residual_y = np.zeros((max_iter,1))
	x = np.zeros((num_edges,1))
	y = np.zeros((num_edges,1))
	
	begin = time.time()
	for k in range(max_iter):
		for i in range(num_edges):
			x[i], y[i] = argm(incidence_matrix.getcol(i),alpha,beta)
		residual_x[k] = np.linalg.norm(incidence_matrix @ x - s,2)
		residual_y[k] = np.linalg.norm(incidence_matrix @ y - t,2)
		alpha = alpha + step_size*(s-incidence_matrix @ x)
		beta = beta + step_size*(t-incidence_matrix @ y)
	end = time.time()
	
	if verbose:
		print("Dual decomposition in series takes %fs." %(end-begin))
		
	return residual_x,residual_y,end-begin