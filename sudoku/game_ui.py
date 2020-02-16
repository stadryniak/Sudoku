import pygame
import sys
from pygame.locals import *

# Sets background color
BACKGROUND = (255, 255, 255)
# Sets frames per second
FPS = 10
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

COLOR_ACTIVE = (200, 200, 200)
COLOR_INACTIVE = WHITE

pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Sudoku")
DISPLAYSURF.fill(BACKGROUND)
FONT = pygame.font.Font('freesansbold.ttf', 30)


def draw_grid():
    """
    Draws sudoku grid
    :return:
    """
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
    """
    Writes prexisting values to grid as text rect
    :param middles: list of cells middle (generated by cells_middle())
    :param data: game board
    :return:
    """
    i = 0
    j = 0
    for row in middles:
        for mid in row:
            if data[i][j]:
                text = FONT.render(str(data[i][j]), True, BLACK, WHITE)
                text_rect = text.get_rect()
                text_rect.center = mid
                DISPLAYSURF.blit(text, text_rect)
            j += 1
        i += 1
        j = 0


def cells_middle():
    """
    Calculates middle of cells and put them into list of lists.
    Every inner list represents one row of cells
    :return:
    """
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


def set_input_boxes(game, cells_mid):
    cells = []
    for i in range(9):
        cells.append([])
        for j in range(9):
            inputbox = InputBox(cells_mid[i][j])
            if game.board[i][j] != 0:
                inputbox.taken = True
            cells[i].append(inputbox)
    return cells


class InputBox:
    def __init__(self, mid, text="", taken=False):
        self.text = FONT.render(text, True, BLACK, WHITE)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (mid[0] - CELLSIZE // 10, mid[1])
        self.taken = taken

    def draw(self):
        text = FONT.render(self.text, True, BLACK, WHITE)
        DISPLAYSURF.blit(text, self.text_rect)


def main_ui(game):
    """

    :type game: SudokuBoard
    """
    global FPSCLOCK, DISPLAYSURF

    draw_grid()
    cells_mid = cells_middle()
    cells = set_input_boxes(game, cells_mid)
    game.interactive_mode = True
    populate_cells(cells_mid, game.board)
    flag = 1
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
        if game.validate_solution():
            for li in cells:
                for box in li:
                    if not box.taken:
                        box.draw()
        pygame.display.update()
        if flag == 1:
            pygame.time.wait(3000)
            game.solver_by_fields(cells)
            flag = 0
        FPSCLOCK.tick(FPS)
