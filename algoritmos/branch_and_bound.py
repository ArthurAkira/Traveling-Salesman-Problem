import heapq

def tsp_branch_and_bound(grafo, initial_ub=float('inf')):
    """
    Resolve o TSP usando Branch and Bound com lower bounds baseados nos menores custos de saída.

    Conceito: Cada nó representa um caminho parcial. Branch gera filhos adicionando cidades não visitadas.
    Bound calcula limite inferior como soma dos menores custos de saída para cidades restantes.
    Poda: Se bound >= upper bound, descarta o ramo.

    Args:
        grafo (Grafo): Objeto grafo com matriz de distâncias.
        initial_ub (float): Limite superior inicial (upper bound), geralmente da heurística.

    Returns:
        tuple: (melhor_caminho, melhor_distancia)
    """
    n = grafo.n
    melhor_caminho = None
    melhor_distancia = initial_ub

    # Calcula os menores custos de saída para cada cidade (excluindo si mesma)
    min_out = [min(grafo.matriz_distancias[i][j] for j in range(n) if j != i) for i in range(n)]

    def lower_bound(visitados):
        """Lower bound: soma dos menores custos de saída para cidades não visitadas."""
        return sum(min_out[i] for i in range(n) if i not in visitados)

    # Priority queue: (prioridade = lower_bound + current_cost, current_cost, caminho, visitados)
    pq = [(lower_bound({0}), 0, [0], {0})]

    while pq:
        _, cost, caminho, visitados = heapq.heappop(pq)

        if cost >= melhor_distancia:
            continue  # Poda: custo atual já excede o melhor encontrado

        if len(caminho) == n:
            # Caminho completo: adiciona o retorno ao início
            total_cost = cost + grafo.matriz_distancias[caminho[-1]][caminho[0]]
            if total_cost < melhor_distancia:
                melhor_distancia = total_cost
                melhor_caminho = caminho[:]
            continue

        ultimo = caminho[-1]
        for prox in range(n):
            if prox not in visitados:
                new_cost = cost + grafo.matriz_distancias[ultimo][prox]
                if new_cost >= melhor_distancia:
                    continue  # Poda antecipada
                new_caminho = caminho + [prox]
                new_visitados = visitados | {prox}
                new_bound = new_cost + lower_bound(new_visitados)
                if new_bound < melhor_distancia:
                    heapq.heappush(pq, (new_bound, new_cost, new_caminho, new_visitados))

    return melhor_caminho, melhor_distancia