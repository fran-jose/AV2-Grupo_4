import pygame
from model_probabilistico import GameOfLifeModel # Modelo do jogo
import numpy as np
import math

def run_GameOfLifeModel(
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
    """
    Função principal para executar o jogo da vida probabilístico.

    Args:
        width (int): Largura da grade (número de células).
        height (int): Altura da grade (número de células).
        cell_size (int): Tamanho de cada célula em pixels.
        revive_probabilities (dict): Probabilidades de reviver células.
        survival_probabilities (dict): Probabilidades de sobrevivência.
        lamb (float): Constante lambda para ajuste.
        age_death (bool): Define se idade influencia na morte.
        initial_config (np.array, optional): Configuração inicial das células.
        colors (dict): Cores para células vivas e mortas.
        alive_fraction (float): Fração inicial de células vivas.
        tick (int): Velocidade inicial da simulação.
    """

    # Definição de cores para células e botões
    empty_color = colors["empty"]
    filled_color = colors["filled"]
    button_color = (200, 200, 200)
    button_hover_color = (150, 150, 150)

    def initialize_pygame(cell_size):
        """
        Inicializa o Pygame em modo tela cheia e configura o relógio.
        Calcula o número de células baseado na resolução da tela.
        """
        pygame.init()

        # Obtém informações da tela
        display_info = pygame.display.Info()
        screen_width = display_info.current_w  # Largura da tela em pixels
        screen_height = display_info.current_h  # Altura da tela em pixels

        # Ajusta a largura e comprimento
        width = (screen_width+3) // cell_size
        height = (screen_height - 100) // cell_size  # Subtraímos 100 pixels para os controles

        # Configura a tela em modo tela cheia
        screen = pygame.display.set_mode((screen_width, screen_height))
        clock = pygame.time.Clock()

        return screen, clock, width, height
    
    def setup_buttons(cell_size, height):
        """
        Configura os botões Clear, Random e Exit.
        """
        clear_button_rect = pygame.Rect(10, height * cell_size + 10, 100, 30)
        random_button_rect = pygame.Rect(120, height * cell_size + 10, 100, 30)
        exit_button_rect = pygame.Rect(230, height * cell_size + 10, 100, 30)  # Novo botão "Exit"
        return clear_button_rect, random_button_rect, exit_button_rect
    
    def setup_slider(cell_size, height):
        """
        Configura o slider para controle da velocidade.
        """
        slider_rect = pygame.Rect(10, height * cell_size + 50, 200, 20)
        slider_pos = 1  # Posição inicial para velocidade de 1
        return slider_rect, slider_pos
    
    def handle_events(
        model, width, height, cell_size, clear_button_rect, random_button_rect, exit_button_rect,
        slider_rect, paused, dragging_slider, slider_pos
    ):
        """
        Processa eventos do usuário, incluindo mouse, teclado e interação com botões.
        """
        running = True
        dragging = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Botão Clear
                if clear_button_rect.collidepoint(mouse_x, mouse_y):
                    model.cell_layer.data = np.zeros((width, height), dtype=bool)

                # Botão Random
                elif random_button_rect.collidepoint(mouse_x, mouse_y):
                    model.cell_layer.data = np.random.rand(width, height) < 0.2

                # Botão Exit
                elif exit_button_rect.collidepoint(mouse_x, mouse_y):  # Lógica para sair
                    running = False

                # Slider
                elif slider_rect.collidepoint(mouse_x, mouse_y):
                    dragging_slider = True
                    slider_pos = max(0, min(200, mouse_x - slider_rect.x))

                # Interação com células
                else:
                    dragging = True
                    grid_x = mouse_x // cell_size
                    grid_y = mouse_y // cell_size
                    if 0 <= grid_x < width and 0 <= grid_y < height:
                        model.cell_layer.data[grid_x, grid_y] = not model.cell_layer.data[grid_x, grid_y]

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging_slider = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused

        # Lida com o dragging do mouse (movimentação contínua do slider)
        if dragging_slider:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            slider_pos = max(0, min(200, mouse_x - slider_rect.x))  # Limita a posição do slider

        return running, paused, dragging_slider, slider_pos
    
    def update_model(paused, slider_pos, clock):
        """
        Atualiza o estado do modelo e controla a velocidade.
        """
        # Inverte o slider para que o valor maior esteja à direita
        slider_value = slider_pos / 200
        
        # Velocidade
        speed = (50 * slider_value)
        if speed < 0.1:
            speed = 0
        else:
            speed = math.ceil((50 * slider_value ** 1.1))
        
        # Pausa o jogo 
        if speed == 0:
            paused = True

        clock.tick(speed)  # Controla o clock de acordo com a velocidade ajustada

        return speed, paused
        
    def draw_cells(screen, model, cell_size, width, height, empty_color):
        """
        Renderiza as células com base no estado do modelo.
        """
        for x in range(width):
            for y in range(height):
                if model.cell_layer.data[x][y]:
                    age = model.age_layer.data[x][y]
                    red_intensity = min(255, max(0, age * 5))
                    green_intensity = max(0, 255 - age * 5)
                    blue_intensity = max(0, 255 - age * 5)
                    cell_color = (red_intensity, green_intensity, blue_intensity)
                else:
                    cell_color = empty_color

                pygame.draw.rect(
                    screen,
                    cell_color,
                    (x * cell_size, y * cell_size, cell_size, cell_size)
                )

    def draw_button(screen, rect, text, font, mouse_pos, color, hover_color):
        """
        Renderiza um botão na tela.
        """
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, hover_color, rect)
        else:
            pygame.draw.rect(screen, color, rect)

        button_text = font.render(text, True, (0, 0, 0))
        screen.blit(button_text, (rect.x + 15, rect.y + 5))

    def render_game(screen, model, cell_size, width, height, empty_color):
        """
        Renderiza o estado atual do jogo na tela.
        """
        screen.fill((0, 0, 0))  # Limpa a tela
        draw_cells(screen, model, cell_size, width, height, empty_color)

    def render_buttons(screen, font, mouse_pos, clear_button_rect, random_button_rect, exit_button_rect, button_color, button_hover_color):
        """
        Renderiza os botões na tela.
        """
        draw_button(screen, clear_button_rect, "Clear", font, mouse_pos, button_color, button_hover_color)
        draw_button(screen, random_button_rect, "Random", font, mouse_pos, button_color, button_hover_color) 
        draw_button(screen, exit_button_rect, "Exit", font, mouse_pos, button_color, button_hover_color) 

    def render_slider(screen, font, slider_rect, slider_pos, speed):
        """
        Renderiza o controle do slider e exibe a velocidade atual.
        """
        pygame.draw.rect(screen, (255, 255, 255), slider_rect, 2)  # Caixa do slider
        pygame.draw.circle(screen, (255, 0, 0), (slider_rect.x + slider_pos, slider_rect.centery), 10)  # Controle
        speed_text = f"Speed: {speed}"
        speed_surface = font.render(speed_text, True, (255, 255, 255))
        screen.blit(speed_surface, (slider_rect.x + 220, slider_rect.y))

    def render_status(screen, font, width, cell_size, paused):
        """
        Exibe o status de pausa/execução do jogo.
        """
        pause_text = "PAUSED" if paused else "RUNNING"
        pause_color = (255, 0, 0) if paused else (0, 255, 0)
        pause_surface = pygame.font.SysFont(None, 30).render(pause_text, True, pause_color)
        screen.blit(pause_surface, (width * cell_size - 120, height * cell_size + 10))

    def render_model_info(screen, font, model, max_age):
        """
        Exibe informações do modelo: células vivas, idade média e máxima.
        """
        try:
            average_age = np.mean(model.age_layer.data[model.cell_layer.data])
            max_age = max(max_age, np.max(model.age_layer.data[model.cell_layer.data]))
        except:
            average_age = 0

        alive_count_text = font.render(f"Vivas: {model.alive_count}", True, (255, 255, 255))
        avg_age_text = font.render(f"Idade Média: {average_age:.2f}", True, (255, 255, 255))
        max_age_text = font.render(f"Idade Máxima: {max_age}", True, (255, 255, 255))
        
        screen.blit(alive_count_text, (10, 10))
        screen.blit(avg_age_text, (10, 30))
        screen.blit(max_age_text, (10, 50))

        return max_age  # Atualiza o valor de idade máxima
    
    # Inicialização do jogo
    screen, clock, width, height = initialize_pygame(cell_size)
    model = GameOfLifeModel( # Instancia o modelo do jogo.
        width, height, revive_probabilities, survival_probabilities, alive_fraction, lamb, age_death
    ) 
    clear_button_rect, random_button_rect, exit_button_rect = setup_buttons(cell_size, height) # Configuração dos botões.
    slider_rect, slider_pos = setup_slider(cell_size, height) # Configuração do slider.
    font = pygame.font.SysFont(None, 24) # Fonte usada nos textos.
    running, paused, dragging_slider = True, False, False # Estados iniciais do jogo.
    max_age = 0 # Idade máxima inicial.

    # Loop Principal do jogo.
    while running:
        running, paused, dragging_slider, slider_pos = handle_events(
        model, width, height, cell_size, clear_button_rect,
        random_button_rect, exit_button_rect, slider_rect, paused, dragging_slider, slider_pos
        )

        mouse_pos = pygame.mouse.get_pos()
        speed, paused = update_model(paused, slider_pos, clock)

        # Renderização
        render_game(screen, model, cell_size, width, height, empty_color)
        render_buttons(screen, font, mouse_pos, clear_button_rect, random_button_rect, exit_button_rect, button_color, button_hover_color)
        render_slider(screen, font, slider_rect, slider_pos, speed)
        render_status(screen, font, width, cell_size, paused)
        max_age = render_model_info(screen, font, model, max_age)
        pygame.display.flip()  # Atualiza a tela

        if not paused:
            model.step() # Avança uma etapa no modelo.

    pygame.quit()

run_GameOfLifeModel(10, {0: 0.001, 3: 1.0}, {2: 1, 3: 1}, 1050, False)
