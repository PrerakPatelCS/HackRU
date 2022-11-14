import time
from twitch_plays_hackru import TwitchPlaysOnline, TwitchPlaysOffline
import DrawBoard as board
import random

state = []
moveCounter = 0
options = []
square = [0]


def initialize():
    """
    Initialize all global variables
    State is array of X's and O's for the computer move
    moveCounter counts the number of moves done so far
    options is the array of all the options twitch chat can choose
    square is the array with all the squares on it and will update with X's and O's
    """
    global state
    global moveCounter
    global options
    global square
    state = []
    moveCounter = 0
    options = []
    square = [0]

    count = 1
    for q in range(board.ROWS * board.COLUMNS):
        square.append(count)
        options.append(count.__str__())
        count += 1
    for x in range(len(options)):
        state.append('')
    board.updatePos()


def reset():
    """
    reset all globals and redraw board
    """
    global state
    global moveCounter
    global options
    global square
    board.drawer.reset()
    for i in range(len(square)):
        square[i] = i
    for w in range(len(options)):
        state[w] = ''
    board.screen.update()
    board.drawer.pensize(board.PENSIZE)
    board.drawer.ht()
    board.drawBoard()
    moveCounter = 0


def computerMove():
    """
    Picks a random square amongst open squares
    :return: position
    """
    global options
    global state
    openSpots = [0]*len(options)
    m = 1
    while m <= len(options):
        if state[m-1] == '':
            openSpots[m-1] = m
        m = m+1
    position = random.choice(openSpots)
    while position == 0:
        position = random.choice(openSpots)
    n = 0
    while n < len(options):
        openSpots[n] = 0
        n = n+1
    return position


def insertMark(choice):
    """
    Insert mark in the square the choice is on.
    Puts an X or O depending on move number
    :param choice:
    :return: 1 if mark placed and -1 if mark cannot be placed
    """
    global square
    global state
    global moveCounter

    if choice != 0 and 0 < choice < len(square) and square[choice] == choice:
        if moveCounter % 2 == 1:
            mark = 'X'
            board.drawX(choice)
        else:
            mark = 'O'
            board.drawO(choice)
        square[choice] = mark
        state[choice - 1] = mark
        moveCounter += 1
    else:
        print('Invalid move ')
        return -1
    return 1


def main():
    """
    Initialize the twitch connection
    Infinite loop for TicTacToe games
    """
    global state
    global moveCounter
    global options
    global square
    initialize()
    twitch_options = {
        "PASS": "oauth:i4dlkrowykpzqpe3z6sm05lzf12xc4",
        "BOT": "TicTacToe",
        "CHANNEL": "patuitar",
        "OWNER": "patuitar",
        "OPTIONS": options,
        "VOTE_INTERVAL": 5
    }
    tPlays = TwitchPlaysOnline(**twitch_options)    # Initialize the TwitchPlays bot.
    board.drawBoard()
    while True:
        status = game_status()
        while status == -1:
            if moveCounter % 2 == 1:
                result = "0"
                while result == "0":
                    result = tPlays.vote_result()
                    if result is None:
                        result = "0"
                        time.sleep(5)
                choice = int(result)
            else:
                time.sleep(5)
                choice = int(computerMove())

            if insertMark(choice) == 1:
                print('\nPlayer', moveCounter % 2)
                status = game_status()

        print('RESULT')
        if status == 1:
            print('Player', moveCounter % 2, 'win')
        else:
            print('Game draw')

        reset()


def game_status():
    """
    Figures out the game state
    :return: 1 for win 0 for tie and -1 for game not decided yet
    """
    global state
    global moveCounter
    global options
    global square

    def winByRow():
        """
        Check every row for win
        :return: 1 if win and -1 otherwise
        """
        isWin = -1
        for r in range(board.ROWS):
            previous = ''
            if isWin == 1:
                return 1
            isWin = -1
            for c in range(board.COLUMNS):
                if previous == '':
                    previous = square[r * board.COLUMNS + (c + 1)]
                else:
                    if square[r * board.COLUMNS + (c + 1)] == previous and isWin != 0:
                        isWin = 1
                    else:
                        isWin = 0
        if isWin == 1:
            return 1
        else:
            return -1

    def winByColumn():
        """
        Check every column for win
        :return: 1 if win and -1 otherwise
        """
        isWin = -1
        for c in range(board.COLUMNS):
            previous = ''
            if isWin == 1:
                return 1
            isWin = -1
            for r in range(board.ROWS):
                if previous == '':
                    previous = square[(c + 1) + (board.ROWS * r)]
                else:
                    if square[(c + 1) + (board.ROWS * r)] == previous and isWin != 0:
                        isWin = 1
                    else:
                        isWin = 0
        if isWin == 1:
            return 1
        return -1

    def winByDiagonal():
        """
        Check both diagonals
        :return: 1 if win and -1 otherwise
        """
        isWin = -1
        previous = ''
        for r in range(board.ROWS):
            if previous == '':
                previous = square[r * board.ROWS + (r + 1)]
            else:
                if square[r * board.ROWS + (r + 1)] == previous and isWin != 0:
                    isWin = 1
                else:
                    isWin = 0
        if isWin == 1:
            return 1

        isWin = -1
        previous = ''
        for r in range(board.ROWS):
            if previous == '':
                previous = square[(board.ROWS - r) + (board.ROWS * r)]
            else:
                if square[(board.ROWS - r) + (board.ROWS * r)] == previous and isWin != 0:
                    isWin = 1
                else:
                    isWin = 0
        if isWin == 1:
            return 1
        else:
            return -1

    def checkTie():
        """
        Check if every square is full and no one won
        :return: 0 if tie and -1 otherwise
        """
        moves = 0
        for q in range(len(square)):
            if square[q] == 'O' or square[q] == 'X':
                moves += 1
        if moves == len(options):
            return 0
        else:
            return -1

    if board.COLUMNS == board.ROWS:
        isWinRow = winByRow()
        if isWinRow == -1:
            isWinColumn = winByColumn()
            if isWinColumn == -1:
                isWinDiagonal = winByDiagonal()
                if isWinDiagonal == -1:
                    isTie = checkTie()
                    if isTie == -1:
                        return -1
                    else:
                        print("TIE")
                        return 0
                else:
                    print("WIN BY DIAGONAL")
                    return 1
            else:
                print("WIN BY COLUMN")
                return 1
        else:
            print("WIN BY ROW")
            return 1
    elif board.COLUMNS > board.ROWS:
        isWinColumn = winByColumn()
        print("COLUMNS>ROWS")
        return isWinColumn
    else:
        isWinRow = winByRow()
        print("ROWS>COLUMNS")
        return isWinRow


if __name__ == '__main__':
    main()
