from random import randint
from sudoku_generator import SudokuGenerator
from sudoku_checker import BoardChecker
from sudoku import Board
from copy import deepcopy
from pygame.locals import *
from pygame import rect, Rect, Surface
import pygame
import sys

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)
YELLOW = (200,200,0)
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800


class BoardCell:
    def __init__(self, x: int, y: int, side_lenght: int, number: int, mutable: bool) -> None:
        self.x = x 
        self.y = y
        self.side_lenght = side_lenght
        self.outer_rect = pygame.Rect(x, y, side_lenght, side_lenght)
        self.inner_rect = pygame.Rect(x+1, y+1, side_lenght-2, side_lenght-2)
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.mutable = mutable
        self.select_color = GREEN
        self.mutable_color = YELLOW
        self.clicked_on = False
        self.setNumber(number)
        pass

    def setNumber(self, number: int) -> None:
        if number == 0:
            self.text =  self.font.render("", True, BLACK, None)
        else:
            self.text =  self.font.render(str(number), True, BLACK, None)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (self.x + self.side_lenght // 2, self.y + self.side_lenght // 2)


class GraphicBoard:
    def __init__(self, board_: Board, side_lengt: int, x_start: int, y_start: int) -> None:
        self.starting_board = deepcopy(board_)
        self.board = deepcopy(board_)
        self.board_dim = self.board.dim
        self.block_size = 1 + side_lengt // self.board_dim
        self.selected_cell_index = -1

        self.boardCellList: "list[BoardCell]" = []
        for i, x in enumerate(range(x_start, x_start + side_lengt, self.block_size)):
            for j, y in enumerate(range(y_start, y_start + side_lengt, self.block_size)):
                number = self.board.getNumber(j, i)
                self.boardCellList.append(
                    BoardCell(x, y, self.block_size, number, mutable=number == 0))
        pass

    def setNumber(self, number: int) -> None:
        if self.selected_cell_index > self.board_dim ** 2 or self.selected_cell_index < 0:
            return
        if self.boardCellList[self.selected_cell_index].mutable:
            col = self.selected_cell_index // self.board_dim
            row = self.selected_cell_index - col * self.board_dim 
            self.boardCellList[self.selected_cell_index].setNumber(number)
            self.board.setNumber(row,col,number)
    def solve(self) -> None:
        checker = BoardChecker("default")
        self.starting_board = checker.solve([self.starting_board])[0]
        self.starting_board.transposeBoard()
        number_list = self.starting_board.getBoardAsRowList()
        for i,cell in enumerate(self.boardCellList):
            cell.setNumber(number_list[i])
        self.starting_board.transposeBoard()
        self.board = deepcopy(self.starting_board)