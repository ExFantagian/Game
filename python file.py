import pygame
import random
import sys
import os
import json

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

# Game states
TITLE, PLAYING, GAME_OVER, HIGH_SCORES = 0, 1, 2, 3
game_state = TITLE

# Game variables
clock = pygame.time.Clock()
dino_x = 50
dino_y = HEIGHT - 100
gravity = 2
dino_vel_y = 0
jump = False
duck = False
attacking = False
obstacle_x = WIDTH
obstacle_speed = 10
obstacle_flying_x = WIDTH
obstacle_flying_speed = 5
hawk_x = WIDTH
hawk_y = HEIGHT - 150
hawk_speed = 10
score = 0
spawn_hawk = False
spawn_shark = False
game_over = False
HAWK_MIN_HEIGHT = HEIGHT - 175
HAWK_MAX_HEIGHT = HEIGHT - 150
SAFE_DISTANCE = 200  # Distance to ensure hawk does not overlap ground obstacles
SCORE_FILE = "scores.json"

# Load images
StartScreen = pygame.image.load("StartScreen.png")
StartScreen = pygame.transform.scale(StartScreen, (WIDTH, HEIGHT))
dino_image = pygame.image.load("cat.png")
dino_image = pygame.transform.scale(dino_image, (50, 50))
dino_jump_image = pygame.image.load("cat_jump.png")
dino_jump_image = pygame.transform.scale(dino_jump_image, (50, 50))
dino_duck_image = pygame.image.load("cat_jump.png")
dino_duck_image = pygame.transform.scale(dino_duck_image, (50, 25))
dino_night_image = pygame.image.load("AngryCat.png")
dino_night_image = pygame.transform.scale(pygame.image.load("AngryCat.png"), (50, 50))
dino_night_jump_image = pygame.image.load("angry_jumpingcat.png")
dino_night_jump_image = pygame.transform.scale(pygame.image.load("angry_jumpingcat.png"), (50, 50))
dino_night_duck_image = pygame.image.load("angry_jumpingcat.png")
dino_night_duck_image = pygame.transform.scale(pygame.image.load("angry_jumpingcat.png"), (50, 25))
obstacle_image_dog = pygame.image.load("obstacle.png")
obstacle_image_dog = pygame.transform.scale(obstacle_image_dog, (50, 50))
obstacle_image_Waterpuddle = pygame.image.load("Waterpuddle.png")
obstacle_image_Waterpuddle = pygame.transform.scale(obstacle_image_Waterpuddle, (50, 50))
obstacle_image_shark = pygame.image.load("shark.png")
obstacle_image_shark = pygame.transform.scale(obstacle_image_shark, (50, 50))
hawk_image = pygame.image.load("hawk.png")
hawk_image = pygame.transform.scale(hawk_image, (50, 50))
game_over_image = pygame.image.load("game_over.png")
game_over_image = pygame.transform.scale(game_over_image, (WIDTH, HEIGHT))
bg_day = pygame.image.load("mariobg.png")
bg_night = pygame.image.load("nightmariobg.png")
bg_forest_day = pygame.image.load("forest.jpg")
bg_forest_night = pygame.image.load("forest.jpg")
bg_day = pygame.transform.scale(pygame.image.load("mariobg.png"), (WIDTH, HEIGHT))
bg_night = pygame.transform.scale(pygame.image.load("nightmariobg.png"), (WIDTH, HEIGHT))
bg_forest_day = pygame.transform.scale(pygame.image.load("forest.jpg"), (WIDTH, HEIGHT))
bg_forest_night = pygame.transform.scale(pygame.image.load("forest.jpg"), (WIDTH, HEIGHT))

def load_score():
    if os.path.exists(SCORE_FILE):
        try:
            with open(SCORE_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []  # Handle corrupted score file

def save_score(new_score):
    scores = load_score()
    scores.append(new_score)
    scores = sorted(scores, reverse=True)[:5]  # Keep top 5
    with open(SCORE_FILE, "w") as file:
        json.dump(scores, file)

def display_game_over_screen(score):
    screen.blit(game_over_image, (0, 0))
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    restart_text = font.render("Press R to Restart", True, BLACK)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 50))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 100))

def display_title_screen():
    screen.blit(StartScreen, (0, 0))
    font = pygame.font.Font(None, 36)
    high_score_text = font.render("Press H for High Scores", True, BLACK)
    screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT - 50))

def display_high_scores():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)
    scores = load_score()
    y_offset = 50
    for index, s in enumerate(scores):
        score_text = font.render(f"{index + 1}. {s}", True, BLACK)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, y_offset))
        y_offset += 40

    return_text = font.render("Press T to Return to Title", True, BLACK)
    screen.blit(return_text, (WIDTH // 2 - return_text.get_width() // 2, HEIGHT - 50))

# Game loop
running = True
while running:
    screen.fill(WHITE)  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        # Game state: TITLE
        if game_state == TITLE:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = PLAYING
                elif event.key == pygame.K_h:
                    game_state = HIGH_SCORES

        # Game state: PLAYING
        elif game_state == PLAYING:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_SPACE, pygame.K_UP, pygame.K_w] and not jump:
                    jump = True
                    dino_vel_y = -20
                    sound.play()
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    duck = True
                elif event.key == pygame.K_k and (150 <= score < 300 or 450 <= score < 600 or 750 <= score < 900):
                    attacking = True
                    attack_timer = 20
                    current_dino = dino_night_jump_image
                    if dino_rect.colliderect(obstacle_rect):
                        obstacle_x = WIDTH + 500
                        score += 100
                    if dino_rect.colliderect(obstacle_flying_rect):
                        obstacle_flying_x = WIDTH + 500
                        score += 100
                    if dino_rect.colliderect(hawk_rect):
                        hawk_x = WIDTH + 500
                        score += 100
                        

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    duck = False

            

        elif game_state == GAME_OVER:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game_state = TITLE
                score = 0
                dino_x, dino_y = 50, HEIGHT - 100
                dino_vel_y = 0
                jump = False
                duck = False
                game_over = False
                obstacle_x = WIDTH
                obstacle_flying_x = WIDTH
                hawk_x = WIDTH
                spawn_hawk = False
                spawn_shark = False

        elif game_state == HIGH_SCORES:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                game_state = TITLE

    # Handle game states
    if game_state == TITLE:
        display_title_screen()
    elif game_state == HIGH_SCORES:
        screen.fill(WHITE)  
        display_high_scores()  


    elif game_state == PLAYING:
        if score < 150:
            screen.blit(bg_day, (0, 0))
        elif score < 300:
            screen.blit(bg_night, (0, 0))
            # Display "Press K" prompt at night transition
            if 150 <= score <= 180:
                font = pygame.font.Font(None, 48)
                press_k_text = font.render("Press K to attack!", True, (255, 0, 0))
                screen.blit(press_k_text, (WIDTH // 2 - press_k_text.get_width() // 2, 50))
        elif score < 450:
            screen.blit(bg_forest_day, (0, 0))
        elif score < 600:
            screen.blit(bg_forest_night, (0, 0))
            # Display "Press K" again when forest turns night
            if 450 <= score <= 480:
                font = pygame.font.Font(None, 48)
                press_k_text = font.render("Press K to attack!", True, (255, 0, 0))
                screen.blit(press_k_text, (WIDTH // 2 - press_k_text.get_width() // 2, 50))
        elif score < 750:
            screen.blit(bg_forest_day, (0, 0))
        elif score < 900:
            screen.blit(bg_forest_night, (0, 0))

        # Update dino image based on score
        if 150 <= score < 300 or 450 <= score < 600 or 750 <= score < 900:  # Night conditions
            if not attacking:
                current_dino = dino_night_image
            current_jump = dino_night_jump_image
            current_duck = dino_night_duck_image
        else:
            current_dino = dino_image
            current_jump = dino_jump_image
            current_duck = dino_duck_image

        if jump:
            dino_y += dino_vel_y
            dino_vel_y += gravity
            if dino_y >= HEIGHT - 100:
                dino_y = HEIGHT - 100
                jump = False

        
        if attacking:
            attack_timer -= 1
            if attack_timer <= 0:  #reset
                attacking = False
                current_dino = dino_night_image  # Restore default image
                

        # Move ground and flying obstacles
        obstacle_x -= obstacle_speed
        if score >= 600:  # Shark spawning starts at score 600
            obstacle_flying_x -= obstacle_flying_speed
        if obstacle_x < -50:
            obstacle_x = WIDTH
        if obstacle_flying_x < -50:
            obstacle_flying_x = WIDTH

        # Hawk logic
        if spawn_hawk:
            hawk_x -= hawk_speed
            if hawk_x < -50:
                hawk_x = WIDTH
                spawn_hawk = False
        if score >= 300 and not spawn_hawk and random.choice([True, False]):
            spawn_hawk = True
            hawk_x = WIDTH
            hawk_y = random.randint(HAWK_MIN_HEIGHT, HAWK_MAX_HEIGHT)

        # Collision detection
        dino_rect = pygame.Rect(dino_x, dino_y, 50, 50 if not duck else 25)
        obstacle_rect = pygame.Rect(obstacle_x, HEIGHT - 100, 50, 50)
        obstacle_flying_rect = pygame.Rect(obstacle_flying_x, HEIGHT - 200, 50, 50)
        hawk_rect = pygame.Rect(hawk_x, hawk_y, 50, 50)

        # Debugging: Draw rectangles for visualization
        pygame.draw.rect(screen, (255, 0, 0), dino_rect, 2)  # Red for Dino
        pygame.draw.rect(screen, (0, 0, 255), obstacle_rect, 2)  # Blue for ground obstacle
        pygame.draw.rect(screen, (0, 255, 0), obstacle_flying_rect, 2)  # Green for flying obstacle
        pygame.draw.rect(screen, (255, 255, 0), hawk_rect, 2)  # Yellow for hawk

        # Collision Logic
        if not attacking and dino_rect.colliderect(obstacle_rect) or dino_rect.colliderect(obstacle_flying_rect) or dino_rect.colliderect(hawk_rect):
            save_score(score)
            game_state = GAME_OVER

        # Draw Dino and obstacles
        if jump:
            screen.blit(current_jump, (dino_x, dino_y))
        elif duck:
            screen.blit(current_duck, (dino_x, HEIGHT - 75))
        else:
            screen.blit(current_dino, (dino_x, dino_y))

        screen.blit(obstacle_image_dog, (obstacle_x, HEIGHT - 100))
        if score >= 600:  # Sharks spawn at score 600
            screen.blit(obstacle_image_shark, (obstacle_flying_x, HEIGHT - 200))
        if score >= 300 and spawn_hawk:  # Hawk spawns at score 300
            screen.blit(hawk_image, (hawk_x, hawk_y))

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        score += 1

    elif game_state == GAME_OVER:
        display_game_over_screen(score)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()


