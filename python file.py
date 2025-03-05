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
dino_vel_y = 0
jump = False
obstacle_x = WIDTH
obstacle_speed = 10
score = 0
game_over = False

# Load Dino image
dino_image = pygame.image.load("cat.png")
dino_image = pygame.transform.scale(dino_image, (50, 50))

# Load obstacle image
obstacle_image = pygame.image.load("obstacle.jpg")
obstacle_image = pygame.transform.scale(obstacle_image, (50, 50))

# Load game over image
game_over_image = pygame.image.load("game_over.png")
game_over_image = pygame.transform.scale(game_over_image, (WIDTH, HEIGHT))

def display_game_over_screen(score):
    screen.blit(game_over_image, (0, 0))  # Display the game over image
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()
    pygame.time.wait(3000)  # Wait for 3 seconds before closing the game

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and not jump and not game_over:
                jump = True
                dino_vel_y = -15

    if not game_over:
        # Dino jumping logic
        if jump:
            dino_y += dino_vel_y
            dino_vel_y += 1
            if dino_y >= HEIGHT - 100:
                dino_y = HEIGHT - 100
                jump = False

        # Move obstacle
        obstacle_x -= obstacle_speed
        if obstacle_x < -50:
            obstacle_x = WIDTH
            score += 1

        # Collision detection
        dino_rect = pygame.Rect(dino_x, dino_y, 50, 50)
        obstacle_rect = pygame.Rect(obstacle_x, HEIGHT - 100, 50, 50)
        if dino_rect.colliderect(obstacle_rect):
            game_over = True

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
    else:
        display_game_over_screen(score)
        running = False

pygame.quit()
