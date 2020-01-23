import unittest
from sudoku import sudoku_game


def _sample_sudoku_with_solution():
    solution = sudoku_game.SudokuBoard()
    solution.board = [
        [9, 7, 6, 4, 8, 1, 3, 2, 5],
        [1, 4, 3, 2, 5, 9, 7, 8, 6],
        [5, 2, 8, 3, 7, 6, 1, 9, 4],
        [6, 9, 4, 5, 1, 8, 2, 3, 7],
        [8, 1, 2, 7, 3, 4, 5, 6, 9],
        [7, 3, 5, 9, 6, 2, 4, 1, 8],
        [4, 6, 7, 8, 2, 3, 9, 5, 1],
        [2, 5, 1, 6, 9, 7, 8, 4, 3],
        [3, 8, 9, 1, 4, 5, 6, 7, 2]
    ]
    game = sudoku_game.SudokuBoard()
    game.board = [
        [9, 0, 0, 0, 8, 0, 3, 0, 0],
        [0, 0, 0, 2, 5, 0, 7, 0, 0],
        [0, 2, 0, 3, 0, 0, 0, 0, 4],
        [0, 9, 4, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 7, 3, 0, 5, 6, 0],
        [7, 0, 5, 0, 6, 0, 4, 0, 0],
        [0, 0, 7, 8, 0, 3, 9, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 3],
        [3, 0, 0, 0, 0, 0, 0, 0, 2]
    ]
    return game, solution


class TestSudoku(unittest.TestCase):
    def test_empty_sudoku(self):
        game = sudoku_game.SudokuBoard()
        for row in game.board:
            self.assertTrue(all(val == 0 for val in row), "Board is not empty")

    def test_not_empty_sudoku(self):
        game, solution = _sample_sudoku_with_solution()
        is_empty = True
        for row in game.board:
            if not all(val == 0 for val in row):
                is_empty = False
        self.assertFalse(is_empty)

    def test_solver_by_fields(self):
        game, solution = _sample_sudoku_with_solution()
        game.solver_by_fields()
        self.assertListEqual(game.board, solution.board)

    def test_solver_by_values(self):
        game, solution = _sample_sudoku_with_solution()
        game.solver_by_values()
        self.assertListEqual(game.board, solution.board)

    def test_is_ready(self):
        game, solution = _sample_sudoku_with_solution()
        self.assertTrue(solution._is_ready())
        self.assertFalse(game._is_ready())

    # def test_possible_digits(self):
    #    game, solution = _sample_sudoku_with_solution()
    #    solution = _missig_squre_digits_data()
    #    for i in range(9):
    #        for j in range(9):
    #            possible_square_digits = game._square_missing_numbers(i, j)
    #            print(solution[i])
    #            self.assertListEqual(possible_square_digits, solution[i])
