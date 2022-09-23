from random import randint
from sudoku_generator import SudokuGenerator
from sudoku_checker import BoardChecker
from sudoku import Board
from copy import deepcopy
from pygame.locals import *
# one of these is probably what you want
from pygame import rect, Rect, Surface
import pygame
import sys

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)
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
        self.clicked_on = False

        self.text = self.setNumber(number)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (x + side_lenght // 2, y + side_lenght // 2)
        pass

    def changeNumber(self, number: int) -> Surface:
        self.text = self.setNumber(number)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (self.x + self.side_lenght // 2, self.y + self.side_lenght // 2)

    def setNumber(self, number: int) -> Surface:
        if number == 0:
            return self.font.render("", True, BLACK, None)
        else:
            return self.font.render(str(number), True, BLACK, None)


class GraphicBoard:
    def __init__(self, board_: Board, side_lengt: int, x_start: int, y_start: int) -> None:
        self.board = board_
        self.board_dim = self.board.dim
        self.block_size = 1 + side_lengt // self.board_dim
        self.selected_cell_index = -1

        self.boardCellList: "list[BoardCell]" = []
        for i, x in enumerate(range(x_start, x_start + side_lengt, self.block_size)):
            for j, y in enumerate(range(y_start, y_start + side_lengt, self.block_size)):
                number = self.board.get_number(j, i)
                self.boardCellList.append(
                    BoardCell(x, y, self.block_size, number, mutable=number == 0))
        pass

    def setNumber(self, number: int) -> None:
        if self.selected_cell_index > self.board_dim ** 2 or self.selected_cell_index < 0:
            return
        if self.boardCellList[self.selected_cell_index].mutable:
            self.boardCellList[self.selected_cell_index].changeNumber(number)
