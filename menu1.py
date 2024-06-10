import pygame
import sys
import tkinter as tk
import os
from io import StringIO
from tkinter import simpledialog, messagebox
import random

pygame.init()

def level1():
    WIDTH = 1000
    HEIGHT = 512

    BOX_WIDTH_SIZE, BOX_HEIGHT_SIZE = 100, 30

    FONT_SIZE = 16
    FONT_SIZE1 = 23

    FONT = pygame.font.SysFont("Arial", FONT_SIZE)
    
    FONT1 = pygame.font.SysFont("Times New Roman", FONT_SIZE1)

    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Techscape")

    BG = pygame.transform.scale(pygame.image.load(os.path.join("level1_png", "level_1.png")), (WIDTH, HEIGHT))

    boxes = []

    places = []
    num_places = 6 
    spacing = 40
    start_y = (HEIGHT - (BOX_HEIGHT_SIZE + spacing) * num_places) / 2 + 50

    for i in range(num_places):
        place_x = (WIDTH - BOX_WIDTH_SIZE) / 2
        place_y = start_y + i * (BOX_HEIGHT_SIZE + spacing)
        places.append((place_x, place_y))

    places.append((WIDTH/2 - BOX_WIDTH_SIZE/2 + 150, HEIGHT/2 - BOX_HEIGHT_SIZE/2 + 70))

    OVAL_WIDTH = 125
    OVAL_HEIGHT = 35

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    TEXT = "start"
    TEXT_1 = "finish"
    TEXT_2 = "Find the sum of the numbers from 1 to n"

    class Rhombus:
        def __init__(self, points, text, id):
            self.id = id
            self.points = points
            self.text = text
            self.dragging = False
            self.offset_x = 0
            self.offset_y = 0
            self.center = (sum(point[0] for point in self.points) / 4,  sum(point[1] for point in self.points) / 4)
            self.left = (points[0][0])
            self.width = (points[1][0] - self.left)
            self.top = (points[1][1])
            self.height = (points[2][1] - self.top)

        def draw(self):
            pygame.draw.polygon(WIN, (255, 255, 255), self.points)
            text_surface = FONT.render(self.text, True, BLACK)
            text_rect = text_surface.get_rect(center=(sum(point[0] for point in self.points) / 4,
                                                      sum(point[1] for point in self.points) / 4))
            WIN.blit(text_surface, text_rect)

        def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.collidepoint(event.pos):
                    self.dragging = True
                    self.offset_x = self.points[0][0] - event.pos[0]
                    self.offset_y = self.points[0][1] - event.pos[1]
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    new_points = []
                    for point in self.points:
                        new_x = point[0] + event.rel[0]
                        new_y = point[1] + event.rel[1]
                        new_points.append((new_x, new_y))
                    self.points = new_points

        def move(self, rel):
            new_points = [(point[0] + rel[0], point[1] + rel[1]) for point in self.points]
            self.points = new_points
            
        def move_to_place(self, new_place):
            bottom_left = self.points[0]
            self.points = [(new_place[0] + point[0] - bottom_left[0],new_place[1] + point[1] - bottom_left[1]) for point in self.points]

        def collidepoint(self, pos):
            points_tuple = tuple(self.points)
            shape_polygon = pygame.draw.polygon(WIN, WHITE, points_tuple)
            return shape_polygon.collidepoint(pos)

    class Parallelogram:
        def __init__(self, points, text, id):
            self.id = id
            self.points = points
            self.text = text
            self.dragging = False
            self.offset_x = 0
            self.offset_y = 0
            self.center = (sum(point[0] for point in self.points) / 4,  sum(point[1] for point in self.points) / 4)
            self.left = (points[0][0])
            self.width = (points[1][0] - self.left)
            self.top = (points[0][1])
            self.height = (points[2][1] - self.top)

        def draw(self):
            pygame.draw.polygon(WIN, (255, 255, 255), self.points)
            text_surface = FONT.render(self.text, True, BLACK)
            text_rect = text_surface.get_rect(center=(sum(point[0] for point in self.points) / 4,
                                                      sum(point[1] for point in self.points) / 4))
            WIN.blit(text_surface, text_rect)

        def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.collidepoint(event.pos):
                    self.dragging = True
                    self.offset_x = self.points[0][0] - event.pos[0]
                    self.offset_y = self.points[0][1] - event.pos[1]
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    new_points = []
                    for point in self.points:
                        new_x = point[0] + event.rel[0]
                        new_y = point[1] + event.rel[1]
                        new_points.append((new_x, new_y))
                    self.points = new_points

        def move(self, rel):
            new_points = [(point[0] + rel[0], point[1] + rel[1]) for point in self.points]
            self.points = new_points
            
        def move_to_place(self, new_place):
            bottom_left = self.points[0]
            self.points = [(new_place[0] + point[0] - bottom_left[0],new_place[1] + point[1] - bottom_left[1]) for point in self.points]

        def collidepoint(self, pos):
            points_tuple = tuple(self.points)
            shape_polygon = pygame.draw.polygon(WIN, WHITE, points_tuple)
            return shape_polygon.collidepoint(pos)
        
    rhombus_ids = [1, 2]
    parallelogram_ids = [3, 4, 5, 6, 7, 8, 9, 10]

    rhombus1 = Rhombus([
        (215, HEIGHT/2 - 100 - 25 + 200 + 100),
        (245, HEIGHT/2 - 100 + 200 + 100),
        (215, HEIGHT/2 - 100 + 25 + 200 + 100),
        (185, HEIGHT/2 - 100 + 200 + 100)
    ], "i<=n", rhombus_ids[0])

    rhombus2 = Rhombus([
        (215, HEIGHT/2 - 100 - 25 - 100 + 200 + 100),
        (245, HEIGHT/2 - 100 - 100 + 200 + 100),
        (215, HEIGHT/2 - 100 + 25 - 100 + 200 + 100),
        (185, HEIGHT/2 - 100 - 100 + 200 + 100)
    ], "n!=0", rhombus_ids[1])

    parallelogram1 = Parallelogram([
        (50 + BOX_WIDTH_SIZE + 20, HEIGHT/2 - BOX_HEIGHT_SIZE/2 - 200),
        (50 + BOX_WIDTH_SIZE*2 + 20, HEIGHT/2 - BOX_HEIGHT_SIZE/2 - 200),
        (50 + BOX_WIDTH_SIZE*2 - (BOX_HEIGHT_SIZE / 2) + 30, HEIGHT/2 - BOX_HEIGHT_SIZE/2 - 200 + BOX_HEIGHT_SIZE),
        (50 + BOX_WIDTH_SIZE - (BOX_HEIGHT_SIZE / 2) + 30, HEIGHT/2 - BOX_HEIGHT_SIZE/2 - 200 + BOX_HEIGHT_SIZE)
    ], "Въведи n", parallelogram_ids[0])

    parallelogram2 = Parallelogram([
        (50 + BOX_WIDTH_SIZE + 20, HEIGHT/2 - BOX_HEIGHT_SIZE/2 - 200 + 100),
        (50 + BOX_WIDTH_SIZE*2 + 20, HEIGHT/2 - BOX_HEIGHT_SIZE/2 - 200 + 100),
        (50 + BOX_WIDTH_SIZE*2 - (BOX_HEIGHT_SIZE / 2) + 30, HEIGHT/2 - BOX_HEIGHT_SIZE/2 - 200 + 100 + BOX_HEIGHT_SIZE),
        (50 + BOX_WIDTH_SIZE - (BOX_HEIGHT_SIZE / 2) + 30, HEIGHT/2 - BOX_HEIGHT_SIZE/2 - 200 + 100 + BOX_HEIGHT_SIZE)
    ], "Изведи n", parallelogram_ids[1])

    parallelogram3 = Parallelogram([
        (50 + BOX_WIDTH_SIZE + 20, HEIGHT/2 - BOX_HEIGHT_SIZE/2 - 200 + 200),
        (50 + BOX_WIDTH_SIZE*2 + 20, HEIGHT/2 - BOX_HEIGHT_SIZE/2 - 200 + 200),
        (50 + BOX_WIDTH_SIZE*2 - (BOX_HEIGHT_SIZE / 2) + 30, HEIGHT/2 - BOX_HEIGHT_SIZE/2 - 200 + 200 + BOX_HEIGHT_SIZE),
        (50 + BOX_WIDTH_SIZE - (BOX_HEIGHT_SIZE / 2) + 30, HEIGHT/2 - BOX_HEIGHT_SIZE/2 - 200 + 200 + BOX_HEIGHT_SIZE)
    ], "Изведи sum", parallelogram_ids[2])

    parallelogram_square1 = Parallelogram([
        (50, HEIGHT/2 - BOX_HEIGHT_SIZE/2 - 200),
        (50 + BOX_WIDTH_SIZE, HEIGHT/2 - BOX_HEIGHT_SIZE/2 - 200 ),
        (50 + BOX_WIDTH_SIZE, HEIGHT/2 + BOX_HEIGHT_SIZE/2 - 200),
        (50, HEIGHT/2 + BOX_HEIGHT_SIZE/2 - 200)
    ], "i++", parallelogram_ids[3])

    parallelogram_square2 = Parallelogram([
        (50, HEIGHT/2 - BOX_HEIGHT_SIZE/2 - 100),
        (50 + BOX_WIDTH_SIZE, HEIGHT/2 - BOX_HEIGHT_SIZE/2 - 100 ),
        (50 + BOX_WIDTH_SIZE, HEIGHT/2 + BOX_HEIGHT_SIZE/2 - 100),
        (50, HEIGHT/2 + BOX_HEIGHT_SIZE/2 - 100)
    ], "sum+=n", parallelogram_ids[4])

    parallelogram_square3 = Parallelogram([
        (50, HEIGHT/2 - BOX_HEIGHT_SIZE/2),
        (50 + BOX_WIDTH_SIZE, HEIGHT/2 - BOX_HEIGHT_SIZE/2),
        (50 + BOX_WIDTH_SIZE, HEIGHT/2 + BOX_HEIGHT_SIZE/2),
        (50, HEIGHT/2 + BOX_HEIGHT_SIZE/2)
    ], "sum = 0", parallelogram_ids[5])

    parallelogram_square4 = Parallelogram([
        (50, HEIGHT/2 - BOX_HEIGHT_SIZE/2 + 100),
        (50 + BOX_WIDTH_SIZE, HEIGHT/2 - BOX_HEIGHT_SIZE/2 + 100),
        (50 + BOX_WIDTH_SIZE, HEIGHT/2 + BOX_HEIGHT_SIZE/2 + 100),
        (50, HEIGHT/2 + BOX_HEIGHT_SIZE/2 + 100)
    ], "i = 1", parallelogram_ids[6])

    parallelogram_square5 = Parallelogram([
        (50, HEIGHT/2 - BOX_HEIGHT_SIZE/2 + 200),
        (50 + BOX_WIDTH_SIZE, HEIGHT/2 - BOX_HEIGHT_SIZE/2 + 200),
        (50 + BOX_WIDTH_SIZE, HEIGHT/2 + BOX_HEIGHT_SIZE/2 + 200),
        (50, HEIGHT/2 + BOX_HEIGHT_SIZE/2 + 200)
    ], "sum+=i", parallelogram_ids[7])

    shapes = [rhombus1, rhombus2, parallelogram1, parallelogram2, parallelogram3, parallelogram_square1, parallelogram_square2, parallelogram_square3, parallelogram_square4, parallelogram_square5]
    placed_ids = []
    correct_ids = [3, 8, 9, 1, 10, 6, 5]
    correct_ids1 = [8, 3, 9, 1, 10, 6, 5]
    correct_ids2 = [8, 9, 3, 1, 10, 6, 5]
    correct_ids3 = [9, 8, 3, 1, 10, 6, 5]
    correct_ids4 = [9, 3, 8, 1, 10, 6, 5]
    correct_ids5 = [3, 9, 8, 1, 10, 6, 5]

    BUTTON_WIDTH = 120
    BUTTON_HEIGHT = 50
    BUTTON_COLOR = (0, 255, 0)
    BUTTON_TEXT_COLOR = (255, 255, 255)
    BUTTON_TEXT = "Check"
    BUTTON_FONT = pygame.font.SysFont("Arial", 20)
    BUTTON_POSITION = (WIDTH - BUTTON_WIDTH - 20, HEIGHT - BUTTON_HEIGHT - 20)

    def draw_button():
        # Draw check button
        pygame.draw.ellipse(WIN, "grey", (BUTTON_POSITION[0], BUTTON_POSITION[1], BUTTON_WIDTH, BUTTON_HEIGHT))
        text_surface = BUTTON_FONT.render(BUTTON_TEXT, True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(BUTTON_POSITION[0] + BUTTON_WIDTH/2, BUTTON_POSITION[1] + BUTTON_HEIGHT/2))
        WIN.blit(text_surface, text_rect)

    def restart_game():
        global placed_ids
        placed_ids = []
        main()

    def create_window(message, restart = True):
        window = tk.Tk()
        window.title("Message Window")

        window_width = 400
        window_height = 200
        
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        label = tk.Label(window, text=message, font=("Arial", 24))
        label.pack()
        
        window.mainloop()

    def check_button_click(pos): 
        global run  
        if BUTTON_POSITION[0] <= pos[0] <= BUTTON_POSITION[0] + BUTTON_WIDTH and \
          BUTTON_POSITION[1] <= pos[1] <= BUTTON_POSITION[1] + BUTTON_HEIGHT:
              for i in range(0, len(correct_ids)):
                  if placed_ids[i] != correct_ids[i]:
                      create_window("You lost!")
                      all()
                      run = False
                      return False
              create_window("You win!")
              all()
              run = False
              return False
              
        elif BUTTON_POSITION[0] - BUTTON_WIDTH - 10 <= pos[0] <= BUTTON_POSITION[0] - 10 and \
            BUTTON_POSITION[1] <= pos[1] <= BUTTON_POSITION[1] + BUTTON_HEIGHT:
                restart_game()
                

    def draw():
        WIN.blit(BG, (0, 0))
        for place_x, place_y in places:
            pygame.draw.circle(WIN, "white", (int(place_x + BOX_WIDTH_SIZE / 2), int(place_y + BOX_HEIGHT_SIZE / 2)), 15)  # Adjust radius as needed

        pygame.draw.ellipse(WIN, WHITE, (WIDTH/2 - OVAL_WIDTH/2, HEIGHT/2 - BOX_HEIGHT_SIZE/2 - 200, OVAL_WIDTH, OVAL_HEIGHT))
        text_surface = FONT.render(TEXT, True, BLACK)
        text_rect = text_surface.get_rect(center=(WIDTH/2, HEIGHT/2 - BOX_HEIGHT_SIZE/2 - 200 + OVAL_HEIGHT//2))
        WIN.blit(text_surface, text_rect)
        
        pygame.draw.ellipse(WIN, WHITE, (WIDTH/2 - BOX_WIDTH_SIZE/2 + 300, HEIGHT/2 - BOX_HEIGHT_SIZE/2 + 65, OVAL_WIDTH, OVAL_HEIGHT))
        text_surface_1 = FONT.render(TEXT_1, True, BLACK)
        text_rect_1 = text_surface_1.get_rect(center=(WIDTH/2 - BOX_WIDTH_SIZE/2 + 360, HEIGHT/2 - BOX_HEIGHT_SIZE/2 + 55 + OVAL_HEIGHT//2 + 10))
        WIN.blit(text_surface_1, text_rect_1)
        
        text_task = FONT1.render(TEXT_2, True, BLACK)
        text_rect_2 = text_task.get_rect(center = (WIDTH/2 + 300, HEIGHT/2 - 230))
        WIN.blit(text_task, text_rect_2)
        
        rhombus1.draw()
        rhombus2.draw()
        parallelogram1.draw()
        parallelogram2.draw()
        parallelogram3.draw()
        parallelogram_square2.draw()
        parallelogram_square1.draw()
        parallelogram_square3.draw()
        parallelogram_square4.draw()
        parallelogram_square5.draw()
        
        draw_button()

        pygame.display.update()

    def main():
        run = True
        clock = pygame.time.Clock()

        active_item = None 
        
        mouse_click_pos = None

        while run == True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False 

                rhombus1.handle_event(event)
                rhombus2.handle_event(event)
                parallelogram1.handle_event(event)
                parallelogram2.handle_event(event)
                parallelogram3.handle_event(event)
                parallelogram_square1.handle_event(event)
                parallelogram_square2.handle_event(event)
                parallelogram_square3.handle_event(event)
                parallelogram_square4.handle_event(event)
                parallelogram_square5.handle_event(event)
                

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and active_item:
                        for place in places:
                            if active_item.collidepoint(place):
                                active_item.move_to_place(place)
                                placed_ids.append(active_item.id)
                                break
                        active_item = None
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_click_pos = event.pos
                        check_button_click(mouse_click_pos)
                        for box in shapes:
                            if box.collidepoint(event.pos):
                                active_item = box
                                break
    

            draw()

        pygame.quit()
        sys.exit()
        main()

    if __name__ == "__main__":
        main()
        
corr = 0
        
def level2():

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

        questions = [
            ("What keyword exits a loop?", "break"),
            ("What operator checks equality?", "=="),
            ("What is the output of 3 // 2?", "1"),
            ("What function returns the length?", "len"),
            ("What is the value of None?", "null"),
            ("What method removes dictionary keys?", "pop"),
            ("What symbol starts a comment?", "#"),
            ("What keyword starts a loop?", "for"),
            ("What method adds an item to a list?", "append"),
            ("What data type is True?", "bool"),
            ("What keyword defines a function?", "def"),
            ("What function converts to string?", "str"),
            ("What method converts all characters in a string to uppercase?", "upper"),
            ("What function returns the maximum value?", "max"),
            ("What keyword is used for logical OR?", "or")
        ]

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

        def show_question(tile_group):
            global corr
            root = tk.Tk()
            root.withdraw()
            while True:
                question, answer = random.choice(questions)
                user_answer = simpledialog.askstring("Question", question)
                if user_answer is not None and user_answer.lower() == answer.lower():
                    messagebox.showinfo("Correct", "Correct answer!")
                    corr += 1
                    root.destroy()
                    if corr == 5:
                        end_game()
                    return True
                else:
                    messagebox.showinfo("Incorrect", "Incorrect answer. The correct answer is " + answer + ".")
                    tile_group.visited = False

        def end_game():
            END_GAME_IMAGE = pygame.image.load(os.path.join('level4_png', 'endscreen_bg.png'))
            END_GAME = pygame.transform.scale(END_GAME_IMAGE, (WIDTH, HEIGHT))
            start_time = pygame.time.get_ticks()
            while pygame.time.get_ticks() < start_time + 5000:
                screen.blit(END_GAME, (0, 0))
                pygame.display.update()
            all()
            pygame.quit()
            sys.exit()

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



def level3():
    
    WIDTH = 1000
    HEIGHT = 512 

    COMP_WIDTH = 40
    COMP_HEIGHT = 30

    BUTTON_WIDTH = 150
    BUTTON_HEIGHT = 50

    FONT = pygame.font.SysFont("comicsans", 30)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("Labyrinth game")

    BG_IMAGE = pygame.image.load(os.path.join('level4_png', 'backround.png'))
    BG = pygame.transform.scale(BG_IMAGE, (WIDTH, HEIGHT)) 

    FLOOR_IMAGE = pygame.image.load(os.path.join('level4_png', 'maze.png'))


    MID_GAME_IMAGE = pygame.image.load(os.path.join('level4_png', 'mid_game.png'))
    MID_GAME = pygame.transform.scale(MID_GAME_IMAGE, (WIDTH, HEIGHT))


    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() < start_time+15000:
        screen.blit(MID_GAME, (0,0))
        pygame.display.update()

    PLAYER_IMAGE = pygame.image.load(os.path.join('level4_png', 'character.png'))

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    GRAY = (39, 42, 46)

    MAZE_MAP = [

    "+++++++++++++++++++++++++++++++++++++++++++++",
    "+         +    +                +           +",
    "+ +++  ++++  + + +++++++++  +++ + +++++++++ +",
    "+   +        +   +            + +         + +",
    "+++ +++++  +++ +   +++++++++  + + +++++++++ +",
    "+ + +   +    + +   +   +      + + +   +     +",
    "+ + +   ++++++ +++ +   +  ++  + + +   +  ++ +",
    "+ + +   +        + +   +  +   +   +   +   + +",
    "+ + +++ +  +++ + + +++ +  +++ + + +++ +++ + +",
    "+   + + +  +   + + + + +    + + +     +   + +",
    "+ +++ + +  +++ + + + + +++  + + + +++++  ++ +",
    "+ +   + +    + +     +      +   +   +     + +",
    "+ +++ + +++  + + +++++ ++++++   +++ +++++ + +",
    "+     +      + +              +   +       + +",
    "+ +++++++  +++++ ++++++++++++ +++++++ +++++ +",
    "+ +   +                  +            +   + +",
    "+ +   +                  +            +   + +",
    "+ + +   +  + +++ +++++ +   +  + + +++   + + +",
    "+ + +   +  + + + +     +   +  + +   +   + + +",
    "+   +++++  +++ +++ +++++++++  + + + +++++ + +",
    "+   +   +  + + +   +     +    + + + +   + + +",
    "+++++   +  + + + +++     +  +++ +++ +   + + +",
    "+   +   +  +   +   +     +  + +     +   +   +",
    "+ + +++ +  + + +++ +     +  + + + +++++ +++ +",
    "+ +   + +  + + +   +     +  + + +   +   + + +",
    "+ +++ + +  + + +++++++ +++  + + +++ + +++ + +",
    "+   +   +  + + +     + + +    + +   + +   + +",
    "+++ ++++++++ + + +++ + +  ++  + + +++ +   + +",
    "+            +     +   +        +     + +   +",
    "+ ++++++++++ +++ +++++++++++  +++++++ + +++++",
    "+ +            +              +             +",
    "+ + ++++++++++ +++++++ ++++++++ +++++++++ + +",
    "+ +     +    +   +              +         + +",
    "+ + +++++  + + + + +++ ++++++++++ +++++++++ +",
    "+   +   +  +   + +   +        +   +   +   + +",
    "+   +   +  +   + +   +        +   +   +   + +",
    "+ +++   +  +++ + + +++++++++  + +++   + + + +",
    "+   +   +    + + + +   +          +   + +   +",
    "+ +++++ ++++ + + + +   +  ++  +++ +++ +++  ++",
    "+ +     +    + +   +   +   +  +     +       +",
    "+++ +++++  +++ +++++++ +++ +  + +++++++++++ +",
    "+   +        +         +   +  +           + +",
    "+ +++++++  + + + +++++++  ++  + +++++++++ + +",
    "+          +   +          +   +         +   +",
    "+++++++++++++++++++++++++++++++++++++++++++++"
    ]

    CELL_SIZE = min(WIDTH // len(MAZE_MAP[0]), HEIGHT // len(MAZE_MAP))

    PLAYER = pygame.transform.scale(PLAYER_IMAGE, (CELL_SIZE, CELL_SIZE))

    MAZE_WIDTH = len(MAZE_MAP[0]) * CELL_SIZE
    MAZE_HEIGHT = len(MAZE_MAP) * CELL_SIZE

    FLOOR = pygame.transform.scale(FLOOR_IMAGE, (MAZE_WIDTH, MAZE_HEIGHT))

    MAZE_X = (WIDTH - MAZE_WIDTH) // 2
    MAZE_Y = (HEIGHT - MAZE_HEIGHT) // 2

    def main():

        comp = pygame.Rect( WIDTH//2 - COMP_WIDTH//2, HEIGHT//2 - COMP_HEIGHT//2, COMP_WIDTH, COMP_HEIGHT)

        player_pos = None
        for y, row in enumerate(MAZE_MAP):
            for x, cell in enumerate(row):
                if cell == " ":
                    player_pos = (MAZE_X + x * CELL_SIZE, MAZE_Y + y * CELL_SIZE)
                    break
            if player_pos:
                break

        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(40)
            screen.blit(BG, (0, 0))
            screen.blit(FLOOR, (MAZE_X, MAZE_Y))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            
            for y, row in enumerate(MAZE_MAP):
                for x, cell in enumerate(row):
                    if cell == "+":
                        pygame.draw.rect(screen, WHITE, (MAZE_X + x * CELL_SIZE, MAZE_Y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

            
            ddz = pygame.Rect(player_pos[0], player_pos[1], CELL_SIZE, CELL_SIZE)
            screen.blit(PLAYER, (ddz.x,ddz.y))

            player_rect = pygame.Rect(player_pos[0], player_pos[1], CELL_SIZE, CELL_SIZE)
            comp_rect = pygame.Rect(comp.x, comp.y, COMP_WIDTH, COMP_HEIGHT)
            
            screen.blit(PLAYER, (player_rect.x, player_rect.y))

            if player_rect.colliderect(comp_rect):
                END_GAME_IMAGE = pygame.image.load(os.path.join('level4_png', 'endscreen_bg.png'))
                END_GAME = pygame.transform.scale(END_GAME_IMAGE, (WIDTH, HEIGHT))
                start_time = pygame.time.get_ticks()
                while pygame.time.get_ticks() < start_time+5000:
                    screen.blit(END_GAME, (0,0))
                    pygame.display.update()
                
                all()    

                pygame.quit()
                sys.exit()


            pygame.display.update()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                if MAZE_MAP[int((player_pos[1] - MAZE_Y) // CELL_SIZE)][int((player_pos[0] - MAZE_X - CELL_SIZE) // CELL_SIZE)] == " ":
                    player_pos = (player_pos[0] - CELL_SIZE, player_pos[1])
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                if MAZE_MAP[int((player_pos[1] - MAZE_Y) // CELL_SIZE)][int((player_pos[0] - MAZE_X + CELL_SIZE) // CELL_SIZE)] == " ":
                    player_pos = (player_pos[0] + CELL_SIZE, player_pos[1])
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                if MAZE_MAP[int((player_pos[1] - MAZE_Y - CELL_SIZE) // CELL_SIZE)][int((player_pos[0] - MAZE_X) // CELL_SIZE)] == " ":
                    player_pos = (player_pos[0], player_pos[1] - CELL_SIZE)
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                if MAZE_MAP[int((player_pos[1] - MAZE_Y + CELL_SIZE) // CELL_SIZE)][int((player_pos[0] - MAZE_X) // CELL_SIZE)] == " ":
                    player_pos = (player_pos[0], player_pos[1] + CELL_SIZE)


        pygame.quit()
        sys.exit()

    main()


screen_width = 1000
screen_height = 512
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Menu")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
background_image = pygame.image.load(os.path.join("level1_png", "back.jpg")).convert()

font = pygame.font.Font(None, 36)

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def main_menu():
    while True:
        screen.blit(background_image, (0, 0))
        
        play_button_radius = 25
        play_button = pygame.Rect(screen_width//2 - 50, screen_height//2 + 70, 100, 50)
        pygame.draw.rect(screen, WHITE, play_button, play_button_radius)
        draw_text("Play", font, BLACK, screen_width//2, screen_height//2 + 95)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_button.collidepoint(mouse_pos):
                    level = level_select()
                    if level:
                        return level

def level_select():
    while True:
        screen.blit(background_image, (0, 0))
        
        button_width = 200
        button_height = 50
        button_spacing = 50
        
        level1_button = pygame.Rect(screen_width//2 - 350, screen_height//2 + 70, button_width, button_height)
        pygame.draw.rect(screen, WHITE, level1_button)
        draw_text("Level 1", font, BLACK, screen_width//2 - 250, screen_height//2 + 2 * button_spacing - 5)
        
        level2_button = pygame.Rect(screen_width//2 - 100, screen_height//2 + 70, button_width, button_height)
        pygame.draw.rect(screen, WHITE, level2_button)
        draw_text("Level 2", font, BLACK, screen_width//2, screen_height//2 + 2 * button_spacing - 5)
        
        level3_button = pygame.Rect(screen_width//2 + 150, screen_height//2 + 70, button_width, button_height)
        pygame.draw.rect(screen, WHITE, level3_button)
        draw_text("Level 3", font, BLACK, screen_width//2 + 250, screen_height//2 + 2 * button_spacing - 5)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if level1_button.collidepoint(mouse_pos):
                    return 1
                elif level2_button.collidepoint(mouse_pos):
                    return 2
                elif level3_button.collidepoint(mouse_pos):
                    return 3

def main():
    
    WIDTH = 1000
    HEIGHT = 512
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("Dialog")

    DIALOG_1_IMAGE = pygame.image.load(os.path.join('dialog_png', 'dialog_1.png'))
    DIALOG_1 = pygame.transform.scale(DIALOG_1_IMAGE, (WIDTH, HEIGHT))

    DIALOG_2_IMAGE = pygame.image.load(os.path.join('dialog_png', 'dialog_2.png'))
    DIALOG_2 = pygame.transform.scale(DIALOG_2_IMAGE, (WIDTH, HEIGHT))

    DIALOG_3_IMAGE = pygame.image.load(os.path.join('dialog_png', 'dialog_3.png'))
    DIALOG_3 = pygame.transform.scale(DIALOG_3_IMAGE, (WIDTH, HEIGHT))

    DIALOG_4_IMAGE = pygame.image.load(os.path.join('dialog_png', 'dialog_4.png'))
    DIALOG_4 = pygame.transform.scale(DIALOG_4_IMAGE, (WIDTH, HEIGHT))

    DIALOG_5_IMAGE = pygame.image.load(os.path.join('dialog_png', 'dialog_5.png'))
    DIALOG_5 = pygame.transform.scale(DIALOG_5_IMAGE, (WIDTH, HEIGHT))

    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() < start_time+5000:
        screen.blit(DIALOG_1, (0,0))
        pygame.display.update()

    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() < start_time+5000:
        screen.blit(DIALOG_2, (0,0))
        pygame.display.update()

    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() < start_time+5000:
        screen.blit(DIALOG_3, (0,0))
        pygame.display.update()

    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() < start_time+5000:
        screen.blit(DIALOG_4, (0,0))
        pygame.display.update()

    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() < start_time+5000:
        screen.blit(DIALOG_5, (0,0))
        pygame.display.update()

    selected_level = main_menu()
    if selected_level == 1:
        level1()
    if selected_level == 2:
        level2()
    else:
        level3()
        
def main_1():
  
    selected_level = main_menu()
    if selected_level == 1:
        level1()
    if selected_level == 2:
        level2()
    else:
        level3()
        
def all():
    main_1()

if __name__ == "__main__":
    main()
