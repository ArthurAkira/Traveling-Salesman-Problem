def vizinho_mais_proximo(grafo):
    n = grafo.n
    melhor_caminho = None
    melhor_distancia = float('inf')

    for inicio in range(n):
        caminho = [inicio]
        visitados = {inicio}
        distancia_atual = 0

        while len(caminho) < n:
            ultimo_nodo = caminho[-1]
            proximo_nodo = None
            menor_distancia = float('inf')

            for i in range(n):
                if i not in visitados and grafo.matriz_distancias[ultimo_nodo][i] < menor_distancia:
                    menor_distancia = grafo.matriz_distancias[ultimo_nodo][i]
                    proximo_nodo = i

            if proximo_nodo is not None:
                caminho.append(proximo_nodo)
                visitados.add(proximo_nodo)
                distancia_atual += menor_distancia
            else:
                break

        distancia_total = distancia_atual + grafo.matriz_distancias[caminho[-1]][caminho[0]]
        if distancia_total < melhor_distancia:
            melhor_distancia = distancia_total
            melhor_caminho = caminho

    return melhor_caminho, melhor_distancia
