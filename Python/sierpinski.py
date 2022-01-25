import random
import pygame

pygame.init()

winWidth, winHeight = 700, 700
window = pygame.display.set_mode((winWidth, winHeight))
pygame.display.set_caption('SIERPINSKI!')
clock = pygame.time.Clock()

white = (255, 255, 255)
black = (0, 0, 0)
line_color = black


def getMid(v1, v2):
    return ((v1[0]+v2[0])/2, (v1[1]+v2[1])/2)


def sierpinski(v1, v2, v3, triNum):
    if not triNum:
        return
    pygame.draw.line(window, line_color, v1, v2)
    pygame.draw.line(window, line_color, v2, v3)
    pygame.draw.line(window, line_color, v3, v1)
    m1 = getMid(v1, v2)
    m2 = getMid(v2, v3)
    m3 = getMid(v3, v1)
    sierpinski(v1, m1, m3, triNum-1)
    sierpinski(m1, v2, m2, triNum-1)
    sierpinski(m3, m2, v3, triNum-1)


def main():
    triNum = 2
    v1 = (winWidth/2, winHeight/10)
    v2 = (winWidth/15, (winHeight/10)*9)
    v3 = ((winWidth/15)*14, (winHeight/10)*9)

    msElapsed = 0
    running = True
    while running:
        if msElapsed >= 1000:  # every 1 second
            triNum += 1
            if triNum > 10:
                triNum = 2
            msElapsed = 0

        window.fill(white)
        sierpinski(v1, v2, v3, triNum)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick()
        msElapsed += clock.get_rawtime()


main()
pygame.quit()
