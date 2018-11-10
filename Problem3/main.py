import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import scipy as sc
from serial import do_serial
from parallel import do_parallel

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
	# Generate an example
	print("Generating an example problem...")
	num_nodes = 3
	incidence_matrix,s,t = create_problem(num_nodes)
	print("Done generating example problem.\n")
	
	# Plot convergence of norm(Ax-s) and norm(Ay-t) to zero
	max_iter = 1000
	step_size = 0.02 # must be proportional to num_edges
	par_resx, par_resy,_ = do_parallel(max_iter,step_size,incidence_matrix,s,t)
	plt.figure(1)
	plt.plot(range(max_iter),par_resx,label="$||Ax-s||_2$")
	plt.plot(range(max_iter),par_resy,label="$||Ay-t||_2$")
	plt.title("Convergence of $||Ax-s||_2$ and $||Ay-t||_2$")
	plt.xlabel("Number of iterations")
	plt.ylabel("Value of norms")
	plt.legend()
	
	
	# Run tests to compare the completion times of parallel and serial
	# computation for increasing problem size.
	num_tests = 10
	num_nodes = [(i+1)*5 for i in range(num_tests)]
	num_edges = [0 for i in range(num_tests)]
	time1 = np.zeros((num_tests,1))
	time2 = np.zeros((num_tests,1))
	for i in range(num_tests):
		print("Generating an example problem...")
		incidence_matrix,s,t = create_problem(num_nodes[i])
		num_edges[i] = incidence_matrix.get_shape()[1]
		print("Done generating example problem.")
		_,_,time1[i] = do_serial(max_iter,step_size,incidence_matrix,s,t,True)
		_,_,time2[i] = do_parallel(max_iter,step_size,incidence_matrix,s,t,True)
		print("\n")
	
	plt.figure(2)
	plt.plot(num_edges,time1,'bx',label="Serial Execution")
	plt.plot(num_edges,time2,'rx',label="Parallel Execution")
	plt.title("Time trials comparing parallel vs. serial computing")
	plt.xlabel("Number of edges")
	plt.ylabel("Completion time (s)")
	plt.legend()
	
	plt.show()
	
	