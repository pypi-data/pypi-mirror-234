import pygame
import os
import random
import time

# Set up the game
pygame.init()
pygame.font.init()
os.environ["SDL_VIDEO_CENTERED"] = "1"

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WINDOW_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 32

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("2-Back Game")
clock = pygame.time.Clock()

# Key mappings
KEY_MAPPING = {
    pygame.K_j: "j",
    pygame.K_f: "f"
}

# Generate sequence
def generate_sequence(length):
    return [random.choice(["1","2","3","4","5","6","7","8","9"]) for _ in range(length)]

def draw_text(text, position, color):
    font = pygame.font.Font(None, FONT_SIZE)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, text_rect)

def incorrect():
    draw_text("Incorrect!", (SCREEN_WIDTH // 2, FONT_SIZE * 2), BLACK)
    pygame.display.update()
    pygame.time.wait(1000)

def correct():
    draw_text("Correct!", (SCREEN_WIDTH // 2, FONT_SIZE * 2), BLACK)
    pygame.display.update()
    pygame.time.wait(1000)

def play_game():
    sequence_length = 12
    sequence = generate_sequence(sequence_length)
    print(sequence)
    current_index = 2
    score = 0
    running = True

    while running:
        screen.fill(WHITE)
        draw_text("2-Back Game", (SCREEN_WIDTH // 2, FONT_SIZE), BLACK)
        draw_text(f'{sequence[current_index]}', (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), BLACK)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in KEY_MAPPING:
                    if sequence[current_index] == sequence[current_index - 2]:
                        if KEY_MAPPING[event.key] == sequence[current_index]:
                            correct()
                            score += 1
                        else:
                            incorrect()
                    else:
                        if KEY_MAPPING[event.key] == sequence[current_index]:
                            incorrect()
                        else:
                            correct()
                            score += 1

                    current_index += 1

                    if current_index >= sequence_length:
                        running = False

        clock.tick(60)

    return score

def introduction():
    screen.fill(WHITE)
    draw_text("Welcome to the 2-Back Game", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), BLACK)
    pygame.display.update()
    pygame.time.wait(2000)

    score = play_game()

    screen.fill(WHITE)
    draw_text("Game Over", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - FONT_SIZE), BLACK)
    draw_text(f"Your score: {score}", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + FONT_SIZE), BLACK)
    pygame.display.update()
    pygame.time.wait(2000)

introduction()
pygame.quit()
