"""
Resources: 
- https://www.youtube.com/watch?v=lk1_h2_GLv8
"""

from model_probabilistico import GameOfLifeModel
import pygame


def run_GameOfLifeModel(
    width,
    height,
    cell_size,
    revive_probabilities,
    survival_probabilities,
    initial_config=None,
    colors={"empty": (0, 0, 0), "filled": (255, 255, 255)},
):
    pygame.init()
    screen = pygame.display.set_mode((width * cell_size, height * cell_size))
    clock = pygame.time.Clock()

    model = GameOfLifeModel(
        width, height, revive_probabilities, survival_probabilities, alive_fraction=0.2
    )
    running = True

    empty_color = colors["empty"]
    filled_color = colors["filled"]
    # O loop que vai ficar rodando enquanto o programa estiver ativo
    while running:
        # Verificando se a janela foi fechada
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        # Talvez de pra otimizar esses 2 loop for, mas por enquanto vou deixar assim
        for x in range(width):
            for y in range(height):
                if model.cell_layer.data[x][y]:
                    pygame.draw.rect(
                        screen,
                        (255, 255, 255),
                        (x * cell_size, y * cell_size, cell_size, cell_size),
                    )

        pygame.display.flip()
        model.step()
        clock.tick(20)  # Aqui ajusta o framerate

    pygame.quit()


"""Um exemplo onde todas as regras permanecem, com a exceção de que as vezes uma célula revive sozinha
É curioso que nesse caso ela pode aparecer perto de uma estrutura estável, fazendo com que esta desestabilize e desapareça
ou (o que é um pouco menos provável) cresça caóticamente"""
run_GameOfLifeModel(200, 100, 5, {0: 0.001, 3: 1.0}, {2: 1, 3: 1}, True)
