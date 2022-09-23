from __future__ import annotations
import numpy as np
import math


class Cell:
    def __init__(self, number: int) -> None:
        self.number = number
        pass

    def __repr__(self):
        if self.number == 0:
            return "X"
        return str(self.number)

    def __str__(self):
        if self.number == 0:
            return " "
        return str(self.number)

    def __eq__(self, __o: object) -> bool:
        return self.number == __o

    def getNumber(self) -> int:
        return self.number

    def setNumber(self, number: int) -> None:
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
                temp_row.append(0)
            self.cell_matrix.append(temp_row)
        pass

    def __eq__(self, __o: Board) -> bool:
        this_board = self.getBoardAsRowList()
        o_list = __o.getBoardAsRowList()
        if len(o_list) != len(this_board):
            return False
        compare = True
        i = 0
        while (i < self.dim ** 2 and compare):
            compare = compare and (this_board[i] == o_list[i])
            i += 1
        return compare

    def setSudokuList(self, sudoku_list: "list[int]") -> None:
        self.cell_matrix = []
        try:
            self.dim = len(sudoku_list)
            self.dim_sqrt = int(math.sqrt(self.dim))
            for i in range(self.dim):
                temp_row = []
                for j in range(self.dim):
                    c = sudoku_list[i][j]
                    temp_row.append(c)
                self.cell_matrix.append(temp_row)
        except:
            raise ValueError

    def getBoardAsRowList(self) -> "list[int]":
        out_list = []
        for i in range(self.dim):
            row_ = self.getRow(i)
            out_list += row_
        return out_list

    def transposeBoard(self) -> None:
        new_matrix = []
        for i in range(self.dim):
            new_matrix.append(self.getCol(i))
        self.cell_matrix = new_matrix

    # 90 degree  CCW rotation
    def rotateBoard(self) -> None:
        self.transposeBoard()
        new_matrix = []
        for i in range(self.dim):
            row_ = self.getRow(i)
            row_ = row_[::-1]
            new_matrix.append(row_)
        self.cell_matrix = new_matrix

    def getRow(self, n_row: int) -> "list[int]":
        return self.cell_matrix[n_row]

    def getCol(self, n_col: int) -> "list[int]":
        return [x for x in [self.cell_matrix[y][n_col] for y in range(self.dim)]]

    def getInnerSquareRowCol(self, row: int, col: int) -> "list[int]":
        return [int(row / self.dim_sqrt), int(col / self.dim_sqrt)]

    def getInnerSquare(self, n_square_row: int, n_square_col: int) -> Board:
        inner_square = []
        for row in range(n_square_row*self.dim_sqrt, n_square_row * self.dim_sqrt + self.dim_sqrt):
            temp_square = []
            for col in range(n_square_col*self.dim_sqrt, self.dim_sqrt + n_square_col*self.dim_sqrt):
                temp_square.append(self.cell_matrix[row][col])
            inner_square.append(temp_square)
        inner_square_board = Board(self.dim_sqrt)
        inner_square_board.cell_matrix = inner_square
        return inner_square_board

    def setNumber(self, row: int, col: int, n: int) -> None:
        self.cell_matrix[row][col] = n

    def getNumber(self, row: int, col: int) -> int:
        return self.cell_matrix[row][col]

    def getFilledCellsAmmount(self) -> int:
        return self.dim ** 2 - self.getBoardAsRowList().count(0)

    def printBoard(self):
        print()
        print((6 * (self.dim-1) + 1) * "-")
        for row in range(self.dim):
            curr_row = self.getRow(row)
            for i, elem in enumerate(curr_row):
                if elem == 0:
                    print("X", " ",  end='')
                else:
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

    print("Filled cells:", b.getFilledCellsAmmount())
    while True:
        row = int(input("Enter row number :"))
        col = int(input("Enter col number :"))
        n = int(input("Enter number :"))
        b.setNumber(row, col, n)
        print("Sub square row,col: ", b.getInnerSquareRowCol(row, col))
        b.printBoard()
