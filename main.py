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
    
    print(f"\n{'='*60}")
    print(f"RESULTADOS PARA {num_cidades} CIDADES")
    print(f"{'='*60}")

    # Busca Exaustiva
    print("\n🔍 BUSCA EXAUSTIVA (Solução Ótima)")
    print("-" * 40)
    try:
        resultado_exaustiva, tempo_exaustiva = benchmark(busca_exaustiva_tsp, grafo_obj)
        print(f"  Caminho: {' → '.join(map(str, resultado_exaustiva[0]))}")
        print(f"  Distância: {resultado_exaustiva[1]:.2f} km")
        print(f"  Tempo: {tempo_exaustiva:.4f} s")
    except ValueError as e:
        print(f"  Erro: {e}")
        return

    # Heurística
    print("\n🎯 HEURÍSTICA (Vizinho Mais Próximo)")
    print("-" * 40)
    resultado_heuristica, tempo_heuristica = benchmark(vizinho_mais_proximo, grafo_obj)
    print(f"  Caminho: {' → '.join(map(str, resultado_heuristica[0]))}")
    print(f"  Distância: {resultado_heuristica[1]:.2f} km")
    print(f"  Tempo: {tempo_heuristica:.4f} s")

    # Branch and Bound
    print("\n🌳 BRANCH AND BOUND (Solução Ótima Otimizada)")
    print("-" * 40)
    resultado_bb, tempo_bb = benchmark(tsp_branch_and_bound, grafo_obj)
    print(f"  Caminho: {' → '.join(map(str, resultado_bb[0]))}")
    print(f"  Distância: {resultado_bb[1]:.2f} km")
    print(f"  Tempo: {tempo_bb:.4f} s")

    # Comparação
    print(f"\n{'='*60}")
    print("COMPARAÇÃO DE RESULTADOS")
    print(f"{'='*60}")
    print(f"{'Algoritmo':<20} {'Distância (km)':<15} {'Tempo (s)':<10}")
    print("-" * 45)
    print(f"{'Busca Exaustiva':<20} {resultado_exaustiva[1]:<15.2f} {tempo_exaustiva:<10.4f}")
    print(f"{'Heurística':<20} {resultado_heuristica[1]:<15.2f} {tempo_heuristica:<10.4f}")
    print(f"{'Branch and Bound':<20} {resultado_bb[1]:<15.2f} {tempo_bb:<10.4f}")

    print(f"\n{'='*60}")
    print("ANÁLISE DE PERFORMANCE")
    print(f"{'='*60}")
    print(f"• Busca Exaustiva: Explora {(num_cidades-1)}! possibilidades")
    print(f"• Heurística: Aproximação rápida")
    erro_heur = ((resultado_heuristica[1] - resultado_exaustiva[1]) / resultado_exaustiva[1]) * 100
    if abs(erro_heur) > 1e-6:
        print(f"  - Erro relativo: {erro_heur:+.2f}%")
    print(f"• Branch and Bound: Solução ótima com poda inteligente")
    erro_bb = ((resultado_bb[1] - resultado_exaustiva[1]) / resultado_exaustiva[1]) * 100
    if abs(erro_bb) > 1e-6:
        print(f"  - Erro relativo: {erro_bb:+.2f}%")
    if tempo_bb < tempo_exaustiva:
        print(f"• Branch and Bound foi {tempo_exaustiva/tempo_bb:.1f}x mais rápido que Busca Exaustiva")
    else:
        print(f"• Para {num_cidades} cidades, Branch and Bound levou mais tempo devido à complexidade")

if __name__ == "__main__":
    main()  