import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chrome Dino")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Dinosaur settings
dino_width = 40
dino_height = 60
dino_x = 50
dino_y = SCREEN_HEIGHT - dino_height - 10
dino_vel_y = 0
gravity = 1

# Obstacle settings
obstacle_width = 20
obstacle_height = 40
obstacle_x = SCREEN_WIDTH
obstacle_y = SCREEN_HEIGHT - obstacle_height - 10
obstacle_speed = 10

# Game variables
jump = False
score = 0
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not jump:
                jump = True
                dino_vel_y = -15

    # Dinosaur movement
    if jump:
        dino_y += dino_vel_y
        dino_vel_y += gravity
        if dino_y >= SCREEN_HEIGHT - dino_height - 10:
            dino_y = SCREEN_HEIGHT - dino_height - 10
            jump = False

    # Obstacle movement
    obstacle_x -= obstacle_speed
    if obstacle_x < -obstacle_width:
        obstacle_x = SCREEN_WIDTH
        score += 1

    # Collision detection
    if (dino_x + dino_width > obstacle_x and dino_x < obstacle_x + obstacle_width and
            dino_y + dino_height > obstacle_y):
        running = False

    # Draw dinosaur
    pygame.draw.rect(screen, BLACK, (dino_x, dino_y, dino_width, dino_height))

    # Draw obstacle
    pygame.draw.rect(screen, BLACK, (obstacle_x, obstacle_y, obstacle_width, obstacle_height))

    # Display score
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()


pygame.quit()


