from sudoku import Board
from copy import deepcopy


class BoardChecker:
    def __init__(self, solving_method: str) -> None:
        self.solving_method = solving_method

    def checkBoardRow(self, b: Board, row: int) -> bool:
        checked_elems = b.dim * [False]
        row_to_check = b.getRow(row)
        for elem in row_to_check:
            if elem == 0:
                continue
            if checked_elems[elem-1]:
                return False
            checked_elems[elem-1] = True
        return True

    def checkBoardColumn(self, b: Board, col: int) -> bool:
        checked_elems = b.dim * [False]
        col_to_check = b.getCol(col)
        for elem in col_to_check:
            if elem == 0:
                continue
            if checked_elems[elem-1]:
                return False
            checked_elems[elem-1] = True
        return True

    def checkBoardInnerSquare(self, b: Board, row: int, col: int) -> bool:
        inner_sq_row, inner_sq_col = b.getInnerSquareRowCol(
            row, col)
        inner_board = b.getInnerSquare(inner_sq_row, inner_sq_col)
        checked_elems = b.dim * [False]
        inner_board_as_row_list = inner_board.getBoardAsRowList()
        for elem in inner_board_as_row_list:
            if elem == 0:
                continue
            if checked_elems[elem - 1]:
                return False
            checked_elems[elem-1] = True
        return True

    def checkCellisValid(self, b: Board, row: int, col: int) -> bool:
        row_possible = self.checkBoardRow(b, row)
        col_possible = self.checkBoardColumn(b, col)
        inner_square_possible = self.checkBoardInnerSquare(b, row, col)
        return row_possible and col_possible and inner_square_possible

    def hasUniqueSolution(self, b: "list[Board]") -> bool:
        sol_list = []
        if (self.solving_method == "default"):
            solutions = self.SolveBruteForce(
                b, sol_list, check_one_soltion=True)
        return len(solutions) == 1

    def solve(self, b: "list[Board]") -> "list[Board]":
        sol_list = []
        if (self.solving_method == "default"):
            return self.SolveBruteForce(b, sol_list)

    def SolveBruteForce(self, b: "list[Board]", sol_list: "list[Board]", check_one_soltion=False) -> "list[Board]":
        input_n = 1
        row = 0
        col = 0

        self.bruteForceSolve(
            b, row, col, input_n, sol_list, check_one_soltion)
        return sol_list

    def bruteForceSolve(self, b: "list[Board]", row: int, col: int, input_n: int, sol_list: "list[Board]", check_one_soltion=False) -> bool:
        dim = b[0].dim
        row_next = row + 1
        col_next = col
        input_n_next = 1

        if row_next >= dim:
            row_next = 0
            col_next += 1
        if col >= dim:
            sol_list.append(deepcopy(b[0]))
            # b[0].printBoard()
            return True
        while col < dim and input_n <= dim and (not (check_one_soltion and len(sol_list) > 1)):
            if b[0].getNumber(row, col) == 0:
                b[0].setNumber(row, col, input_n)
                if not self.checkCellisValid(b[0], row, col):
                    input_n += 1
                    b[0].setNumber(row, col, 0)
                    continue
                self.bruteForceSolve(
                    b, row_next, col_next, input_n_next, sol_list)
                if (check_one_soltion and len(sol_list) > 1):
                    break

                input_n += 1
                b[0].setNumber(row, col, 0)
                continue
            return self.bruteForceSolve(b, row_next, col_next, input_n_next, sol_list)
        return False


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
    b.setSudokuList(copied_sudoku)
    b.printBoard()

    print("Solutions: ")

    sol_list = checker.solve([b])

    for board in sol_list:
        board.printBoard()

    # print(checker.hasUniqueSolution([b]))

    # -------------------------------------------------
    # 1     2     3  |  4     5     6  |  7     8     9
    # 4     6     8  |  2     7     9  |  5     3     1
    # 5     7     9  |  8     3     1  |  4     6     2
    # -------------------------------------------------
    # 2     1     4  |  6     9     5  |  8     7     3
    # 3     8     5  |  1     2     7  |  6     9     4
    # 6     9     7  |  3     8     4  |  2     1     5
    # -------------------------------------------------
    # 7     3     1  |  5     4     8  |  9     2     6
    # 8     4     2  |  9     6     3  |  1     5     7
    # 9     5     6  |  7     1     2  |  3     4     8
