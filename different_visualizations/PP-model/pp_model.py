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
        game_type=[[0], [2]],
        probabilidade_presa=0.5,
        probabilidade_predador=0.01,
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
        # Cria uma cópia do estado atual para evitar alterações durante a iteração
        new_state = np.copy(self.cell_layer.data)
        # Regra para as presas:
        # 1. As presas sobrevivem se tiverem 2 ou 3 vizinhos do tipo "presa"
        # 2. As presas nascem se tiverem exatamente 3 vizinhos do tipo "presa"
        new_state = np.where(
            np.logical_or(
                np.logical_and(
                    self.cell_layer.data == 1,
                    np.isin(vizinhos_presas, self.game_type[0]),
                ),
                np.logical_and(
                    self.cell_layer.data == 0,
                    np.isin(vizinhos_presas, self.game_type[1]),
                ),
            ),
            1,
            0,
        )
        new_state[(self.cell_layer.data == 1) & (vizinhos_predadores > 0)] = (
            2  # Predadores sobrevivem e convertem presas em predadores
        )
        # Predadores morrem se não tiverem presas ao lado
        new_state[(self.cell_layer.data == 2) & (vizinhos_presas == 0)] = (
            0  # Predadores morrem se não houver presas
        )
        # Atualiza o estado da camada de células
        self.cell_layer.data = new_state
        # Atualiza as métricas de presas e predadores
        self.presas_count = np.sum(self.cell_layer.data == 1)
        self.preadores_count = np.sum(self.cell_layer.data == 2)
        self.datacollector.collect(self)
