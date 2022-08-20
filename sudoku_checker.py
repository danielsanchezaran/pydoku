from sudoku_generator import Board


class BoardChecker:
    def __init__(self, solving_method: str) -> None:
        self.solving_method = solving_method

    def checkBoardRow(self, b: Board, row: int) -> bool:
        checked_elems = b.dim * [False]
        row_to_check = b.get_row(row)
        for elem in row_to_check:
            if elem == 0:
                continue
            if checked_elems[elem.get_number()-1]:
                return False
            checked_elems[elem.get_number()-1] = True
        return True

    def checkBoardColumn(self, b: Board, col: int) -> bool:
        checked_elems = b.dim * [False]
        col_to_check = b.get_col(col)
        # print(col_to_check)
        for elem in col_to_check:
            if elem == 0:
                continue
            if checked_elems[elem.get_number()-1]:
                return False
            checked_elems[elem.get_number()-1] = True
        return True

    def checkBoardInnerSquare(self, b: Board, row: int, col: int) -> bool:
        inner_sq_row, inner_sq_col = b.get_inner_square_row_col(
            row, col)
        inner_board = b.get_inner_square(inner_sq_row, inner_sq_col)
        checked_elems = b.dim * [False]
        inner_board_as_row_list = inner_board.get_board_as_row_list()
        for elem in inner_board_as_row_list:
            if elem == 0:
                continue
            if checked_elems[elem.get_number() - 1]:
                return False
            checked_elems[elem.get_number()-1] = True
        return True

    def checkCellisValid(self, b: Board, row: int, col: int) -> bool:
        row_possible = self.checkBoardRow(b, row)
        col_possible = self.checkBoardColumn(b, col)
        inner_square_possible = self.checkBoardInnerSquare(b, row, col)
        return row_possible and col_possible and inner_square_possible

    def solve(self, b: "list[Board]") -> "list[Board]":
        if (self.solving_method == "default"):
            return self.solve_brute_force(b)

    def solve_brute_force(self, b: "list[Board]") -> "list[Board]":
        input_n = 1
        row = 0
        col = 0

        b_clone = b
        if self.brute_force_solver(b_clone,row,col,input_n):
            print("Solved!")
            return b_clone
        return b
      
    def brute_force_solver(self, b: "list[Board]", row: int, col: int, input_n: int) -> bool:
        print("starting new solve at ")
        print("row" , row, "col", col)
        print("input", input_n)
        print()
        dim = b[0].dim
        row_next = row + 1
        col_next = col
        input_n_next = 1

        if row_next >= dim:
            row_next = 0
            col_next += 1
        if col >= dim:
            return True 
        while col < dim and input_n <= dim:
            if b[0].get_number(row, col) == 0:
                b[0].input_number(row, col, input_n)
                if not self.checkCellisValid(b[0], row, col):
                    print("wrong input: ", input_n, " row" , row, " col", col)
                    input_n += 1
                    b[0].input_number(row, col, 0)
                    continue
                print("possibly right input: ", input_n, " row" , row, " col", col, "row_next, col_next,", row_next, col_next)
                b[0].print_board()
                if self.brute_force_solver(b, row_next, col_next, input_n_next):
                    return True
                input_n += 1
                b[0].input_number(row, col, 0)
                print("row" , row, "col", col)
                print("input", input_n)
                continue
            return self.brute_force_solver(b, row_next, col_next, input_n_next)
        return False


if __name__ == "__main__":
    print()
    b = Board(9)
    checker = BoardChecker("default")

    n = 1
    for i in range(9):
        b.input_number(0, i, n)
        n += 1
    n = 1
    for i in range(1,9):
        b.input_number(i, 8, n)
        n += 1
    
    b.print_board()
    b = checker.solve([b])
    b[0].print_board()

    print(checker.checkBoardColumn(b[0],2))
