import pygame
import random
import time


WIDTH = 800
HEIGHT = 800
FPS = 60

# Set color
WHITE = (255,255,255)
BLACK = (0,0,0)

# Initiation
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(WHITE)

# Set variables
MAX_GENEARATIONS = 10000
GENEARATIONS = 0
DISTANCE = 0
planetsList = []


def text_display(generations, max_generations, bestDistance):
    font = pygame.font.SysFont('Arial', 18, True)
    # Title
    title = font.render("Finding the Shortest Route Using the Genetic Algorithm", True, BLACK)
    title_rect = title.get_rect()
    title_rect.center = (WIDTH//2, 20)
    screen.blit(title, title_rect)
    
    font = pygame.font.SysFont("Arial", 16, False)
    # Subtitle
    subtitle = font.render(f"Best Generation {generations} / {max_generations}", False, BLACK)
    subtitle_rect = subtitle.get_rect()
    subtitle_rect.center = (WIDTH//2, 50)
    screen.blit(subtitle, subtitle_rect)

    # Distance text
    distance_text = font.render(f"Shortest Distance: {bestDistance}", False, BLACK)
    distance_text_rect = distance_text.get_rect()
    distance_text_rect.center = (WIDTH//2, 70)
    screen.blit(distance_text, distance_text_rect)

#text_display(GENEARATIONS, DISTANCE)

class Planet():
    def __init__(self, x, y):
        self.pos = (x,y)
        self.radius = 15
        self.color = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))

    def draw(self):
        pygame.draw.circle(screen, self.color, self.pos, self.radius)

class Route():
    def __init__(self, planetsList):
        self.planetsList = planetsList
        self.generation = 0
        self.bestParent = self.generate_parent()
        self.routesList = []
    
    def draw(self, parent):
        self.color = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
        
        for i in range(len(parent) - 1):
            x1, y1 = parent[i].pos
            x2, y2 = parent[i+1].pos
            pygame.draw.line(screen, self.color, (x1,y1), (x2,y2), 3)
        
            
    def generate_parent(self):
        self.randomParent = [planet for planet in random.sample(self.planetsList, len(self.planetsList))]
        return self.randomParent

    def fitness(self, parent):
        distanceList = []
        parentList = parent
        for i in range(len(parentList) - 1):
            x1, y1 = parentList[i].pos
            x2, y2 = parentList[i+1].pos
            
            A = pow(x1 - x2, 2)
            B = pow(y1 - y2, 2)
            distance = pow(A + B, 0.5)
            
            distanceList.append(distance)

        score = round(sum(distanceList), 2)
        return score

    def mutate(self, parent):
        parentList = parent
        rand_index = random.randrange(0, len(parentList))
        rand_value = random.choice(parentList)
        rand_value_index = parentList.index(rand_value)

        temp = parentList[rand_index]
        parentList[rand_index] = parentList[rand_value_index]
        parentList[rand_value_index] = temp

        mutatedParent = parentList

        return mutatedParent
    
    def train(self):
        self.bestGeneration = 0
        self.bestFitness =self.fitness(self.bestParent)
        
        self.generationList = []

        while self.generation < MAX_GENEARATIONS:
            self.generation += 1

            

            child = self.mutate(self.bestParent)
            childFitness = self.fitness(child)

            self.routesList.append(child)
        
            if childFitness >= self.bestFitness:
                continue
            
            self.bestParent = child
            self.bestFitness = childFitness
            self.bestGeneration = self.generation
            self.routesList.append(self.bestParent)
            self.generationList.append(self.generation)
            print(self.generation, self.bestFitness)

running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mousex, mousey = pygame.mouse.get_pos()
            planet = Planet(mousex, mousey)
            planetsList.append(planet)
            planet.draw()

            route = Route(planetsList)
            route.train()
            GENEARATIONS = route.bestGeneration
            DISTANCE = route.bestFitness

            for r in route.routesList:
                screen.fill(WHITE)
                route.draw(r)
                for p in r:
                    p.draw()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and len(planetsList) >= 2:
                route = Route(planetsList)
                route.train()
                # for p in planetsList:
                #     p.draw()
                GENEARATIONS = route.bestGeneration
                DISTANCE = route.bestFitness

            if event.key == pygame.K_SPACE:
                planetsList = []
                GENEARATIONS = 0
                DISTANCE = 0
                screen.fill(WHITE)

    text_display(GENEARATIONS, MAX_GENEARATIONS, DISTANCE)
    clock.tick(FPS)
    pygame.display.update()

pygame.quit()
