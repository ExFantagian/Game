import pygame
import random
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.quit()
pygame.mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Feline Jumper")
sound = pygame.mixer.Sound("meow.wav")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Game states
TITLE, PLAYING, GAME_OVER = 0, 1, 2
game_state = TITLE

# Game variables
clock = pygame.time.Clock()
dino_x = 50
dino_y = HEIGHT - 100
gravity = 2
dino_vel_y = 0
jump = False
duck = False
obstacle_x = WIDTH
obstacle_speed = 10
obstacle_flying_x = WIDTH
obstacle_flying_speed = 5
hawk_x = WIDTH
hawk_y = HEIGHT - 150
hawk_speed = 10
score = 0
spawn_hawk = False
game_over = False
HAWK_MIN_HEIGHT = HEIGHT - (175 + min(score, 100))  # Gradually raises the spawn floor
HAWK_MAX_HEIGHT = HEIGHT - (150 + min(score, 100))
SAFE_DISTANCE = 200  # Distance to ensure hawk does not overlap ground obstacles



# Load Dino images
dino_image = pygame.image.load("cat.png")
dino_image = pygame.transform.scale(dino_image, (50, 50))
dino_jump_image = pygame.image.load("cat_jump.png")  # Image for dino when it jumps
dino_jump_image = pygame.transform.scale(dino_jump_image, (50, 50))
dino_duck_image = pygame.image.load("cat_jump.png")  # Image for dino when it ducks
dino_duck_image = pygame.transform.scale(dino_duck_image, (50, 25))

# Load obstacle images
obstacle_image_dog = pygame.image.load("obstacle.png")
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

# Load bg image
bg_image = pygame.image.load("mariobg.png")
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

def display_game_over_screen(score):
    screen.blit(game_over_image, (0, 0))  # Display the game over image
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 50))
    restart_text = font.render("Press R to Restart", True, BLACK)
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 100))
    pygame.display.flip()

def display_title_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 72)
    title_text = font.render("Feline Jumper", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 50))
    instruction_text = font.render("Press S to Start", True, BLACK)
    screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()

# Game loop
running = True
while running:
    for event in pygame.event.get():  # Single event loop
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        # TITLE state events
        if game_state == TITLE:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                game_state = PLAYING

        # PLAYING state events
        elif game_state == PLAYING:
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_j) and not jump:
                    jump = True
                    dino_vel_y = -12
                    sound.play()
                if (event.key == pygame.K_DOWN or event.key == pygame.K_d or event.key == pygame.K_s) and not jump:
                    duck = True
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_DOWN, pygame.K_d, pygame.K_s]:
                    duck = False

        # GAME_OVER state events
        elif game_state == GAME_OVER:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game_state = TITLE
                game_over = False
                score = 0
                obstacle_x = WIDTH
                hawk_x = WIDTH
                dino_y = HEIGHT - 100

    # TITLE state logic
    if game_state == TITLE:
        screen.fill(WHITE)  # Clear the screen
        display_title_screen()  # Draw title screen content

    # PLAYING state logic
    elif game_state == PLAYING:
        screen.blit(bg_image, (0, 0))  # Clear the screen

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

        # Randomly decide whether to spawn the hawk
        if abs(hawk_x - obstacle_x) < SAFE_DISTANCE:
                hawk_x += SAFE_DISTANCE  # Adjust the hawk's position
        if score >= 5 and not spawn_hawk and random.choice([True, False]):
            spawn_hawk = True
            hawk_x = WIDTH
            if random.choice([True, False]): 
                hawk_y = random.randint(HEIGHT - 360, HEIGHT - 180)
            else:
                hawk_y = random.randint(HEIGHT - 130, HEIGHT - 50)
        
        if spawn_hawk:
            hawk_x -= hawk_speed
            if hawk_x < -50:
                spawn_hawk = False

        # Collision detection
        dino_rect = pygame.Rect(dino_x, dino_y, 50, 50 if not duck else 25)
        obstacle_rect = pygame.Rect(obstacle_x, HEIGHT - 100, 50, 50)
        obstacle_rect_flying = pygame.Rect(obstacle_flying_x, HEIGHT - 200, 100, 50)
        hawk_rect = pygame.Rect(hawk_x, hawk_y, 50, 50)

        pygame.draw.rect(screen, (255, 0, 0), dino_rect, 2)  # Red for Dino
        pygame.draw.rect(screen, (0, 0, 255), obstacle_rect, 2)  # Blue for ground obstacle
        pygame.draw.rect(screen, (255, 255, 0), hawk_rect, 2)  # Yellow for hawk

        if dino_rect.colliderect(obstacle_rect) or dino_rect.colliderect(obstacle_rect_flying) or dino_rect.colliderect(hawk_rect):
            game_over = True
            game_state = GAME_OVER


        # Draw Dino and obstacles
        if jump:
            screen.blit(dino_jump_image, (dino_x, dino_y))
        elif duck:
            screen.blit(dino_duck_image, (dino_x, HEIGHT - 75))
        else:
            screen.blit(dino_image, (dino_x, dino_y))

        if score < 5:
            screen.blit(obstacle_image_dog, (obstacle_x, HEIGHT - 100))
        else:
            screen.blit(obstacle_image_Waterpuddle, (obstacle_x, HEIGHT - 100))
            screen.blit(obstacle_image_shark, (obstacle_flying_x, HEIGHT - 200))

        if spawn_hawk:
            screen.blit(hawk_image, (hawk_x, hawk_y))

        # Display the score
        font = pygame.font.Font(None, 36)
        score_text = font.render("Score: " + str(score), True, BLACK)
        screen.blit(score_text, (10, 10))

    # GAME_OVER state logic
    elif game_state == GAME_OVER:
        screen.fill(WHITE)  # Clear the screen
        display_game_over_screen(score)  # Draw the game over screen

    # Flip display
    pygame.display.flip()
    clock.tick(30)
pygame.quit()
