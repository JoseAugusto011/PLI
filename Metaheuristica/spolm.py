import random
import numpy as np

# Função para calcular a distância total percorrida por um time
def calcular_custo_time(solucao, distancias):
    custo_total = 0
    for time, rodadas in enumerate(solucao):
        for rodada in range(len(rodadas)):
            adversario = solucao[time][rodada]
            if adversario > 0:  # Jogou em casa
                custo_total += distancias[time][adversario - 1]
            else:  # Jogou fora de casa
                custo_total += distancias[abs(adversario) - 1][time]
    return custo_total

# Geração da solução inicial com base nas restrições de mandos de campo
def gerar_solucao_inicial(n_times):
    solucao = np.zeros((n_times, n_times-1), dtype=int)
    
    # Gera a solução inicial com as rodadas alternadas
    for time in range(n_times):
        for rodada in range(n_times-1):
            adversario = (time + rodada) % n_times
            if adversario == time:
                adversario = n_times - 1  # Último adversário
            
            # Alterna mando de campo
            if rodada % 2 == 0:
                solucao[time][rodada] = adversario + 1
            else:
                solucao[time][rodada] = -(adversario + 1)
    
    return solucao

# Função de avaliação da solução
def avaliar_solucao(solucao, distancias, penalidade):
    custo_total = calcular_custo_time(solucao, distancias)
    
    # Penaliza soluções que violam restrições (exemplo: jogos consecutivos em casa/fora)
    violacoes = 0
    for time in range(len(solucao)):
        consecutivos = 0
        for rodada in range(1, len(solucao[time])):
            if (solucao[time][rodada] > 0 and solucao[time][rodada-1] > 0) or (solucao[time][rodada] < 0 and solucao[time][rodada-1] < 0):
                consecutivos += 1
            else:
                consecutivos = 0
            if consecutivos >= 2:
                violacoes += 1
    
    return custo_total + (penalidade * violacoes)

# Movimentos de vizinhança
def swap_rounds(solucao):
    i, j = random.sample(range(solucao.shape[1]), 2)
    nova_solucao = solucao.copy()
    nova_solucao[:, [i, j]] = nova_solucao[:, [j, i]]
    return nova_solucao

def swap_teams(solucao):
    i, j = random.sample(range(solucao.shape[0]), 2)
    nova_solucao = solucao.copy()
    nova_solucao[[i, j], :] = nova_solucao[[j, i], :]
    return nova_solucao

def swap_homes(solucao):
    time = random.choice(range(solucao.shape[0]))
    rodada = random.choice(range(solucao.shape[1]))
    nova_solucao = solucao.copy()
    nova_solucao[time, rodada] *= -1
    return nova_solucao

def replace_teams(solucao):
    i, j = random.sample(range(solucao.shape[0]), 2)
    nova_solucao = solucao.copy()
    nova_solucao[i], nova_solucao[j] = nova_solucao[j], nova_solucao[i]
    return nova_solucao

# Método randômico de descida
def metodo_randomico_descida(solucao, distancias, penalidade, max_iter=1000):
    melhor_solucao = solucao.copy()
    melhor_avaliacao = avaliar_solucao(solucao, distancias, penalidade)
    
    for _ in range(max_iter):
        vizinho = random.choice([swap_rounds, swap_teams, swap_homes, replace_teams])(melhor_solucao)
        avaliacao_vizinho = avaliar_solucao(vizinho, distancias, penalidade)
        
        if avaliacao_vizinho < melhor_avaliacao:
            melhor_solucao = vizinho
            melhor_avaliacao = avaliacao_vizinho
    
    return melhor_solucao, melhor_avaliacao

# Iterated Local Search (ILS)
def iterated_local_search(solucao_inicial, distancias, penalidade, max_iter_ils=100):
    melhor_solucao = solucao_inicial
    melhor_avaliacao = avaliar_solucao(solucao_inicial, distancias, penalidade)
    
    for _ in range(max_iter_ils):
        nova_solucao, nova_avaliacao = metodo_randomico_descida(melhor_solucao, distancias, penalidade)
        
        if nova_avaliacao < melhor_avaliacao:
            melhor_solucao = nova_solucao
            melhor_avaliacao = nova_avaliacao
    
    return melhor_solucao, melhor_avaliacao


if __name__ == "__main__":
    # Distâncias hipotéticas entre os times (matriz de distâncias)
    n_times = 6
    distancias = np.array([[105, 163, 334, 479, 340, 322],
                           [264, 174, 265, 396, 202, 189],
                           [362, 202, 214, 102, 106, 378],
                           [119, 208, 385, 245, 332, 383],
                           [124, 238, 266, 214, 286, 346],
                           [221, 145, 371, 108, 208, 454]])
    
    # Parâmetros
    penalidade = 1000
    
    # Geração de solução inicial
    solucao_inicial = gerar_solucao_inicial(n_times)
    
    print("Solução Inicial:\n", solucao_inicial)
    
    # Aplicação do ILS
    melhor_solucao, melhor_avaliacao = iterated_local_search(solucao_inicial, distancias, penalidade)
    
    print("Melhor Avaliação:", melhor_avaliacao)
    print("Melhor Solução:\n", melhor_solucao)
    print("Custo Total:", calcular_custo_time(melhor_solucao, distancias))
    print("Custo Total com Penalidade:", avaliar_solucao(melhor_solucao, distancias, penalidade))
    print("Matriz de Distâncias:\n", distancias)
    