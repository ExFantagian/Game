import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Feline Jumper")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Game variables
clock = pygame.time.Clock()
dino_x = 50
dino_y = HEIGHT - 100
jump = False
jump_height = 15
obstacle_x = WIDTH
obstacle_speed = 10
score = 0

# Load Dino image
dino_image = pygame.image.load("cat.png")
dino_image = pygame.transform.scale(dino_image, (50, 50))

# Load obstacle image
obstacle_image = pygame.image.load("obstacle.jpg")
obstacle_image = pygame.transform.scale(obstacle_image, (50, 50))

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not jump:
                jump = True

    # Dino jumping logic
    if jump:
        dino_y -= jump_height
        jump_height -= 1
        if jump_height < -10:
            jump = False
            jump_height = 10
    else:
        dino_y = HEIGHT - 100

    # Move obstacle
    obstacle_x -= obstacle_speed
    if obstacle_x < -50:
        obstacle_x = WIDTH
        score += 1

    # Collision detection
    if dino_y < HEIGHT - 150 and dino_x < obstacle_x < dino_x + 50:
        running = False

    # Draw Dino
    screen.fill(WHITE)
    screen.blit(dino_image, (dino_x, dino_y))

    # Draw obstacle
    screen.blit(obstacle_image, (obstacle_x, HEIGHT - 100))

    # Display score
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
