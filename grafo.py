import math

def distancia(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

class Grafo:
    def __init__(self, cidades, matriz=None):
        self.cidades = cidades
        self.n = len(cidades)
        if matriz:
            self.matriz_distancias = matriz
        else:
            self.matriz_distancias = self.calcular_matriz_distancias()


    def calcular_matriz_distancias(self):
        n = len(self.cidades)
        matriz = [[0] * n for _ in range(n)]

        for i in range(n):
            for j in range(i + 1, n):
                d = distancia((self.cidades[i].x, self.cidades[i].y), (self.cidades[j].x, self.cidades[j].y))
                matriz[i][j] = d
                matriz[j][i] = d

        return matriz