from sudoku import Board
from sudoku_checker import BoardChecker
from copy import deepcopy
from random import randint


class SudokuGenerator:
    def __init__(self, checker: BoardChecker) -> None:
        self.checker = checker

    def get_one_solution_sudoku(self, solved_sudoku: "list[Board]") -> Board:
        temp_sudoku = deepcopy(solved_sudoku[0])
        row_to_null = randint(0, 8)
        col_to_null = randint(0, 8)
        solved_sudoku[0].input_number(row_to_null, col_to_null, 0)
        one_solution = self.checker.has_unique_solution(solved_sudoku)

        if (not one_solution):
            return temp_sudoku
        return self.get_one_solution_sudoku(solved_sudoku)


if __name__ == "__main__":
    print()
    b = Board(9)
    checker = BoardChecker("default")
    copied_sudoku = [[0, 0, 3, 0, 2, 0, 6, 0, 0],
                     [9, 0, 0, 3, 0, 5, 0, 0, 1],
                     [0, 0, 1, 8, 0, 6, 4, 0, 0],
                     [0, 0, 8, 1, 0, 2, 9, 0, 0],
                     [7, 0, 0, 0, 0, 0, 0, 0, 8],
                     [0, 0, 6, 7, 0, 8, 2, 0, 0],
                     [0, 0, 2, 6, 0, 9, 5, 0, 0],
                     [8, 0, 0, 2, 0, 3, 0, 0, 9],
                     [0, 0, 5, 0, 1, 0, 3, 0, 0]]
    b.set_sudoku_list(copied_sudoku)
    b.print_board()
    sol = checker.solve([b])
    sol[0].print_board()

    generator = SudokuGenerator(checker)

    one_solution_sudoku = generator.get_one_solution_sudoku(sol)
    one_solution_sudoku.print_board()
