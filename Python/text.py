import pygame

pygame.init()
black = (0,0,0)

screen = pygame.display.set_mode((200,200))
pygame.display.set_caption("READ ME")
screen.fill((255,255,255))
clock = pygame.time.Clock()
clock.tick(60)

def print_text(message):
    leFont = pygame.font.Font('/usr/share/fonts/TTF/Times.TTF',34)
    text_surface = leFont.render(message,True,black)
    text_rect = text_surface.get_rect()
    text_rect.center = (100,100)
    screen.blit(text_surface,text_rect)
    
print_text("Aloha")
pygame.display.update()