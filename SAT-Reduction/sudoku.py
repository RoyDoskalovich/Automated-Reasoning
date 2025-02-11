from pysmt.shortcuts import Symbol, And, Solver
from pysmt.typing import BOOL


def sudoku_solver(puzzle):
    from pysmt.shortcuts import Not, Or
    def _one_number_in_cell(i, j, cells):
        constraints = []
        for cell_num in range(1, 10):
            one_num_constraints = []
            for d in range(8):
                one_num_constraints.append(Not(cells[i, j, ((cell_num + d) % 9) + 1]))
            constraints.append(And(cells[i, j, cell_num], *one_num_constraints))
        return constraints

    def _one_number_in_row(i, d, cells):
        constraints = []
        for j in range(9):
            number_once = []
            for colum in range(8):
                number_once.append(Not(cells[i, ((j + colum) % 9), d]))
            constraints.append(And(cells[i, ((j - 1) % 9), d], *number_once))
        return constraints

    def _one_number_in_colum(j, d, cells):
        constraints = []
        for i in range(9):
            number_once = []
            for row in range(8):
                number_once.append(Not(cells[((i + row) % 9), j, d]))
            constraints.append(And(cells[((i - 1) % 9), j, d], *number_once))
        return constraints

    def _one_number_in_a_qube(i, j, cells):
        constraints = []
        numbers_all_places = []

        for d in range(1, 10):
            all_number_possibole_places = []
            for iterator in range(9):
                true_place = 0
                one_pace_formula = []
                for ii in range(3):
                    for jj in range(3):
                        if iterator == true_place:
                            one_pace_formula.append(cells[i + ii, j + jj, d])
                        else:
                            one_pace_formula.append(Not(cells[i + ii, j + jj, d]))
                        true_place += 1
                all_number_possibole_places.append(And(*one_pace_formula))

            numbers_all_places.append(Or(all_number_possibole_places))

        constraints.append(And(*numbers_all_places))
        return constraints

    def _generate_constraints_empty_sudoku(constraints, cells):
        for i in range(9):
            for j in range(9):
                constraints.append(Or(*_one_number_in_cell(i, j, cells)))

        for i in range(9):
            for d in range(1, 10):
                _one_number_in_row(i, d, cells)
                constraints.append(Or(*_one_number_in_row(i, d, cells)))

        for i in range(9):
            for d in range(1, 10):
                _one_number_in_colum(i, d, cells)
                constraints.append(Or(*_one_number_in_colum(i, d, cells)))

        for i in range(3):
            for j in range(3):
                constraints.append(And(*_one_number_in_a_qube(i * 3, j * 3, cells)))

    def _add_constraints_from_puzzle(constraints, puzzle, cells):
        constrain_puzzle = []
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] != 0:
                    constrain_puzzle.append(cells[i, j, puzzle[i][j]])
        constraints.append(And(*constrain_puzzle))


    # Create Boolean variables x_i_j_d for each cell (i, j) and digit d
    cells = {(i, j, d): Symbol(f"x_{i}_{j}_{d}", BOOL) for i in range(9) for j in range(9) for d in range(1, 10)}

    # Define constraints
    constraints = []
    _generate_constraints_empty_sudoku(constraints, cells)
    _add_constraints_from_puzzle(constraints, puzzle, cells)

    # Solve the puzzle
    with Solver(name="z3") as solver:
        solver.add_assertion(And(constraints))
        if solver.solve():
            solution = [[0 for _ in range(9)] for _ in range(9)]
            for i in range(9):
                for j in range(9):
                    for d in range(1, 10):
                        if solver.get_value(cells[(i, j, d)]).is_true():
                            solution[i][j] = d
            return solution
        else:
            return None  # No solution found

# Example usage
# Puzzle 1
# puzzle =
puzzles = [
[
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
],
[
    [0, 0, 0, 2, 6, 0, 7, 0, 1],
    [6, 8, 0, 0, 7, 0, 0, 9, 0],
    [1, 9, 0, 0, 0, 4, 5, 0, 0],
    [8, 2, 0, 1, 0, 0, 0, 4, 0],
    [0, 0, 4, 6, 0, 2, 9, 0, 0],
    [0, 5, 0, 0, 0, 3, 0, 2, 8],
    [0, 0, 9, 3, 0, 0, 0, 7, 4],
    [0, 4, 0, 0, 5, 0, 0, 3, 6],
    [7, 0, 3, 0, 1, 8, 0, 0, 0]
],
[
    [0, 0, 0, 0, 0, 7, 0, 0, 9],
    [0, 0, 4, 0, 6, 0, 3, 0, 0],
    [0, 6, 0, 5, 0, 0, 4, 0, 0],
    [0, 9, 0, 0, 5, 1, 0, 0, 6],
    [5, 0, 0, 8, 0, 3, 0, 0, 7],
    [6, 0, 0, 9, 2, 0, 0, 8, 0],
    [0, 0, 8, 0, 0, 9, 0, 2, 0],
    [0, 0, 1, 0, 8, 0, 9, 0, 0],
    [3, 0, 0, 4, 0, 0, 0, 0, 0]
],
[
    [0, 0, 0, 7, 0, 0, 3, 0, 0],
    [8, 0, 0, 0, 0, 4, 0, 0, 5],
    [0, 0, 0, 0, 0, 0, 6, 0, 0],
    [5, 0, 1, 0, 3, 0, 9, 0, 0],
    [0, 4, 0, 0, 0, 0, 0, 5, 0],
    [0, 0, 9, 0, 7, 0, 2, 0, 8],
    [0, 0, 8, 0, 0, 0, 0, 0, 0],
    [6, 0, 0, 4, 0, 0, 0, 0, 1],
    [0, 0, 2, 0, 0, 1, 0, 0, 0]
],
[
    [0, 0, 0, 8, 0, 0, 0, 0, 1],
    [0, 0, 4, 0, 0, 0, 0, 2, 0],
    [0, 2, 0, 7, 1, 0, 0, 0, 0],
    [0, 4, 3, 0, 0, 0, 0, 0, 8],
    [9, 0, 0, 0, 0, 0, 0, 0, 3],
    [6, 0, 0, 0, 0, 0, 2, 9, 0],
    [0, 0, 0, 0, 4, 8, 0, 3, 0],
    [0, 9, 0, 0, 0, 0, 5, 0, 0],
    [8, 0, 0, 0, 0, 5, 0, 0, 0]
],
[
    [2, 0, 0, 0, 0, 0, 0, 0, 5],
    [0, 0, 7, 0, 3, 0, 2, 0, 0],
    [0, 6, 0, 8, 0, 2, 0, 4, 0],
    [0, 0, 8, 1, 0, 5, 4, 0, 0],
    [0, 2, 0, 4, 0, 6, 0, 3, 0],
    [0, 0, 3, 7, 0, 8, 1, 0, 0],
    [0, 1, 0, 6, 0, 9, 0, 8, 0],
    [0, 0, 2, 0, 5, 0, 6, 0, 0],
    [6, 0, 0, 0, 0, 0, 0, 0, 3]
],
[
    [0, 0, 0, 6, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 9, 0, 2, 0, 5],
    [0, 0, 8, 0, 0, 1, 0, 6, 0],
    [0, 5, 0, 1, 0, 0, 8, 0, 0],
    [6, 0, 3, 0, 0, 0, 5, 0, 1],
    [0, 0, 7, 0, 0, 4, 0, 2, 0],
    [0, 3, 0, 4, 0, 0, 7, 0, 0],
    [7, 0, 6, 0, 1, 0, 0, 5, 0],
    [0, 0, 0, 0, 0, 7, 0, 0, 0]
],
[
    [0, 0, 0, 0, 5, 0, 0, 0, 0],
    [0, 0, 7, 1, 0, 0, 0, 0, 3],
    [3, 0, 2, 0, 0, 0, 4, 0, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 2],
    [0, 0, 1, 0, 0, 0, 3, 0, 0],
    [9, 0, 0, 0, 2, 0, 0, 0, 4],
    [0, 0, 4, 0, 0, 0, 1, 0, 9],
    [2, 0, 0, 0, 0, 8, 7, 0, 0],
    [0, 0, 0, 0, 3, 0, 0, 0, 0]
],
[
    [0, 0, 0, 0, 8, 0, 0, 0, 6],
    [9, 0, 0, 0, 5, 0, 1, 0, 0],
    [0, 0, 0, 3, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 0, 9, 0, 4, 0],
    [0, 5, 0, 7, 0, 1, 0, 6, 0],
    [0, 4, 0, 8, 0, 0, 0, 2, 0],
    [0, 0, 0, 0, 0, 5, 0, 0, 0],
    [0, 0, 1, 0, 2, 0, 0, 0, 4],
    [5, 0, 0, 0, 9, 0, 0, 0, 0]
],
[
    [0, 0, 0, 0, 0, 7, 0, 8, 0],
    [6, 0, 0, 0, 0, 0, 4, 0, 3],
    [0, 0, 0, 2, 0, 0, 0, 5, 9],
    [0, 0, 0, 8, 4, 0, 0, 0, 0],
    [4, 0, 6, 0, 0, 0, 2, 0, 7],
    [0, 0, 0, 0, 9, 1, 0, 0, 0],
    [2, 6, 0, 0, 0, 3, 0, 0, 0],
    [1, 0, 8, 0, 0, 0, 0, 0, 4],
    [0, 7, 0, 9, 0, 0, 0, 0, 0]
],
[
    [0, 0, 4, 1, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 4, 0, 1, 6],
    [0, 3, 0, 0, 5, 0, 0, 0, 9],
    [0, 0, 0, 4, 0, 2, 8, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 3, 5, 7, 0],
    [5, 0, 0, 8, 0, 0, 0, 0, 0],
    [6, 0, 2, 0, 1, 0, 0, 0, 0],
    [4, 0, 0, 0, 0, 7, 9, 0, 0]
]
]

def is_valid_sudoku(matrix):
    def is_valid_group(group):
        """Helper function to check if a group contains numbers 1-9 with no duplicates."""
        group = [num for num in group if num != 0]  # Exclude empty cells (0)
        return len(group) == len(set(group)) and all(1 <= num <= 9 for num in group)

    # Check rows
    for row in matrix:
        if not is_valid_group(row):
            return False

    # Check columns
    for col in range(9):
        if not is_valid_group([matrix[row][col] for row in range(9)]):
            return False

    # Check 3x3 sub-grids
    for start_row in range(0, 9, 3):
        for start_col in range(0, 9, 3):
            sub_grid = [
                matrix[row][col]
                for row in range(start_row, start_row + 3)
                for col in range(start_col, start_col + 3)
            ]
            if not is_valid_group(sub_grid):
                return False

    return True

for puzzle in puzzles:
    solution = sudoku_solver(puzzle)
    if solution:
        for row in solution:
            print(row)
        print(is_valid_sudoku(solution))
    else:
        print("No solution exists.")