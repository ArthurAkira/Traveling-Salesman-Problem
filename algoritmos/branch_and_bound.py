import heapq

def tsp_branch_and_bound(grafo):
    n = grafo.n
    melhor_caminho = None
    melhor_distancia = float('inf')

    # Calcula os custos mínimos de saída para cada cidade
    min_out = [min(grafo.matriz_distancias[i][j] for j in range(n) if j != i) for i in range(n)]

    def lower_bound(caminho, visitados):
        if len(caminho) == n:
            return grafo.matriz_distancias[caminho[-1]][caminho[0]]
        
        lb = sum(min_out[i] for i in range(n) if i not in visitados)
        # Adicionar custo de volta ao início
        ultimo = caminho[-1]
        min_to_start = min(grafo.matriz_distancias[i][caminho[0]] for i in range(n) if i not in visitados and i != caminho[0])
        lb += min_to_start
        return lb

    # Priority queue: (lower_bound, current_cost, caminho, visitados)
    pq = [(0, 0, [0], {0})]

    while pq:
        bound, cost, caminho, visitados = heapq.heappop(pq)

        if bound >= melhor_distancia:
            continue

        if len(caminho) == n:
            total_cost = cost + grafo.matriz_distancias[caminho[-1]][caminho[0]]
            if total_cost < melhor_distancia:
                melhor_distancia = total_cost
                melhor_caminho = caminho[:]
            continue

        ultimo = caminho[-1]
        for i in range(n):
            if i not in visitados:
                new_cost = cost + grafo.matriz_distancias[ultimo][i]
                new_caminho = caminho + [i]
                new_visitados = visitados | {i}
                new_bound = new_cost + lower_bound(new_caminho, new_visitados)
                if new_bound < melhor_distancia:
                    heapq.heappush(pq, (new_bound, new_cost, new_caminho, new_visitados))

    return melhor_caminho, melhor_distancia