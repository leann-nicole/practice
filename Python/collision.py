import pygame
import math

pygame.init()
clock = pygame.time.Clock()
blue = (0, 255, 255)
black = (0, 0, 0)
purple = (128, 0, 128)
white = (255, 255, 255)
screen = pygame.display.set_mode((400, 400))
r = 15


class Square:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = purple

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, 100, 100))

    def collide(self):
        self.color = blue

    def reset(self):
        self.color = purple


class Circle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.h = 0
        self.v = 0

    def draw(self):
        pygame.draw.circle(screen, blue, (self.x, self.y), r)

    def update(self):
        if self.x - r + self.h >= 0 and self.x + r + self.h <= 400:
            self.x += self.h
        else:
            self.h = 0
        if self.y - r + self.v >= 0 and self.y + r + self.v <= 400:
            self.y += self.v
        else:
            self.v = 0

    def horiz(self, direction):
        self.h = direction

    def vert(self, direction):
        self.v = direction

    def collisionCheck(self, square):
        testX = self.x
        testY = self.y

        if self.x < square.x:  # circle is to the left of square
            testX = square.x
        elif self.x > square.x + 100:  # circle is to the right of square
            testX = square.x + 100

        if self.y < square.y:
            testY = square.y
        elif self.y > square.y + 100:
            testY = square.y + 100

        a = self.x - testX
        b = self.y - testY

        dist = math.sqrt(a**2 + b**2)
        pygame.draw.line(screen, white, (self.x, self.y), (testX, testY))

        if dist <= r:
            square.collide()
        else:
            square.reset()


circle = Circle(200, 200)
square = Square(185, 185)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        h = 3
        v = 3
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                circle.vert(-v)
            if event.key == pygame.K_DOWN:
                circle.vert(v)
            if event.key == pygame.K_LEFT:
                circle.horiz(-h)
            if event.key == pygame.K_RIGHT:
                circle.horiz(h)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or pygame.K_DOWN:
                circle.vert(0)
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                circle.horiz(0)

    square.draw()
    circle.draw()
    circle.update()

    circle.collisionCheck(square)

    pygame.display.update()
    screen.fill(black)
    clock.tick(60)

pygame.quit()
