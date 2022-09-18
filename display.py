import pygame 
import sys 

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800

def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(WHITE)

    while True:
        drawGrid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


def drawGrid():
    blockSize = 1 + ((3 * WINDOW_WIDTH // 4) - (WINDOW_WIDTH // 4)) // 9  #Set the size of the grid block

    for x in range(WINDOW_WIDTH // 4, 3 * WINDOW_WIDTH // 4, blockSize):
        for y in range(WINDOW_HEIGHT // 4, 3 * WINDOW_HEIGHT // 4, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(SCREEN, BLACK, rect, 1)

if __name__ == "__main__":
    main()