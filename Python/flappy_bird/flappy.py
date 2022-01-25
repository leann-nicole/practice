import random
import time
import pygame

pygame.init()

black = (0, 0, 0)
green = (102, 176, 50)
yellow = (255, 255, 0)
red = (255, 0, 0)
black = (20, 20, 20)

win_width, win_height = 300, 400
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('FLAPPY BIRD 2P')
clock = pygame.time.Clock()

gravity = .5
birdRadius = 15
gapLength = 150
pipeWidth = 60

yellowBird = pygame.image.load(
    '/home/leann/Desktop/Python/flappy_bird/yellowbird.png')
redBird = pygame.image.load(
    '/home/leann/Desktop/Python/flappy_bird/redbird.png')
redShell = pygame.image.load(
    '/home/leann/Desktop/Python/flappy_bird/redshell.png')
skyclouds = pygame.image.load('/home/leann/Desktop/Python/flappy_bird/sky.png')
yellowBird = pygame.transform.scale(
    yellowBird, (birdRadius*2 + 15, birdRadius*2 + 5))
redBird = pygame.transform.scale(
    redBird, (birdRadius*2 + 15, birdRadius*2 + 5))
redShell = pygame.transform.scale(
    redShell, (birdRadius*2 + 15, birdRadius*2 + 5))


class Bird:
    jumpSpeed = 7

    def __init__(self, color, x=win_width//2):
        self.x = x
        self.y = win_height//2
        self.color = color
        self.direction = 1  # falling
        self.speed = 0

    def move(self, pipes):
        if self.speed <= 0:
            self.direction = 1  # start to fall and gain speed

        if self.y + 15 >= win_height and self.direction > 0:
            self.y = win_height - 15
        elif self.y - 15 <= 0 and self.direction < 0:  # when ceiling is hit, speed zeroes out
            self.y = 15
            self.speed = 0
        else:
            self.y += self.speed * self.direction
            # going up, bird loses speed. going down, bird gains speed
            self.speed += gravity * self.direction

        for pipe in pipes:
            if self.x + birdRadius >= pipe.x1 and self.x - birdRadius <= pipe.x1 + pipeWidth:
                if self.y - birdRadius <= pipe.len1 or self.y + birdRadius >= pipe.y2:
                    self.color = black

    def show(self):
        pygame.draw.circle(window, self.color, (self.x, self.y), birdRadius)
        if self.color == red:
            window.blit(redBird, (self.x - birdRadius -
                        10, self.y - birdRadius - 5))
        elif self.color == yellow:
            window.blit(yellowBird, (self.x - birdRadius -
                        10, self.y - birdRadius - 5))
        elif self.color == black:
            window.blit(redShell, (self.x - birdRadius -
                        10, self.y - birdRadius - 5))


class Pipe:
    def __init__(self, x1, len1):
        self.x1 = x1
        self.len1 = len1
        self.y2 = self.len1 + gapLength
        self.len2 = win_height - self.y2

    @staticmethod
    def showAid(x, y, width, height):
        pygame.draw.rect(window, green, pygame.Rect(  # tube
            x, y, width, height))
        pygame.draw.rect(window, black, pygame.Rect(
            x, y, width, height), 3)

    def show(self):
        Pipe.showAid(self.x1, -1, pipeWidth, self.len1)
        Pipe.showAid(self.x1, self.y2, pipeWidth, self.len2+3)
        Pipe.showAid(self.x1-5, self.y2, pipeWidth+10, 30)
        Pipe.showAid(self.x1-5, self.len1-30, pipeWidth+10, 30)


def updateWindow(bird1, bird2, pipes):
    window.blit(skyclouds, (0, 0))
    for pipe in pipes:
        pipe.show()
    bird1.show()
    bird2.show()
    pygame.display.flip()


def flappy():
    playing = True

    while playing:
        gameover = False
        bird1 = Bird(yellow,  win_width//2 - 50)
        bird2 = Bird(red)
        pipes = [Pipe(win_width, random.randrange(50, 200))]
        for x in range(4):
            pipes.append(Pipe(pipes[-1].x1 + 240, random.randrange(50, 200)))

        while not gameover:
            updateWindow(bird1, bird2, pipes)

            if bird1.color == black and bird2.color == black:
                gameover = True

            for pipe in pipes:
                if pipe.x1 + pipeWidth <= 0:
                    pipes.remove(pipe)
                    pipes.append(
                        Pipe(pipes[-1].x1 + 240, random.randrange(50, 200)))
                else:
                    pipe.x1 -= 2

            bird1.move(pipes)
            bird2.move(pipes)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameover = True
                    playing = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        bird1.direction = -1
                        bird1.speed = Bird.jumpSpeed
                    if event.key == pygame.K_w:
                        bird2.direction = -1
                        bird2.speed = Bird.jumpSpeed

            clock.tick(60)
        time.sleep(1)
    pygame.quit()


flappy()
