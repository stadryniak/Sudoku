class SudokuBoard:
    """
    creates sudoku board of given size (and appropriate max field value), initial values are 0, solver function
    """

    def __init__(self):
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

    def solver(self):
        return self._solver_internal(0, 0, self.board[0][0])

    def _solver_internal(self, x: int, y: int, move):
        flag = 0
        self.board[x][y] = move
        if self._is_ready():
            return True
        for i in range(self.nDims):
            for j in range(self.nDims):
                if self.board[i][j] != 0:
                    continue
                possible_moves = tuple(self._possible_moves(i, j))
                if not possible_moves:
                    self.board[x][y] = 0
                    return False
                for new_move in possible_moves:
                    if self._solver_internal(i, j, new_move):
                        return True
                    else:
                        flag = 1
                if flag == 1:
                    break
            if flag == 1:
                break
        self.board[x][y] = 0
        return False

    def _possible_moves(self, x, y) -> list:
        available_numbers = self._square_missing_numbers(x, y)
        possible_numbers = self._line_missing_numbers(x, y, available_numbers)
        # print(possible_numbers)
        return possible_numbers

    def _is_ready(self):
        for row in self.board:
            is_filled = all(val != 0 for val in row)
            if not is_filled:
                return False
        return True

    def _line_missing_numbers(self, v, c, available_numbers):  # fix it later, poor performance
        if self.board[v][c] != 0:
            return []
        for i in range(9):
            for j in range(9):
                if i == v or j == c:
                    try:
                        available_numbers.remove(self.board[i][j])
                    except ValueError:
                        pass
        return available_numbers

    def _square_missing_numbers(self, v: int, c: int) -> list:
        possible_numbers = list(range(1, self.nDims + 1))
        for i in range(v // 3 * 3, v // 3 * 3 + 3):
            for j in range(c // 3 * 3, c // 3 * 3 + 3):
                if not (i == v and j == c):
                    try:
                        possible_numbers.remove(self.board[i][j])
                    except ValueError:
                        pass
        return possible_numbers
