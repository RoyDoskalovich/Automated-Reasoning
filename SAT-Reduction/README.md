# SAT-Reduction

## Overview

This folder contains implementations of reductions from **Sudoku** and **Hamiltonian Cycle** problems to **Boolean Satisfiability (SAT)**. The goal is to encode these problems into SAT formulas, which can then be solved using a SAT solver.

## Implemented Reductions

- **Sudoku to SAT:**  
  Sudoku is a number-placement puzzle where each row, column, and subgrid must contain distinct numbers. The reduction converts a Sudoku grid into a SAT formula that enforces these constraints.

- **Hamiltonian Cycle to SAT:**  
  The Hamiltonian Cycle problem asks whether a given graph contains a cycle that visits each vertex exactly once. The reduction encodes this as a SAT problem, ensuring a valid path exists.

## Usage

Each script generates a **CNF formula** that can be solved using a SAT solver:

```python
cnf_formula = sudoku_to_sat(sudoku_grid)
cnf_formula = hamiltonian_to_sat(graph)

