from pp_model import GameOfLifeModel
import pygame


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

    # Cores para cada tipo de célula
    empty_color = colors["empty"]
    prey_color = colors["prey"]  # Cor para presas (branco)
    predator_color = colors["predator"]  # Cor para predadores (vermelho)

    # O loop que vai ficar rodando enquanto o programa estiver ativo
    while running:
        # Verificando se a janela foi fechada
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(empty_color)  # Preencher o fundo de preto (cor de células vazias)

        # Loop para desenhar as células
        for x in range(width):
            for y in range(height):
                # Verificando o tipo da célula
                if model.cell_layer.data[x][y] == 1:  # Célula de presa
                    pygame.draw.rect(
                        screen,
                        prey_color,  # Cor das presas (branca)
                        (x * cell_size, y * cell_size, cell_size, cell_size),
                    )
                elif model.cell_layer.data[x][y] == 2:  # Célula de predador
                    pygame.draw.rect(
                        screen,
                        predator_color,  # Cor dos predadores (vermelho)
                        (x * cell_size, y * cell_size, cell_size, cell_size),
                    )

        pygame.display.flip()  # Atualizar a tela
        model.step()  # Avançar uma etapa do modelo
        clock.tick(2)  # Ajusta o framerate para 20 FPS

    pygame.quit()


# Chamar a função para rodar o modelo
run_GameOfLifeModel(100, 100, 10)
