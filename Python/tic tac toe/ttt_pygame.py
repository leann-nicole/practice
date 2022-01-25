from random import randint
from math import inf
from time import sleep
import pygame
pygame.init()

winWidth, winHeight = 210, 210
markWidth, markHeight = 50, 50
offset = 10
window = pygame.display.set_mode([winWidth, winHeight])
pygame.display.set_caption('TIC TAC TOE')
grid = pygame.image.load('/home/leann/Desktop/ttt/resources/grid.jpg')
cross = pygame.image.load('/home/leann/Desktop/ttt/resources/cross.jpg')
circle = pygame.image.load('/home/leann/Desktop/ttt/resources/circle.jpg')
botwins = pygame.image.load('/home/leann/Desktop/ttt/resources/botwins.jpg')
youwin = pygame.image.load('/home/leann/Desktop/ttt/resources/youwin.jpg')
draw = pygame.image.load('/home/leann/Desktop/ttt/resources/draw.jpg')
grid = pygame.transform.scale(grid, (winWidth, winHeight))
cross = pygame.transform.scale(cross, (markWidth, markHeight))
circle = pygame.transform.scale(circle, (markWidth, markHeight))
botwins = pygame.transform.scale(botwins, (winWidth, winHeight))
youwin = pygame.transform.scale(youwin, (winWidth, winHeight))
draw = pygame.transform.scale(draw, (winWidth, winHeight))
white = (255, 255, 255)

Board = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
]

origboard = [0, 1, 2, 3, 4, 5, 6, 7, 8]

pair = {
    0: (0, 0),
    1: (0, 1),
    2: (0, 2),
    3: (1, 0),
    4: (1, 1),
    5: (1, 2),
    6: (2, 0),
    7: (2, 1),
    8: (2, 2)
}

rows = [[0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]]

cols = [[0, 3, 6],
        [1, 4, 7],
        [2, 5, 8]]

diag = [[0, 4, 8],
        [2, 4, 6]]

human = '@'
bot = '#'


def displayResult(result):
    window.fill(white)
    if result == 1:
        window.blit(youwin, (0, 0))
    elif result == 2:
        window.blit(botwins, (0, 0))
    else:
        window.blit(draw, (0, 0))
    pygame.display.update()
    sleep(1)


def gameOver():
    lines = [rows, cols, diag]
    for set in lines:
        for item in set:
            vals = list(map(lambda x: origboard[x], item))
            if vals.count(human) == 3:
                displayResult(1)
                return 1
            if vals.count(bot) == 3:
                displayResult(2)
                return 2
    free = 0
    for n in range(9):
        free += origboard.count(n)
    if not free:
        displayResult(3)
        return 3  # DRAW

    return 0


def emptySpots(board):
    return list(filter(lambda x: x != '#' and x != '@', board))


def won(board, player):
    lines = [rows, cols, diag]
    for set in lines:
        for item in set:
            vals = list(map(lambda x: board[x], item))
            if vals.count(player) == 3:
                return True
    return False


def minimax(newBoard, maximizing):
    freeSpots = emptySpots(newBoard)

    if won(newBoard, human):
        return -10
    elif won(newBoard, bot):
        return 10
    elif len(freeSpots) == 0:
        return 0

    scores = []

    for spot in freeSpots:
        if maximizing:
            newBoard[spot] = bot
            score = minimax(newBoard, False)
        else:
            newBoard[spot] = human
            score = minimax(newBoard, True)

        newBoard[spot] = spot  # reset spot after testing

        scores.append(score)

    return max(scores) if maximizing else min(scores)


def findBestMove(board):
    bestScore = -inf
    bestMove = None

    freeSpots = emptySpots(board)

    for spot in freeSpots:
        origboard[spot] = bot
        score = minimax(board, False)
        origboard[spot] = spot

        if score > bestScore:
            bestScore = score
            bestMove = spot

    return bestMove


def botMove():
    bestSpot = findBestMove(origboard)
    x, y = pair[bestSpot]
    Board[x][y] = bot
    origboard[bestSpot] = bot


def validate(x, y):
    row = x//(winWidth//3)
    col = y//(winHeight//3)
    humanMove = None
    for i in range(9):
        if pair[i] == (row, col):
            humanMove = i
    if origboard[humanMove] == human or origboard[humanMove] == bot:
        return False
    origboard[humanMove] = human
    Board[row][col] = human
    return True


def displayBoard():
    window.fill(white)
    window.blit(grid, (0, 0))
    for row in range(3):
        for cell in range(3):
            if Board[row][cell] == '@':
                window.blit(circle, (cell*markWidth+(cell*2+1) *
                            offset, row*markHeight+(row*2+1)*offset))
            elif Board[row][cell] == '#':
                window.blit(cross, (cell*markWidth+(cell*2+1) *
                            offset, row*markHeight+(row*2+1)*offset))
    pygame.display.update()


def resetBoard():
    for i in range(9):
        origboard[i] = i
    for row in range(3):
        for col in range(3):
            Board[row][col] = 0


def tictactoe():
    quit = False
    while not quit:
        resetBoard()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit = True
                    break
                if event.type == pygame.MOUSEBUTTONUP:
                    y, x = pygame.mouse.get_pos()
                    if validate(x, y):
                        if gameOver():
                            break
                        displayBoard()
                        sleep(0.5)
                        botMove()
                        if gameOver():
                            break
            else:
                displayBoard()
                continue
            break
    pygame.quit()


tictactoe()
