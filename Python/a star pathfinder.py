import pygame
from math import sqrt
from queue import PriorityQueue


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

pygame.init()
width = 500
units = 50
unit_size = width / units
window = pygame.display.set_mode((width, width))
pygame.display.set_caption("A* Pathfinding Algorithm")
window.fill(WHITE)

class Point:
    def __init__(self, row, col):
        self.x = row * unit_size
        self.y = col * unit_size
        self.row = row
        self.col = col
        self.neighbors = []
        self.color = WHITE
        
    def appear(self):
        pygame.draw.rect(window, self.color, (self.x, self.y, unit_size, unit_size))
    
    def make_start(self):
        self.color = GREEN
    def make_end(self):
        self.color = RED
    def make_barrier(self):
        self.color = BLACK
    def make_seen(self):
        self.color = PURPLE
    def make_explored(self):
        self.color = GREY
    def make_path(self):
        self.color = ORANGE
    def reset(self):
        self.color = WHITE
    def is_barrier(self):
        return self.color == BLACK
    
    def look_around(self, grid):
        self.neighbors = []
        
        if self.row < units - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < units - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])
            
        if self.row < units - 1 and self.col > 0 and not grid[self.row + 1][self.col - 1].is_barrier(): # DOWN LEFT
            self.neighbors.append(grid[self.row + 1][self.col - 1])

        if self.row > 0 and self.col > 0 and not grid[self.row - 1][self.col - 1].is_barrier(): # UP LEFT
            self.neighbors.append(grid[self.row - 1][self.col - 1])

        if self.col < units - 1 and self.row > 0 and not grid[self.row - 1][self.col + 1].is_barrier(): # UP RIGHT 
            self.neighbors.append(grid[self.row - 1][self.col + 1])

        if self.col < units - 1 and self.row < units - 1 and not grid[self.row + 1][self.col + 1].is_barrier(): # DOWN RIGHT
            self.neighbors.append(grid[self.row + 1][self.col + 1])
            

def heuristic(point1, point2):
    x1, y1 = point1.x, point1.y
    x2, y2 = point2.x, point2.y
    rise = abs(y1 - y2)
    run = abs(x1 - x2)
    side = min(rise, run)
    return abs(rise - run) + int(sqrt(side**2 * 2))

def find_path(start, end, grid):
    g_score = {point: float("inf") for row in grid for point in row}
    g_score[start] = 0
    f_score = {point: float("inf") for row in grid for point in row}
    f_score[start] = heuristic(start, end)
    
    parent = {}
    parent[start] = None
    
    count = 0
    to_explore = PriorityQueue()
    to_explore.put((0, count, start))
    
    seen = {start}
    
    while not to_explore.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        visualize(grid)
        current = to_explore.get()[2]
        
        if current == end:
            show_path(current, parent)
            current.make_end()
            return True
        
        for neighbor in current.neighbors:
            if neighbor.x == current.x or neighbor.y == current.y:
                temp_g = g_score[current] + 10
            else: temp_g = g_score[current] + 14
            
            if temp_g < g_score[neighbor]:
                g_score[neighbor] = temp_g
                parent[neighbor] = current
                f_score[neighbor] = temp_g + heuristic(neighbor, end)
            
                if neighbor not in seen:
                    count += 1
                    to_explore.put((f_score[neighbor], count, neighbor))
                    seen.add(neighbor)
                    neighbor.make_seen()
        
        if current != start:
            current.make_explored()
    
    return False    

def know_neighbors(grid):
    for row in grid:
        for point in row:
            point.look_around(grid)
            
def show_path(point, parent):
    while True:
        point.make_path()
        if not parent[point]: break
        point = parent[point]
    point.make_start()

def get_xy(coordinate):
    return int(coordinate[0]/unit_size), int(coordinate[1]/unit_size)

def reset_all(grid):
    for row in grid:
        for point in row:
            point.reset()

def create_pointgrid():
    pointgrid = []
    for row in range(units):
        pointgrid.append([])
        for col in range(units):
            point = Point(row,col)
            pointgrid[row].append(point)
    return pointgrid

def show_gridlines():
    for r in range(units):
        pygame.draw.line(window, BLACK, (0, r * unit_size),(width, r * unit_size))
        for c in range(units):
            pygame.draw.line(window, BLACK, (c * unit_size, 0),(c * unit_size, width))
            
def visualize(grid):
    for row in grid:
        for point in row:
            point.appear()
    show_gridlines()
    pygame.display.update()
    
def main():
    grid = create_pointgrid()
    
    start = None
    end = None

    while True:
        visualize(grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            elif pygame.mouse.get_pressed()[0]:
                coordinate = pygame.mouse.get_pos()
                x, y = get_xy(coordinate)
                clicked_point = grid[x][y]
                
                if not start and clicked_point != end:
                    start = clicked_point
                    clicked_point.make_start()
                    
                elif not end and clicked_point != start:
                    end = clicked_point
                    clicked_point.make_end()
                    
                elif clicked_point != start and clicked_point != end:
                    clicked_point.make_barrier()
                    
            elif pygame.mouse.get_pressed()[2]:
                coordinate = pygame.mouse.get_pos()
                x, y = get_xy(coordinate)
                clicked_point = grid[x][y]
                
                clicked_point.reset()
                if clicked_point == start:
                    start = None
                elif clicked_point == end:
                    end = None
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    know_neighbors(grid)
                    
                    find_path(start, end, grid)
                    
                if event.key == pygame.K_c:
                    reset_all(grid)
                    start = None
                    end = None

main()