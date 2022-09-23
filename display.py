from random import randint
from sudoku_generator import SudokuGenerator
from sudoku_checker import BoardChecker
from sudoku import Board
from copy import deepcopy
from pygame.locals import *
from pygame import rect, Rect  # one of these is probably what you want
from drawables import *
import pygame
import sys


def main():
    global SCREEN, CLOCK
    pygame.init()
    pygame.display.set_caption('Sudoku')
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(WHITE)

    mother_sudoku = Board(9)
    copied_sudoku = [[0, 0, 3, 0, 2, 0, 6, 0, 0],
                     [9, 0, 0, 3, 0, 5, 0, 0, 1],
                     [0, 0, 1, 8, 0, 6, 4, 0, 0],
                     [0, 0, 8, 1, 0, 2, 9, 0, 0],
                     [7, 0, 0, 0, 0, 0, 0, 0, 8],
                     [0, 0, 6, 7, 0, 8, 2, 0, 0],
                     [0, 0, 2, 6, 0, 9, 5, 0, 0],
                     [8, 0, 0, 2, 0, 3, 0, 0, 9],
                     [0, 0, 5, 0, 1, 0, 3, 0, 0]]
    mother_sudoku.set_sudoku_list(copied_sudoku)
    checker = BoardChecker("default")
    generator = SudokuGenerator(checker)
    mother_sudoku = checker.solve([mother_sudoku])
    mother_sudoku = mother_sudoku[0]
    list_of_sudokus = generator.generate_sudoku_list(mother_sudoku, 10000)
    mother_sudoku.print_board()
    game_sudoku_solved = list_of_sudokus[randint(0, 10000)]
    game_sudoku_solved.print_board()
    game_sudoku = generator.get_one_solution_sudoku([game_sudoku_solved])

    while (game_sudoku.get_filled_cells_ammount() > (game_sudoku.dim**2) * 0.4):
        game_sudoku = generator.get_one_solution_sudoku([game_sudoku_solved])
    print("Filled cells ", game_sudoku.get_filled_cells_ammount())
    graphic_board = GraphicBoard(game_sudoku, side_lengt=WINDOW_WIDTH //
                                 2, x_start=WINDOW_WIDTH // 4, y_start=WINDOW_HEIGHT // 4)

    # drawGrid(game_sudoku)
    while True:
        SCREEN.fill(WHITE)
        checkClicks(graphic_board=graphic_board)
        drawBoard(graphic_board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


def checkClicks(graphic_board: GraphicBoard) -> None:
    if pygame.mouse.get_pressed()[0]:
        for i, cell in enumerate(graphic_board.boardCellList):
            cell.clicked_on = False
            if cell.outer_rect.collidepoint(pygame.mouse.get_pos()):
                cell.clicked_on = True

def drawBoard(graphic_board: GraphicBoard) -> None:
    for cell in graphic_board.boardCellList:
        pygame.draw.rect(SCREEN, BLACK, cell.outer_rect, 1)
        if cell.clicked_on:
            pygame.draw.rect(SCREEN, cell.select_color, cell.inner_rect, 0)
        SCREEN.blit(cell.text, cell.text_rect)


def drawGrid(game_sudoku: Board) -> None:
    # Set the size of the grid block
    block_size = 1 + ((3 * WINDOW_WIDTH // 4) - (WINDOW_WIDTH // 4)) // 9
    for i, x in enumerate(range(WINDOW_WIDTH // 4, 3 * WINDOW_WIDTH // 4, block_size)):
        for j, y in enumerate(range(WINDOW_HEIGHT // 4, 3 * WINDOW_HEIGHT // 4, block_size)):
            rect = pygame.Rect(x, y, block_size, block_size)
            pygame.draw.rect(SCREEN, BLACK, rect, 1)
            showNumbers(x + block_size // 2, y +
                        block_size // 2, game_sudoku.get_number(j, i))


def showNumbers(x: int, y: int, n: int) -> None:
    font = pygame.font.Font('freesansbold.ttf', 32)
    if n == 0:
        text = font.render(" ", True, BLACK, WHITE)
    else:
        text = font.render(str(n), True, BLACK, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (x, y)
    SCREEN.blit(text, text_rect)


if __name__ == "__main__":
    main()
