from matplotlib.pyplot import angle_spectrum
import pygame
from math import sin, cos, pi

# Constants
WIDTH = 800
HEIGHT = 800
SUN_X = WIDTH/2
SUN_Y = HEIGHT/2
FPS = 30
K = 0.98630136986
R = 57.2957795131
SPEED = 10

WHITE = (255,255,255)
GARY = (50,50,50)

# Dictionaries
SUN = {
    "radius": 40,
    "color": (255,165,0)
}

PLANETS = {
    "Mercury":{
        "radius": 5,
        "distance": 75,
        "direction":-1,
        "daysPerYear": 88,
        "color": (153, 61, 0)
    },
    "Venus":{
        "radius": 6,
        "distance": 100,
        "direction": 1,
        "daysPerYear": 225,
        "color": (200, 100, 200)
    },
    "Earth":{
        "radius":8,
        "distance": 125,
        "direction":-1,
        "daysPerYear": 355,
        "color": (51, 127, 214)
    },
    "Mars":{
        "radius": 7,
        "distance": 150,
        "direction":-1,
        "daysPerYear": 686,
        "color": (200, 0, 0)
    },
    "Jupiter":{
        "radius": 12,
        "distance": 200,
        "direction":-1,
        "daysPerYear": 4328.9,
        "color": (255, 127, 53)
    },
    "Saturn":{
        "radius": 10,
        "distance": 250,
        "direction":-1,
        "daysPerYear": 10753,
        "color": (176, 143, 54)
    },
    "Uranus":{
        "radius": 9,
        "distance": 300,
        "direction": 1,
        "daysPerYear": 30664,
        "color": (0, 100, 100)
    },
    "Neptune":{
        "radius": 7,
        "distance": 350,
        "direction":-1,
        "daysPerYear": 60148,
        "color": (79, 208, 231)
    }
}

# Sun Class
class Sun:
    def __init__(self, screen):
        self.screen = screen
        self.x = SUN_X
        self.y = SUN_Y
        self.name = "Sun"
        self.radius = SUN["radius"]
        self.color =  SUN["color"]
        self.font = pygame.font.SysFont('Arial', 10)
    
    def draw(self):
        # Draw sun
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)

        # Add text
        text =  self.font.render(self.name, False, WHITE)
        text_width = text.get_width()/2
        text_height = text.get_height()/2
        self.screen.blit(text,(self.x-text_width, self.y-text_height))

# Planet class
class Planet:
    def __init__(self, screen, days, radius, color, distance, name="", speed=10, direction=-1):
        self.x = 0
        self.y = 0
        self.radius = radius
        self.angle = 0
        self.distance = distance
        self.direction = direction
        self.days =  days
        self.current_day = 0
        self.speed = speed
        self.screen = screen
        self.name = name
        self.color = color
        self.font = pygame.font.SysFont('Arial', 10)    
    
    def draw(self):
        # Draw path for the planet
        pygame.draw.circle(self.screen, GARY, (SUN_X, SUN_Y), self.distance, width=1)
        
        # Draw the planet
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)
        
        # Add text
        text =  self.font.render(self.name, False, WHITE)
        self.screen.blit(text,(self.x+self.radius, self.y+self.radius))

        # Update variables
        self.update()

    def update(self):
        # Update coordinates
        self.x = SUN_X +  self.distance * cos(self.angle)
        self.y = SUN_Y + self.distance * sin(self.angle)

        # Update current planet day
        self.current_day += FPS * self.speed / self.days * self.direction

        # Update planet angel
        self.angle = (self.current_day * K) / R
