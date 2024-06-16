import pygame
import random
import sys
import time
import os
from pathlib import Path


# Inicialização do Pygame
pygame.init()

# Constantes
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 4
TILE_SIZE = WIDTH // GRID_SIZE
MARGIN = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
FPS = 30
MAX_ATTEMPTS = 10

# Caminho da pasta de imagens
IMAGE_DIR = f"{Path(__file__).parent}/images"

# Carregar imagens
def load_images():
    if not os.path.exists(IMAGE_DIR):
        raise FileNotFoundError(f"A pasta '{IMAGE_DIR}' não foi encontrada.")
    
    images = []
    image_files = [f for f in os.listdir(IMAGE_DIR) if os.path.isfile(os.path.join(IMAGE_DIR, f))]
    random.shuffle(image_files)
    
    # Garantir que há imagens suficientes para o jogo
    num_images_needed = (GRID_SIZE ** 2) // 2
    if len(image_files) < num_images_needed:
        raise ValueError(f"Não há imagens suficientes na pasta '{IMAGE_DIR}' para o número de pares necessários. É necessário pelo menos {num_images_needed} imagens.")
    
    for i in range(num_images_needed):
        image_path = os.path.join(IMAGE_DIR, image_files[i])
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (TILE_SIZE - 2 * MARGIN, TILE_SIZE - 2 * MARGIN))
        images.append(image)
    
    images *= 2  # Criar pares
    random.shuffle(images)
    return images

# Configuração da janela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo da Memória")

# Funções de desenho
def draw_tile(screen, image, x, y):
    rect = pygame.Rect(x, y, TILE_SIZE - 2 * MARGIN, TILE_SIZE - 2 * MARGIN)
    screen.blit(image, rect)

def draw_board(screen, board, revealed):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x = j * TILE_SIZE + MARGIN
            y = i * TILE_SIZE + MARGIN
            if revealed[i][j]:
                draw_tile(screen, board[i][j], x, y)
            else:
                pygame.draw.rect(screen, BLUE, (x, y, TILE_SIZE - 2 * MARGIN, TILE_SIZE - 2 * MARGIN))

def draw_info(screen, attempts, start_time):
    font = pygame.font.Font(None, 36)
    attempts_text = font.render(f"Tentativas restantes: {attempts}", True, WHITE)
    time_elapsed = time.time() - start_time
    time_text = font.render(f"Tempo: {int(time_elapsed)}s", True, WHITE)
    
    screen.blit(attempts_text, (10, 10))
    screen.blit(time_text, (10, 50))

# Menu inicial
def main_menu():
    font = pygame.font.Font(None, 74)
    title_text = font.render("Jogo da Memória", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

    font_small = pygame.font.Font(None, 36)
    instruction_text = font_small.render("Pressione ENTER para iniciar", True, WHITE)
    instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    
    while True:
        screen.fill(BLACK)
        screen.blit(title_text, title_rect)
        screen.blit(instruction_text, instruction_rect)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

# Loop principal do jogo
def game_loop():
    board = [[None] * GRID_SIZE for _ in range(GRID_SIZE)]
    revealed = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]
    images = load_images()
    idx = 0
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            board[i][j] = images[idx]
            idx += 1

    first_selection = None
    attempts = MAX_ATTEMPTS
    matches = 0
    start_time = time.time()

    running = True
    while running:
        screen.fill(BLACK)
        draw_board(screen, board, revealed)
        draw_info(screen, attempts, start_time)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    row = y // TILE_SIZE
                    col = x // TILE_SIZE
                    if not revealed[row][col]:
                        revealed[row][col] = True
                        if first_selection is None:
                            first_selection = (row, col)
                        else:
                            r1, c1 = first_selection
                            r2, c2 = row, col
                            if board[r1][c1] != board[r2][c2]:
                                attempts -= 1
                                pygame.time.wait(1000)
                                revealed[r1][c1] = False
                                revealed[r2][c2] = False
                            else:
                                matches += 1
                            first_selection = None

                            # Verificar vitória após uma tentativa bem-sucedida
                            if matches == (GRID_SIZE * GRID_SIZE) // 2:
                                running = False
                                break
        
        if attempts <= 0:
            running = False

    elapsed_time = time.time() - start_time
    show_game_over_screen(matches == (GRID_SIZE * GRID_SIZE) // 2, elapsed_time)

def show_game_over_screen(won, elapsed_time):
    font = pygame.font.Font(None, 74)
    if won:
        text = font.render(f"Você venceu! Tempo: {elapsed_time:.2f}s", True, WHITE)
    else:
        text = font.render("Você perdeu!", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    
    while True:
        screen.fill(BLACK)
        screen.blit(text, text_rect)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

# Loop principal
while True:
    main_menu()
    game_loop()
