import pygame
import sys
import os
import tkinter as tk
from tkinter import simpledialog, messagebox
import random

pygame.init()

WIDTH = 1000
HEIGHT = 512

FONT = pygame.font.SysFont("comicsans", 30)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Techscape")

tile_size = 20
bg_images = [pygame.transform.scale(pygame.image.load(os.path.join("level2_png", f"level_2_portal_{i}.png")), (WIDTH, HEIGHT)) for i in range(1, 3)]
num_images = len(bg_images)
current_image = 0

class Player():
    def __init__(self, x, y):
        self.animation_frames = [pygame.transform.scale(pygame.image.load(os.path.join("level2_png", f'player{i}.png')), (80, 80)) for i in range(1, 9)]
        self.standing_image = pygame.transform.scale(pygame.image.load(os.path.join('level2_png', 'player1.png')), (80, 80))
        self.image_index = 0
        self.image = self.animation_frames[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.vel_x = 2 
        self.animation_timer = 0
        self.animation_delay = 8

    def update(self):
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.jumped == False:
            self.vel_y = -20
            self.jumped = True
        if key[pygame.K_SPACE] == False:
            self.jumped = False
        if key[pygame.K_LEFT]:
            dx -= 8
            self.direction = -1
        if key[pygame.K_RIGHT]:
            dx += 8
            self.direction = 1

        self.vel_y += 20
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        if dx != 0: 
            self.image_index = (self.image_index + 1) % len(self.animation_frames)
            self.image = self.animation_frames[self.image_index]
        else: 
            self.image = self.standing_image

        for tile_group in world.tile_groups:
            for tile in tile_group.tile_list:
                if tile[1].colliderect(self.rect.move(dx, 0)):
                    dx = 0
                    if not tile_group.visited:
                        if not show_question(tile_group):
                            tile_group.visited = False
                        else:
                            tile_group.visited = True
                if tile[1].colliderect(self.rect.move(0, dy)):
                    if not tile_group.visited:
                        if not show_question(tile_group):
                            tile_group.visited = False
                        else:
                            tile_group.visited = True
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0

        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            dy = 0

        screen.blit(self.image, self.rect)

class TileGroup():
    def __init__(self, data):
        self.tile_list = data
        self.visited = False

class World():
    def __init__(self, data):
        self.tile_list = []
        self.tile_groups = []

        dirt_img = pygame.image.load(os.path.join('level2_png', 'dot.png'))

        row_count = 0
        for row in data:
            col_count = 0
            tiles_in_group = []
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    tiles_in_group.append(tile)
                col_count += 1
            if (len(tiles_in_group) > 0):
                self.tile_groups.append(TileGroup(tiles_in_group))
            row_count += 1

    def draw(self):
        for tile_group in self.tile_groups:
            for tile in tile_group.tile_list:
                screen.blit(tile[0], tile[1])

world_data = [
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1],
]

player = Player(0, 0)
world = World(world_data)

questions = [
    ("What is the capital of France?", "Paris"),
    ("What is 2 + 2?", "4"),
    ("Who wrote 'To Kill a Mockingbird'?", "Harper Lee"),
    ("What is the speed of light?", "299792458"),
    ("Who painted the Mona Lisa?", "Leonardo da Vinci"),
    ("What is the smallest prime number?", "2"),
    ("What is the largest planet in our solar system?", "Jupiter"),
    ("Who discovered penicillin?", "Alexander Fleming"),
    ("What is the square root of 64?", "8"),
    ("What is the chemical symbol for gold?", "Au"),
    ("Who is known as the father of computers?", "Charles Babbage"),
    ("What year did the Titanic sink?", "1912"),
    ("What is the largest mammal?", "Blue whale"),
    ("Who wrote '1984'?", "George Orwell"),
    ("What is the boiling point of water?", "100")
]

correct_answers = 0

def show_question(tile_group):
    global correct_answers
    root = tk.Tk()
    root.withdraw()
    while True:
        question, answer = random.choice(questions)
        user_answer = simpledialog.askstring("Question", question)
        if user_answer is not None and user_answer.lower() == answer.lower():
            messagebox.showinfo("Correct", "Correct answer!")
            correct_answers += 1
            root.destroy()
            if correct_answers >= 5:
                print("Correct!")
                pygame.quit()
                sys.exit()
            return True
        else:
            messagebox.showinfo("Incorrect", "Incorrect answer. The correct answer is " + answer + ".")
            tile_group.visited = False

clock = pygame.time.Clock()
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(bg_images[current_image], (0, 0))
    current_image = (current_image + 1) % num_images

    world.draw()
    player.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    clock.tick(30)

pygame.quit()
sys.exit()
