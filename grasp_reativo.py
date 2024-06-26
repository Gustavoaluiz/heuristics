import random
import numpy as np


class GraspReativo:
    def __init__(
            self, 
            matriz, 
            alphas, 
            busca_local, 
            max_iter=10, 
            num_amostras=10, 
            cidade_partida=0
    ):
        self.alpha = {
            #Lista com os alphas possíveis de serem escolhidos
            'alphas' : alphas, 
            # 'Score' de cada alpha, funciona como sua probabilidade de ser escolhido
            'scores' : np.zeros(len(alphas)), 
            # Quantas vezes cada alpha foi usado ao longo das iterações
            'usos' : np.zeros(len(alphas), dtype=int), 
            # Quantidade de amostras de cada valor de alphas para começar a atualizar
            # as probabilidades dos mesmos
            'num_amostras' : num_amostras, 
            # Quantidade de alphas possíveis
            'qtd' : len(alphas) 
        }

        self.busca_local = busca_local
        self.max_iter = max_iter  # Critério de parada 
        self.matriz_custo = matriz  # Matriz com os custos entre os nós
        self.cidade_partida = cidade_partida
        self.melhor_solucao = []
        self.melhor_custo = float('inf')

    def _atualizar_alpha_prob(self, index, custo_solucao):
        # Atualiza o score do alpha com o inverso do custo da solução, ou seja, um custo menor gera um score maior
        self.alpha['scores'][index] += 1 / (custo_solucao + 1) 

    def _retorna_alpha(self, iteracao):
        # Após a fase de amostragem, temos a distribuiçao de probabilidade dos alphas
        # e entao começamos a utiliza-la, mas continuamos atualizando as probabilidades
        if iteracao >= self.alpha['num_amostras'] * self.alpha['qtd']:
            # Tira a média do score de acordo com o uso
            # porque alphas mais escolhidos terão maior score, o que não é a intenção.
            prob_alphas = self.alpha['scores'] / self.alpha['usos'] 
            # Normaliza as probabilidades entre 0 e 1
            prob_alphas = prob_alphas / np.sum(prob_alphas) 

            # Escolhe um alpha de acordo com a distribuição de probabilidade 
            index = np.random.choice(range(self.alpha['qtd']), p=prob_alphas) 
            self.alpha['usos'][index] += 1

            return self.alpha['alphas'][index], index

        # A cada iteraçao, é utilizado um alpha diferente de forma cíclica
        # Faz "num_amostras" amostras para cada alpha para construir a distribuiçao de probabilidade
        # antes de começar a utilizá-la
        index = iteracao % self.alpha['qtd'] 
        self.alpha['usos'][index] += 1

        return self.alpha['alphas'][index], index

    def _construcao(self, alpha):
        tamanho_matriz = len(self.matriz_custo)
        # Inicializa pela cidade fixada como primeira
        indice_atual = self.cidade_partida 
        solucao = [indice_atual]

        # Constroi a solução até que todos os nós tenham sido inseridos nela
        restantes = set(range(tamanho_matriz)) - set(solucao) 

        while restantes:
            # Lista para guardar os custos de adicionar cada candidato restante
            lista_candidatos = [] 

            # Calcula o custo para cada candidato considerando a cidade atual
            for candidato in restantes:
                custo = self.matriz_custo[indice_atual][candidato] 
                lista_candidatos.append((custo, candidato))

            # Ordena candidatos pelo custo
            lista_candidatos.sort() 

            custo_min, custo_max = lista_candidatos[0][0], lista_candidatos[-1][0]
            # Utiliza o alpha * amplitude como limiar de escolha de candidataos
            limite = custo_min + alpha * (custo_max - custo_min)  
            # Lista de Candidatos Restrita - candidadtos que possuem custo "aceitável" (abaixo do limiar)
            rcl = [c for c in lista_candidatos if c[0] <= limite] 

            # Escolhe um candidato aleatório da RCL
            _, candidato_escolhido = random.choice(rcl) 
            solucao.append(candidato_escolhido)
            restantes.remove(candidato_escolhido)
            
            # "Percorre" para a próxima cidade, que será a atual na próxima iteração
            indice_atual = candidato_escolhido

        return solucao

    def _calcula_custo(self, solucao):
        custo_total = 0

        for i in range(len(solucao) - 1):
            custo_total += self.matriz_custo[solucao[i]][solucao[i+1]]

        custo_total += self.matriz_custo[solucao[-1]][solucao[0]] 
        return custo_total

    def gerar_solucao(self):
        for iteracao in range(self.max_iter):
            print(f'Iteração {iteracao}')
            alpha, alpha_index = self._retorna_alpha(iteracao)

            solucao_inicial = self._construcao(alpha)

            self.busca_local.inicia_busca(solucao_inicial, max_iter=1000)
            melhor_solucao = self.busca_local.melhor_solucao
            custo_solucao = self._calcula_custo(melhor_solucao)

            if custo_solucao < self.melhor_custo:
                self.melhor_solucao = melhor_solucao
                self.melhor_custo = custo_solucao
            
            # Atualizamos a probabilidade do alpha conforme o custo que sua soluçao gerou
            self._atualizar_alpha_prob(alpha_index, custo_solucao)
