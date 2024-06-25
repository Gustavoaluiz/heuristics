from random import shuffle
import random
import numpy as np

matriz = [
        [0   , 59.6, 198 , 51.0, 260 , 26.7, 124 , 207 , 142 , 21.1, 260 , 175 , 169 , 321 , 281 , 93.8, 208 , 426 , 29.9, 409],
        [59.3, 0   , 159 , 105 , 207 , 82.1, 63.1, 154 , 158 , 69  , 273 , 139 , 220 , 380 , 228 , 79.0, 262 , 489 , 70.2, 377],
        [199 , 159 , 0   , 187 , 115 , 225 , 162 , 60.6, 317 , 193 , 259 , 244 , 249 , 518 , 136 , 104 , 356 , 623 , 228 , 448],
        [51.0, 104 , 187 , 0   , 304 , 77.1, 173 , 252 , 193 , 38.9, 211 , 225 , 121 , 373 , 325 , 82.8, 185 , 477 , 80.3, 458],
        [259 , 205 , 114 , 300 , 0   , 282 , 200 , 57.5, 367 , 261 , 348 , 276 , 363 , 580 , 38.7, 218 , 462 , 684 , 283 , 430],
        [26.9, 81.2, 225 , 77.0, 281 , 0   , 145 , 229 , 137 , 46.8, 286 , 191 , 195 , 315 , 302 , 121 , 232 , 419 , 24.5, 422],
        [124 , 62.8, 160 , 169 , 199 , 146 , 0   , 150 , 169 , 133 , 333 , 82.6, 287 , 444 , 220 , 139 , 326 , 548 , 146 , 345],
        [208 , 154 , 62.0, 249 , 57.3, 233 , 159 , 0   , 314 , 218 , 316 , 206 , 311 , 528 , 78.6, 166 , 413 , 633 , 234 , 416],
        [142 , 159 , 327 , 193 , 365 , 136 , 169 , 317 , 0   , 162 , 402 , 179 , 314 , 379 , 387 , 235 , 348 , 463 , 113 , 382],
        [23.6, 58.0, 193 , 40.3, 269 , 49.8, 133 , 217 , 165 , 0   , 249 , 190 , 159 , 345 , 290 , 84.8, 222 , 450 , 53.0, 423],
        [262 , 269 , 258 , 213 , 347 , 288 , 334 , 315 , 404 , 250 , 0   , 405 , 119 , 497 , 359 , 194 , 206 , 602 , 291 , 643],
        [176 , 139 , 242 , 225 , 275 , 187 , 82.2, 198 , 179 , 189 , 409 , 0   , 344 , 493 , 290 , 215 , 382 , 597 , 164 , 243],
        [169 , 219 , 249 , 120 , 362 , 195 , 285 , 309 , 311 , 157 , 119 , 356 , 0   , 402 , 374 , 145 , 130 , 506 , 193 , 576],
        [321 , 380 , 518 , 372 , 579 , 315 , 449 , 527 , 379 , 343 , 498 , 494 , 404 , 0   , 601 , 414 , 289 , 108 , 338 , 727],
        [281 , 226 , 135 , 322 , 39.0, 304 , 221 , 79.7, 384 , 282 , 355 , 291 , 373 , 601 , 0   , 239 , 483 , 706 , 305 , 445],
        [95.2, 77.4, 105 , 82.7, 218 , 121 , 144 , 164 , 233 , 89.3, 198 , 215 , 145 , 414 , 240 , 0   , 252 , 519 , 124 , 453],
        [209 , 262 , 356 , 186 , 462 , 235 , 331 , 410 , 348 , 220 , 206 , 382 , 130 , 289 , 483 , 252 , 0   , 394 , 236 , 616],
        [425 , 489 , 623 , 477 , 684 , 420 , 553 , 631 , 431 , 448 , 602 , 598 , 508 , 108 , 705 , 519 , 393 , 0   , 443 , 831],
        [29.1, 70.2, 227 , 82.7, 279 , 22.8, 146 , 227 , 114 , 48.9, 292 , 167 , 201 , 336 , 300 , 123 , 235 , 440 , 0   , 401],
        [410 , 377 , 447 , 459 , 430 , 422 , 345 , 409 , 382 , 423 , 643 , 243 , 577 , 726 , 445 , 453 , 616 , 831 , 399 , 0]
    ]

class TabuSearch:
    def __init__(self, matrix, tabu_size=10):
        self.cost_matrix = matrix
        self.len_matrix = len(matrix)
        self.tabu_list = []
        self.tabu_size = tabu_size
        self.best_sol = []
        self.best_cost = float('inf')

    def _calculate_cost(self, solution):
        """Retorna função objetivo/custo da solução."""

        cost = 0
        for i in range(self.len_matrix-1):
            # Solução é uma lista dos índices da cidade.
            # A ordem em que as cidades são visitadas é a ordem da lista.
            # Portanto, visitamos a cidade i+1 após i.
            cost += self.cost_matrix[solution[i]][solution[i+1]]
        cost += self.cost_matrix[solution[-1]][solution[0]]

        return cost

    def _get_initial_solution(self):
        """Retorna uma solução inicial aleatória."""

        # Fixa a cidade de origem
        solution = [0]
        cities = list(range(1,20))
        shuffle(cities)
        solution.extend(cities)

        return solution


    def _get_neighborhood(self, solution):
        """Retorna vizinhança da solução através de movimentos de TROCA"""

        neighborhood = []
        for i in range(1, self.len_matrix):
            for j in range(i+1, self.len_matrix):
                neighbor = solution.copy()
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                move = (i, j)  # movimento que gerou o vizinho
                neighborhood.append((neighbor, move))

        return neighborhood

    def _get_best_neighbor(self, neighborhood):
        """Retorna o melhor vizinho (candidato) da vizinhança."""

        best_neighbor_cost = float('inf')

        for neighbor, move in neighborhood:
            # Calcular custo do vizinho analisado
            neighbor_cost = self._calculate_cost(neighbor)

            if move not in self.tabu_list:
                # Se o vizinho é melhor que a solução corrente e não está na lista tabu
                # então atualiza a solução corrente.
                if neighbor_cost < best_neighbor_cost:
                    best_neighbor = neighbor
                    best_neighbor_cost = neighbor_cost
                    best_move = move
            # Função de aspiração
            elif neighbor_cost < self.best_cost:
                self.tabu_list.remove(move)
                self.best_cost = neighbor_cost
                self.best_sol = neighbor

        return best_neighbor, best_neighbor_cost, best_move

    def _update_tabu(self, solution):
        """Atualiza lista tabu."""

        if len(self.tabu_list) >= self.tabu_size:
            self.tabu_list.pop(0)
        self.tabu_list.append(solution)

    def search(self, initial_solution, max_iter=100):
        """Executa busca tabu."""

        # Inicialização aleatória
        current_sol = initial_solution
        current_cost = self._calculate_cost(current_sol)
        if current_cost < self.best_cost:
            self.best_cost = current_cost
            self.best_sol = current_sol

        # Executa busca
        for _ in range(max_iter):
            neighborhood = self._get_neighborhood(current_sol)
            current_sol, current_cost, current_move = self._get_best_neighbor(neighborhood)

            # Atualiza melhor solução
            if current_cost < self.best_cost:
                self.best_cost = current_cost
                self.best_sol = current_sol

            self._update_tabu(current_move)

        return self.best_sol, self.best_cost


class GraspReativo:
    def __init__(self, matriz, alphas, busca_local, max_iterations=10, num_amostras = 10, cidade_partida=0):
        self.alpha = {
            'alphas' : alphas, #Lista com os alphas possíveis de serem escolhidos
            'scores' : np.zeros(len(alphas)), # 'Score' de cada alhpa, usado para atualizar as probabilidades do mesmo
            'usos' : np.zeros(len(alphas), dtype=int), # Quantas vezes cada alpha foi usado ao longo das iterações
            'num_amostras' : num_amostras, # Quantidade de amostras de cada valor de alphas para começar a atualizar as probabilidades dos mesmos
            'qtd' : len(alphas) # Quantidade de alphas possíveis
        }

        self.tabu_search = busca_local
        self.max_iterations = max_iterations # Critério de parada 
        self.matriz = matriz # Matriz com os custos entre os nós
        self.cidade_partida = cidade_partida
        self.melhor_solucao = []
        self.melhor_custo = float('inf')

    def atualizar_alpha_prob(self, index, custo_solucao):
        # Atualiza o score do alpha com o inverso do custo da solução, ou seja, um custo menor gera um score maior
        self.alpha['scores'][index] += 1 / (custo_solucao + 1) 

    def retorna_alpha(self, iteracao):
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

    def construcao(self, alpha):
        '''A fase de construção é utilizada para gerar uma solução inicial, a qual mistura gulosidade e aleatoriedade, gernado um range de possíveis escolhas de caminho entre dois nós, sendo essas escolhas baseadas na solução gulosa.'''

        tamanho_matriz = len(self.matriz)
        indice_atual = self.cidade_partida # Inicializa pela cidade definida como primeira
        solucao = [indice_atual]

        restantes = set(range(tamanho_matriz)) - set(solucao) # Constroi a solução até que todos os nós tenham sido inseridos nela

        while restantes:
            # Lista para guardar os custos de adicionar cada candidato restante
            lista_candidatos = [] 

            for candidato in restantes:
                custo = self.matriz[indice_atual][candidato] # Calcula o custo para cada candidato
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

    def busca_local(self, solucao_inicial, iteracoes=1000):
        '''É esperado que o algoritmo possua a informação da matriz e possua o método search'''
        self.tabu_search.search(solucao_inicial, max_iter=iteracoes)

        return self.tabu_search.best_sol

    def calcula_custo(self, solucao):
        custo_total = 0

        for i in range(len(solucao) - 1):
            custo_total += self.matriz[solucao[i]][solucao[i+1]]

        custo_total += self.matriz[solucao[-1]][solucao[0]]  # Assumindo problema circular
        return custo_total


    def gerar_solucao(self):
        for iteracao in range(self.max_iterations):
            # Cada iteraçao é analisado um alfa diferente, de forma ciclica
            alpha, alpha_index = self.retorna_alpha(iteracao)

            solucao_inicial = self.construcao(alpha)
            solucao_melhorada = self.busca_local(solucao_inicial)
            custo_solucao = self.calcula_custo(solucao_melhorada)

            if custo_solucao < self.melhor_custo:
                self.melhor_solucao = solucao_melhorada
                self.melhor_custo = custo_solucao
            
            # Atualizamos a probabilidade do alfa conforme o custo que sua soluçao gerou
            self.atualizar_alpha_prob(alpha_index, custo_solucao)

if __name__ == "__main__":
    alphas = [0.2, 0.25, 0.3, 0.35, 0.4]
    max_iter = 100
    num_amostras = 10

    tabu_search = TabuSearch(matriz, tabu_size=20)
    grasp = GraspReativo(
        matriz=matriz, 
        alphas=alphas, 
        busca_local=tabu_search, 
        max_iterations=max_iter, 
        num_amostras=num_amostras
    )

    grasp.gerar_solucao()
    print(f'Melhor solução: {grasp.melhor_solucao}\nMelhor custo: {grasp.melhor_custo}')
