from pysmt.shortcuts import Symbol, And, Or, Not, Solver
from pysmt.typing import BOOL
import random


def hamiltonian_cycle_sat(nodes, edges):
    constraints = []
    n = len(nodes)
    positions = range(n)
    vars = {(node, position): Symbol(f"{node}_{position}", BOOL) for node in nodes for position in positions}

    for node in nodes:
        constraints.append(Or([vars[(node, position)] for position in positions]))

        for position1 in positions:
            for position2 in positions:
                if position1 < position2:
                    constraints.append(Or(Not(vars[(node, position1)]), Not(vars[(node, position2)])))

    for position in positions:
        constraints.append(Or([vars[(node, position)] for node in nodes]))  # Do I need this?

        for node1 in nodes:
            for node2 in nodes:
                if node1 < node2:
                    constraints.append(Or(Not(vars[(node1, position)]), Not(vars[(node2, position)])))

    neighbors = {i: [] for i in nodes}
    for node1, node2 in edges:
        neighbors[node1].append(node2)
        neighbors[node2].append(node1)

    for position in range(n):
        for node1 in nodes:
            position_next = (position + 1) % n
            neighbor_constraint = [vars[(node2, position_next)] for node2 in neighbors[node1]]
            if neighbor_constraint:
                constraints.append(Or(Not(vars[(node1, position)]), Or(*neighbor_constraint)))

    # Combine all constraints
    formula = And(constraints)

    # Solve with a SAT solver
    with Solver(name="z3") as solver:
        solver.add_assertion(formula)
        if solver.solve():
            # If satisfiable, extract solution
            cycle = [None] * n
            for pos in range(n):
                for node in nodes:
                    if solver.get_value(vars[(node, pos)]).is_true():
                        cycle[pos] = node
            return cycle
        else:
            return None


# Example usage
# nodes = ["A", "B", "C", "D"]
# edges = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("B", "D")]


# Example presentation
# nodes = [x + 1 for x in range(20)]
# edges = [(1, 20), (1, 2), (1, 5),
#          (2, 18), (2, 3),
#          (3, 4), (3, 16),
#          (4, 5), (4, 14),
#          (5, 6),
#          (6, 7), (6, 13),
#          (7, 8), (7, 20),
#          (8, 9), (8, 12),
#          (9, 19), (9, 10),
#          (10, 17), (10, 11),
#          (11, 12), (11, 15),
#          (12, 13),
#          (13, 14),
#          (14, 15),
#          (15, 16),
#          (17, 18),
#          (18, 19),
#          (19, 20)]

nodes = [x + 1 for x in range(5)]
edges = [(1, 2), (2, 3), (3, 4),
         (4, 5), (5, 1)]

# BIG Example
# def generate_random_pairs(num_pairs,n):
#     pairs = [(random.randint(0, n-1), random.randint(0, n-1)) for _ in range(num_pairs)]
#     pairs = set(pairs)
#     pairs = [(x1,x2) for (x1,x2) in pairs if x1 != x2]
#     return pairs
#
# n = 50
# num_pairs = 450
# nodes = [x for x in range(n)]
# edges = set(generate_random_pairs(num_pairs, n))

solution = hamiltonian_cycle_sat(nodes, edges)
if solution:
    print("Hamiltonian Cycle found:")
    for v in solution:
        print(f'{v} -> ', end='')
    print(solution[0])
else:
    print("No Hamiltonian Cycle exists.")
