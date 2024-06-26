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
        # Após a fase de amostragem, temos a distribuiçao de probabilidade dos alfas
        # E entao começamos a utiliza-la, mas ainda atualizamos as probabilidades
        if iteracao >= self.alpha['num_amostras'] * self.alpha['qtd']: # Retorna as probabilidades somente se já forem retiradas num_amostras de cada alpha

            prob_alphas = self.alpha['scores'] / self.alpha['usos'] # Tira a média do score de acordo com o uso, por que alphas mais escolhidos terão maior score, o que não é a intenção.
            prob_alphas = prob_alphas / np.sum(prob_alphas) # Normaliza as probabilidades entre 0 e 1

            index = np.random.choice(range(self.alpha['qtd']), p=prob_alphas) # Índice de alpha escolhido aleatoriamente
            self.alpha['usos'][index] += 1

            return self.alpha['alphas'][index], index # Retorna o alpha e seu índice

        # A cada iteraçao, é utiliado um alfa diferente de forma cíclica
        # Faz 10 amostras para cada alfa para construir a distribuiçao de probabilidade
        index = iteracao % self.alpha['qtd'] 
        self.alpha['usos'][index] += 1
        return self.alpha['alphas'][index], index

    def _construcao(self, alpha):
        '''A fase de construção é utilizada para gerar uma solução inicial, a qual mistura gulosidade e aleatoriedade, gernado um range de possíveis escolhas de caminho entre dois nós, sendo essas escolhas baseadas na solução gulosa.'''

        tamanho_matriz = len(self.matriz_custo)
        indice_atual = self.cidade_partida # Inicializa pela cidade definida como primeira
        solucao = [indice_atual]

        restantes = set(range(tamanho_matriz)) - set(solucao) # Constroi a solução até que todos os nós tenham sido inseridos nela

        while restantes:
            # Lista para guardar os custos de adicionar cada candidato restante
            lista_candidatos = [] 

            for candidato in restantes:
                custo = self.matriz_custo[indice_atual][candidato] # Calcula o custo para cada candidato
                lista_candidatos.append((custo, candidato))

            lista_candidatos.sort() # Ordenar candidatos pelo custo

            custo_min, custo_max = lista_candidatos[0][0], lista_candidatos[-1][0]
            limite = custo_min + alpha * (custo_max - custo_min) # Trabalha com o alpha * amplitude para o range de escolha
            rcl = [c for c in lista_candidatos if c[0] <= limite] # Lista de candidatos que tem custo "aceitável"

            _, candidato_escolhido = random.choice(rcl) # Escolher um candidato aleatório da RCL
            solucao.append(candidato_escolhido)
            restantes.remove(candidato_escolhido)
            indice_atual = candidato_escolhido

        return solucao

    def _calcula_custo(self, solucao):
        custo_total = 0

        for i in range(len(solucao) - 1):
            custo_total += self.matriz_custo[solucao[i]][solucao[i+1]]

        custo_total += self.matriz_custo[solucao[-1]][solucao[0]]  # Assumindo problema circular
        return custo_total


    def gerar_solucao(self):
        for iteracao in range(self.max_iter):
            # Cada iteraçao é analisado um alfa diferente, de forma ciclica
            alpha, alpha_index = self._retorna_alpha(iteracao)

            solucao_inicial = self._construcao(alpha)

            self.busca_local.inicia_busca(solucao_inicial, max_iter=1000)
            melhor_solucao = self.busca_local.melhor_solucao
            custo_solucao = self._calcula_custo(melhor_solucao)

            if custo_solucao < self.melhor_custo:
                self.melhor_solucao = melhor_solucao
                self.melhor_custo = custo_solucao
            
            # Atualizamos a probabilidade do alfa conforme o custo que sua soluçao gerou
            self._atualizar_alpha_prob(alpha_index, custo_solucao)
