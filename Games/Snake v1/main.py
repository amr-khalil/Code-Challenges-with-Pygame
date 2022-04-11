from turtle import right
import pygame
import random

# Initialize pygame
pygame.init()

# Set surface and its caption
WIDTH = 800
HEIGHT= 800
CX = WIDTH//2
CY = HEIGHT//2

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")


# Set FPS and clock
FPS = 20
clock = pygame.time.Clock()

# Set game values
SNAKE_SIZE = 20

head_x = CX
head_y = CY + 100

snake_dx = 0
snake_dy = 0

score = 0



# Set colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
DARKGREEN = (10,50,10)
RED = (255,0,0)
DARKRED = (150,0,0)


# Set fonts
font = pygame.font.SysFont("comicsansms", 48)

# Set text
title_text = font.render("~~Snake~~", True, GREEN, DARKRED)
title_rect = title_text.get_rect()
title_rect.center = (CX,CY)

score_text = font.render(f"Score: {score}", True, GREEN, DARKRED)
score_rect = score_text.get_rect()
score_rect.topleft = (10,10)

gameover_text = font.render("GAMEOVER", True, GREEN, DARKRED)
gameover_rect = gameover_text.get_rect()
gameover_rect.center = (CX,CY)

continue_text = font.render("Press Space to play again", True, GREEN, DARKRED)
continue_rect = continue_text.get_rect()
continue_rect.center = (CX,CY+64)

# Set sound and music
pick_up_sound = pygame.mixer.Sound("assets/pick_up.wav")

# Set shapes
apple_coord = (500, 500, SNAKE_SIZE, SNAKE_SIZE)
apple_rect = pygame.draw.rect(screen, RED, apple_coord)

head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)
head_rect = pygame.draw.rect(screen, GREEN, head_coord)

body_coords = []


# The main game loop
running = True
while running:
    # Loop through a list of events that occured
    for event in pygame.event.get():
        # Quit
        if event.type == pygame.QUIT:
            running = False

        # Move the snake
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake_dx = -1 * SNAKE_SIZE
                snake_dy = 0
            
            if event.key == pygame.K_RIGHT:
                snake_dx =  SNAKE_SIZE
                snake_dy = 0
            
            if event.key == pygame.K_UP:
                snake_dx = 0
                snake_dy = -1 * SNAKE_SIZE

            if event.key == pygame.K_DOWN:
                snake_dx = 0
                snake_dy = SNAKE_SIZE

    body_coords.append(head_coord)
    if len(body_coords) > score:
        del body_coords[0]
        
    # Update x,y positions of the snake head
    head_x += snake_dx
    head_y += snake_dy
    head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)

    # Check for gameover
    if head_rect.left < 0 or head_rect.right > WIDTH or head_rect.top < 0 \
        or head_rect.bottom > HEIGHT or head_coord in body_coords:
        screen.blit(gameover_text, gameover_rect)
        screen.blit(continue_text, continue_rect)
        pygame.display.update()

        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        score = 0
                        head_x = CX
                        head_y = CY + 100
                        head_coord = (head_y, head_y, SNAKE_SIZE, SNAKE_SIZE)
                        body_coords = []
                        snake_dx = 0
                        snake_dy = 0

                        is_paused = False
                
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False


    # Check collisions
    if head_rect.colliderect(apple_rect):
        pick_up_sound.play()
        score += 1
        apple_x = random.randint(0, WIDTH-SNAKE_SIZE)
        apple_y = random.randint(0, HEIGHT-SNAKE_SIZE)
        apple_coord = (apple_x, apple_y, SNAKE_SIZE, SNAKE_SIZE)

        body_coords.append(head_coord)


    # Screen
    screen.fill(WHITE)
    
    # Bliting text
    screen.blit(title_text, title_rect)
    screen.blit(score_text, score_rect)

    # Bliting images
    for body in body_coords:
        pygame.draw.rect(screen, DARKGREEN, body)
    
    head_rect = pygame.draw.rect(screen, GREEN, head_coord)
    apple_rect = pygame.draw.rect(screen, RED, apple_coord)
    score_text = font.render(f"Score: {score}", True, GREEN, DARKRED)



    # Update
    pygame.display.update()

    # Clock
    clock.tick(FPS)

# End the game
pygame.quit()
