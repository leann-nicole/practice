import pygame
from time import sleep
from random import randint

#setup
pygame.init()
width, height = 500, 500
screen = pygame.display.set_mode((width, height))
FPS = 60
clock = pygame.time.Clock()

#colors
black = (0,0,0)
white = (255,255,255)
green = (0,255,128)
red = (255,0,0)
purple = (128,0,128)

#constants
blockSize = 20
cols, rows = width//blockSize, height//blockSize

class Block:
    def __init__(self, row, col):
        self.x = row*blockSize
        self.y = col*blockSize
        self.row = row
        self.col = col
        self.color = black
        
    def make_food(self):
        self.color = red
    def make_head(self):
        self.color = purple
    def make_segment(self):
        self.color = green
    def is_segment(self):
        return self.color == green or self.color == purple
    def is_food(self):
        return self.color == red
    def reset(self):
        self.color = black
    def show(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, blockSize, blockSize))
        
def createGrid():
    grid = []
    for row in range(rows):
        grid.append([])
        for col in range(cols):
            block = Block(row,col)
            grid[row].append(block)
            
    return grid

class Snake:
    def __init__(self, row, col, grid):
        self.body = [grid[col][row], grid[col-1][row], grid[col-2][row]]
        self.body[0].make_head()
        self.direction = (1,0)
        
    def move(self,grid):
        last = len(self.body) - 1
                
        #reset tail color     
        self.body[last].reset()
            
        #change head direction
        r = self.body[0].row + self.direction[0]
        c = self.body[0].col + self.direction[1]

        if r < rows and r >= 0 and c < cols and c >= 0 and not grid[r][c].is_segment():
            
            #change body direction
            if last:
                for i in range(last, 0, -1):
                    self.body[i] = self.body[i-1]
            
            self.body[0] = grid[r][c]
            if grid[r][c].is_food():
                newFood(grid)
                Snake.grow(self, grid)
                
        else: return False

        #make blocks part of the body green!
        for block in self.body:
            block.make_segment()
            
        self.body[0].make_head()
           
        #show changes
        for row in grid:
            for block in row:
                block.show()
                
        return True
                
    @classmethod
    def grow(cls, snake, grid):
        last = len(snake.body)-1
        tail1 = snake.body[last]
        tail2 = snake.body[last-1]
        
        if tail1.row == tail2.row: 
            snake.body.append(grid[tail1.row][tail1.col+1])     
        else:
            snake.body.append(grid[tail1.row+1][tail1.col])
            
def newFood(grid):
    while True:
        r = randint(0,rows-1)
        c = randint(0,cols-1)
        if not grid[r][c].is_segment() and not grid[r][c].is_food():
            grid[r][c].make_food()
            break

def newSnake(grid):
    return Snake(9,5,grid)

def clearBoard(grid):
    for row in grid:
        for block in row:
            if not block.is_food():
                block.reset()

def updateScreen():
    sleep(.1)
    pygame.display.update()
    clock.tick(FPS)

def game_loop():
    
    grid = createGrid()
    newFood(grid)
    snake = newSnake(grid)
    movement = (1,0)
    
    playing = True
    while playing:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if snake.direction != (0,1):
                        snake.direction = (0,-1)
                        
                if event.key == pygame.K_DOWN:
                    if snake.direction != (0,-1):
                        snake.direction = (0,1)
                        
                if event.key == pygame.K_LEFT:
                    if snake.direction != (1,0):
                        snake.direction = (-1,0)
                        
                if event.key == pygame.K_RIGHT:
                    if snake.direction != (-1,0):
                        snake.direction = (1,0)
        
        if not snake.move(grid):
            clearBoard(grid)
            snake = newSnake(grid)
            
        updateScreen()
        if not playing:
            return 
                                        
game_loop()
pygame.quit()