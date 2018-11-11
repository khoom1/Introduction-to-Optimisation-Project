# Introduction-to-Optimisation-Project

This repository was created as a final project for the subject ELEN90026 Introduction to Optimisation at The University of Melbourne.

The purpose of this project is to demonstrate two aspects of using the method of dual decomposition for solving an optimisation problem with a separable cost function (and one complicating variable). The first aspect is the application of parallel computing to simulate decomposing the separable problem into subproblems and solving those subproblems in parallel on separate machines. The second aspect is the affect of a limit on the packet size of messages passed between these parallel processes/machines on convergence of the overall algorithm.

## Background

### Separable Cost Function

The following separable unconstrained problem will be considered:

<img src="https://latex.codecogs.com/svg.latex?\min_{x_1,x_2,x_3}f_1(x_1,x_3)+f_2(x_2,x_3)" />

or equivalently:

<img src="https://latex.codecogs.com/svg.latex?\begin{align*}\min_{x_1,\xi_1,x_2,\xi_2}\qquad&f_1(x_1,\xi_1)+f_2(x_2,\xi_2)\\s.t.\qquad&\xi_1=\xi_2,\end{align*}" />

where <img src="https://latex.codecogs.com/svg.latex?x_1\in\mathbb{R}^n" />, <img src="https://latex.codecogs.com/svg.latex?x_2\in\mathbb{R}^m" /> and <img src="https://latex.codecogs.com/svg.latex?x_3,\xi_1,\xi_2\in\mathbb{R}" /> for some <img src="https://latex.codecogs.com/svg.latex?n" /> and <img src="https://latex.codecogs.com/svg.latex?m" />. Then the dual function is

<img src="https://latex.codecogs.com/svg.latex?\begin{align*}q(\lambda)&=\inf_{x_1,\xi_1,x_2,\xi_2}[f_1(x_1,\xi_1)+f_2(x_2,\xi_2)-\lambda^\top(\xi_1-\xi_2)]\\&=\inf_{x_1,\xi_1}[f_1(x_1,\xi_1)-\lambda^\top(\xi_1)]+\inf_{x_2,\xi_2}[f_2(x_2,\xi_2)+\lambda^\top(\xi_2)]\\&=q_1(\lambda)+q_2(\lambda)\end{align*}" />.

We seek a <img src="https://latex.codecogs.com/svg.latex?\lambda" /> that maximises this dual function, which can be found using the subgradient method. Here the negative subgradient of the dual function at a given point <img src="https://latex.codecogs.com/svg.latex?\lambda_k" /> is given as <img src="https://latex.codecogs.com/svg.latex?g_k=\xi_1-\xi_2" />. The subgradient method involves iteratively

* finding <img src="https://latex.codecogs.com/svg.latex?(x_1,\xi_1,x_2,\xi_2)\in\arg\min\limits_{x_1,\xi_1,x_2,\xi_2}[f_1(x_1,\xi_1)+f_2(x_2,\xi_2)-\lambda^\top(\xi_1-\xi_2)]" />, and

* updating <img src="https://latex.codecogs.com/svg.latex?\lambda_{k+1}=\lambda_k-\alpha_k(\xi_1-\xi_2)" />, where <img src="https://latex.codecogs.com/svg.latex?\alpha_k" /> is the step size.

The method of dual decomposition is simply making use of the fact that the dual function can be decomposed into <img src="https://latex.codecogs.com/svg.latex?q_1(\lambda)" /> and <img src="https://latex.codecogs.com/svg.latex?q_2(\lambda)" /> as shown above, and so finding

<img src="https://latex.codecogs.com/svg.latex?(x_1,\xi_1,x_2,\xi_2)\in\arg\min\limits_{x_1,\xi_1,x_2,\xi_2}[f_1(x_1,\xi_1)+f_2(x_2,\xi_2)-\lambda^\top(\xi_1-\xi_2)]" />

can instead be done by two individual agents separately finding the minimisers

<img src="https://latex.codecogs.com/svg.latex?(x_1,\xi_1)\in\arg\min_{x_1,\xi_1}[f_1(x_1,\xi_1)-\lambda^\top(\xi_1)]" />
<img src="https://latex.codecogs.com/svg.latex?(x_2,\xi_2)\in\arg\min_{x_2,\xi_2}[f_2(x_2,\xi_2)+\lambda^\top(\xi_2)]." />

### Parallel Computing

The `multiprocessing` module on Python was used to execute processes in parallel. A key point is that to simulate different agents separately executing tasks, this is better reflected by spawning parallel processes rather than threads.


## Overview of This Project

In Problems 1, 2 and 3, we know that by applying dual decomposition and the subgradient method, the decomposed dual function will converge (it is an iterative method) to an optimum value, which corresponds to the optimum value found by solving the unseparated dual function. Thus, the focus is more on demonstrating the trade-off between doing dual decomposition via parallel versus serial computing, rather than the trade-off between separating the cost function versus not separating the cost function.

Problem 4 then explores the convergence of the decomposed problem when a limit on the size of messages passed between processes is imposed.

Each folder has its own README.pdf file that explains the findings of each problem in more detail as well as how to run the functions.

In terms of hardware, a 2.90GHz Intel i7-7500U CPU with 2 cores (4 logical processors) was used in each problem. This was sufficient for the purpose of Problems 1, 2, and 4 where only two agents need to be simulated, but Problem 3 involves a much larger number of agents. The discussion in the Problem 3 README file elaborate on the implications of this in more detail.
