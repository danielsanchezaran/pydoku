from __future__ import annotations
import numpy as np
import math


class Cell:
    def __init__(self, number) -> None:
        self.number = number
        pass

    def __repr__(self):
        if self.number == 0:
            return "X"
        return str(self.number)

    def __str__(self):
        if self.number == 0:
            return "X"
        return str(self.number)

    def __eq__(self, __o: object) -> bool:
        return self.number == __o

    def get_number(self) -> int:
        return self.number

    def input_number(self, number: int) -> None:
        self.number = number

    def print_number(self) -> None:
        print(self.number)


CellList = list[Cell]


class Board:
    def __init__(self, n: int) -> None:
        self.cell_matrix = []
        self.dim = n
        # Should throw error if not int anyways
        self.dim_sqrt = int(math.sqrt(n))
        for _ in range(n):
            temp_row = []
            for __ in range(n):
                c = Cell(0)
                temp_row.append(c)
            self.cell_matrix.append(temp_row)
        pass

    def get_board_as_row_list(self) -> CellList:
        out_list = []
        for i in range(self.dim):
            row_ = self.get_row(i)
            out_list += row_
        return out_list

    def get_row(self, n_row: int) -> CellList:
        return self.cell_matrix[n_row]

    def get_col(self, n_col: int) -> CellList:
        return [x for x in [self.cell_matrix[y][n_col] for y in range(self.dim)]]

    def get_inner_square_row_col(self, row: int, col: int) -> "list[int]":
        return [int(row / self.dim_sqrt), int(col / self.dim_sqrt)]

    def get_inner_square(self, n_square_row: int, n_square_col: int) -> Board:
        inner_square = []
        for row in range(n_square_row*self.dim_sqrt, n_square_row * self.dim_sqrt + self.dim_sqrt):
            temp_square = []
            for col in range(n_square_col*self.dim_sqrt, self.dim_sqrt + n_square_col*self.dim_sqrt):
                temp_square.append(self.cell_matrix[row][col])
            inner_square.append(temp_square)
        inner_square_board = Board(self.dim_sqrt)
        inner_square_board.cell_matrix = inner_square
        return inner_square_board

    def input_number(self, row: int, col: int, n: int) -> None:
        self.cell_matrix[row][col].input_number(n)
    
    def get_number(self, row: int, col: int) -> Cell:
        return self.cell_matrix[row][col]

    def print_board(self):
        print()
        print((6 * (self.dim-1) + 1) * "-")
        for row in range(self.dim):
            curr_row = self.get_row(row)
            for i, elem in enumerate(curr_row):
                print(elem, " ",  end='')
                if (i + 1) % self.dim_sqrt == 0 and i < self.dim - 1:
                    print("|" + 2 * " ",  end='')
                else:
                    print(3 * " ",  end='')
            if (row + 1) % self.dim_sqrt == 0:
                print()
                print((6 * (self.dim-1) + 1) * "-")
            else:
                print()


if __name__ == "__main__":
    from sudoku_checker import *
    b = Board(4)
    checker = BoardChecker("default")
    while True:
        row = int(input("Enter row number :"))
        col = int(input("Enter col number :"))
        n = int(input("Enter number :"))
        b.input_number(row, col, n)
        print("Sub square row,col: ", b.get_inner_square_row_col(row, col))
        b.print_board()
        # f = b.get_inner_square(1,1)
        # f.print_board()
        print(checker.checkBoardColumn(b, 1))
        print(b.get_board_as_row_list())
        print("Inner square 0,0 is correct: ",
              checker.checkBoardInnerSquare(b, 0, 0))
        print("Cell is possible: ", checker.checkCellisValid(b, row, col))
