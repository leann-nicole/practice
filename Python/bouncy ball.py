import pygame

pygame.init()
clock = pygame.time.Clock()

white = (255,255,255)
black = (0,0,0)
purple = (128,0, 128)
winsize = 480
screen = pygame.display.set_mode((winsize,winsize))
pygame.display.set_caption("Bouncy Ball")
screen.fill(white)

x,y = winsize/2,winsize/2
x_move, y_move = 5,3
bounce_count = 0

def circle(x,y):
    pygame.draw.circle(screen,purple,(x,y),15)
    

def show_count(count):
    leFont = pygame.font.Font('/usr/share/fonts/TTF/Arial.TTF',25)
    text = leFont.render(count,True,black)
    text_rect = text.get_rect()
    text_rect.center = (460,20)
    screen.blit(text,text_rect)   
    
def main():
    global x,y,x_move,y_move, bounce_count
    hori, vert = 0,0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    hori = -10
                    if x_move > 0: x_move *= -1 # change direction
                if event.key == pygame.K_RIGHT:
                    hori = 10
                    if x_move < 0: x_move *= -1
                if event.key == pygame.K_UP:
                    vert = -10
                    if y_move > 0: y_move *= -1
                if event.key == pygame.K_DOWN:
                    vert = 10
                    if y_move < 0: y_move *= -1
            if event.type == pygame.KEYUP:
                hori, vert = 0,0
    
        if x + hori - 15 + x_move >= 0 and x + hori + 15 + x_move <= winsize:
            x += x_move + hori # move
        else:
            x_move *= -1 # bounce
            x_move += -1 * hori # bounce in the same rate, angle 
            hori = 0
            bounce_count += 1
        if y + vert - 15 + y_move >= 0 and y + vert + 15 + y_move <= winsize:
            y += y_move + vert 
        else:
            y_move *= -1
            y_move += -1 * vert
            vert = 0
            bounce_count += 1
        
        circle(x,y)
        show_count(str(bounce_count))
        pygame.display.update()
        screen.fill(white)
        clock.tick(50)
             
main()
pygame.quit() 
        
    