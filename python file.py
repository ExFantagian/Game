import pygame
import random
import sys

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
duck = False
obstacle_x = WIDTH
obstacle_flying_x = WIDTH
obstacle_flying_speed = 5
obstacle_speed = 10
hawk_x = WIDTH
hawk_y = HEIGHT - 150
hawk_speed = 10
score = 0
game_over = False

# Load Dino images
dino_image = pygame.image.load("cat.png")
dino_image = pygame.transform.scale(dino_image, (50, 50))
dino_jump_image = pygame.image.load("cat_jump.png")
dino_jump_image = pygame.transform.scale(dino_jump_image, (50, 50))
dino_duck_image = pygame.image.load("cat_jump.png")
dino_duck_image = pygame.transform.scale(dino_duck_image, (50, 25))

# Load obstacle images
obstacle_image_dog = pygame.image.load("obstacle.jpg")
obstacle_image_dog = pygame.transform.scale(obstacle_image_dog, (50, 50))
obstacle_image_Waterpuddle = pygame.image.load("Waterpuddle.png")
obstacle_image_Waterpuddle = pygame.transform.scale(obstacle_image_Waterpuddle, (50, 50))
obstacle_image_shark = pygame.image.load("shark.png")
obstacle_image_shark = pygame.transform.scale(obstacle_image_shark, (50, 50))
hawk_image = pygame.image.load("hawk.png")
hawk_image = pygame.transform.scale(hawk_image, (50, 50))

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
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_j) and not jump and not game_over:
                jump = True
                dino_vel_y = -15
            if (event.key == pygame.K_DOWN or event.key == pygame.K_d or event.key == pygame.K_s) and not jump and not game_over:
                duck = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN or event.key == pygame.K_d or event.key == pygame.K_s:
                duck = False

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

        # Move flying obstacles
        if score >= 5:
            obstacle_flying_x -= obstacle_flying_speed
            if obstacle_flying_x < -50:
                obstacle_flying_x = WIDTH
                score += 1

        # Move hawk
        hawk_x -= hawk_speed
        if hawk_x < -50:
            hawk_x = WIDTH
            hawk_y = random.randint(HEIGHT - 200, HEIGHT - 100)
            score += 1

        # Collision detection
        dino_rect = pygame.Rect(dino_x, dino_y, 50, 50 if not duck else 25)
        obstacle_rect = pygame.Rect(obstacle_x, HEIGHT - 100, 50, 50)
        obstacle_rect_flying = pygame.Rect(obstacle_flying_x, HEIGHT - 200, 100, 50)
        hawk_rect = pygame.Rect(hawk_x, hawk_y, 50, 50)
        if dino_rect.colliderect(obstacle_rect) or dino_rect.colliderect(obstacle_rect_flying) or dino_rect.colliderect(hawk_rect):
            game_over = True

        # Draw Dino
        screen.fill(WHITE)
        if jump:
            screen.blit(dino_jump_image, (dino_x, dino_y))
        elif duck:
            screen.blit(dino_duck_image, (dino_x, HEIGHT - 75))
        else:
            screen.blit(dino_image, (dino_x, dino_y))

        # Draw obstacles
        if score < 5:
            screen.blit(obstacle_image_dog, (obstacle_x, HEIGHT - 100))
        else:
            screen.blit(obstacle_image_Waterpuddle, (obstacle_x, HEIGHT - 100))
            screen.blit(obstacle_image_shark, (obstacle_flying_x, HEIGHT - 200))
        screen.blit(hawk_image, (hawk_x, hawk_y))

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
