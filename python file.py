import pygame
#from pygame.locals import *
pygame.init()

# Color (in RGB)
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 128)

ball = pygame.image.load("ball.gif")
rect = ball.get_rect()

speed = [1, 1]
clock = pygame.time.Clock()

width = 800
height = 500

screen = pygame.display.set_mode((width, height)) 

running = True
background = GRAY

while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                background = RED
            elif event.key == pygame.K_g:
                background = GREEN

    rect = rect.move(speed)
    if rect.left < 0 or rect.right > width:
        speed[0] = -speed[0]
    if rect.top < 0 or rect.bottom > height:
        speed[1] = -speed[1]
            

    screen.fill(background)
    pygame.draw.rect(screen, RED, rect, 1)
    screen.blit(ball, rect)
    pygame.display.flip()
    clock.tick(60)


pygame.quit()


