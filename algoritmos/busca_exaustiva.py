"""
Busca em Espaço de Estados para TSP - Solução Ótima (Exaustiva)

Este módulo implementa uma busca exaustiva no espaço de estados para o Problema do Caixeiro Viajante (TSP).
Utiliza uma abordagem de busca em profundidade (DFS) para explorar todas as possíveis permutações de cidades,
garantindo a solução ótima.

Complexidade: O(n!) onde n é o número de cidades, devido à explosão combinatória.
Para n=10: ~3.6 milhões de possibilidades
Para n=15: ~1.3 trilhões de possibilidades
O tempo de execução cresce exponencialmente com n, tornando inviável para instâncias grandes.
"""

def busca_exaustiva_tsp(grafo):
    """
    Realiza uma busca exaustiva no espaço de estados usando DFS para encontrar a solução ótima do TSP.

    Args:
        grafo (Grafo): Objeto grafo contendo as cidades e matriz de distâncias.

    Returns:
        tuple: (melhor_caminho, melhor_distancia)
            - melhor_caminho: Lista com a sequência ótima de cidades (índices).
            - melhor_distancia: Distância total do caminho ótimo.
    """
    import sys
    
    n = grafo.n
    
    # Limite de cidades para busca exaustiva - acima disso é computacionalmente inviável
    MAX_CITIES_EXHAUSTIVE = 15
    if n > MAX_CITIES_EXHAUSTIVE:
        raise ValueError(
            f"Busca Exaustiva não é viável para {n} cidades. "
            f"Máximo suportado: {MAX_CITIES_EXHAUSTIVE} cidades (limite de profundidade de recursão). "
            f"Use a heurística ou Branch and Bound para instâncias maiores."
        )
    
    # Aumentar limite de recursão temporariamente (máximo necessário é n)
    original_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(max(2000, n + 100))
    
    melhor_caminho = None
    melhor_distancia = float('inf')

    def dfs(caminho, visitados, distancia_atual):
        nonlocal melhor_caminho, melhor_distancia

        # Se o caminho contém todas as cidades, calcula a distância de retorno
        if len(caminho) == n:
            distancia_total = distancia_atual + grafo.matriz_distancias[caminho[-1]][caminho[0]]
            if distancia_total < melhor_distancia:
                melhor_distancia = distancia_total
                melhor_caminho = caminho[:]
            return

        # Explora todas as cidades não visitadas
        for i in range(n):
            if i not in visitados:
                visitados.add(i)
                # Recursão: adiciona a cidade ao caminho e atualiza a distância
                dfs(caminho + [i], visitados, distancia_atual + grafo.matriz_distancias[caminho[-1]][i])
                visitados.remove(i)

    # Inicia a busca a partir da cidade 0
    dfs([0], {0}, 0)
    
    # Restaurar limite de recursão original
    sys.setrecursionlimit(original_limit)

    return melhor_caminho, melhor_distancia