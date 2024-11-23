import time
import random
import numpy as np
from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import PropertyLayer

class Vertex:
    
    def __init__(self, val):
        self.val = val
        self.fac = ''
        self.adj = []
        self.devoc = [0,0,0]
        self.caos = 0
        self.next = ''


class G:    
    def __init__(self):
        self.Core = []
        
    def adjacent(self, x: Vertex, y: Vertex):
        if y in x.adj:
            return True
        return False

    def neighbors(self, x: Vertex):
        ans = []
        for v in x.adj:
            ans.append(v)
        return ans

    def add_vertex(self, x: Vertex):
        ans = True
        if x in self.Core:
            ans = False
        self.Core.append(x)
        return ans

    def remove_vertex(self, x: Vertex):     
        if x in self.Core:
            self.Core.remove(x)
            return True
        return False
    
    def add_edge(self, x: Vertex, y: Vertex):
        if (not y in x.adj ):
            x.adj.append(y)
            y.adj.append(x)
            return True
        return False
    
    def remove_edge(self, x: Vertex, y: Vertex):
        if (y in x.adj ):
            x.adj.remove(y)
            return True
        return False
        
    def get_vertex_value(self, x: Vertex):   
        return x.val

    def set_vertex_value(self, x: Vertex, v):     
        x.val = v

class Conway_empires(Model):
    
    
    
    def __init__(
        self,
        cell,
        gradeX,
        gradeY,
        nodes,
        vilas,
        mst,
        grid,
        
        
    ):
        self.graph = G()
        self.grid = grid
        
        BLACK = (0, 0, 0)
        Barbarians = (255, 255, 255) 
        Fac = [
        (55, 182, 118),    # Golgari
        (246, 145, 168),   # Boros
        (73, 81, 131),     # Dimir
        ]
        
        super().__init__()
        self.cell_layer = PropertyLayer("cells", gradeX, gradeY, False, dtype=int)
        
        '''self.cell_layer.data = np.random.choice(
            [True, False], size=(gradeX, gradeY), p=[1, 0]
        )'''
        
        
        for v in vilas:
            x, y = v
            k = Vertex(v)
            if grid[y][x] == (55, 182, 118):
                    k.fac = 'Golgari'
            if grid[y][x] == (246, 145, 168):
                    k.fac = 'Boros'
            if grid[y][x] == (73, 81, 131):
                    k.fac = 'Dimir'
            if grid[y][x] == (255, 255, 255):
                    k.fac = 'Barbarian'
            
            self.graph.add_vertex(k)
            
        for m in mst:
            n1, n2 = m
            for v in self.graph.Core:
                if v.val == n1:
                    a = v
                if v.val == n2:
                    b = v
            self.graph.add_edge(a, b)
            
        
    def step(self):       
        
            for v in self.graph.Core:
                v.devoc = [0, 0, 0]
                v.caos = 0
                N = self.graph.neighbors(v)

                for n in N:
                    print(n.fac)
                    if n.fac == 'Golgari':
                        v.devoc[0] += 1
                    if n.fac == 'Boros':
                        v.devoc[1] += 1
                    if n.fac == 'Dimir':
                        v.devoc[2] += 1
                    if n.fac == 'Barbarian':
                        v.caos += 1


                print(v.devoc)


                p = random.randint(0,100)

                c = 100

                if v.devoc[0] >=1 and p <= c:
                    v.next = 'Golgari'
                elif v.devoc[1] >=1 and p <= c:
                    v.next = 'Boros'
                elif v.devoc[2] >=1 and p <= c:
                    v.next = 'Dimir'
                elif v.caos >=1 and p <= c:
                    v.next = 'Barbarian'



                # Determina a próxima facção com base nos vizinhos
                if v.devoc[0] >= 2:
                    v.next = 'Golgari'
                elif v.devoc[1] >= 2:
                    v.next = 'Boros'
                elif v.devoc[2] >= 2:
                    v.next = 'Dimir'
                elif v.caos >= 2:
                    v.next = 'Barbarian'

            # Atualiza as facções de cada vértice
            for v in self.graph.Core:
                v.fac = v.next
                x, y = v.val
                # Agora a cor depende da facção
                if v.fac == 'Golgari':
                    self.grid[y][x] = (55, 182, 118)
                elif v.fac == 'Boros':
                    self.grid[y][x] = (246, 145, 168)
                elif v.fac == 'Dimir':
                    self.grid[y][x] = (73, 81, 131)
                elif v.fac == 'Barbarian':
                    self.grid[y][x] = (255, 255, 255)  # Barbarians podem ter uma cor específica.
            
            
            
                
            
                    
                
                        
                
                    
            
