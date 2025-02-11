# SAT-Reduction

## Overview

This folder contains implementations of reductions from **Sudoku** and **Hamiltonian Cycle** problems to **Boolean Satisfiability (SAT)**. The goal is to encode these problems into SAT formulas, which can then be solved using a SAT solver.

## Implemented Reductions

- **Sudoku to SAT:** Encodes a given Sudoku puzzle as a SAT formula, ensuring valid row, column, and box constraints.
- **Hamiltonian Cycle to SAT:** Translates a graph's Hamiltonian cycle problem into a SAT instance, enforcing path constraints.

## Usage

Each script generates a **CNF formula** that can be solved using a SAT solver:

```python
cnf_formula = sudoku_to_sat(sudoku_grid)
cnf_formula = hamiltonian_to_sat(graph)

