"""
Resources: 
- https://www.youtube.com/watch?v=lk1_h2_GLv8
"""
from model import GameOfLifeModel
import pygame

def run_GameOfLifeModel(width, height, cell_size, initial_config = None, colors = {"empty" : (0,0,0),
                                                                                   "filled" : (255, 255, 255)}):
    pygame.init()
    screen = pygame.set_display(width * cell_size, height * cell_size)
    clock = pygame.time.Clock()

    model = GameOfLifeModel(width, height, alive_fraction = 0.2)
    running = True

    """
    Deixei esse dicionário de cores ja implementado mesmo que eu não use ele de fato,
    acho que vai ser útil pra quando vocês forem criar mais de um tipo de célula
    """
    
    empty_color = colors["empty"]
    filled_color = colors["filled"]
    # O loop que vai ficar rodando enquanto o programa estiver ativo
    while running:
        # Verificando se a janela foi fechada
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        for x in range(width):
            for y in range(height):
                if model.cell_layer.data[x][y]:
                    pygame.draw.rect(screen, (255, 255, 255), (x * cell_size, y * cell_size, cell_size, cell_size))

        pygame.display.flip()
        model.step()
        clock.tick(10)  

    pygame.quit()
