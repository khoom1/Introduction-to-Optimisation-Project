import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import scipy as sc

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

num_nodes = 10
G = nx.scale_free_graph(num_nodes)
incidence_matrix = -nx.incidence_matrix(G, oriented=True)
s = np.random.random(size=(num_nodes-1,1))-0.5
s=np.append(s,[-sum(s)],axis=0)
t = np.random.random(size=(num_nodes-1,1))-0.5
t=np.append(t,[-sum(t)],axis=0)
incidence_matrix = sc.sparse.hstack([incidence_matrix,-incidence_matrix])
num_edges = np.shape(incidence_matrix)[1]

print(incidence_matrix.getcol(0))
max_iter = 1000
k=1
step_size = 0.01
alpha = np.zeros((num_nodes,1))
beta = np.zeros((num_nodes,1))
residual_x = np.zeros((max_iter,1))
residual_y = np.zeros((max_iter,1))
x = np.zeros((num_edges,1))
y = np.zeros((num_edges,1))

for k in range(1,max_iter):
	
	#TODO put into multiprocessing pool
	for i in range(num_edges):
		x[i], y[i] = argm(incidence_matrix.getcol(i),alpha,beta)
	
	residual_x[k] = np.linalg.norm(incidence_matrix @ x - s,2)
	residual_y[k] = np.linalg.norm(incidence_matrix @ y - t,2)

	alpha = alpha + step_size*(s-incidence_matrix @ x)
	beta = beta + step_size*(t-incidence_matrix @ y)

#incidence_matrix = incidence_matrix.toarray()
#print(np.sum(s))
print(incidence_matrix @ x -s)

plt.plot(range(max_iter),residual_x)
plt.show()