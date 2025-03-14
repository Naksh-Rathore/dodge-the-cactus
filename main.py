import pygame
import os
import random
import time

screen_width = 600
screen_height = 500
fps = 60
player_width = 150
player_height = 150

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dodge The Cactus by Naksh Rathore")

player_image = pygame.transform.scale(pygame.image.load(os.path.join("images", "player.png")), (player_width, player_height))

jump_sfx = pygame.mixer.Sound(os.path.join("sounds", "jump.mp3"))
game_over_sfx = pygame.mixer.Sound(os.path.join("sounds", "game-over.mp3"))

hitbox_size = 90

player_x = 50
player_y = 150
player_velocity = 0
player_rect = pygame.Rect(player_x, player_y, player_width - hitbox_size, player_height - hitbox_size)

jump_height = -22
gravity = 0.9
is_jumping = False
ground_y = 250

cacti = []
cactus_vel = 8
cactus_width = 100
cactus_height = 150
cactus_gap = 10000000

playing = True
clock = pygame.time.Clock()

font = pygame.font.SysFont("comicsans", 30)

score = 0
text = font.render(f"Score: {score}", True, (0, 0, 0))

def game_over():
    global playing, text

    game_over_sfx.play() 

    print(f"Game Over!")

    text = font.render("Game Over!", True, (0, 0, 0))
    draw_window(player_x, player_y)

    time.sleep(1.75)
    playing = False 


def display_score(score):
    global text

    text = font.render(f"Score: {score}", True, (0, 0, 0))

class Cactus:
    def __init__(self, x):
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("images", "cactus.png")), (cactus_width, cactus_height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = ground_y

    def move(self):
        self.rect.x -= cactus_vel

        if self.rect.right < 0:
            self.rect.x = screen_width + random.randint(200, 300)  

    def check_collision(self):
        return player_rect.colliderect(self.rect)

initial_x = screen_width + 100  
for i in range(3): 
    cacti.append(Cactus(initial_x + i * cactus_gap + random.randint(20, 50))) 

def draw_window(player_x, player_y):
    screen.fill((255, 255, 255)) 
    screen.blit(player_image, (player_x, player_y))  

    player_rect.x = player_x
    player_rect.y = player_y

    for cactus in cacti:
        screen.blit(cactus.image, cactus.rect)  

    screen.blit(text, (screen_width/2 - 35, 10))  

    pygame.display.update() 

def jump():
    global player_y, player_velocity, is_jumping

    player_velocity += gravity 
    player_y += player_velocity  

    if player_y >= ground_y:  
        player_y = ground_y
        player_velocity = 0
        is_jumping = False

while playing:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and not is_jumping:
                player_velocity = jump_height  
                is_jumping = True
                jump_sfx.play()  

    jump()

    score += 1
    display_score(score)

    draw_window(player_x, player_y)

    for cactus in cacti:
        cactus.move() 

        if cactus.check_collision():
            game_over()

pygame.quit()
