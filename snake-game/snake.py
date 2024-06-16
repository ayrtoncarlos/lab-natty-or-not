import pygame
import random
from pathlib import Path


# Inicializa o pygame
pygame.init()

# Configurações da tela
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jogo da Cobrinha")

# Cores
green = pygame.Color(0, 255, 0)
black = pygame.Color(0, 0, 0)
red = pygame.Color(255, 0, 0)

# Clock
clock = pygame.time.Clock()

# Fontes
font = pygame.font.SysFont('Arial', 25)

# Função para mostrar o texto na tela
def show_text(text, color, x, y):
    display_text = font.render(text, True, color)
    screen.blit(display_text, [x, y])

# Função para o menu principal
def main_menu():
    menu = True
    while menu:
        screen.fill(green)
        show_text("Jogo da Cobrinha", black, 220, 150)
        show_text("Pressione Enter para jogar", black, 180, 200)
        show_text("Pressione ESC para sair", black, 180, 250)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

# Função principal do jogo
def game():
    game_over = False
    game_close = False

    x1 = screen_width / 2
    y1 = screen_height / 2

    x1_change = 0
    y1_change = 0

    snake_block = 10
    snake_speed = 15

    snake_list = []
    length_of_snake = 1

    # Carregar imagem de comida
    food_img = pygame.image.load(f"{Path(__file__).parent}/images/image.png")
    food_img = pygame.transform.scale(food_img, (snake_block, snake_block))

    foodx = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0

    while not game_over:
        while game_close == True:
            screen.fill(green)
            show_text("Você perdeu! Pressione Q-Quit ou C-Play Again", red, 100, 150)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        screen.fill(green)
        screen.blit(food_img, (foodx, foody))

        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        for x in snake_list:
            pygame.draw.rect(screen, black, [x[0], x[1], snake_block, snake_block])

        show_text("Pontuação: " + str(length_of_snake - 1), black, 0, 0)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0
            length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Executa o menu principal
main_menu()
# Inicia o jogo
game()
