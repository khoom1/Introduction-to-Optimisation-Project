# Introduction-to-Optimisation-Project

This repository was created as a final project for the subject ELEN90026 Introduction to Optimisation at The University of Melbourne.

The purpose of this project is to demonstrate two aspects of using the method of dual decomposition for solving an optimisation problem with a separable cost function (and one complicating variable). The first aspect is the application of parallel computing to simulate decomposing the separable problem into subproblems and solving those subproblems in parallel on separate machines. The second aspect is the affect of a limit on the packet size of messages passed between these parallel processes/machines on convergence of the overall algorithm.

## Background

### Separable Cost Function

### Parallel Computing




## Overview of This Project

Problems 1, 2 and 3 explore the convergence of the decomposed problem to the minimum of the original separable problem. The goal here is to demonstrate the trade-off between parallel and serial computing, as well as the trade-off between separating the cost function vs. not separating the cost function.

Problem 4 then explores the convergence of the decomposed problem to the minimum of the original separable cost function given the size of messages passed between processes is limited to only a small number of bits.

Each folder has its own README file that explains the findings of each problem in more detail.


