import pygame

pygame.init()

winWidth, winHeight = 500, 500
cols, rows = 100, 100
sqrWidth, sqrHeight = winWidth/cols, winHeight/rows

window = pygame.display.set_mode((winWidth, winHeight))
pygame.display.set_caption('Langton\'s Ant')

white = (255, 255, 255)
black = (20, 26, 27)
up, left, right, down = 1, 2, 3, 4


class Ant:
    def __init__(self):
        self.row = rows//2
        self.col = cols//2
        self.heading = up

    def moveLeft(self):
        if self.heading == up:
            self.col += -1
            self.heading = left
        elif self.heading == left:
            self.row += 1
            self.heading = down
        elif self.heading == right:
            self.row += -1
            self.heading = up
        else:
            self.col += 1
            self.heading = right

    def moveRight(self):
        if self.heading == up:
            self.col += 1
            self.heading = right
        elif self.heading == left:
            self.row += -1
            self.heading = up
        elif self.heading == right:
            self.row += 1
            self.heading = down
        else:
            self.col += -1
            self.heading = left

def getGrid():
    return [[black for col in range(cols)] for row in range(rows)]

def updateWindow(grid):
    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            pygame.draw.rect(window, col, (c*sqrWidth, r *
                             sqrHeight, sqrWidth, sqrHeight))

    pygame.display.update()


def main():
    running = True
    ant = Ant()
    grid = getGrid()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        updateWindow(grid)

        if grid[ant.row][ant.col] == black:
            grid[ant.row][ant.col] = white
            ant.moveRight()
        else:
            grid[ant.row][ant.col] = black
            ant.moveLeft()

        if ant.row == rows:
            ant.row = 0
        elif ant.row < -rows:
            ant.row = -1
        elif ant.col == cols:
            ant.col = 0
        elif ant.col < -cols:
            ant.col = -1


main()
pygame.quit()
