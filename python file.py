import pygame
import random
import sys
import os
import json
import threading

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Feline Jumper")

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
obstacle_flying_y = HEIGHT - 100
obstacle_flying_speed = 10
hawk_x = WIDTH
hawk_y = HEIGHT - 125
hawk_speed = 10
score = 0
spawn_hawk = False
spawn_shark = False
HAWK_MIN_HEIGHT = HEIGHT - 125
HAWK_MAX_HEIGHT = HEIGHT - 100
shark_direction = 1  #1 up, -1 down
SHARK_MIN_HEIGHT = HEIGHT - 200  
SHARK_MAX_HEIGHT = HEIGHT - 100
shark_speed_vertical = 3
SCORE_FILE = "scores.json"
jumpsound = pygame.mixer.Sound("meow.wav")
hitsound = pygame.mixer.Sound("angrycat_audio.mp3")
gameover_sound = pygame.mixer.Sound("CatSadSound.wav")
pygame.mixer.music.load("daysound.mp3")
pygame.mixer.music.play(-1)
current_music = "day"


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
dino_night_image = pygame.transform.scale(dino_night_image, (50, 50))
dino_night_jump_image = pygame.image.load("angry_jumpingcat.png")
dino_night_jump_image = pygame.transform.scale(dino_night_jump_image, (50, 50))
dino_night_duck_image = pygame.image.load("angry_jumpingcat.png")
dino_night_duck_image = pygame.transform.scale(pygame.image.load("angry_jumpingcat.png"), (50, 25))
obstacle_image_dog = pygame.image.load("obstacle.png")
obstacle_image_dog = pygame.transform.scale(obstacle_image_dog, (50, 50))
obstacle_image_puddle = pygame.image.load("puddle.png")
obstacle_image_puddle = pygame.transform.scale(obstacle_image_puddle, (50, 50))
obstacle_image_shark = pygame.image.load("shark.png")
obstacle_image_shark = pygame.transform.scale(obstacle_image_shark, (50, 50))
hawk_image = pygame.image.load("hawk.png")
hawk_image = pygame.transform.scale(hawk_image, (50, 50))
game_over_image = pygame.image.load("game_over.png")
game_over_image = pygame.transform.scale(game_over_image, (WIDTH, HEIGHT))
bg_day = pygame.transform.scale(pygame.image.load("mariobg.png"), (WIDTH, HEIGHT))
bg_night = pygame.transform.scale(pygame.image.load("nightmariobg.png"), (WIDTH, HEIGHT))
bg_forest_day = pygame.transform.scale(pygame.image.load("forest.jpg"), (WIDTH, HEIGHT))
bg_forest_night = pygame.transform.scale(pygame.image.load("forest_dark.jpg"), (WIDTH, HEIGHT))
bg_beach_day = pygame.transform.scale(pygame.image.load("bg_beach_day.png"), (WIDTH, HEIGHT))
bg_beach_night = pygame.transform.scale(pygame.image.load("bg_beach_night.png"), (WIDTH, HEIGHT))

def load_score():
    if os.path.exists(SCORE_FILE):
        try:
            with open(SCORE_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []

def save_score(new_score):
    scores = load_score()
    scores.append(new_score)
    scores = sorted(scores, reverse=True)[:5]  # Keep top 5
    with open(SCORE_FILE, "w") as file:
        json.dump(scores, file)

def display_game_over_screen(score):
    screen.fill(WHITE)
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
    screen.blit(StartScreen, (0, 0))
    font = pygame.font.Font(None, 36)
    scores = load_score()
    y_offset = 50
    for index, s in enumerate(scores):
        score_text = font.render(f"{index + 1}. {s}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, y_offset))
        y_offset += 40

    return_text = font.render("Press T to Return to Title", True, WHITE)
    screen.blit(return_text, (WIDTH // 2 - return_text.get_width() // 2, HEIGHT - 50))

def fade_transition(screen, color, duration=500):
    fade_surface = pygame.Surface(screen.get_size())
    fade_surface.fill(color)
    
    
    for alpha in range(0, 255, 5):  
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
    pygame.time.set_timer(pygame.USEREVENT, 50)

def change_music(new_track):
    pygame.mixer.music.fadeout(2000)

    def load_new_track():
        pygame.mixer.music.load(new_track)
        pygame.mixer.music.play(-1)

    threading.Thread(target=load_new_track).start()

def get_environment(score):
    stage_length = 500
    looped_score = score % (stage_length * 6)  # Resets every 3000 points

    if looped_score < stage_length:
        return "day"
    elif looped_score < stage_length * 2:
        return "night"
    elif looped_score < stage_length * 3:
        return "forest_day"
    elif looped_score < stage_length * 4:
        return "forest_night"
    elif looped_score < stage_length * 5:
        return "beach_day"
    else:
        return "beach_night"

# Game loop
running = True
while running:  
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
                    jumpsound.play()
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    duck = True
                elif event.key == pygame.K_k and get_environment(score).endswith("night"):
                    attacking = True
                    attack_timer = 20
                    current_dino = dino_night_jump_image
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    duck = False

            

        elif game_state == GAME_OVER:
            pygame.mixer.music.fadeout(3000)
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
                pygame.mixer.music.stop()  
                pygame.mixer.music.load("daysound.mp3")  
                pygame.mixer.music.play(-1) 
                current_music = "day"

        elif game_state == HIGH_SCORES:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                game_state = TITLE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  
                game_state = PLAYING

    # Handle game states
    if game_state == TITLE:
        display_title_screen()
    elif game_state == HIGH_SCORES:
        screen.fill(WHITE)  
        display_high_scores()  


    elif game_state == PLAYING:
        current_environment = get_environment(score)
        
        if previous_environment != current_environment:  
            if obstacle_x > -50:
                pass
            else:
                obstacle_x = WIDTH + random.randint(300, 500) #Only reset if fully off-screen
        previous_environment = current_environment

        if current_environment == "day":
            screen.blit(bg_day, (0, 0))
        elif current_environment == "night":
            screen.blit(bg_night, (0, 0))
            font = pygame.font.Font(None, 48)
            press_k_text = font.render("Press K to attack!", True, (255, 0, 0))
            screen.blit(press_k_text, (WIDTH // 2 - press_k_text.get_width() // 2, 50))
        elif current_environment == "forest_day":
            screen.blit(bg_forest_day, (0, 0))
        elif current_environment == "forest_night":
            screen.blit(bg_forest_night, (0, 0))
        elif current_environment == "beach_day":
            screen.blit(bg_beach_day, (0, 0))
        else:
            screen.blit(bg_beach_night, (0, 0))

        if current_environment in ["beach_day", "beach_night"]: 
            spawn_hawk = False
            if not spawn_shark:
                spawn_shark = True
                obstacle_flying_x = WIDTH
                obstacle_flying_y = random.randint(SHARK_MIN_HEIGHT, SHARK_MAX_HEIGHT)
                obstacle_x = WIDTH + random.randint(200, 400)
            if dino_rect.colliderect(obstacle_rect):
                print(f"Collision detected at Beach! Dog position: {obstacle_x}, Dino position: {dino_x}")
        elif current_environment in ["forest_day", "forest_night"]:
            if not spawn_hawk and not spawn_shark:
                spawn_hawk = True
                hawk_x = WIDTH
                hawk_y = random.randint(HAWK_MIN_HEIGHT, HAWK_MAX_HEIGHT)
                obstacle_x = hawk_x + random.randint(150, 400)

        #Music
        new_music = "daysound.mp3" if current_environment.endswith("day") else "nightsound.mp3"
        if new_music != current_music:
            change_music(new_music)
            current_music = new_music

        # Update dino image
        if current_environment.endswith("night"):
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
            current_dino = dino_night_jump_image
        elif duck:
            current_dino = dino_night_duck_image if current_environment.endswith("night") else dino_duck_image
        else:
            current_dino = dino_night_image if current_environment.endswith("night") else dino_image

        if attacking:
            attack_timer -= 1
            if attack_timer <= 0:  #reset
                attacking = False

                fade_transition(screen, BLACK)
                current_dino = dino_night_image
                pygame.time.set_timer(pygame.USEREVENT, 1000)

            if dino_rect.colliderect(obstacle_rect):
                obstacle_x = WIDTH + 500
                score += 100
                hitsound.play()
            if dino_rect.colliderect(obstacle_flying_rect):
                obstacle_flying_x = WIDTH + 500
                score += 100
                hitsound.play()
            if dino_rect.colliderect(hawk_rect):
                hawk_x = WIDTH + 500
                score += 100
                hitsound.play()
                
        
        obstacle_x -= obstacle_speed
        if spawn_shark:
            obstacle_flying_x -= obstacle_flying_speed
            obstacle_flying_y += shark_speed_vertical * shark_direction
            if obstacle_flying_y <= SHARK_MIN_HEIGHT or obstacle_flying_y >= SHARK_MAX_HEIGHT:
                shark_direction *= -1
        if spawn_hawk:
            hawk_x -= hawk_speed

        if obstacle_x < -50:
            obstacle_x = WIDTH + random.randint(300, 500)
        if obstacle_flying_x < -50:
            obstacle_flying_x = WIDTH
            spawn_shark = False
        if hawk_x < -50:
            hawk_x = WIDTH
            hawk_y = random.randint(HAWK_MIN_HEIGHT, HAWK_MAX_HEIGHT)
            spawn_hawk = True 

        # Collision detection
        dino_rect = pygame.Rect(dino_x, dino_y, 50, 50 if not duck else 25)
        obstacle_rect = pygame.Rect(obstacle_x, HEIGHT - 100, 50, 50)
        obstacle_flying_rect = pygame.Rect(obstacle_flying_x, obstacle_flying_y, 50, 50)
        hawk_rect = pygame.Rect(hawk_x, hawk_y, 50, 50)

        # Debugging: Draw rectangles for visualization
        pygame.draw.rect(screen, (255, 0, 0), dino_rect, 2)
        #pygame.draw.rect(screen, (0, 0, 255), obstacle_rect, 2)
        pygame.draw.rect(screen, (0, 255, 0), obstacle_flying_rect, 2)
        #pygame.draw.rect(screen, (255, 255, 0), hawk_rect, 2)

        # Collision Logic
        if not attacking and (dino_rect.colliderect(obstacle_rect) or dino_rect.colliderect(obstacle_flying_rect) or (dino_rect.colliderect(hawk_rect) and not duck)):
            gameover_sound.play()
            pygame.mixer.music.stop()
            save_score(score)
            game_state = GAME_OVER 

        # Draw game
        if jump:
            screen.blit(current_jump, (dino_x, dino_y))
        elif duck:
            screen.blit(current_duck, (dino_x, HEIGHT - 75))
        else:
            screen.blit(current_dino, (dino_x, dino_y))

        screen.blit(obstacle_image_dog, (obstacle_x, HEIGHT - 100))
        if current_environment in ["beach_day", "beach_night"]:
            screen.blit(obstacle_image_shark, (obstacle_flying_x, obstacle_flying_y))
        if current_environment in ["forest_day", "forest_night"]:
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
