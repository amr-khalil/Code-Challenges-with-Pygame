import pygame
import random

# Initialize pygame
pygame.init()

# Set surface and its caption
WIDTH = 945
HEIGHT= 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Clown")


# Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

# Set game values
PLAYER_STARTING_LIVES = 5
CLOWN_STARTING_VELOCITY = 3
CLOWN_ACCELERATION = 0.5


score = 0
player_lives = PLAYER_STARTING_LIVES

clown_velocity = CLOWN_STARTING_VELOCITY
clown_dx = random.choice([-1,1])
clown_dy = random.choice([-1,1])
 
# Set colors
BLACK = (0,0,0)
WHITE = (255,255,255)

BLUE = (1,175,209)
YELLOW = (248,231,28)

# Set fonts
font = pygame.font.Font("assets/Franxurter.ttf", 32)

# Set text

title_text = font.render("Catch the clown", True, BLUE)
title_rect = title_text.get_rect()
title_rect.topleft = (50, 10)

score_text = font.render(f"Score: {score}", True, YELLOW)
score_rect = score_text.get_rect()
score_rect.topright = (WIDTH - 50,10)

lives_text = font.render(f"Lives: {player_lives}", True, YELLOW)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WIDTH - 50,50)

gameover_text = font.render(f"GAMEOVER", True, BLUE, YELLOW)
gameover_rect = gameover_text.get_rect()
gameover_rect.center = (WIDTH//2, HEIGHT//2)

continue_text = font.render(f"Press space key to play again", True, BLUE, YELLOW)
continue_rect = continue_text.get_rect()
continue_rect.center = (WIDTH//2, HEIGHT//2 + 64)

# Set sound and music
click_sound = pygame.mixer.Sound("assets/click_sound.wav")
miss_sound = pygame.mixer.Sound("assets/miss_sound.wav")
miss_sound.set_volume(0.1)
pygame.mixer.music.load("assets/ctc_background_music.wav")


# Set images
background_img = pygame.image.load("assets/background.png")
background_rect = background_img.get_rect()
background_rect.topleft = (0,0)

clown_img = pygame.image.load("assets/clown.png")
clown_rect = clown_img.get_rect()
clown_rect.center = (WIDTH//2, HEIGHT//2)

# The main game loop
pygame.mixer.music.play(-1,0.0)
running = True
while running:
    # Loop through a list of events that occured
    for event in pygame.event.get():
        # Quit
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            # The clown clicked
            if clown_rect.collidepoint((mouse_x, mouse_y)):
                click_sound.play()
                score += 1
                clown_velocity += CLOWN_ACCELERATION

                # Move the clown in a new direction
                previous_dx = clown_dx
                previous_dy = clown_dy

                while previous_dx == clown_dx and previous_dy == clown_dy:
                    clown_dx = random.choice([-1,1])
                    clown_dy = random.choice([-1,1])
            
            else:
                miss_sound.play()
                player_lives -= 1
        
    

    # Move the clown
    clown_rect.x += clown_dx * clown_velocity
    clown_rect.y += clown_dy * clown_velocity

    # Bounce the clown
    if clown_rect.left < 0 or clown_rect.right > WIDTH:
        clown_dx = -1 * clown_dx

    if clown_rect.top < 0 or clown_rect.bottom > HEIGHT:
        clown_dy = -1 * clown_dy


    # Screen
    screen.fill(BLACK)

    # Bliting background
    screen.blit(background_img, background_rect)


    # Update text
    score_text = font.render(f"Score: {score}", True, YELLOW)
    lives_text = font.render(f"Lives: {player_lives}", True, YELLOW)

    # Check gameover
    if player_lives == 0:
        screen.blit(gameover_text, gameover_rect)
        screen.blit(continue_text, continue_rect)
        pygame.display.update()
        
        # Pause game
        pygame.mixer.music.stop()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                # The player wants to continue
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        score = 0
                        player_lives = PLAYER_STARTING_LIVES

                        clown_rect.center = (WIDTH//2, HEIGHT//2)
                        clown_velocity = CLOWN_STARTING_VELOCITY
                        clown_dx = random.choice([-1,1])
                        clown_dy = random.choice([-1,1])

                        pygame.mixer.music.play(-1, 0.0)
                        is_paused = False
                
            # the player want to quit
            if event.type == pygame.QUIT:
                is_paused = False
                running = False

        # is_paused = False
        # while is_paused:
        # is_paused = True


    
    # Bliting text
    screen.blit(title_text, title_rect)
    screen.blit(score_text, score_rect)
    screen.blit(lives_text, lives_rect)

    # Bliting images
    screen.blit(clown_img, clown_rect)

    # Update
    pygame.display.update()

    # Clock
    clock.tick(FPS)

# End the game
pygame.quit()



