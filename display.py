from random import randint
from sudoku_generator import SudokuGenerator
from sudoku_checker import BoardChecker
from sudoku import Board
from copy import deepcopy
import pygame
import sys

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800


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
    game_sudoku = list_of_sudokus[randint(0, 10000)]
    game_sudoku.print_board()
    game_sudoku = generator.get_one_solution_sudoku([game_sudoku])
    while True:
        drawGrid(game_sudoku)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


def drawGrid(game_sudoku: Board) -> None:
    # Set the size of the grid block
    blockSize = 1 + ((3 * WINDOW_WIDTH // 4) - (WINDOW_WIDTH // 4)) // 9
    for i, x in enumerate(range(WINDOW_WIDTH // 4, 3 * WINDOW_WIDTH // 4, blockSize)):
        for j, y in enumerate(range(WINDOW_HEIGHT // 4, 3 * WINDOW_HEIGHT // 4, blockSize)):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(SCREEN, BLACK, rect, 1)
            showNumbers(x + blockSize // 2, y +
                        blockSize // 2, game_sudoku.get_number(j, i))


def showNumbers(x: int, y: int, n: int) -> None:
    font = pygame.font.Font('freesansbold.ttf', 32)
    if n == 0:
        text = font.render("X", True, BLACK, WHITE)
    else:
        text = font.render(str(n), True, BLACK, WHITE)
    textRect = text.get_rect()
    textRect.center = (x, y)
    SCREEN.blit(text, textRect)


if __name__ == "__main__":
    main()
