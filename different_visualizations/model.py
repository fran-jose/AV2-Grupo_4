import pygame
from model_probabilistico import GameOfLifeModel
import numpy as np

def run_GameOfLifeModel(width, height, cell_size, tick=20, initial_config=None, colors={"empty": (0, 0, 0), "filled": (255, 255, 255)}):
    pygame.init()
    screen = pygame.display.set_mode((width * cell_size, height * cell_size + 50))  # Include space for buttons
    clock = pygame.time.Clock()

    model = GameOfLifeModel(width, height, alive_fraction=0.2)
    running = True
    paused = False
    dragging = False

    # Colors
    empty_color = colors["empty"]
    filled_color = colors["filled"]
    button_color = (200, 200, 200)
    button_hover_color = (150, 150, 150)

    # Button Rect for clearing the grid
    clear_button_rect = pygame.Rect(10, height * cell_size + 10, 100, 30)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Mouse events
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print(f"Mouse clicked at: ({mouse_x}, {mouse_y})")  # Debugging: Print mouse position

                # Check if the click is on the clear button
                if clear_button_rect.collidepoint(mouse_x, mouse_y):
                    print("Clear button clicked")  # Debugging: Button clicked
                    model.cell_layer.data = np.zeros((width, height), dtype=bool)
                else:
                    # Otherwise, toggle cell state
                    dragging = True
                    grid_x = mouse_x // cell_size
                    grid_y = mouse_y // cell_size
                    print(f"Clicked on grid cell: ({grid_x}, {grid_y})")  # Debugging: Grid cell clicked
                    if 0 <= grid_x < width and 0 <= grid_y < height:
                        model.cell_layer.data[grid_x, grid_y] = not model.cell_layer.data[grid_x, grid_y]

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False

            # Keyboard events (for pausing)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused

        # Handle dragging (to toggle multiple cells while dragging)
        if dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x = mouse_x // cell_size
            grid_y = mouse_y // cell_size
            if 0 <= grid_x < width and 0 <= grid_y < height:
                model.cell_layer.data[grid_x, grid_y] = not model.cell_layer.data[grid_x, grid_y]

        screen.fill((0, 0, 0))  # Clear screen

        # Draw the cells
        for x in range(width):
            for y in range(height):
                if model.cell_layer.data[x][y]:
                    age = model.age_layer.data[x][y]

                    # Gradually change the color based on the cell's age
                    if age > 0:
                        red_intensity = max(255 - (age * 3), 75)  # Red fades with age
                        cell_color = (red_intensity, 75, 75)
                    else:
                        cell_color = empty_color  # Dead cells are empty

                    pygame.draw.rect(
                        screen,
                        cell_color,
                        (x * cell_size, y * cell_size, cell_size, cell_size)
                    )

        # Draw the button with hover effect
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if clear_button_rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(screen, button_hover_color, clear_button_rect)
        else:
            pygame.draw.rect(screen, button_color, clear_button_rect)

        # Draw the button text
        font = pygame.font.SysFont(None, 24)
        text = font.render("Clear", True, (0, 0, 0))
        screen.blit(text, (clear_button_rect.x + 25, clear_button_rect.y + 5))

        # Draw pause status
        pause_text = "PAUSED" if paused else "RUNNING"
        pause_color = (255, 0, 0) if paused else (0, 255, 0)
        pause_font = pygame.font.SysFont(None, 30)
        pause_surface = pause_font.render(pause_text, True, pause_color)
        screen.blit(pause_surface, (width * cell_size - 120, height * cell_size + 10))

        pygame.display.flip()  # Update screen

        # Only update the model if not paused
        if not paused:
            model.step()

        clock.tick(tick)  # Control the game's frame rate

    pygame.quit()

run_GameOfLifeModel(80, 50, 15)
