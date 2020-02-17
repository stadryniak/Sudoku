from pygame.constants import QUIT

from game_ui import pg
import sys

WAITMS = 10


def update_dispay_text(boxes, x, y, move):
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit(0)
    boxes[x][y].text = str(move)
    if move == 0:
        boxes[x][y].text = "    "
    boxes[x][y].draw()
    pg.display.update()
    pg.time.wait(WAITMS)


class SudokuBoard:
    """
    creates sudoku board of given size (and appropriate max field value), initial values are 0, solver function
    """

    def __init__(self):
        self.interactive_mode = False
        self.nDims = 9
        self.maxNumber = 9
        self.board = []
        for i in range(self.nDims):
            self.board.append([])
            for j in range(self.nDims):
                self.board[i].append(0)

    def print_board(self):
        for i in range(self.nDims):
            print(self.board[i])

    def solver_by_values(self):
        loc = [0, 0]
        if not self._empty_fields(loc):
            return True
        for val in range(1, 10):
            possible_moves = self._possible_moves(loc[0], loc[1])
            if val not in possible_moves:
                continue
            if possible_moves:
                self.board[loc[0]][loc[1]] = val
                if self.solver_by_values():
                    return True
                self.board[loc[0]][loc[1]] = 0
        return False

    def _empty_fields(self, li):
        for row in range(self.nDims):
            for col in range(self.nDims):
                if self.board[row][col] == 0:
                    li[0] = row
                    li[1] = col
                    return True
        return False

    def solver_by_fields(self, boxes=None):
        """
        Calls backtracking solver function
        :param boxes:
        :return:
        """
        if boxes is None:
            boxes = [[]]
        return self._solver_by_fields_internal(0, 0, self.board[0][0], boxes)

    def _solver_by_fields_internal(self, x: int, y: int, move, boxes=None):
        """
        Backtracking solver. Boxes are for display function.
        :param x:
        :param y:
        :param move:
        :param boxes:
        :return:
        """
        if boxes is None:
            boxes = [[]]
        flag = 0  # is set to 1 when backtracking occurs (breaks loops)
        self.board[x][y] = move
        if self.interactive_mode:
            update_dispay_text(boxes, x, y, move)
        if self._is_ready():
            return True
        for i in range(self.nDims):
            for j in range(self.nDims):
                if self.board[i][j] != 0:
                    continue
                possible_moves = tuple(self._possible_moves(i, j))
                if not possible_moves:
                    self.board[x][y] = 0
                    if self.interactive_mode:
                        update_dispay_text(boxes, x, y, 0)
                    return False
                for new_move in possible_moves:
                    if self._solver_by_fields_internal(i, j, new_move, boxes):
                        return True
                    else:
                        flag = 1
                if flag == 1:
                    break
            if flag == 1:
                break
        self.board[x][y] = 0
        if self.interactive_mode:
            update_dispay_text(boxes, x, y, 0)
        return False

    def _possible_moves(self, x, y) -> list:
        """
        Generate list of values possible in given square
        :param x:
        :param y:
        :return:
        """
        available_numbers = list(range(1, self.nDims + 1))
        self._square_missing_numbers(x, y, available_numbers)
        self._line_missing_numbers(x, y, available_numbers)
        return available_numbers

    def _is_ready(self):
        """
        Check if all squares are filled
        :return:
        """
        for row in self.board:
            is_filled = all(val != 0 for val in row)
            if not is_filled:
                return False
        return True

    def _line_missing_numbers(self, x, y, available_numbers):
        """
        Removes impossible values from available numbers
        :param x:
        :param y:
        :param available_numbers:
        """
        if self.board[x][y] != 0:
            return []
        for i in range(9):
            for j in range(9):
                if i == x or j == y:
                    try:
                        available_numbers.remove(self.board[i][j])
                    except ValueError:
                        pass

    def _square_missing_numbers(self, x: int, y: int, possible_numbers):
        """
        Removes imposible numbers from possible numbers
        :param x:
        :param y:
        :param possible_numbers:
        """
        for i in range(x // 3 * 3, x // 3 * 3 + 3):
            for j in range(y // 3 * 3, y // 3 * 3 + 3):
                if not (i == x and j == y):
                    try:
                        possible_numbers.remove(self.board[i][j])
                    except ValueError:
                        pass

    def validate_solution(self):
        possible_numbers = []
        for i in range(self.nDims):
            possible_numbers = list(range(1, self.nDims + 1))
            for j in self.board[i]:
                try:
                    possible_numbers.remove(j)
                except ValueError:
                    return False
        if possible_numbers:
            return False
        for j in range(self.nDims):
            possible_numbers = list(range(1, self.nDims + 1))
            for i in range(self.nDims):
                try:
                    possible_numbers.remove(self.board[i][j])
                except ValueError:
                    return False
            if possible_numbers:
                return False
        return True
