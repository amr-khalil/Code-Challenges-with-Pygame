import math
from matplotlib.pyplot import draw
import pygame, sys
from pygame.locals import *
from solar_system import Sun, Planet, WIDTH, HEIGHT, PLANETS, FPS

# Colors
BLACK = pygame.Color(0,0,0)

# Pygame Initiation
def init():
    global screen
    global clock
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Solar System")
    pygame.init()

init()

# Initiate classes


speed = 10
sun = Sun(screen)
p_list = [Planet(screen, data["daysPerYear"], data["radius"],  data["color"], data["distance"], name, speed, data["direction"]) for name, data in PLANETS.items()]
    
# Font
font = pygame.font.SysFont('Arial', 15)
font2 = pygame.font.SysFont(None, 30)

def maps(num, min1, max1, min2, max2):
    return(((num - min1) / (max1 - min1)) * (max2 - min2)) + min2

# Draw
def draw():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # Background
    screen.fill(BLACK)

    # Draw sun
    sun.draw()
    # Draw planets
    for p in p_list:
        p.draw()
        p.speed = maps(mouse_x, 0, WIDTH, 1, 100)
    
    # Number of earth days
    number_of_days = int(p_list[2].current_day)
    # Earth days to year
    years = abs(round(number_of_days/365, 2))
    
    # Show time text
    text =  font.render(f"Time = {years} Earth Years", False, (255,255,255))
    screen.blit(text,(10,10))

    text =  font.render(f"Speed = {int(p.speed)} X", False, (255,255,255))
    screen.blit(text,(10,30))

    text =  font2.render(f"Solar System", False, (255,255,255))
    text_x = text.get_width()/2
    screen.blit(text,(WIDTH/2-text_x,10))

    

# Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
    draw()

    pygame.display.update()
    clock.tick(FPS)
