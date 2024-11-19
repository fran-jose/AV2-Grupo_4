import pygame
import matplotlib.pyplot as plt
from pp_model import GameOfLifeModel


def run_GameOfLifeModel(
    width,
    height,
    cell_size,
    initial_config=None,
    colors={"empty": (0, 0, 0), "prey": (0, 255, 0), "predator": (255, 0, 0)},
):
    pygame.init()
    screen = pygame.display.set_mode((width * cell_size, height * cell_size))
    clock = pygame.time.Clock()

    model = GameOfLifeModel(width, height, alive_fraction=0.2)
    running = True
    paused = False  # Para controlar a pausa do jogo
    last_click_time = 0  # Para controlar o clique duplo

    # Cores para cada tipo de célula
    empty_color = colors["empty"]
    prey_color = colors["prey"]  # Cor para presas
    predator_color = colors["predator"]  # Cor para predadores

    # Definir a área do botão RESET (na parte inferior esquerda)
    reset_button_rect = pygame.Rect(10, height * cell_size - 40, 100, 30)

    # Listas para armazenar os dados de presas e predadores
    prey_counts = []
    predator_counts = []
    time_steps = []

    time_step = 0  # Contador de passos de tempo

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Controle de pausa (tecla 'space')
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Pausar ou despausar com a tecla 'space'
                    paused = not paused

            # Controle de mutabilidade (clique do mouse)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x, grid_y = mouse_x // cell_size, mouse_y // cell_size

                # Verificar clique esquerdo
                if event.button == 1:
                    # Verificar se o clique foi dentro do botão RESET
                    if reset_button_rect.collidepoint(mouse_x, mouse_y):
                        model = GameOfLifeModel(width, height, alive_fraction=0.2)  # Resetando o modelo
                    else:
                        current_time = pygame.time.get_ticks()  # Tempo atual em milissegundos
                        if current_time - last_click_time < 500:  # Detectar clique duplo (menos de 500ms)
                            # Clique duplo: transformar em presa
                            model.cell_layer.data[grid_x][grid_y] = 1
                        else:
                            # Clique simples: transformar em predador
                            model.cell_layer.data[grid_x][grid_y] = 2
                        last_click_time = current_time

        if not paused:
            model.step()  # Avançar uma etapa do modelo

        # Coletar o número de presas e predadores
        prey_count = sum(1 for x in range(width) for y in range(height) if model.cell_layer.data[x][y] == 1)
        predator_count = sum(1 for x in range(width) for y in range(height) if model.cell_layer.data[x][y] == 2)

        # Armazenar os dados
        prey_counts.append(prey_count)
        predator_counts.append(predator_count)
        time_steps.append(time_step)
        time_step += 1

        # Desenho das células
        screen.fill(empty_color)  # Preencher o fundo com cor de células vazias

        for x in range(width):
            for y in range(height):
                if model.cell_layer.data[x][y] == 1:  # Célula de presa
                    pygame.draw.rect(
                        screen,
                        prey_color,
                        (x * cell_size, y * cell_size, cell_size, cell_size),
                    )
                elif model.cell_layer.data[x][y] == 2:  # Célula de predador
                    pygame.draw.rect(
                        screen,
                        predator_color,
                        (x * cell_size, y * cell_size, cell_size, cell_size),
                    )

        # Desenhar o botão RESET no canto inferior esquerdo
        pygame.draw.rect(
            screen, (200, 200, 200), reset_button_rect)  # Cor do fundo do botão
        font = pygame.font.SysFont("Arial", 20)
        text = font.render("RESET", True, (0, 0, 0))  # Cor do texto
        screen.blit(text, (reset_button_rect.x + 20, reset_button_rect.y + 5))

        pygame.display.flip()  # Atualizar a tela
        clock.tick(2)  # Ajusta o framerate para 2 FPS, para visualização lenta

    # Gerar o gráfico ao final
    pygame.quit()

    # Plotando o gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(time_steps, prey_counts, label="Presas", color="green")
    plt.plot(time_steps, predator_counts, label="Predadores", color="red")
    plt.xlabel("Tempo (Passos)")
    plt.ylabel("Quantidade")
    plt.title("Dinâmica Predador-Prey ao Longo do Tempo")
    plt.legend()
    plt.grid(True)
    plt.show()


# Chamar a função para rodar o modelo
run_GameOfLifeModel(120, 70, 10)
