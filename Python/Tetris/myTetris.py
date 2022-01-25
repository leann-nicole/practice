import random
from time import sleep
from copy import deepcopy
import pygame
import numpy
pygame.init()

white = (255, 255, 255)
gray = (20, 26, 27)
black = (0, 0, 0)

cyan = (0, 255, 255)
orange = (255, 127, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
violet = (128, 0, 128)
green = (0, 255, 0)


FPS = 8
clock = pygame.time.Clock()

screen_width, screen_height = 300, 720
block_size = 30
rows, cols = 24, 10
window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('TETRIS')

grid = [[gray for x in range(cols)] for y in range(rows)]
fixed = {}
shapes = {
    'S':
        [[[0, 1, 1],
         [1, 1, 0],
         [0, 0, 0]],
         green],
    'Z':
        [[[1, 1, 0],
         [0, 1, 1],
         [0, 0, 0]],
         red],
    'I':
        [[[0, 0, 0, 0],
         [1, 1, 1, 1],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
         cyan],
    'O':
        [[[1, 1],
          [1, 1]],
         yellow],
    'J':
        [[[1, 0, 0],
         [1, 1, 1],
         [0, 0, 0]],
         blue],
    'L':
        [[[0, 0, 1],
         [1, 1, 1],
         [0, 0, 0]],
         orange],
    'T':
        [[[0, 1, 0],
         [1, 1, 1],
         [0, 0, 0]],
         violet]}


class Piece:
    def __init__(self, shape):
        self.form = deepcopy(shapes[shape][0])
        self.color = shapes[shape][1]
        if len(self.form) == 4:
            self.col = 3
        else:
            self.col = 4
        self.row = 2
        self.fallspeed = 1

    def rotate(self):
        formCopy = deepcopy(self.form)
        s = len(self.form)
        for x, r in enumerate(formCopy):
            for y, c in enumerate(r):
                row = y
                col = s - x - 1
                self.form[row][col] = formCopy[x][y]
        if not can_move(self):
            self.form = formCopy


def showGrid(p, nextp, curr_score):
    global grid
    grid = [[gray for x in range(cols)]
            for y in range(rows)]  # set all blocks to gray

    for r in range(rows):  # make fixed/captured blocks colored
        for c in range(cols):
            if (r, c) in fixed:
                grid[r][c] = fixed[(r, c)]

    # ripple down
    newGrid = []
    blank_lines = 0
    for line in grid:  # extract blank lines
        if line.count(gray) != 10:
            newGrid.append(line)
        else:
            blank_lines += 1

    for n in range(blank_lines):  # place blank lines at top
        newGrid.insert(0, [gray for x in range(cols)])

    grid = newGrid
    fixed.clear()
    for r, line in enumerate(grid):  # reposition fixed blocks
        for c, block in enumerate(line):
            if newGrid[r][c] != gray:
                fixed[(r, c)] = newGrid[r][c]

    # make blocks where next piece is located colored
    for r, line in enumerate(nextp.form):
        for c, mark in enumerate(line):
            if mark == 1:
                grid[nextp.row+r][nextp.col+c] = nextp.color

    for r, line in enumerate(p.form):  # make blocks where piece is located colored
        for c, mark in enumerate(line):
            if mark == 1:
                grid[p.row+r][p.col+c] = p.color

    for r in range(rows):  # display the grid
        for c in range(cols):
            pygame.draw.rect(window, grid[r][c],
                             ((c*block_size), (r*block_size), block_size, block_size), 0)

    for c in range(cols):  # make gridlines
        if c > 0:
            pygame.draw.line(window, gray, (c*block_size, 0),
                             (c*block_size, screen_height))
    for r in range(rows):
        if r > 0:
            if r == 4:
                pygame.draw.line(window, red, (0, r*block_size),
                                 (screen_width, r*block_size))
            else:
                pygame.draw.line(window, gray, (0, r*block_size),
                                 (screen_width, r*block_size))
    # update scores
    scoreFile = open(
        '/home/leann/Desktop/Python/Tetris/myTetris_highscore.txt', 'r+')
    high_score = scoreFile.read()
    if curr_score > int(high_score):
        scoreFile.seek(0)
        scoreFile.write(str(curr_score))
    scoreFile.close()
    fontstyle = pygame.font.Font('/usr/share/fonts/TTF/Roboto-Regular.ttf', 12)
    score1 = fontstyle.render('Score: ' + str(curr_score), 1, white)
    score2 = fontstyle.render('Best: ' + high_score, 1, white)
    window.blit(score1, (0, 0))
    window.blit(score2, (0, 15))

    pygame.display.update()


def can_move(p):
    colored = []
    for row, line in enumerate(p.form):
        for col, block in enumerate(line):
            if p.form[row][col]:
                colored.append((row+p.row, col+p.col))

    for block in colored:
        if block[0] > 23 or block[1] > 9 or block[1] < 0 or block in fixed:
            return False

    return True


def capturePiece(p):
    for r, line in enumerate(p.form):  # set the location of the piece
        for c, mark in enumerate(line):
            if mark == 1:
                fixed[(p.row+r, p.col+c)] = p.color


def clearStreak():
    rows_cleared = 0
    for row, line in enumerate(grid):
        if gray not in line:
            for col, block in enumerate(line):
                fixed.pop((row, col))
            rows_cleared += 1

    return rows_cleared


def limitReached():
    fixed_locations = list(fixed.keys())
    for (row, col) in fixed_locations:
        if row <= 4:
            return True
    return False


def gameover():
    fixed.clear()
    fontstyle = pygame.font.Font('/usr/share/fonts/TTF/Roboto-Regular.ttf', 12)
    status = fontstyle.render('GAME OVER', 1, white)
    window.blit(status, (120, 30))
    pygame.display.update()


def tetris():
    playing = True
    while playing:
        msElapsed = 0
        belowLimit = True
        current_score = 0
        next = Piece(random.choice(list(shapes.keys())))
        piece = Piece(random.choice(list(shapes.keys())))

        while belowLimit:
            showGrid(piece, next, current_score)
            if limitReached():
                gameover()
                break

            msElapsed += clock.get_rawtime()
            clock.tick()

            if msElapsed >= 1000/piece.fallspeed:
                msElapsed = 0
                piece.row += 1

            if not can_move(piece):
                piece.row -= 1
                capturePiece(piece)
                current_score += clearStreak()*10
                piece = next
                next = Piece(random.choice(list(shapes.keys())))
                next.fallspeed = piece.fallspeed

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    belowLimit = False
                    playing = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        piece.rotate()
                    if event.key == pygame.K_LEFT:
                        piece.col -= 1
                        if not can_move(piece):
                            piece.col += 1
                    if event.key == pygame.K_RIGHT:
                        piece.col += 1
                        if not can_move(piece):
                            piece.col -= 1
                    if event.key == pygame.K_DOWN:
                        piece.fallspeed, next.fallspeed = 40, 40
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        piece.fallspeed, next.fallspeed = 1, 1


tetris()
pygame.quit()
