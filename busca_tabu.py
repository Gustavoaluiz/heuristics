from random import shuffle
from data import MATRIZ_DE_DISTANCIAS


class BuscaTabu:
    def __init__(self, matriz, tamanho_tabu=10):
        self.matriz_custo = matriz
        self.lista_tabu = []
        self.tamanho_tabu = tamanho_tabu
        self.melhor_solucao = []
        self.melhor_custo = None

    def _calcular_custo(self, solucao):
        """Retorna função objetivo/custo da solução."""

        custo = 0
        for i in range(len(solucao) - 1):
            # Solução é uma lista dos índices da cidade.
            # A ordem em que as cidades são visitadas é a ordem da lista.
            # Portanto, visitamos a cidade i+1 após i.
            custo += self.matriz_custo[solucao[i]][solucao[i+1]]
        custo += self.matriz_custo[solucao[-1]][solucao[0]]

        return custo
    
    def gerar_solucao_inicial(self):
        """Retorna uma solução inicial aleatória."""

        # Fixa a cidade de origem
        solucao = [0]
        # Adiciona as cidades restantes de forma aleatória
        cidades = list(range(1,20))
        shuffle(cidades)
        # Gera solução aleatória com cidade de origem fixa
        solucao.extend(cidades)

        return solucao
    
    def _gerar_vizinhanca(self, solucao):
        """Retorna vizinhança da solução através de movimentos de TROCA"""

        vizinhanca = []
        for i in range(1, len(solucao)):
            for j in range(i+1, len(solucao)):
                vizinho = solucao.copy()
                vizinho[i], vizinho[j] = vizinho[j], vizinho[i]
                # Movimento que gerou o vizinho
                movimento = (i, j)  
                vizinhanca.append((vizinho, movimento))

        return vizinhanca
    
    def _obter_melhor_vizinho(self, vizinhanca):
        """Retorna o melhor vizinho (candidato) da vizinhança."""

        melhor_custo_vizinho = float('inf')

        for vizinho, movimento in vizinhanca:
            custo_vizinho = self._calcular_custo(vizinho)
            
            if movimento not in self.lista_tabu:
                # Se o vizinho é melhor que a solução corrente e não está na lista tabu
                # então atualiza a solução corrente.
                if custo_vizinho < melhor_custo_vizinho:
                    melhor_vizinho = vizinho
                    melhor_custo_vizinho = custo_vizinho
                    melhor_movimento = movimento
            # Função de aspiração
            elif custo_vizinho < self.melhor_custo:
                self.lista_tabu.remove(movimento)
                self.melhor_custo = custo_vizinho
                self.melhor_solucao = vizinho

        return melhor_vizinho, melhor_custo_vizinho, melhor_movimento
    
    def _atualiza_lista_tabu(self, solucao):
        """Atualiza lista tabu."""

        if len(self.lista_tabu) >= self.tamanho_tabu:
            self.lista_tabu.pop(0)
        self.lista_tabu.append(solucao)

    def inicia_busca(self, solucao_inicial: list, max_iter=100):
        """Executa busca tabu."""

        # Inicialização aleatória
        sol_corrente = solucao_inicial
        custo_corrente = self._calcular_custo(sol_corrente)
        self.melhor_custo = custo_corrente
        self.melhor_solucao = sol_corrente

        # Executa busca
        for _ in range(max_iter):
            vizinhanca = self._gerar_vizinhanca(sol_corrente)
            sol_corrente, custo_corrente, mov_corrente = self._obter_melhor_vizinho(vizinhanca)

            # Atualiza melhor solução
            if custo_corrente < self.melhor_custo:
                self.melhor_custo = custo_corrente
                self.melhor_solucao = sol_corrente

            self._atualiza_lista_tabu(mov_corrente)
    
    
if __name__ == "__main__":
    # Testar a busca tabu separadamente
    busca_tabu = BuscaTabu(matriz=MATRIZ_DE_DISTANCIAS, tamanho_tabu=15)

    solucao_inicial = busca_tabu.gerar_solucao_inicial()
    busca_tabu.inicia_busca(solucao_inicial, max_iter=1000)

    print(f'Melhor solução: {busca_tabu.melhor_solucao}\nMelhor custo: {busca_tabu.melhor_custo}')
