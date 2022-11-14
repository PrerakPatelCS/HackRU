import time
import unittest
import TicTacToe as game
import DrawBoard as board


BOARD_SIZE = 3
BOARD_INCREMENT = 2
SLEEP = 1


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        board.drawBoard()
        time.sleep(SLEEP/4)

    def test_insertMark(self):
        """
        Test insertMark function
        Test the insertMark by putting an O and an X in every Square and in multiple board sizes
        make sure the square and state arrays are updated accordingly
        Test that it oscillates between O and X correctly
        Test that it cannot put a O or X in an already claimed square
        Test out of bounds inserts
        :return:
        """
        for r in range(BOARD_SIZE):
            game.initialize()
            game.reset()
            for i in range(board.ROWS * board.COLUMNS):
                self.assertEqual(game.insertMark(i + 1), 1)  
                if i % 2:
                    self.assertEqual(game.square[i + 1], 'X')  
                    self.assertEqual(game.state[i], 'X')  
                else:
                    self.assertEqual(game.square[i + 1], 'O')  
                    self.assertEqual(game.state[i], 'O')  
                self.assertEqual(game.moveCounter, i + 1)
                time.sleep(SLEEP/40)
            game.reset()
            game.moveCounter += 1
            for t in range(board.ROWS * board.COLUMNS):
                self.assertEqual(game.insertMark(t + 1), 1)  
                if t % 2:
                    self.assertEqual(game.square[t + 1], 'O')  
                    self.assertEqual(game.state[t], 'O')  
                else:
                    self.assertEqual(game.square[t + 1], 'X')  
                    self.assertEqual(game.state[t], 'X')  
                self.assertEqual(game.moveCounter, t + 2)
                time.sleep(SLEEP/200)
            board.ROWS += BOARD_INCREMENT
            board.COLUMNS += BOARD_INCREMENT
        board.ROWS = 3
        board.COLUMNS = 3
        game.reset()
        game.initialize()

        self.assertEqual(game.insertMark(1), 1)  
        self.assertEqual(game.square[1], 'O')  
        self.assertEqual(game.state[1 - 1], 'O')  
        self.assertEqual(game.moveCounter, 1)
        time.sleep(SLEEP/4)
        # test same input
        self.assertEqual(game.insertMark(1), -1)  
        self.assertEqual(game.square[1], 'O')  
        self.assertEqual(game.state[1 - 1], 'O')  
        self.assertEqual(game.moveCounter, 1)
        time.sleep(SLEEP/4)

        # out of bounds tests
        self.assertEqual(game.insertMark(0), -1)  
        time.sleep(SLEEP)
        self.assertEqual(game.insertMark(-2), -1)  
        time.sleep(SLEEP)
        self.assertEqual(game.insertMark(10), -1)  
        time.sleep(SLEEP)
        board.ROWS = 3
        board.COLUMNS = 3
        game.reset()
        game.initialize()

    def test_winByRow(self):
        """
        Test win by a row in every row and in multiple different grind sizes
        :return:
        """
        for i in range(BOARD_SIZE):
            game.initialize()
            game.reset()
            for r in range(board.ROWS):
                game.reset()
                for c in range(board.COLUMNS):
                    game.insertMark(r * board.COLUMNS + (c + 1))
                    if c != board.COLUMNS - 1:
                        game.insertMark(((r + 1) % board.ROWS) * board.COLUMNS + (c + 1))
                        self.assertEqual(game.game_status(), -1)
                        continue
                    self.assertEqual(game.game_status(), 1)
                    time.sleep(SLEEP)
            board.ROWS += BOARD_INCREMENT
            board.COLUMNS += BOARD_INCREMENT
        board.ROWS = 3
        board.COLUMNS = 3

    def test_winByColumn(self):
        """
        Test win by a column in every row and in multiple different grind sizes
        :return:
        """
        for i in range(BOARD_SIZE):
            game.initialize()
            game.reset()
            for c in range(board.COLUMNS):
                game.reset()
                for r in range(board.ROWS):
                    game.insertMark((c + 1) + (board.ROWS * r))
                    if r != board.ROWS - 1:
                        game.insertMark(((c + 1) % board.COLUMNS) + 1 + (board.ROWS * r))
                        self.assertEqual(game.game_status(), -1)
                        continue
                    self.assertEqual(game.game_status(), 1)
                    time.sleep(SLEEP)
            board.ROWS += BOARD_INCREMENT
            board.COLUMNS += BOARD_INCREMENT
        board.ROWS = 3
        board.COLUMNS = 3

    def test_winByDiagonal(self):
        """
        Test win by diagonal in multiple different grid sizes
        :return:
        """
        for i in range(BOARD_SIZE):
            game.initialize()
            game.reset()
            for r in range(board.ROWS):
                game.insertMark(r * board.ROWS + (r + 1))
                if r != board.ROWS - 1:
                    game.insertMark(r * board.ROWS + ((r + 1) % board.ROWS) + 1)
                    self.assertEqual(game.game_status(), -1)
                    continue
                self.assertEqual(game.game_status(), 1)
                time.sleep(SLEEP)
            board.ROWS += BOARD_INCREMENT
            board.COLUMNS += BOARD_INCREMENT

        board.ROWS = 3
        board.COLUMNS = 3

        for i in range(BOARD_SIZE):
            game.initialize()
            game.reset()
            for r in range(board.ROWS):
                game.insertMark((board.ROWS - r) + (board.ROWS * r))
                if r != board.ROWS - 1:
                    game.insertMark(((board.ROWS - r - 1) % board.ROWS) + (board.ROWS * r))
                    self.assertEqual(game.game_status(), -1)
                    continue
                self.assertEqual(game.game_status(), 1)
                time.sleep(SLEEP)
            board.ROWS += BOARD_INCREMENT
            board.COLUMNS += BOARD_INCREMENT
        board.ROWS = 3
        board.COLUMNS = 3

    def test_checkTie(self):
        """
        Randomly pick squares on the board until there is a tie
        :return:
        """
        game.initialize()
        game.reset()
        while True:
            if game.game_status() == 1:
                game.reset()
            if game.moveCounter == board.ROWS * board.COLUMNS:
                self.assertEqual(game.game_status(), 0)
                time.sleep(SLEEP*3)
                break
            game.insertMark(game.computerMove())
            time.sleep(SLEEP)

    if __name__ == '__main__':
        unittest.main()
