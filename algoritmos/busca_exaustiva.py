"""
O(n!) onde n é o número de cidades, devido à explosão combinatória.
Para n=10: ~3.6 milhões de possibilidades
Para n=15: ~1.3 trilhões de possibilidades
O tempo de execução cresce exponencialmente com n, tornando inviável para instâncias grandes.
"""

import itertools

def busca_exaustiva_tsp(grafo):
    """
    Realiza uma busca exaustiva no espaço de estados usando itertools.permutations para encontrar a solução ótima do TSP.

    Args:
        grafo (Grafo): Objeto grafo contendo as cidades e matriz de distâncias.

    Returns:
        tuple: (melhor_caminho, melhor_distancia)
            - melhor_caminho: Lista com a sequência ótima de cidades (índices).
            - melhor_distancia: Distância total do caminho ótimo.
    """
    n = grafo.n
    
    melhor_caminho = None
    melhor_distancia = float('inf')
    
    # Gera todas as permutações começando de 0
    for perm in itertools.permutations(range(1, n)):
        caminho = [0] + list(perm)
        distancia = sum(grafo.matriz_distancias[caminho[i]][caminho[i+1]] for i in range(n-1))
        distancia += grafo.matriz_distancias[caminho[-1]][caminho[0]]
        if distancia < melhor_distancia:
            melhor_distancia = distancia
            melhor_caminho = caminho[:]
    
    return melhor_caminho, melhor_distancia