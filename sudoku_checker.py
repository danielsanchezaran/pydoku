from sudoku_generator import Board
class BoardChecker:
    def checkBoardRow(self, b : Board, row : int) -> bool:
        checked_elems = b.dim * [False]
        row_to_check = b.get_row(row)

        for elem in row_to_check:
            if elem == 0:
                return False
            if checked_elems[elem.get_number()-1]:
                return False
            checked_elems[elem.get_number()-1] = True
    def checkBoardColumn(self, b : Board, col: int) -> bool:
        checked_elems = b.dim * [False]
        col_to_check = b.get_col(col)
        print(col_to_check)
        for elem in col_to_check:
            print("Test ", elem.get_number())
            print()
            if elem == 0:   
                return False
            if checked_elems[elem.get_number()-1]:
                return False
            checked_elems[elem.get_number()-1] = True
        return True

if __name__ == "__main__":
    print()
