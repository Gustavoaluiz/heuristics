import random

class TabuSearch:
    def __init__(self, matrix, tabu_size=10):
        self.cost_matrix = matrix
        self.len_matrix = len(matrix)
        self.tabu_list = []
        self.tabu_size = tabu_size
        self.best_sol = []
        self.best_cost = float('inf')

    def calculate_cost(self, solution):
        """Retorna função objetivo/custo da solução."""

        cost = 0
        for i in range(self.len_matrix-1):
            # Solução é uma lista dos índices da cidade.
            # A ordem em que as cidades são visitadas é a ordem da lista.
            # Portanto, visitamos a cidade i+1 após i.
            cost += self.cost_matrix[solution[i]][solution[i+1]]
        cost += self.cost_matrix[solution[-1]][solution[0]]

        return cost
    
    def get_initial_solution(self):
        """Retorna uma solução inicial aleatória."""

        solution = list(range(self.len_matrix))
        random.shuffle(solution)

        return solution
        
    
    def get_neighborhood(self, solution):
        """Retorna vizinhança da solução através de movimentos de TROCA"""

        neighborhood = []
        for i in range(self.len_matrix):
            for j in range(i+1, self.len_matrix):
                neighbor = solution.copy()
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                move = (i, j)  # movimento que gerou o vizinho
                neighborhood.append((neighbor, move))

        return neighborhood
    
    def get_best_neighbor(self, neighborhood):
        """Retorna o melhor vizinho (candidato) da vizinhança."""

        best_neighbor_cost = float('inf')

        for neighbor, move in neighborhood:
            if move not in self.tabu_list:
                neighbor_cost = self.calculate_cost(neighbor)

                # Se o vizinho é melhor que a solução corrente e não está na lista tabu
                # então atualiza a solução corrente.
                if neighbor_cost < best_neighbor_cost:
                    best_neighbor = neighbor
                    best_neighbor_cost = neighbor_cost
                    best_move = move

        return best_neighbor, best_neighbor_cost, best_move
    
    def update_tabu(self, solution):
        """Atualiza lista tabu."""

        if len(self.tabu_list) >= self.tabu_size:
            self.tabu_list.pop(0)
        self.tabu_list.append(solution)

    def search(self, max_iter=100):
        """Executa busca tabu."""

        # Inicialização aleatória
        current_sol = self.get_initial_solution()
        current_cost = self.calculate_cost(current_sol)
        if current_cost < self.best_cost:
            self.best_cost = current_cost
            self.best_sol = current_sol

        # Executa busca
        for _ in range(max_iter):
            neighborhood = self.get_neighborhood(current_sol)
            current_sol, current_cost, current_move = self.get_best_neighbor(neighborhood)

            # Atualiza melhor solução
            if current_cost < self.best_cost:
                self.best_cost = current_cost
                self.best_sol = current_sol

            self.update_tabu(current_move)

        return self.best_sol, self.best_cost
    