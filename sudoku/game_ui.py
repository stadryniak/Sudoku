import pygame
import sys
from pygame.locals import *
from sudoku import sudoku_game

# Sets background color
BACKGROUND = (255, 255, 255)
# Sets frames per second
FPS = 30
# Sets size of grid
WINDOWMULTIPLIER = 5  # Modify this number to change size of grid
WINDOWSIZE = 90
WINDOWWIDTH = WINDOWSIZE * WINDOWMULTIPLIER
WINDOWHEIGHT = WINDOWSIZE * WINDOWMULTIPLIER
SQUARESIZE = (WINDOWSIZE * WINDOWMULTIPLIER) // 3
CELLSIZE = SQUARESIZE // 3
# Sets colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)

pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Sudoku")
DISPLAYSURF.fill(BACKGROUND)


def draw_grid():
    # Draw minor lines
    for x in range(0, WINDOWWIDTH, CELLSIZE):  # draw vertical lines
        pygame.draw.line(DISPLAYSURF, GRAY, (x, 0), (x, WINDOWHEIGHT))
        if x % SQUARESIZE == 0:  # draw major lines
            pygame.draw.line(DISPLAYSURF, BLACK, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, GRAY, (0, y), (WINDOWWIDTH, y))
        if y % SQUARESIZE == 0:
            pygame.draw.line(DISPLAYSURF, BLACK, (0, y), (WINDOWWIDTH, y))
    return None


def populate_cells(middles, data):
    i = 0
    j = 0
    for row in middles:
        for mid in row:
            if data[i][j]:
                font = pygame.font.Font('freesansbold.ttf', 30)
                text = font.render(str(data[i][j]), True, BLACK, WHITE)
                text_rect = text.get_rect()
                text_rect.center = mid
                DISPLAYSURF.blit(text, text_rect)
            j += 1
        i += 1
        j = 0


def cells_middle():
    middle = [CELLSIZE // 2, CELLSIZE // 2]
    res = []
    for i in range(9):
        res.append([])
        for j in range(9):
            res[i].append((middle[0], middle[1]))
            middle[0] += CELLSIZE
        middle[1] += CELLSIZE
        middle[0] = CELLSIZE // 2
    return res


def main_ui(game):
    global FPSCLOCK, DISPLAYSURF

    draw_grid()
    cells_mid = cells_middle()
    populate_cells(cells_mid, game.board)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
        pygame.display.update()
        FPSCLOCK.tick(FPS)
