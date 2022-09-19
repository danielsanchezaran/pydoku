from sudoku import Board
from sudoku_checker import BoardChecker
from copy import deepcopy
from random import randint, sample
import time


class SudokuGenerator:
    def __init__(self, checker: BoardChecker) -> None:
        self.checker = checker

    def get_one_solution_sudoku(self, solved_sudoku: "list[Board]") -> Board:
        temp_sudoku = deepcopy(solved_sudoku[0])
        row_to_null = randint(0, solved_sudoku[0].dim - 1)
        col_to_null = randint(0, solved_sudoku[0].dim - 1)
        solved_sudoku[0].input_number(row_to_null, col_to_null, 0)

        if (not self.checker.has_unique_solution(solved_sudoku)):
            return temp_sudoku
        return self.get_one_solution_sudoku(solved_sudoku)

    def swap_digits(self, n_1: int, n_2: int, board: Board) -> Board:
        # board[0] = deepcopy(board[0])
        pos_1 = -1
        pos_2 = -1
        for i in range(board.dim):
            row = board.get_row(i)
            for j in range(len(row)):
                if row[j] == n_1:
                    pos_1 = j
                if row[j] == n_2:
                    pos_2 = j
                if pos_1 > 0 and pos_2 > 0:
                    break
            row[pos_1], row[pos_2] = row[pos_2], row[pos_1]
            board.cell_matrix[i] = row
            pos_1 = -1
            pos_2 = -1
        return board

    def swap_random_digits(self, board: Board) -> Board:
        n_1, n_2 = sample(range(1, board.dim - 1), 2)
        return self.swap_digits(n_1, n_2, board)

    def swap_rows(self, row_1: int, row_2: int, board: Board) -> Board:
        # board[0] = deepcopy(board[0])
        board.cell_matrix[row_1], board.cell_matrix[row_2] = board.cell_matrix[row_2], board.cell_matrix[row_1]
        return board

    def shuffle_large_rows(self, board: Board) -> Board:
        # board[0] = deepcopy(board[0])
        for original_row in range(board.dim_sqrt):
            target_row = randint(0, board.dim_sqrt - 1)
            for n in range(board.dim_sqrt):
                board = self.swap_rows(
                    (original_row * board.dim_sqrt) + n, (target_row * board.dim_sqrt) + n, board)
        return board

    def shuffle_large_cols(self, board: Board) -> Board:
        # board[0] = deepcopy(board[0])
        board.transpose_board()
        board = self.shuffle_large_rows(board)
        board.transpose_board()
        return board

    def shuffle_rows(self, board: Board) -> Board:
        # board[0] = deepcopy(board[0])
        for i in range(board.dim):
            block_num = int(i / board.dim_sqrt)
            n = randint(0, board.dim_sqrt - 1)
            board = self.swap_rows(
                i, block_num * board.dim_sqrt + n, board)
        return board

    def shuffle_cols(self, board: Board) -> Board:
        # board[0] = deepcopy(board[0])
        board.transpose_board()
        board = self.shuffle_rows(board)
        board.transpose_board()
        return board

    def generate_sudoku_list(self, mother_board: "Board", n_sudokus: int) -> Board:
        out_list = []
        out_list.append(deepcopy(mother_board))
        created_sudokus = 1
        while created_sudokus < n_sudokus:
            i = randint(0, len(out_list)-1)
            out_list.append(self.randomnize_board(deepcopy(out_list[i])))
            created_sudokus += 1
            if created_sudokus >= n_sudokus:
                break
        return out_list

    def randomnize_board(self, starting_board: Board) -> Board:
        n_function = randint(0, 4)
        # starting_board.print_board()
        if n_function == 0:
            return self.swap_random_digits(starting_board)
        if n_function == 1:
            return self.shuffle_rows(starting_board)
        if n_function == 2:
            return self.shuffle_cols(starting_board)
        if n_function == 3:
            return self.shuffle_large_rows(starting_board)
        if n_function == 4:
            return self.shuffle_large_cols(starting_board)


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
    print("Original Sudoku")
    b.print_board()

    sol = checker.solve([b])
    print("Solution:")
    sol[0].print_board()

    generator = SudokuGenerator(checker)
    print("Swapping 9 by 5")
    new_board = generator.swap_digits(9, 5, sol[0])
    new_board.print_board()

    print("Shuffled Cols")
    new_board = generator.shuffle_cols(new_board)
    new_board.print_board()

    print("Shuffled Large Row")
    new_board = generator.shuffle_large_rows(new_board)
    new_board.print_board()

    print("Shuffled Large Col")
    new_board = generator.shuffle_large_cols(new_board)
    new_board.print_board()

    one_solution_sudoku = generator.get_one_solution_sudoku(sol)
    print("A random sudoku with one solution:")
    one_solution_sudoku.print_board()

    print("Mother sudoku")
    mother_sudoku = checker.solve([one_solution_sudoku])
    mother_sudoku[0].print_board()

    print("Getting a list of 10 one solution sudokus")
    t_start = time.time()
    list_of_sudokus = generator.generate_sudoku_list(mother_sudoku[0], 100000)
    print("elapsed time is ", time.time() - t_start)
    print("Total Sudokus: ", len(list_of_sudokus))

    for i in range(10):
        list_of_sudokus[i].print_board()
