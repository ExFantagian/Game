import pygame
#from pygame.locals import *
pygame.init()

# Color (in RGB)
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 128)

cat = pygame.image.load("cat.gif")
rect = cat.get_rect()

x, y = 100, 100
velocity = 12
clock = pygame.time.Clock()

width = 800
height = 500

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Cat")

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
            if event.key == pygame.K_UP:
                y -= velocity
            if pygame.key.get_pressed() == K_UP:
                y -= velocity
            

    screen.fill(background)
    pygame.draw.rect(screen, RED, rect, 1)
    screen.blit(cat, rect)
    pygame.display.flip()
    clock.tick(60)


pygame.quit()


