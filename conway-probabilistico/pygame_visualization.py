import pygame
from model_probabilistico import GameOfLifeModel
import numpy as np

def run_GameOfLifeModel(
    width,
    height,
    cell_size,
    revive_probabilities,
    survival_probabilities,
    lamb,
    age_death,
    initial_config=None,
    colors={"empty": (0, 0, 0), "filled": (255, 255, 255)},
    alive_fraction = 0.2,
    tick=20 
):
    pygame.init()
    screen = pygame.display.set_mode((width * cell_size, height * cell_size + 50))  # Include space for buttons
    clock = pygame.time.Clock()

    model = GameOfLifeModel(
        width, height, revive_probabilities, survival_probabilities, alive_fraction, lamb, age_death
    )
    running = True
    paused = False
    dragging = False

     # Cores
    empty_color = colors["empty"]
    filled_color = colors["filled"]
    # Cores pros botões
    button_color = (200, 200, 200)
    button_hover_color = (150, 150, 150)

    
    clear_button_rect = pygame.Rect(10, height * cell_size + 10, 100, 30)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Eventos com o mause
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if clear_button_rect.collidepoint(mouse_x, mouse_y):
                    model.cell_layer.data = np.zeros((width, height), dtype=bool)  
                else:
                    dragging = True
                    grid_x = mouse_x // cell_size
                    grid_y = mouse_y // cell_size
                    if 0 <= grid_x < width and 0 <= grid_y < height:
                        model.cell_layer.data[grid_x, grid_y] = not model.cell_layer.data[grid_x, grid_y]

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False

            # Eventos com o teclado
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused

        # Lida com o dragging do mause
        if dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x = mouse_x // cell_size
            grid_y = mouse_y // cell_size
            if 0 <= grid_x < width and 0 <= grid_y < height:
                model.cell_layer.data[grid_x, grid_y] = not model.cell_layer.data[grid_x, grid_y]  

        screen.fill((0, 0, 0)) 

        '''
        David: Alterei a configuração dessa visualização em dois aspectos:
            -Mudei para rodar de maneira probabilística
            -Incluí também a morte por idade da célula, que o Carlos havia 
        '''        
        for x in range(width):
            for y in range(height):
                if model.cell_layer.data[x][y]:  
                    age = model.age_layer.data[x][y]  

                    red_intensity = max(255 - (age * 3), 128)  
                    green_intensity = max(50 - (age * 3), 128) 
                    blue_intensity = max(50 - (age * 3), 128)  

                    cell_color = (red_intensity, green_intensity, blue_intensity) 

                else:
                    cell_color = empty_color

                pygame.draw.rect(
                    screen,
                    cell_color,
                    (x * cell_size, y * cell_size, cell_size, cell_size)
                )

        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if clear_button_rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(screen, button_hover_color, clear_button_rect)
        else:
            pygame.draw.rect(screen, button_color, clear_button_rect)

        
        font = pygame.font.SysFont(None, 24)
        text = font.render("Clear", True, (0, 0, 0))
        screen.blit(text, (clear_button_rect.x + 25, clear_button_rect.y + 5))

        
        pause_text = "PAUSED" if paused else "RUNNING"
        pause_color = (255, 0, 0) if paused else (0, 255, 0)
        pause_font = pygame.font.SysFont(None, 30)
        pause_surface = pause_font.render(pause_text, True, pause_color)
        screen.blit(pause_surface, (width * cell_size - 120, height * cell_size + 10))

        pygame.display.flip()

        if not paused:
            model.step()
        clock.tick(tick)

    pygame.quit()

run_GameOfLifeModel(200, 100, 5, {0: 0.001, 3: 1.0}, {2: 1, 3: 1}, 1000,False)
