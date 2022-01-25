import pygame
import math

pygame.init()

# constants
FPS = 60

black = (0,0,0)
white = (255,255,255)
blue = (0,255,255)
red = (255,0,0)

width = 800
height = 500

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

rectw = 20
recth = 80

startpos = (height/2 - rectw/2)


p1x, p1y = 50, startpos
p2x, p2y = width-50-rectw, startpos

ballHorizontalSpeed = 4
ballVerticalSpeed = 4 
ballRadius = 10

class Rectangle:
    
    def __init__(self, x,y ):
        self.x = x
        self.y = y
        
        self.speed = 0  
        
    def draw(self):
        pygame.draw.rect(screen,blue,(self.x, self.y, rectw, recth))
        
      
    def update(self):
        
        #if adding speed would make us out of bounds, set position to adjacent.
        #else: add speed normally
        if self.y + self.speed <= 0:
            self.y = 0
        elif self.y + recth + self.speed >= height:
            self.y = height - recth
        else:
            self.y += self.speed
            
         
    def setSpeed(self, newSpeed):
        self.speed = newSpeed
        
      

class Ball:
    
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r #radius
           

    def draw(self):
        pygame.draw.circle(screen, white, (self.x, self.y), self.r)
        
    def update(self):
        
        global ballHorizontalSpeed, ballVerticalSpeed
        
        #if adding speed would make us out of bounds, set position to adjacent and *=-1 for a bounce
        #else: add speed normally
        
        if self.x - self.r + ballHorizontalSpeed <= 0:
            self.x = self.r # 0+radius
            ballHorizontalSpeed *= -1
        elif self.x + self.r + ballHorizontalSpeed >= width:
            self.x = width - self.r # width-radius
            ballHorizontalSpeed *= -1
        else:
            self.x += ballHorizontalSpeed
            
        if self.y - self.r + ballVerticalSpeed <= 0:
            self.y = self.r # 0+radius
            ballVerticalSpeed *= -1    
        elif self.y + self.r + ballVerticalSpeed >= height:
            self.y = height - self.r # height-radius
            ballVerticalSpeed *= -1      
        else:
            self.y += ballVerticalSpeed
        
    def checkForCollisionWithPlayer(self, player):
        
        global ballHorizontalSpeed, ballVerticalSpeed
        
        #temporary variables to set edges for testing
        testX = self.x
        testY = self.y
      
        #which edge is closest?
        if self.x < player.x: #test left edge
            testX = player.x
            
        elif self.x > player.x + rectw : #test right edge
            testX = player.x + rectw
            
        if self.y < player.y: #test top edge      
            testY = player.y
            
        elif self.y > player.y + recth : #test bottom edge
            testY = player.y + recth;   
        
        
        
        #get distance from closest edges
        distX = self.x - testX
        distY = self.y - testY
        distance = math.sqrt( (distX*distX) + (distY*distY) )
        
        if distance <= self.r and self.y + 15 >= player.y and self.y + 15 <= player.y + recth:
            ballHorizontalSpeed *= -1
        elif distance <= self.r:
            ballVerticalSpeed *= -1
        
              
            
  

               
ball = Ball(width/2, height/2, ballRadius)
player1 = Rectangle(p1x, p1y)
player2 = Rectangle(p2x, p2y)
  
# main function
def game_loop():
    
    playing = True
    
    while playing:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                
            #key pressed
            pSpeed = 4
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player2.setSpeed(-pSpeed) 
                if event.key == pygame.K_DOWN:
                    player2.setSpeed(pSpeed) 
                if event.key == pygame.K_w:
                    player1.setSpeed(-pSpeed) 
                if event.key == pygame.K_s:
                    player1.setSpeed(pSpeed)
                    
            #key release
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or pygame.K_DOWN:
                    player2.setSpeed(0) 
                if event.key == pygame.K_w or pygame.K_s:
                    player1.setSpeed(0)     
           
        #draw
        pygame.draw.line(screen,white,(width/2,0),(width/2,height))
        ball.draw()
        player1.draw()
        player2.draw()
        
        #update
        ball.update()
        player1.update()
        player2.update()
        
        #etc
        ball.checkForCollisionWithPlayer(player1)
        ball.checkForCollisionWithPlayer(player2)
        
        #lib methods
        pygame.display.update()
        screen.fill(black)
        clock.tick(FPS)
        if not playing:
            return 
        
game_loop()
pygame.quit()
