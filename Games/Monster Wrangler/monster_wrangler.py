import pygame
import random
import sys

# Set constants
WIDTH = 1200
HEIGHT= 700
CX = WIDTH//2
CY = HEIGHT//2
FPS = 60

# Set colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (20, 176, 235)
GREEN = (87, 201, 47)
PURPLE = (226, 73, 243)
YELLOW = (243, 157, 20)

### Game Class ###
class Game():
    """A class tp control gameplay"""
    def __init__(self, screen, player, monster_group):
        # Intialize game objects
        self.screen = screen
        self.player = player
        self.monster_group = monster_group
        self.score = 0
        self.round_number = 0
        self.round_time = 0
        self.frame_count = 0
        
        # Set sounds and music
        self.next_level_sound = pygame.mixer.Sound("assets/next_level.wav")
        self.next_level_sound.set_volume(0.1)

        # Set font
        self.font = pygame.font.Font("assets/Abrushow.ttf", 24)

        # Set images
        blue_image = pygame.image.load("assets/blue_monster.png")
        green_image = pygame.image.load("assets/green_monster.png")
        purple_image = pygame.image.load("assets/purple_monster.png")
        yellow_image = pygame.image.load("assets/yellow_monster.png")

        # This list contributes with monster type attribute
        self.target_monster_images = [blue_image, green_image, purple_image, yellow_image]
        self.target_monster_type = random.randint(0,3) # 0=blue, 1=green, 2=purple, 3=yellow
        self.target_monster_image = self.target_monster_images[self.target_monster_type]

        self.target_monster_rect = self.target_monster_image.get_rect()
        self.target_monster_rect.centerx = CX
        self.target_monster_rect.top = 30

    def update(self):
        """Update our game object"""
        self.frame_count += 1
        if self.frame_count == FPS:
            self.round_time += 1
            self.frame_count = 0
        
        # Check for collisions
        self.check_collsions()
    
    def draw(self):
        """Draw in the screen"""
        # Add the monster colors to a list where the index of the color matches target_monster_images
        colors = [BLUE, GREEN, PURPLE, YELLOW]

        # Set text
        catch_text = self.font.render("Current Catch", True, WHITE)
        catch_rect = catch_text.get_rect()
        catch_rect.centerx = CX
        catch_rect.top = 5

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.topleft = (5,5)

        lives_text = self.font.render(f"Lives: {self.player.lives}", True, WHITE)
        lives_rect = lives_text.get_rect()
        lives_rect.topleft = (5, 35)

        round_text = self.font.render(f"Current Round: {self.round_number}", True, WHITE)
        round_rect = round_text.get_rect()
        round_rect.topleft = (5, 65)

        time_text = self.font.render(f"Current Time: {self.round_time}", True, WHITE)
        time_rect = time_text.get_rect()
        time_rect.topright = (WIDTH - 10, 5)

        warp_text = self.font.render(f"Wraps: {self.player.warps}", True, WHITE)
        warp_rect = warp_text.get_rect()
        warp_rect.topright = (WIDTH -10, 35)


        # Blit the text
        self.screen.blit(catch_text, catch_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(lives_text, lives_rect)
        self.screen.blit(round_text, round_rect)
        self.screen.blit(time_text, time_rect)
        self.screen.blit(warp_text, warp_rect)
        self.screen.blit(self.target_monster_image, self.target_monster_rect)


        pygame.draw.rect(self.screen, colors[self.target_monster_type], (CX-32, 30, 64, 64), 2)
        pygame.draw.rect(self.screen, colors[self.target_monster_type], (0, 100, WIDTH, HEIGHT-200), 4)

    
    def check_collsions(self):
        """Check for collision between player and monsters"""
        # Check for collisions between a player and an individual monster
        # We will test the type of the monster to see if it matches the type of our target monster
        collided_monster = pygame.sprite.spritecollideany(self.player, self.monster_group)

        # We collided with a monster
        if collided_monster:
            # Caught the correct monster
            if collided_monster.type == self.target_monster_type:
                # increment the score
                self.score += 100 * self.round_number
                #  Remove caught monster
                collided_monster.remove(self.monster_group)
                if(self.monster_group):
                    # There are more monster to catch
                    self.player.catch_sound.play()
                    self.choose_new_target()
                else:
                    # The round is compelte
                    self.player.reset()
                    self.start_new_round()

            # Caught the wrong monster     
            else:
                self.player.die_sound.play()
                self.player.lives -= 1
                # Chek gameover
                if self.player.lives <= 0:
                    self.pause_game(f"Final Score: {self.score}", "Press Enter to play again")
                    self.reset_game()
                self.player.reset()
                
    def start_new_round(self):
        """Populate board with new monster"""
        # Provide a score bouns based on how quickly the round was finished
        self.score += int(10000 * self.round_number/(1 + self.round_time))

        # Reset round values
        self.round_time = 0
        self.frame_count = 0
        self.round_number += 1
        self.player.warps += 1

        # Remove any remaining monsters from a game reset
        for monster in self.monster_group:
            self.monster_group.remove(monster)
        
        # Add monsters to the monster group
        for i in range(self.round_number):
            self.monster_group.add(Monster(random.randint(0, WIDTH - 64), random.randint(100, HEIGHT - 164), self.target_monster_images[0], 0))
            self.monster_group.add(Monster(random.randint(0, WIDTH - 64), random.randint(100, HEIGHT - 164), self.target_monster_images[1], 1))
            self.monster_group.add(Monster(random.randint(0, WIDTH - 64), random.randint(100, HEIGHT - 164), self.target_monster_images[2], 2))
            self.monster_group.add(Monster(random.randint(0, WIDTH - 64), random.randint(100, HEIGHT - 164), self.target_monster_images[3], 3))
        
        # Choose a new target monster
        self.choose_new_target()
        self.next_level_sound.play()

    def choose_new_target(self):
        """Choose a new target monster for the player"""
        target_monster = random.choice(self.monster_group.sprites())
        self.target_monster_type = target_monster.type
        self.target_monster_image = target_monster.image

    def pause_game(self, main_text, sub_text):
        """Pause the game"""
        main_text = self.font.render(main_text, True, WHITE)
        main_rect = main_text.get_rect()
        main_rect.center = (CX, CY)

        sub_text = self.font.render(sub_text, True, WHITE)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (CX, CY+64)

        # Display the pause text
        self.screen.fill(BLACK)
        self.screen.blit(main_text, main_rect)
        self.screen.blit(sub_text, sub_rect)
        pygame.display.update()

        # Pause the game
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_paused = False
                
                if event.type == pygame.QUIT:
                    is_paused = False
                    sys.exit()
        
    def reset_game(self):
        """Reset the game"""
        self.score = 0
        self.round_number = 0
        self.player.lives = 5
        self.player.warps = 2
        self.start_new_round()



### Player Class ###
class Player(pygame.sprite.Sprite):
    """A player class that the user can control"""
    def __init__(self):
        """Intialize the player"""
        super().__init__()
        self.image = pygame.image.load("assets/knight.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = CX
        self.rect.bottom = HEIGHT

        self.lives = 5
        self.warps = 2
        self.velocity = 8

        self.catch_sound = pygame.mixer.Sound("assets/catch.wav")
        self.catch_sound.set_volume(0.1)
        self.die_sound = pygame.mixer.Sound("assets/die.wav")
        self.die_sound.set_volume(0.1)
        self.wrap_sound = pygame.mixer.Sound("assets/warp.wav")
        self.wrap_sound.set_volume(0.1)


    def update(self):
        """Update the player"""
        keys = pygame.key.get_pressed()

        # Move the player within the bounds of the screen
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity

        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.velocity

        if keys[pygame.K_UP] and self.rect.top > 100:
            self.rect.y -= self.velocity

        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT - 100:
            self.rect.y += self.velocity


    def warp(self):
        """Warp the player to the bottom 'safe zone'"""
        if self.warps > 0:
            self.warps -= 1
            self.wrap_sound.play()
            self.rect.bottom = HEIGHT

    def reset(self):
        """Resets the player position"""
        self.rect.centerx = CX
        self.rect.bottom = HEIGHT



### Monster Class ###
class Monster(pygame.sprite.Sprite):
    """A class to create enemy monster objects"""
    def __init__(self, x, y, image, monster_type):
        """Intialize the monster"""
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        # Monster type is an int 0=blue, 1=green, 2=purple, 3=yellow
        self.type = monster_type

        # Set random motion
        self.dx = random.choice([-1,1])
        self.dy = random.choice([-1,1])
        self.velocity = random.randint(1,5)
    
    def update(self):
        """Update the monster"""
        self.rect.x += self.dx * self.velocity
        self.rect.y += self.dy * self.velocity

        # Bounce the monster off the edges of the display
        if self.rect.left <= 0 or self.rect.right >=  WIDTH:
            self.dx = -1 * self.dx
        
        if self.rect.top <= 100 or self.rect.bottom >= HEIGHT - 100:
            self.dy = -1 * self.dy


