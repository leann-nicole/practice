import time
import random
import pygame
pygame.init()

winWidth, winHeight = 403, 403
cols, rows = 10, 10
tileWidth, tileHeight = 40, 40


# colors
white = (255, 255, 255)
yellow = (248, 223, 13)
cyan = (6, 190, 171)
green = (8, 160, 4)
pink = (248, 32, 88)
bgColor = (20, 26, 27)
colors = [yellow, cyan, pink]

window = pygame.display.set_mode((winWidth, winHeight))
pygame.display.set_caption('Color Match')


class Tile:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

    def show(self):
        if (self.color):
            pygame.draw.rect(window, self.color, ((self.col *
                             tileWidth)+1, (self.row*tileHeight)+1, tileWidth, tileHeight))
            pygame.draw.rect(window, bgColor, ((self.col *
                             tileWidth)+1, (self.row*tileHeight)+1, tileWidth, tileHeight), 2)

    def disappear(self):
        self.color = 0


def genGrid():
    grid = []
    for row in range(rows):
        grid.append([])
        for column in range(cols):
            color = random.choice(colors) if row >= 5 else 0
            tile = Tile(row, column, color)
            grid[row].append(tile)
    return grid


def rippleDelete(tile, grid, found):
    r = tile.row
    c = tile.col

    sameColoredNeighbors = []
    if r > 0 and grid[r-1][c].color == tile.color and grid[r-1][c] not in found:
        sameColoredNeighbors.append(grid[r-1][c])
    if c > 0 and grid[r][c-1].color == tile.color and grid[r][c-1] not in found:
        sameColoredNeighbors.append(grid[r][c-1])
    if r < rows-1 and grid[r+1][c].color == tile.color and grid[r+1][c] not in found:
        sameColoredNeighbors.append(grid[r+1][c])
    if c < cols-1 and grid[r][c+1].color == tile.color and grid[r][c+1] not in found:
        sameColoredNeighbors.append(grid[r][c+1])

    found.extend(sameColoredNeighbors)

    for tile in sameColoredNeighbors:
        rippleDelete(tile, grid, found)

    tile.disappear()
    for tile in sameColoredNeighbors:
        tile.disappear()


def dropTiles(grid):
    for row in range(rows-1, -1, -1):  # start from second to the last row, stop at first row
        for col in range(cols):
            if grid[row][col].color:
                nRow = row+1
                while nRow <= rows-1 and not grid[nRow][col].color:
                    nRow += 1
                nRow -= 1
                if nRow != row:
                    grid[nRow][col].color = grid[row][col].color
                    grid[row][col].disappear()


def showTiles(grid):
    for row in grid:
        for tile in row:
            tile.show()


def showMovesLeft(movesLeft):
    fontstyle = pygame.font.Font('/usr/share/fonts/TTF/Roboto-Regular.ttf', 12)
    text = fontstyle.render('moves left: ' + str(movesLeft), 1, green)
    window.blit(text, (0, 0))


def addRow(grid):
    for tile in grid[0]:
        if tile.color != 0:
            return False
    for r in range(rows):
        for c in range(cols):
            if r < rows-1:
                grid[r][c].color = grid[r+1][c].color
            else:
                grid[r][c].color = random.choice(colors)
    return True


def gameOverScreen():
    fontstyle = pygame.font.Font('/usr/share/fonts/TTF/Roboto-Regular.ttf', 14)
    text = fontstyle.render('GAME OVER', 1, green)
    containerRect = text.get_rect()
    containerRect.center = (winWidth/2, winHeight/2)
    window.fill(bgColor)
    window.blit(text, containerRect)
    pygame.display.update()


def updateWindow(grid, movesLeft):
    window.fill(bgColor)
    showTiles(grid)
    showMovesLeft(movesLeft)
    pygame.display.update()


def colorMatch():
    running = True
    while running:
        gameOver = False
        grid = genGrid()
        movesLeft = 5
        while not gameOver:
            if not movesLeft:
                if not addRow(grid):  # top reached
                    gameOverScreen()
                    time.sleep(5)
                    break
                movesLeft = 5

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    gameOver = True
                    break
                elif pygame.mouse.get_pressed()[0]:
                    coordinate = pygame.mouse.get_pos()  # a tuple
                    tile = grid[coordinate[1] //
                                tileWidth][coordinate[0]//tileHeight]
                    if tile.color:
                        rippleDelete(tile, grid, [])
                        dropTiles(grid)
                        movesLeft -= 1

            updateWindow(grid, movesLeft)


colorMatch()
pygame.quit()
