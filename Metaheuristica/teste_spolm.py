import numpy as np
import random
import pandas as pd
import time
from spolm import *

tamanho_rol = 5
n0 = 5
nn = 20
# Instância do  n° de times ---> Lista com 20 exemplos aleatórios de qtd de times
num_times = [random.randint(n0, nn) for _ in range(tamanho_rol)] # Gera 20 números aleatórios entre  n0 e nn
# Instância da matriz de distâncias
p0 = 50
pn = 1000
# Gera 20 matrizes de distâncias aleatórias para cada quantidade de times com valores entre p0 e pn
matriz_distancias = [np.random.randint(p0, pn, size=(n, n)) for n in num_times] 

penalidade = 1000

solucao_inicial = [gerar_solucao_inicial(n) for n in num_times]


melhores_solucoes = []
melhores_avaliacoes = []
delta_t = []

# Realizar teste e coletar resultados



for i in range(len(num_times)):
    # rodar iterated_local_search
    print(f"\n_________________________Testes Instancia: {i}_____________________________\n")
    tempo_inicio = time.time()
    melhor_solucao, melhor_avaliacao = iterated_local_search(solucao_inicial[i], matriz_distancias[i], penalidade)
    tempo_fim = time.time()
    tempo_total = tempo_fim - tempo_inicio

    melhores_solucoes.append(melhor_solucao)
    melhores_avaliacoes.append(melhor_avaliacao)
    delta_t.append(tempo_total)

lista_n0 = [n0] * tamanho_rol
lista_nn = [nn] * tamanho_rol
lista_p0 = [p0] * tamanho_rol
lista_pn = [pn] * tamanho_rol
lista_penalidade = [penalidade] * tamanho_rol

# Gerar um DataFrame com os resultados

resultados = {'num_times': num_times,"melhores_solucoes": melhores_solucoes, "melhores_avaliacoes": melhores_avaliacoes, "tempo_total": delta_t, "n0": lista_n0, "nn": lista_nn, "p0": lista_p0, "pn": lista_pn, "penalidade": lista_penalidade}

df_resultados = pd.DataFrame(resultados)
df_resultados.to_csv(f'resultados_spolm_len_{tamanho_rol}.csv', index=False)

#printar matriz de distancias

# for i in range(len(num_times)):
#     print(f"\n_________________________Testes Instancia: {num_times[i]}_____________________________\n")
#     print(f"Matriz de Distâncias (Times: {matriz_distancias[i]}):")