# QUBO

A Quadratic Unconstrained Binary Optimization (QUBO) problem is an NP-hard problem which aims at minimizing 
$$x^T Q x = \sum_{i \leq j} Q_{ij}x_{i}x{j}$$
where $Q$ is an upper triangular matrix and $x_1$, ..., $x_N$ are binary variables.

A wide range of optimization problems can be formulated as QUBO models.
