import pygame
import random

# Initialize pygame
pygame.init()

# Set surface and its caption
WIDTH = 1000
HEIGHT= 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Feed the Dragon")


# Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

# Set game values
PLAYER_STARTING_LIVES = 5
PLAYER_VELOCITY = 10
COIN_STARTING_VELOCITY = 10
COIN_ACCELERATION = 0.5
BUFFER_DISTANCE = 100

score = 0
player_lives = PLAYER_STARTING_LIVES
coin_velocity = COIN_STARTING_VELOCITY
 
# Set colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
DARKGREEN = (10,50,10)
BLUE = (0,0,255)
YELLOW = (255,255,0)
CYAN = (0,255,255)
MAGENTA = (255,0,255)

# Set fonts
font = pygame.font.Font("assets/AttackGraffiti.ttf", 32)

# Set text
score_text = font.render(f"Score: {score}", True, GREEN)
score_rect = score_text.get_rect()
score_rect.topleft = (10,10)

title_text = font.render("Feed the Dragon", True, GREEN)
title_rect = title_text.get_rect()
title_rect.centerx = WIDTH//2
title_rect.y = 10

lives_text = font.render(f"Lives: {player_lives}", True, GREEN)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WIDTH - 10,10)


gameover_text = font.render(f"GAMEOVER", True, GREEN)
gameover_rect = gameover_text.get_rect()
gameover_rect.center = (WIDTH//2, HEIGHT//2)

continue_text = font.render(f"Press space key to play again", True, GREEN)
continue_rect = continue_text.get_rect()
continue_rect.center = (WIDTH//2, HEIGHT//2 + 32)


# Set sound and music
coin_sound = pygame.mixer.Sound("assets/coin_sound.wav")
miss_sound = pygame.mixer.Sound("assets/miss_sound.wav")
miss_sound.set_volume(0.1)
pygame.mixer.music.load("assets/ftd_background_music.wav")


# Set images
player_img = pygame.image.load("assets/dragon_right.png")
player_rect = player_img.get_rect()
player_rect.left = 32
player_rect.centery = HEIGHT//2

coin_img = pygame.image.load("assets/coin.png")
coin_rect = coin_img.get_rect()
coin_rect.x = WIDTH + BUFFER_DISTANCE
coin_rect.y = random.randint(64, HEIGHT - 32)

# The main game loop
pygame.mixer.music.play(-1,0.0)
running = True
while running:
    # Loop through a list of events that occured
    for event in pygame.event.get():
        # Quit
        if event.type == pygame.QUIT:
            running = False

    # Movements
    keys = pygame.key.get_pressed()
    # Move the Dragon
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and player_rect.top > 64:
        player_rect.y -= PLAYER_VELOCITY
        print(player_rect.left)

    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player_rect.bottom < HEIGHT:
        player_rect.y += PLAYER_VELOCITY

    # Move the Coin
    if coin_rect.right < 0:
        # Player missed the coin
        player_lives -= 1
        miss_sound.play()
        coin_rect.x = WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(64, HEIGHT-32)
    
    else:
        coin_rect.x -= coin_velocity


    # Check for collisions
    if player_rect.colliderect(coin_rect):
        score += 1
        coin_sound.play()
        coin_rect.x = WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(64, HEIGHT-32)
        coin_velocity +=  COIN_ACCELERATION
    
    # Update score and lives text
    score_text = font.render(f"Score: {score}", True, GREEN)
    lives_text = font.render(f"Lives: {player_lives}", True, GREEN)

    # Check for game over
    if player_lives == 0:
        screen.blit(gameover_text, gameover_rect)
        screen.blit(continue_text, continue_rect)
        pygame.display.update()

        # Pause and reset the game
        pygame.mixer.music.stop()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                # Play again
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        score = 0
                        player_lives = PLAYER_STARTING_LIVES
                        player_rect.y = HEIGHT//2
                        coin_velocity = COIN_STARTING_VELOCITY
                        pygame.mixer.music.play(-1, 0.0)
                        is_paused = False

                # The player want to quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False

    # Screen
    screen.fill(BLACK)
    
    # Bliting text
    screen.blit(score_text, score_rect)
    screen.blit(title_text, title_rect)
    screen.blit(lives_text, lives_rect)
    pygame.draw.line(screen, WHITE, (0,64), (WIDTH,64), 2)

    # Bliting images
    screen.blit(player_img, player_rect)
    screen.blit(coin_img, coin_rect)


    # Update
    pygame.display.update()

    # Clock
    clock.tick(FPS)

# End the game
pygame.quit()
