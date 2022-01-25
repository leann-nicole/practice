import pygame
from time import sleep

pygame.init()

FPS = 60
win_width = 800
win_height = 500
window = pygame.display.set_mode((win_width, win_height))
clock = pygame.time.Clock()

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 255, 255)
gray = (25, 25, 25)

center = (win_width//2, win_height//2)
paddleWidth, paddleHeight = 10, 100
ballRadius = 10
ballSpeedx, ballSpeedy = 5, 5
paddleSpeed = 5
xPery, yPerx = ballSpeedx/ballSpeedy, ballSpeedy/ballSpeedx  # slope
topBorder, bottomBorder = ballRadius, win_height - ballRadius
leftBorder, rightBorder = paddleWidth + \
    ballRadius, win_width - paddleWidth - ballRadius


def showScores(scores):
    typeface = pygame.font.Font('/usr/share/fonts/TTF/Roboto-Light.ttf', 14)
    player_scores = typeface.render(
        f'{str(scores[0])} {str(scores[1])}', True, white)
    container = player_scores.get_rect()
    container.center = center
    window.blit(player_scores, container)


def updateWindow(paddle1, paddle2, ball, scores):
    window.fill(black)
    paddle1.show()
    paddle2.show()
    pygame.draw.line(window, gray, (center[0], 0), (center[0], win_height))
    showScores(scores)
    ball.show()
    pygame.display.update()


class Ball:

    def __init__(self):
        self.x = center[0]
        self.y = center[1]
        self.speedx = ballSpeedx
        self.speedy = ballSpeedy
        self.directionX = 1
        self.directionY = 1

    def move(self):
        if (self.x + ballRadius + self.speedx >= 0) and (self.x - ballRadius + self.speedx <= win_width):
            self.x += self.speedx
        else:
            self.x, self.y = center
        if (self.y - ballRadius + self.speedy >= 0) and (self.y + ballRadius + self.speedy <= win_height):
            self.y += self.speedy
        else:
            self.speedy *= -1
            self.directionY *= -1

    def show(self):
        pygame.draw.circle(window, white, (self.x, self.y), ballRadius)

    def bounceOnCollision(self, paddle):
        testX, testY = self.x, self.y

        if paddle.color == blue:
            if self.x > paddle.x + paddleWidth:
                testX = paddle.x + paddleWidth
        else:
            if self.x < paddle.x:
                testX = paddle.x

        if self.y > paddle.y + paddleHeight:
            testY = paddle.y + paddleHeight
        elif self.y < paddle.y:
            testY = paddle.y

        horDist = self.x - testX
        verDist = self.y - testY

        distSqrd = (horDist**2 + verDist**2)

        if distSqrd <= ballRadius**2:
            paddleFaceCollision = False
            if paddle.color == red:
                if self.x < paddle.x and (self.y + ballRadius >= paddle.y and self.y - ballRadius <= paddle.y + paddleHeight):
                    paddleFaceCollision = True
            elif paddle.color == blue:
                if self.x > paddle.x + paddleWidth and (self.y + ballRadius >= paddle.y and self.y - ballRadius <= paddle.y + paddleHeight):
                    paddleFaceCollision = True

            if paddleFaceCollision:
                self.speedx *= -1
                self.directionX *= -1
            elif self.directionY != paddle.directionY:
                self.speedy *= -1
                self.directionY *= -1


class Paddle:
    createdPaddles = 0

    def __init__(self, isBot):
        if not Paddle.createdPaddles:
            self.x = 0
            self.directionX = 1
            self.color = blue
            Paddle.createdPaddles += 1
        else:
            self.x = win_width - paddleWidth
            self.directionX = -1
            self.color = red
        self.y = center[1] - paddleHeight//2
        self.directionY = 0
        self.speed = 0
        self.isBot = isBot
        if isBot:
            self.destination = self.y

    def getDestination(self, ball):
        ballXdir, ballYdir = ball.directionX, ball.directionY

        nx, ny = ball.x, ball.y
        pballYdir, px, py = ballYdir, nx, ny

        while nx > leftBorder and nx < rightBorder:
            pballYdir, px, py = ballYdir, nx, ny
            if ballYdir < 0:  # ball is going up
                yDist = ny - topBorder
                ny = topBorder
            else:
                yDist = bottomBorder - ny
                ny = bottomBorder
            if ballXdir < 0:  # ball is going left
                nx -= yDist*xPery
            else:
                nx += yDist*xPery
            ballYdir *= -1

        ballYdir, nx, ny = pballYdir, px, py

        if ballXdir < 0:  # ball is going left
            xDist = nx - leftBorder
        else:
            xDist = rightBorder - nx
        if ballYdir < 0:  # ball is going up
            ny -= xDist*yPerx
        else:
            ny += xDist*yPerx

        return ny 

    def chngSpeedDir(self, dirY):
        self.directionY = dirY
        self.speed = paddleSpeed*self.directionY

    def move(self, ball):
        if self.isBot:
            if self.directionX != ball.directionX:
                self.destination = self.getDestination(ball)
            else:
                self.destination = ball.y
            if self.destination < self.y + paddleHeight//2:
                self.chngSpeedDir(-1)
            elif self.destination > self.y + paddleHeight//2:
                self.chngSpeedDir(1)
            else:
                self.chngSpeedDir(0)

        if (self.y + self.speed >= 0) and (self.y + paddleHeight + self.speed <= win_height):
            self.y += self.speed
        else:
            self.chngSpeedDir(0)

    def show(self):
        pygame.draw.rect(window, self.color,
                         (self.x, self.y, paddleWidth, paddleHeight))


def pingpong():
    playing = True
    ball = Ball()
    paddle1 = Paddle(1)
    paddle2 = Paddle(0)
    scores = [0, 0]

    while playing:
        updateWindow(paddle1, paddle2, ball, scores)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    paddle2.chngSpeedDir(-1)
                if event.key == pygame.K_DOWN:
                    paddle2.chngSpeedDir(1)

            # key release
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or pygame.K_DOWN:
                    paddle2.chngSpeedDir(0)

        if ball.speedx < 0:
            ball.bounceOnCollision(paddle1)
        else:
            ball.bounceOnCollision(paddle2)

        ball.move()
        paddle1.move(ball)
        paddle2.move(ball)

        if ball.x + ballRadius + ball.speedx < 0:
            scores[1] += 1
        elif ball.x - ballRadius + ball.speedx > win_width:
            scores[0] += 1

        clock.tick(FPS)


pingpong()
pygame.quit()
