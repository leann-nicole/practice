import pygame
from math import sqrt
import time

pygame.init()

FPS = 60
width = 800
height = 500
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

black = (0,0,0)
white = (255,255,255)
blue = (0,255,255)
horizontalCenter = width/2
verticalCenter = height/2
rectw = 20
recth = 90

def updateScreen():
    scorer.update()
    pygame.draw.line(screen, white, (width/2,0), (width/2,height))
    pygame.display.update()
    screen.fill(black)
    clock.tick(FPS)

def make_text(score):
    fontstyle = pygame.font.Font('/usr/share/fonts/TTF/Arial.TTF',28)
    text = fontstyle.render(score, True, white)
    container = text.get_rect()
    container.center = (horizontalCenter, verticalCenter)
    return text, container

class Scoreboard:
    player1 = 0
    player2 = 0
    
    def __init__(self):
        pass
    
    def update(self):
        score1, container1 = make_text(str(Scoreboard.player1))
        score2, container2 = make_text(str(Scoreboard.player2))
        container1.center = (width/2 - 30, 30)
        container2.center = (width/2 + 30, 30)
        screen.blit(score1, container1)
        screen.blit(score2, container2)
        
    @classmethod
    def winner(cls,winner):
        
        if winner == 1:
            message, container = make_text('Player 1 scores!')
            screen.blit(message, container)
            pygame.display.update()
            time.sleep(1)

        elif winner == 2:
            message, container = make_text('Player 2 scores!')
            screen.blit(message, container)
            pygame.display.update()
            time.sleep(1)
        
    def p1Scores(self):
        Scoreboard.player1 += 1
        Scoreboard.winner(1)
        
    def p2Scores(self):
        Scoreboard.player2 += 1
        Scoreboard.winner(2)
        
scorer = Scoreboard()   
    
class Ball:
    
    def __init__(self,x,y,radius,speedx,speedy):
        
        self.x = x
        self.y = y
        self.radius = radius
        self.speedx = speedx
        self.speedy = speedy
        
    def move(self):
        
        # bounce ball if a border is hit
        if self.x + self.radius + self.speedx >= 0 and self.x - self.radius + self.speedx <= width:
            self.x += self.speedx
        else:
            if self.x + self.radius + self.speedx < 0:
                scorer.p2Scores()
            else:
                scorer.p1Scores()
            self.x, self.y = horizontalCenter, verticalCenter
            
        if self.y - self.radius + self.speedy >= 0 and self.y + self.radius + self.speedy <= height:
            self.y += self.speedy
        else: self.speedy *= -1
        
        # update ball
        pygame.draw.circle(screen,white,(self.x,self.y),self.radius)
        
    def checkCollision(self,player):

        testX, testY = self.x, self.y
        
        if self.x < player.x:
            testX = player.x
        elif self.x > player.x + rectw:
            testX = player.x + rectw
        
        if self.y < player.y:
            testY = player.y
        elif self.y > player.y + recth:
            testY = player.y + recth
        
        a = self.x - testX
        b = self.y - testY
        
        distance = sqrt(a**2 + b**2)
        
        if distance <= self.radius and self.y + 10 >= player.y and self.y + 10 <= player.y + recth:
            self.speedx *= -1
        elif distance <= self.radius:
            self.speedy *= -1

class Player:
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.speed = 0
        
    def move(self):
        if self.y + self.speed >= 0 and self.y + recth + self.speed <= height:
            self.y += self.speed
        else: self.speed = 0
        pygame.draw.rect(screen,blue,(self.x, self.y, rectw, recth))
        
    def setSpeed(self,speed):
        self.speed = speed

ball = Ball(horizontalCenter, verticalCenter, 10, 5, 5)
player1 = Player(0, verticalCenter-recth/2)
player2 = Player(width-rectw, verticalCenter-recth/2)

def game_loop():
    
    playing = True
    pSpeed = 4
    
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_w:
                    player1.setSpeed(-pSpeed)
                if event.key == pygame.K_s:
                    player1.setSpeed(pSpeed)
                if event.key == pygame.K_UP:
                    player2.setSpeed(-pSpeed)
                if event.key == pygame.K_DOWN:
                    player2.setSpeed(pSpeed)
                    
            if event.type == pygame.KEYUP:
                
                if event.key == pygame.K_w or pygame.K_s:
                    player1.setSpeed(0)
                if event.key == pygame.K_UP or pygame.K_DOWN:
                    player2.setSpeed(0)
        
        ball.checkCollision(player1)
        ball.checkCollision(player2)
        
        ball.move()
        player1.move()
        player2.move()
        
        updateScreen()
        if not playing:
            return
        
game_loop()
pygame.quit()