import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import scipy as sc
from serial import do_serial
from parallel import do_parallel
from p2 import do_p2

def create_problem(num_nodes):
	G = nx.scale_free_graph(num_nodes)
	incidence_matrix = -nx.incidence_matrix(G, oriented=True)
	s = np.random.random(size=(num_nodes-1,1))-0.5
	s=np.append(s,[-sum(s)],axis=0)
	t = np.random.random(size=(num_nodes-1,1))-0.5
	t=np.append(t,[-sum(t)],axis=0)
	incidence_matrix = sc.sparse.hstack([incidence_matrix,-incidence_matrix])
	return incidence_matrix,s,t

if __name__=="__main__":
	max_iter = 10
	num_nodes = 3
	step_size = 0.01 #proportional to num_edges
	incidence_matrix,s,t = create_problem(num_nodes)
	
	#do_serial(max_iter,step_size,incidence_matrix,s,t)
	#do_parallel(max_iter,step_size,incidence_matrix,s,t)
	do_p2(max_iter,step_size,incidence_matrix,s,t)