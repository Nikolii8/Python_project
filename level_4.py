import pygame
import sys
import os
from io import StringIO
pygame.init()

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