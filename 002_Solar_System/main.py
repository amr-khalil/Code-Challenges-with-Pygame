import pygame
import sys

WIDTH = 800
HEIGHT = 800
CENTER_X = WIDTH/2
CENTER_Y = HEIGHT/2

WHITE = (255,255, 255)
BLACK = (0,0,0)

SUN = pygame.color.Color('orange')
MERCURY =  pygame.color.Color('grey')
VENUS =  pygame.color.Color('brown')
EARTH =  pygame.color.Color('blue')
MARS =  pygame.color.Color('red')
JUPITER =  pygame.color.Color('orange')
SATURN =  pygame.color.Color('beige')
URANUS =  pygame.color.Color('beige')
NEPTUNE =  pygame.color.Color('darkblue')
PLUTO =  pygame.color.Color('darkred')

FPS = 50
TITLE = "Solar System"

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()


class Planet:
    def __init__(self, distance, radius, speed, name, color):
        self.x = CENTER_X + distance
        self.y = CENTER_Y + distance
        self.distance = distance
        self.radius = radius
        self.speed = speed
        self.name = name
        self.color = color
    
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        self.move()

    def move(self):
        self.x += self.speed



def update():
    pass

sun = Planet(0, 50, 0, "Sun", SUN)
mercury = Planet(100, 10, 10, "Mercury", MERCURY)
def draw():
    screen.fill(BLACK)
    sun.draw()
    mercury.draw()




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
