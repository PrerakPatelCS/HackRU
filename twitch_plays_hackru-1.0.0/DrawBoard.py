import math
import turtle


SIZE = 300
# For Tic Tac Toe ROWS and COLUMNS should be the same
ROWS = 3
COLUMNS = 3
PENSIZE = 10
HALF_CIRCLE = 180
X_ANGLE = 60
FONT_SIZE = 12
drawer = turtle.Turtle()
turtle.title("Tic Tac Toe")
drawer.pensize(PENSIZE)
drawer.ht()

screen = turtle.Screen()
screen.screensize(canvwidth=SIZE, canvheight=SIZE)
screen.tracer(0)
pos = 0


def updatePos():
    """
    Used to help size the X's and O's for each square
    """
    global pos
    R_or_C = COLUMNS
    if ROWS > COLUMNS:
        R_or_C = ROWS
    pos = SIZE / (R_or_C - 1)


def drawBoard():
    """
    Draw TicTacToe board with N rows and M columns and number each square starting from 1 to N*M
    """
    for i in range(ROWS - 1):
        drawer.penup()
        drawer.goto(-SIZE, SIZE - ((SIZE * 2) / ROWS) * (i + 1))
        drawer.pendown()
        drawer.forward(SIZE * 2)

    drawer.right(HALF_CIRCLE/2)

    for i in range(COLUMNS - 1):
        drawer.penup()
        drawer.goto(-SIZE + ((SIZE * 2) / COLUMNS) * (i + 1), SIZE)
        drawer.pendown()
        drawer.forward(SIZE * 2)

    num = 1
    for i in range(ROWS):
        for j in range(COLUMNS):
            drawer.penup()
            drawer.goto(-SIZE + PENSIZE + j * ((SIZE * 2) / COLUMNS), SIZE - (PENSIZE * 2) - i * ((SIZE * 2) / ROWS))
            drawer.pendown()

            drawer.write(num, font=("Arial", FONT_SIZE))
            num += 1

    screen.update()


def position(num):
    """
    Takes in the square number and returns the coordinates of the center of that square
    :param num:
    :return: x, y
    """
    row = 0
    col = 0
    while num > COLUMNS:
        num -= COLUMNS
        row += 1
    col = num - 1

    x = -SIZE + (SIZE / COLUMNS) + col * ((SIZE * 2) / COLUMNS)
    y = SIZE - (SIZE / ROWS) - row * ((SIZE * 2) / ROWS)
    return x, y


def drawX(num):
    """
    Draws an X at num square
    :param num:
    """
    x, y = position(num)

    drawer.penup()
    drawer.goto(x, y)
    drawer.pendown()
    drawer.setheading(X_ANGLE)

    for i in range(2):
        drawer.forward(pos/2)
        drawer.backward(pos)
        drawer.forward(pos/2)
        drawer.left(X_ANGLE)

    screen.update()


def drawO(num):
    """
    Draws an O at num square
    :param num:
    """
    x, y = position(num)

    drawer.penup()
    drawer.goto(x, y + pos/2)
    drawer.pendown()
    drawer.setheading(0)

    for i in range(HALF_CIRCLE):
        drawer.forward((pos * math.pi) / HALF_CIRCLE)
        drawer.right(2)

    screen.update()
