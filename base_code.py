import pygame
import random
pygame.init()

WIDTH = 800
HEIGHT = 600

rows = 4
columns = 8
CARD_WIDTH = 75
CARD_HEIGHT = 100

correct_list = [[0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]

options_list = []
spaces_list = []
used_cards = []

game_over = False

first_guess = False
second_guess = False
first_guess_num = 0
second_guess_num = 0

score = 0
best_score = 0
matches = 0

new_board = True

white = (255, 255, 255)
black = (0, 0, 0)
grey = (128, 128, 128)
green = (0, 255, 0)
blue = (0, 0, 255)

speed = 60
clock = pygame.time.Clock()

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("MultyPlayer Memmory Card Game")
title_font = pygame.font.Font('freesansbold.ttf', 30)
card_font = pygame.font.Font('freesansbold.ttf', 40)
small_font = pygame.font.Font('freesansbold.ttf', 18)

def generate_board():
    global options_list
    global spaces_list
    global used_cards
    
    for item in range(rows * columns // 2):
        options_list.append(item)
        
    for item in range(rows * columns):
        card = options_list[random.randint(0, len(options_list)-1)]
        spaces_list.append(card)
        if card in used_cards:
            used_cards.remove(card)
            options_list.remove(card)
        else:
            used_cards.append(card)

def draw_menus():
    top_menu = pygame.draw.rect(screen, black, [0, 0, WIDTH, 50])
    board_space = pygame.draw.rect(screen, grey, [0, 50, WIDTH, HEIGHT - 50])
    title_text = title_font.render("Memmory Game!", True, white)
    screen.blit(title_text, (275, 13))
    restart_button = pygame.draw.rect(screen, black, [635, HEIGHT - 35, 120, 30], 0, 5)
    restart_button_text = title_font.render("Restart", True, white)
    screen.blit(restart_button_text, (640, HEIGHT - 32))
    score_text = small_font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (50, HEIGHT - 35))
    best_text = small_font.render(f"Previous Best: {best_score}", True, white)
    screen.blit(best_text, (50, HEIGHT - 17))
    
    return restart_button
    
def draw_cards():
    global rows 
    global columns
    global correct_list
    
    card_list = []
    for i in range(columns):
        for j in range(rows):
            card = pygame.draw.rect(screen, white, [i * 90 + 50, j * 120 + 100, CARD_WIDTH, CARD_HEIGHT], 0, 4)
            card_list.append(card)
            '''place_text = card_font.render(f"{spaces_list[i * rows + j]}", True, black)
            screen.blit(place_text, (i * 90 + 63, j * 120 + 130))'''
            
    for r in range(rows):
        for c in range(columns):
            if correct_list[r][c] == 1:
                pygame.draw.rect(screen, green, [c * 90 + 50, r * 120 + 100, CARD_WIDTH, CARD_HEIGHT], 3, 4)
                card_list.append(card)
                place_text = card_font.render(f"{spaces_list[c * rows + r]}", True, black)
                screen.blit(place_text, (c * 90 + 63, r * 120 + 130))
                
            
    return card_list

def check_guesses(first, second):
    global spaces_list
    global correct_list
    global score
    global matches
    
    if spaces_list[first] == spaces_list[second]:
        col1 = first // rows
        col2 = second // rows
        row1 = first - (first // rows * rows)
        row2 = second - (second // rows * rows)
        if correct_list[row1][col1] == 0 and correct_list[row2][col2] == 0:
            correct_list[row1][col1] = 1
            correct_list[row2][col2] = 1
            score += 1
            matches += 1
    else:
        score += 1

run = True

while run:
    
    clock.tick(speed)
    screen.fill(white)
    
    if new_board:
        generate_board()
        print(spaces_list)
        new_board = False
    
    restart = draw_menus()
    board = draw_cards()
    
    if first_guess and second_guess:
        check_guesses(first_guess_num, second_guess_num)
        pygame.time.delay(600)
        first_guess = False
        second_guess = False
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(board)):
                button = board[i]
                if not game_over:
                    if button.collidepoint(event.pos) and not first_guess:
                        first_guess = True
                        first_guess_num = i
                    if button.collidepoint(event.pos) and not second_guess and first_guess and i != first_guess_num:
                        second_guess = True
                        second_guess_num = i

            if restart.collidepoint(event.pos):
                score = 0
                matches = 0
                options_list = []
                used_cards = []
                spaces_list = []
                new_board = True
                correct_list = [[0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0]]
                first_guess = False
                second_guess = False
                game_over = False
                
    if matches == rows * columns // 2:
        game_over = True
        winner = pygame.draw.rect(screen, grey, [0, 50, WIDTH, HEIGHT - 50])
        winner_text = card_font.render(f"You won in {score} moves!", True, white)
        screen.blit(winner_text, (WIDTH / 2 - 200, (HEIGHT - 50) / 2 - 35))
        if best_score > score or best_score == 0:
            best_score = score      
                    
    if first_guess:
        place_text = card_font.render(f"{spaces_list[first_guess_num]}", True, blue)
        location = (first_guess_num // rows * 90 + 63, (first_guess_num - (first_guess_num // rows * rows)) * 120 + 130)
        screen.blit(place_text, (location))
        
    if second_guess:
        place_text = card_font.render(f"{spaces_list[second_guess_num]}", True, blue)
        location = (second_guess_num // rows * 90 + 63, (second_guess_num - (second_guess_num // rows * rows)) * 120 + 130)
        screen.blit(place_text, (location))                
            
    pygame.display.flip()
    
pygame.quit()        