from random import shuffle


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

    def search(self, max_iter=100):
        """Executa busca tabu."""

        # Inicialização aleatória
        current_sol = self._get_initial_solution()
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
    