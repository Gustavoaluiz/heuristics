from data import MATRIZ_DE_DISTANCIAS, NUM_CIDADE
from grasp_reativo import GraspReativo
from busca_tabu import BuscaTabu


def percorrer_solucao(solucao):
    dist_total = 0

    for cidade1, cidade2 in zip(solucao, solucao[1:]):
        dist = MATRIZ_DE_DISTANCIAS[cidade1][cidade2]
        dist_total += dist
        print(f'Distância entre {NUM_CIDADE[cidade1]} e {NUM_CIDADE[cidade2]}: {dist}')

    # Calcular volta para a cidade de origem
    dist = MATRIZ_DE_DISTANCIAS[solucao[-1]][solucao[0]]
    print(f'Distância entre {NUM_CIDADE[solucao[-1]]} e {NUM_CIDADE[solucao[0]]}: {dist}')

    dist_total += MATRIZ_DE_DISTANCIAS[solucao[-1]][solucao[0]]    
    print(f'Distância total percorrida: {dist_total}')


alphas = [0.2, 0.25, 0.3, 0.35, 0.4]
max_iter = 70
num_amostras = 10

busca_tabu = BuscaTabu(
    matriz=MATRIZ_DE_DISTANCIAS, 
    tamanho_tabu=15
)

grasp = GraspReativo(
    matriz=MATRIZ_DE_DISTANCIAS, 
    alphas=alphas, 
    busca_local=busca_tabu, 
    max_iter=max_iter, 
    num_amostras=num_amostras
)

grasp.gerar_solucao()
print(f'Melhor solução: {grasp.melhor_solucao}\nMelhor custo: {grasp.melhor_custo}')
percorrer_solucao(grasp.melhor_solucao)
