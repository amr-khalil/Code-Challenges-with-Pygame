import pygame
import sys
import random

WIDTH = 960
HEIGHT = 720
WHITE = (255,255, 255)
BLACK = (0,0,0)
FPS = 50
TITLE = "Old TV"

def update():
    pass

def draw():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 100)
    text = font.render("OLD TV", 1, WHITE)
    x_text =  WIDTH/2 - text.get_width()/2
    y_text =  HEIGHT/2 - text.get_height()/2
    screen.blit(text, (x_text, y_text))

    for i in range(10000):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = 2
        pygame.draw.rect(screen, WHITE, (x, y, size, size))


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

app_running = True
while app_running:
    mouse_position = pygame.mouse.get_pos()

    # Loop over events
    for event in pygame.event.get():
        # Quit event
        if event.type == pygame.QUIT:
            app_running == False
            sys.exit()

        # Keydown events
        elif event.type == pygame.KEYDOWN:
            # Escape
            if event.key == pygame.K_ESCAPE:
                app_running == False
                sys.exit()
        

    update()
    draw()

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
