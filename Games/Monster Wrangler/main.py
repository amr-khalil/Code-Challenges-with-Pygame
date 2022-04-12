import pygame
import random
from monster_wrangler import Game, Player, WIDTH, HEIGHT, FPS

# Initialize pygame
pygame.init()

# Set surface and its caption
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Monster Wrangler")

# Set FPS and clock
clock = pygame.time.Clock()

# Set colors
BLACK = (0,0,0)
WHITE = (255,255,255)

# Create a palyer group and player object
player_group = pygame.sprite.Group()
player = Player()
player_group.add(player)

#  Create a mosnter group and monster objects
monster_group = pygame.sprite.Group()

# Create a game object
game = Game(screen, player, monster_group)
game.pause_game("Monster Wangler", "Press Enter to begin")
game.start_new_round()

# The main game loop
running = True
while running:
    # Loop through a list of events that occured
    for event in pygame.event.get():
        # Quit
        if event.type == pygame.QUIT:
            running = False
        
        # Player wants to go back
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.warp()

    # Fill the screen
    screen.fill(BLACK)

    # Update and draw sprite groups
    player_group.update()
    player_group.draw(screen)
    monster_group.update()
    monster_group.draw(screen)
    game.update()
    game.draw()

    # Update
    pygame.display.update()

    # Clock
    clock.tick(FPS)
# End the game
pygame.quit()
