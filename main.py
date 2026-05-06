from leitor import ler_tsp
from grafo import Grafo
from benchmark import benchmark
from algoritmos.heuristica import  vizinho_mais_proximo
from algoritmos.branch_and_bound import tsp_branch_and_bound
from algoritmos.busca_exaustiva import busca_exaustiva_tsp

def main():
    cidades, matriz = ler_tsp('instances/japao.tsp')
    
    # Opção para limitar o número de cidades
    limitar = input("Deseja limitar o número de cidades para demonstração? (s/n): ").strip().lower()
    if limitar == 's':
        try:
            num_cidades = int(input("Digite o número de cidades a usar (máximo {}): ".format(len(cidades))))
            num_cidades = min(num_cidades, len(cidades))
            if num_cidades > 15:
                print("⚠ Atenção: Busca Exaustiva suporta no máximo 15 cidades.")
                print("  Para mais de 15 cidades, use Heurística ou Branch and Bound.")
                usar_exaustiva = input("Deseja usar uma instância menor (≤15 cidades)? (s/n): ").strip().lower()
                if usar_exaustiva == 's':
                    num_cidades = min(num_cidades, 15)
        except ValueError:
            print("Entrada inválida. Usando 10 cidades por padrão.")
            num_cidades = 10
    else:
        num_cidades = len(cidades)
        if num_cidades > 15:
            print(f"⚠ Arquivo contém {num_cidades} cidades. Busca Exaustiva não é viável.")
            print("  Usando 12 cidades para demonstração da Busca Exaustiva.")
            print("  Use a Heurística ou Branch and Bound para instâncias maiores.")
            num_cidades = 12
    
    cidades_subset = cidades[:num_cidades]
    if matriz:
        matriz_subset = [row[:num_cidades] for row in matriz[:num_cidades]]
        grafo_obj = Grafo(cidades_subset, matriz_subset)
    else:
        grafo_obj = Grafo(cidades_subset)
    
    print(f"\nUsando {num_cidades} cidades.")

    print("\nExecutando Busca Exaustiva (Espaço de Estados)...")
    try:
        resultado_exaustiva, tempo_exaustiva = benchmark(busca_exaustiva_tsp, grafo_obj)
        print(f"Busca Exaustiva - Melhor caminho: {resultado_exaustiva[0]}, Distância: {resultado_exaustiva[1]:.2f}, Tempo: {tempo_exaustiva:.4f} segundos")
    except ValueError as e:
        print(f"Erro: {e}")
        return

    print("\nExecutando Heurística...")
    resultado_heuristica, tempo_heuristica = benchmark(vizinho_mais_proximo, grafo_obj)
    print(f"Heurística - Melhor caminho: {resultado_heuristica[0]}, Distância: {resultado_heuristica[1]:.2f}, Tempo: {tempo_heuristica:.4f} segundos")

    print("\nExecutando Branch and Bound...")
    resultado_bb, tempo_bb = benchmark(tsp_branch_and_bound, grafo_obj)
    print(f"Branch and Bound - Melhor caminho: {resultado_bb[0]}, Distância: {resultado_bb[1]:.2f}, Tempo: {tempo_bb:.4f} segundos")

if __name__ == "__main__":
    main()  