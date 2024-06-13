import pygame
import random
import os

pygame.init()

WIDTH = 1000
HEIGHT = 512
CARD_WIDTH, CARD_HEIGHT = 100, 150
MARGIN = 10
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Card Game")

BACKGROUND_1 = pygame.image.load(os.path.join('cards_pics', 'background_1.png'))
BACK = pygame.transform.scale(BACKGROUND_1, (WIDTH, HEIGHT))
start_time = pygame.time.get_ticks()
while pygame.time.get_ticks() < start_time + 5000:
    screen.blit(BACK, (0, 0))
    pygame.display.update()

background_image = pygame.image.load(os.path.join('cards_pics', 'background_2.png'))
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
screen.blit(background_image, (0, 0))
pygame.display.update()

PAIRS = [
    ('back_card_1.png', 'Рутер'),
    ('back_card_2.png', 'Диод'),
    ('back_card_3.png', 'Светодиод'),
    ('back_card_4.png', 'Ценеров диод'),
    ('back_card_5.png', 'Схема диод'),
    ('back_card_6.png', 'Транзистор'),
    ('back_card_7.png', 'Switch'),
    ('back_card_8.png', 'Схема рутер')
]

card_back_image = pygame.image.load(os.path.join('cards_pics', 'card_front.png'))
card_back_image = pygame.transform.scale(card_back_image, (CARD_WIDTH, CARD_HEIGHT))

image_cards = []
text_cards = []
for image_file, text in PAIRS:
    image = pygame.image.load(os.path.join('cards_pics', image_file))
    image = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
    image_cards.append((image, text))
    text_cards.append((None, text))

cards = []
for (image, text), (_, text_only) in zip(image_cards, text_cards):
    cards.append((image, text, True))
    cards.append((None, text_only, False))

random.shuffle(cards)

class Card:
    def __init__(self, x, y, image, text, is_image_card):
        self.rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        self.image = image
        self.text = text
        self.is_image_card = is_image_card
        self.flipped = False
        self.matched = False

    def draw(self):
        if self.flipped or self.matched:
            if self.is_image_card and self.image:
                screen.blit(self.image, self.rect.topleft)
            else:
                pygame.draw.rect(screen, WHITE, self.rect)
                font = pygame.font.Font(None, 18)
                text_surf = font.render(self.text, True, BLACK)
                screen.blit(text_surf, text_surf.get_rect(center=self.rect.center))
        else:
            screen.blit(card_back_image, self.rect.topleft)

grid_width = 8 * (CARD_WIDTH + MARGIN) - MARGIN
grid_height = 2 * (CARD_HEIGHT + MARGIN) - MARGIN
start_x = (WIDTH - grid_width) // 2
start_y = (HEIGHT - grid_height) // 2 + 50

card_objects = []
for i in range(2):
    for j in range(8):
        x = start_x + j * (CARD_WIDTH + MARGIN)
        y = start_y + i * (CARD_HEIGHT + MARGIN)
        image, text, is_image_card = cards.pop()
        card_objects.append(Card(x, y, image, text, is_image_card))

first_card = None
second_card = None
running = True
clock = pygame.time.Clock()
waiting = False
wait_start_time = 0
current_player = 1
scores = {1: 0, 2: 0}

def draw_cards():
    screen.blit(background_image, (0, 0))
    for card in card_objects:
        card.draw()
    draw_scores()
    pygame.display.flip()

def draw_scores():
    font = pygame.font.Font(None, 36)
    score_text = f"Player 1: {scores[1]}  |  Player 2: {scores[2]}"
    text = font.render(score_text, True, WHITE)
    screen.blit(text, (20, 20))

def check_winner():
    total_matches = sum(card.matched for card in card_objects)
    if total_matches == len(card_objects):
        font = pygame.font.Font(None, 74)
        if scores[1] > scores[2]:
            BACKGROUND_4 = pygame.image.load(os.path.join('cards_pics', 'wins1.png'))
            BACK4 = pygame.transform.scale(BACKGROUND_4, (WIDTH, HEIGHT))
            start_time = pygame.time.get_ticks()
            while pygame.time.get_ticks() < start_time + 5000:
                screen.blit(BACK4, (0, 0))
                pygame.display.update()
        elif scores[1] < scores[2]:
            BACKGROUND_5 = pygame.image.load(os.path.join('cards_pics', 'wins2.png'))
            BACK5 = pygame.transform.scale(BACKGROUND_5, (WIDTH, HEIGHT))
            start_time = pygame.time.get_ticks()
            while pygame.time.get_ticks() < start_time + 5000:
                screen.blit(BACK5, (0, 0))
                pygame.display.update()
        else:
            BACKGROUND_6 = pygame.image.load(os.path.join('cards_pics', 'tie.png'))
            BACK6 = pygame.transform.scale(BACKGROUND_6, (WIDTH, HEIGHT))
            start_time = pygame.time.get_ticks()
            while pygame.time.get_ticks() < start_time + 5000:
                screen.blit(BACK6, (0, 0))
                pygame.display.update()
        return True
    return False

while running:
    draw_cards()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not waiting:
            pos = pygame.mouse.get_pos()
            for card in card_objects:
                if card.rect.collidepoint(pos) and not card.flipped and not card.matched:
                    card.flipped = True
                    if not first_card:
                        first_card = card
                    elif not second_card:
                        second_card = card
                        draw_cards()
                        pygame.time.wait(1000)
                        if first_card.text == second_card.text:
                            first_card.matched = True
                            second_card.matched = True
                            scores[current_player] += 1
                        else:
                            first_card.flipped = False
                            second_card.flipped = False
                            current_player = 2 if current_player == 1 else 1
                        first_card = None
                        second_card = None
                        if check_winner():
                            running = False

    clock.tick(FPS)

pygame.quit()
