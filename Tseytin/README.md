# Tseytin Transformation

## Overview

Tseytin transformation is a method for converting propositional logic formulas into **Conjunctive Normal Form (CNF)** while preserving satisfiability. CNF is a standard form used in SAT solvers, consisting of a conjunction (AND) of disjunctions (OR) of literals (e.g., `(A ∨ B) ∧ (¬C ∨ D)`). This transformation ensures that the formula size grows linearly, making it efficient for Boolean satisfiability (SAT) solving.

## How It Works

Tseytin transformation introduces auxiliary variables to represent subformulas in the original Boolean formula. This avoids exponential growth in formula size and ensures a linear increase in size relative to the input.

The transformation follows these steps:

1. Assign a new Boolean variable to each subformula in the input formula.
2. Replace each logical operation (AND, OR, NOT, IMPLIES, IFF) with a set of CNF clauses that encode the logical equivalence of the new variable and the corresponding subformula.
3. Combine all generated clauses into a single CNF formula.
4. Ensure the final CNF formula is equisatisfiable with the original formula.

## Input & Output

- **Input:** A Boolean formula composed of logical operations such as AND (`∧`), OR (`∨`), NOT (`¬`), IMPLIES (`→`), and IFF (`↔`).
- **Output:** An equisatisfiable CNF formula represented as a conjunction of disjunctions of literals.

## Example

### Given Formula:

```plaintext
(A ∧ B) ∨ (C ∧ ¬D)
```

### Tseytin Transformation Steps:

1. Introduce new variables for subformulas:
   - `X1 = A ∧ B`
   - `X2 = C ∧ ¬D`
   - `X3 = X1 ∨ X2`
2. Convert each equation into CNF constraints.
3. Final CNF output (simplified representation):

```plaintext
(¬X1 ∨ A) ∧ (¬X1 ∨ B) ∧ (X1 ∨ ¬A ∨ ¬B)
(¬X2 ∨ C) ∧ (¬X2 ∨ ¬D) ∧ (X2 ∨ ¬C ∨ D)
(¬X3 ∨ X1 ∨ X2) ∧ (X3 ∨ ¬X1) ∧ (X3 ∨ ¬X2)
```

## Usage

This repository contains an implementation of Tseytin transformation using **PySMT**. To use it:

### Run the Script

```bash
python tseytin.py
```

