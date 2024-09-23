import numpy as np
import random
import math

# Função de avaliação que calcula a distância total percorrida pelas equipes
def calc_total_distance(schedule, distance_matrix):
    total_distance = 0
    num_teams = len(schedule)
    
    for team in range(num_teams):
        current_location = team  # O time começa na sua cidade-sede
        for round_index in range(len(schedule[0])):
            opponent = abs(schedule[team][round_index]) - 1  # Oponente na rodada
            if schedule[team][round_index] < 0:  # Jogo fora de casa
                total_distance += distance_matrix[current_location][opponent]
                current_location = opponent  # Atualiza a localização do time
        
        # Retorna à cidade-sede no final
        total_distance += distance_matrix[current_location][team]
    
    return total_distance


# Geração de uma solução inicial (aleatória)
def generate_initial_solution(num_teams):
    schedule = []
    teams = list(range(1, num_teams + 1))
    
    for team in range(num_teams):
        # Gera jogos sem repetir o time atual
        team_schedule = random.sample([i for i in teams if i != team + 1], num_teams - 1)
        # Aleatoriamente, metade dos jogos fora de casa
        team_schedule = [opponent if random.random() > 0.5 else -opponent for opponent in team_schedule]
        schedule.append(team_schedule)
    
    return schedule


# Função de vizinhança para gerar um vizinho (alterar o cronograma)
def get_neighbor(solution):
    neighbor = [row[:] for row in solution]  # Cria uma cópia
    team = random.randint(0, len(solution) - 1)
    round1, round2 = random.sample(range(len(solution[0])), 2)
    neighbor[team][round1], neighbor[team][round2] = neighbor[team][round2], neighbor[team][round1]
    return neighbor

# 1. Late Acceptance Hill Climbing (LAHC)
def late_acceptance_hill_climbing(distance_matrix, max_iter=1000, L=50):
    current_solution = generate_initial_solution(len(distance_matrix))
    current_cost = calc_total_distance(current_solution, distance_matrix)
    history = [current_cost] * L
    best_solution = current_solution
    best_cost = current_cost
    
    for i in range(max_iter):
        candidate_solution = get_neighbor(current_solution)
        candidate_cost = calc_total_distance(candidate_solution, distance_matrix)
        
        if candidate_cost < history[i % L] or candidate_cost < current_cost:
            current_solution = candidate_solution
            current_cost = candidate_cost
        
        if current_cost < best_cost:
            best_solution = current_solution
            best_cost = current_cost
        
        history[i % L] = current_cost
    
    return best_solution, best_cost

# 2. Iterated Local Search (ILS)
def iterated_local_search(distance_matrix, max_iter=1000):
    current_solution = generate_initial_solution(len(distance_matrix))
    current_cost = calc_total_distance(current_solution, distance_matrix)
    best_solution = current_solution
    best_cost = current_cost
    
    for i in range(max_iter):
        # Aplica a busca local
        candidate_solution = get_neighbor(current_solution)
        candidate_cost = calc_total_distance(candidate_solution, distance_matrix)
        
        # Perturbação
        if random.random() < 0.1:  # Pequena chance de grande perturbação
            candidate_solution = generate_initial_solution(len(distance_matrix))
            candidate_cost = calc_total_distance(candidate_solution, distance_matrix)
        
        # Critério de aceitação
        if candidate_cost < current_cost:
            current_solution = candidate_solution
            current_cost = candidate_cost
            
        if current_cost < best_cost:
            best_solution = current_solution
            best_cost = current_cost
            
    return best_solution, best_cost

# 3. Simulated Annealing (SA)
def simulated_annealing(distance_matrix, T0=1000, alpha=0.99, max_iter=1000):
    current_solution = generate_initial_solution(len(distance_matrix))
    current_cost = calc_total_distance(current_solution, distance_matrix)
    best_solution = current_solution
    best_cost = current_cost
    T = T0
    
    for i in range(max_iter):
        candidate_solution = get_neighbor(current_solution)
        candidate_cost = calc_total_distance(candidate_solution, distance_matrix)
        
        # Aceitar por probabilidade
        delta = candidate_cost - current_cost
        if delta < 0 or random.random() < math.exp(-delta / T):
            current_solution = candidate_solution
            current_cost = candidate_cost
        
        if current_cost < best_cost:
            best_solution = current_solution
            best_cost = current_cost
        
        T *= alpha  # Resfriamento
    
    return best_solution, best_cost

import numpy as np

# Função para gerar uma matriz de distâncias aleatória para 20 times
def generate_distance_matrix(num_teams=20, max_distance=1000):
    # Gera uma matriz simétrica de distâncias
    distance_matrix = np.random.randint(50, max_distance, size=(num_teams, num_teams))
    np.fill_diagonal(distance_matrix, 0)  # Distância de um time para si mesmo é 0
    
    for i in range(num_teams):
        for j in range(i+1, num_teams):
            distance_matrix[j][i] = distance_matrix[i][j]  # Garante que a matriz seja simétrica
    
    return distance_matrix

# Exemplo de geração de matriz de distâncias para 20 times
# distance_matrix = generate_distance_matrix(20)

# Exibir a matriz de distâncias gerada
print("Matriz de Distâncias (20 Times):")
# print(distance_matrix)
def print_schedule(schedule):
    num_teams = len(schedule)
    
    for team in range(num_teams):
        print(f"Confrontos Time {team + 1}:")
        for round_index, opponent in enumerate(schedule[team]):
            if opponent > 0:
                print(f"  - Rodada {round_index + 1}: Contra Time {opponent} (Casa)")
            else:
                print(f"  - Rodada {round_index + 1}: Contra Time {-opponent} (Fora)")
        print()  # Linha em branco entre os times




# Exemplo de execução
if __name__ == "__main__":
    # Exemplo de matriz de distâncias (6 equipes)
    distance_matrix = np.array([
        [0, 10, 20, 30, 40, 50],
        [10, 0, 15, 25, 35, 45],
        [20, 15, 0, 35, 25, 30],
        [30, 25, 35, 0, 20, 10],
        [40, 35, 25, 20, 0, 15],
        [50, 45, 30, 10, 15, 0]
    ])
    
    print("Rodando LAHC...")
    best_solution_lahc, best_cost_lahc = late_acceptance_hill_climbing(distance_matrix)
    # print("Melhor solução (LAHC):", best_solution_lahc, "Custo:", best_cost_lahc)
    print("Melhor solução (LAHC): Custo:", best_cost_lahc)
    print_schedule(best_solution_lahc)
    
    print("Rodando ILS...")
    best_solution_ils, best_cost_ils = iterated_local_search(distance_matrix)
    # print("Melhor solução (ILS):", best_solution_ils, "Custo:", best_cost_ils)
    print("Melhor solução (ILS): Custo:", best_cost_ils)
    print_schedule(best_solution_ils)
    
    print("Rodando SA...")
    best_solution_sa, best_cost_sa = simulated_annealing(distance_matrix)
    # print("Melhor solução (SA):", best_solution_sa, "Custo:", best_cost_sa)
    print("Melhor solução (SA): Custo:", best_cost_sa)
    print_schedule(best_solution_sa)
