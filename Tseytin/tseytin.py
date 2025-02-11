from pysmt.shortcuts import Symbol, And, Not, Or, Implies, Iff
from pysmt.typing import BOOL


def tseitin_transformation(formula):

    subformula_vars = {}
    cnf_clauses = []

    def process_formula(formula):

        if formula in subformula_vars:
            return subformula_vars[formula]

        # TODO: Consider changing it to
        var = Symbol(f"var_{formula}", BOOL)
        # var = Symbol(f"var_{len(subformula_vars) + 1}", BOOL)
        subformula_vars[formula] = var

        if formula.is_and() or formula.is_or() or formula.is_implies() or formula.is_iff():
            arg1, arg2 = formula.args()

            var1 = process_formula(arg1)
            var2 = process_formula(arg2)

            if formula.is_and():
                cnf_clauses.append(Or(Not(var), var1))
                cnf_clauses.append(Or(Not(var), var2))
                cnf_clauses.append(Or(var, Not(var1), Not(var2)))

            elif formula.is_or():
                cnf_clauses.append(Or(var, Not(var1)))
                cnf_clauses.append(Or(var, Not(var2)))
                cnf_clauses.append(Or(Not(var), var1, var2))

            elif formula.is_implies():
                cnf_clauses.append(Or(var, var1))
                cnf_clauses.append(Or(var, Not(var2)))
                cnf_clauses.append(Or(Not(var), Not(var1), var2))

            elif formula.is_iff():
                cnf_clauses.append(Or(var, Not(var1), Not(var2)))
                cnf_clauses.append(Or(Not(var), var1, Not(var2)))
                cnf_clauses.append(Or(Not(var), Not(var1), var2))
                cnf_clauses.append(Or(var, var1, var2))

        elif formula.is_not():
            [arg1] = formula.args()
            var1 = process_formula(arg1)

            cnf_clauses.append(Or(Not(var), Not(var1)))
            cnf_clauses.append(Or(var, var1))

        elif formula.is_literal():
            cnf_clauses.append(Or(Not(var), formula))
            cnf_clauses.append(Or(var, Not(formula)))

        return var

    top_var = process_formula(formula)

    cnf_formula = And(*cnf_clauses)

    return cnf_formula



# Example usage:
if __name__ == "__main__":
    # Define symbols
    A = Symbol("A", BOOL)
    B = Symbol("B", BOOL)
    C = Symbol("C", BOOL)
    D = Symbol("D", BOOL)
    E = Symbol("E", BOOL)
    F = Symbol("F", BOOL)
    G = Symbol("G", BOOL)
    H = Symbol("H", BOOL)

    # Example
    formula1 = And(Or(And(A, B), And(C, Not(D))), Or(E, Not(F)), Implies(G, H))
    formula2 = Implies(Implies(A, B), Implies(Not(B), C))
    formula3 = And(Iff(A, B), Iff(Not(C), D))
    formula4 = And(Or(A, B), Not(And(A, B)))

    formula5 = Or(And(A, Not(B)), And(B, Not(C)))   # DNF formula.
    formula6 = Not(Not(Not(A)))

    # Apply Tseitin transformation
    cnf_formula = tseitin_transformation(formula6)
    print("formula:", formula6)
    print("CNF formula:", cnf_formula)

