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

    font = pygame.font.Font('freesansbold.ttf', 32)
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
    mother_sudoku.setSudokuList(copied_sudoku)
    checker = BoardChecker("default")
    generator = SudokuGenerator(checker)
    mother_sudoku = checker.solve([mother_sudoku])
    mother_sudoku = mother_sudoku[0]
    list_of_sudokus = generator.generate_sudoku_list(mother_sudoku, 1000)
    mother_sudoku.printBoard()
    game_sudoku_solved : Board = list_of_sudokus[randint(0, 1000)]
    game_sudoku = generator.get_one_solution_sudoku([deepcopy(game_sudoku_solved)])
    game_sudoku_solved.printBoard()
    while (game_sudoku.getFilledCellsAmmount() > (game_sudoku.dim**2)):
        game_sudoku = generator.get_one_solution_sudoku([deepcopy(game_sudoku_solved)])
    print("Filled cells ", game_sudoku.getFilledCellsAmmount())
    graphic_board = GraphicBoard(game_sudoku, side_lengt=WINDOW_WIDTH //
                                 2, x_start=WINDOW_WIDTH // 4, y_start=WINDOW_HEIGHT // 4)
    solve_button = pygame.Rect(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 10, WINDOW_HEIGHT // 10, WINDOW_HEIGHT // 10)
    button_list = [solve_button]
    while True:
        SCREEN.fill(WHITE)
        drawBoard(graphic_board)
        drawButtons(button_list=button_list)
        if (checkPuzzleSolved(game_sudoku_solved,graphic_board.board)):
            graphic_board.selected_cell_index = -1
            solved_text = font.render("Solved", True, BLACK, None)
            solved_text_rect = solved_text.get_rect()
            solved_text_rect.center = (WINDOW_WIDTH // 2, 9 * WINDOW_HEIGHT // 10)
            SCREEN.blit(solved_text, solved_text_rect)
        else: 
            checkClicks(graphic_board=graphic_board, button_list=button_list)
            
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.unicode.isdigit():
                graphic_board.setNumber(int(event.unicode))
                game_sudoku_solved.printBoard()
                graphic_board.board.printBoard()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

def drawButtons(button_list : "list[Rect]"):
    for button in button_list:
        pygame.draw.rect(SCREEN, BLACK, button, 1)

def checkPuzzleSolved(solved_board: Board, current_board: Board) -> bool:
    if current_board.getFilledCellsAmmount() != current_board.dim ** 2:
        return False
    solved_list = solved_board.getBoardAsRowList()
    current_list = current_board.getBoardAsRowList()
    if len(current_list) != len(solved_list):
        return False 
    for i in range(len(solved_list)):
        if solved_list[i] != current_list[i]:
            return False 
    return True

def checkBoardClicks(graphic_board: GraphicBoard) -> None:
    if pygame.mouse.get_pressed()[0]:
        graphic_board.selected_cell_index = -1
        for i, cell in enumerate(graphic_board.boardCellList):
            cell.clicked_on = False
            if cell.outer_rect.collidepoint(pygame.mouse.get_pos()) and cell.mutable:
                cell.clicked_on = True
                graphic_board.selected_cell_index = i

def checkButtonPress(graphic_board: GraphicBoard, button_list : "list[Rect]") -> int:
    for i, button in enumerate(button_list):
        if pygame.mouse.get_pressed()[0] and button.collidepoint(pygame.mouse.get_pos()):
            graphic_board.solve()
            return i 
    return -1


def checkClicks(graphic_board: GraphicBoard, button_list : "list[Rect]") -> None:
    checkBoardClicks(graphic_board=graphic_board)
    checkButtonPress(graphic_board=graphic_board, button_list=button_list)


def drawBoard(graphic_board: GraphicBoard) -> None:
    for cell in graphic_board.boardCellList:
        pygame.draw.rect(SCREEN, BLACK, cell.outer_rect, 1)
        if cell.mutable:
            pygame.draw.rect(SCREEN, cell.mutable_color, cell.inner_rect, 0)
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
                        block_size // 2, game_sudoku.getNumber(j, i))


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
