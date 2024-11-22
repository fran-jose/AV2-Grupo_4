import numpy as np
from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import PropertyLayer
from scipy.signal import convolve2d
class GameOfLifeModel(Model):
    def __init__(
        self,
        width=10,
        height=10,
        alive_fraction=0.2,
#        game_type=[[2,3], [3]],
        game_type=[[0], []],
        probabilidade_presa=0.05,
        probabilidade_predador=0.001,
    ):
        super().__init__()
        # Initialize the property layer for cell states
        # [0->Vazio, 1->Presa, 2->Predador]
        self.cell_layer = PropertyLayer("cells", width, height, 0, dtype=int)
        # Randomly set cells to alive
        # Vamos determinar o número de presas e predador
        presa_inicializacao = np.random.choice(
            [0, 1],
            size=(width, height),
            p=[1 - probabilidade_presa, probabilidade_presa],
        )
        predador_inicializa = np.random.choice(
            [0, 2],
            size=(width, height),
            p=[1 - probabilidade_predador, probabilidade_predador],
        )
        self.cell_layer.data = np.maximum(presa_inicializacao, predador_inicializa)
        # Metrics and datacollector
        self.cells = width * height
        self.presas_count = 0
        self.preadores_count = 0
        self.datacollector = DataCollector(
            model_reporters={
                "Presas count": "self.presas_count",
                "Predador count": "self.preadores_count",
            }
        )
        self.datacollector.collect(self)
        self.game_type = game_type  # Matriz que determina a regra do jogo
    def step(self):
        # Define a kernel for counting neighbors. The kernel has 1s around the center cell (which is 0).
        kernel = np.array(
            [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
        )  # Define a vizinhança, no nosso caso a vizinhança será Norte, Sul, Leste, Oeste
        # Count neighbors using convolution.
        neighbor_count = convolve2d(
            self.cell_layer.data, kernel, mode="same", boundary="wrap"
        )
        vizinhos_presas = convolve2d(
            self.cell_layer.data == 1, kernel, mode="same", boundary="wrap"
        )
        vizinhos_predadores = convolve2d(
            self.cell_layer.data == 2, kernel, mode="same", boundary="wrap"
        )
        
        new_state =self.cell_layer.data.copy()
        predador_positions = np.argwhere(self.cell_layer.data == 2) # Pegar todos os que são predadores
        presa_positions = np.argwhere(self.cell_layer.data == 1) # Pegar todos que são presas

        for pos in predador_positions:
            x, y = pos
            
            # O nosso modelo em um modelo sem bordas, podemos então não nos preucupar com o tamanho da matriz
            dx, dy = np.random.choice([-1, 0, 1], size=2)
            new_x, new_y = (x + dx) % self.cell_layer.width, (y + dy) % self.cell_layer.height

            if new_state[new_x, new_y] == 0:
                new_state[new_x, new_y] = 2
                new_state[x, y] = 0
        for pos in presa_positions:
            x, y = pos
            dx, dy = np.random.choice([-1, 0, 1], size=2)
            new_x, new_y = (x + dx) % self.cell_layer.width, (y + dy) % self.cell_layer.height

            if new_state[new_x, new_y] == 0:
                new_state[new_x, new_y] = 1
                new_state[x, y] = 0

        self.cell_layer.data = new_state


        
        # Atualiza as métricas de presas e predadores
        self.presas_count = np.sum(self.cell_layer.data == 1)
        self.preadores_count = np.sum(self.cell_layer.data == 2)
        self.datacollector.collect(self)
