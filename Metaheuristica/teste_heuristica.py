import numpy as np
import random
import pandas as pd
import time
from heuristica import *

tamanho_rol = 20 # tamanho do rol de instâncias

e0 = 5 # número de equipes inicial
en = 15 # número de equipes final

# lista do len do rol de equipes com o número de equipes no intervalo de e0 a en aleatório
lista_qtd_times_rol = [random.randint(e0, en) for i in range(tamanho_rol)]
# para cada quantidade de equipes no rol, gera uma matriz de distâncias aleatória
d0 = 50 # distância mínima
dn = 1000 # distância máxima
lista_matriz_distancias = [generate_distance_matrix(qtd_times, dn) for qtd_times in lista_qtd_times_rol]

lahc_custos = []
sa_custos = []
ils_custos = []

lahc_grid_results = []
sa_grid_results = []
ils_grid_results = []

lahc_tempo = []
sa_tempo = []
ils_tempo = []

for i in range(tamanho_rol):

    print(f"\n_________________________Testes Instancia: {i}__________{lista_qtd_times_rol[i]}___________________\n")

    time_start = time.time()
    best_solution_lahc, best_cost_lahc = late_acceptance_hill_climbing(lista_matriz_distancias[i])
    time_end = time.time()
    tempo_total = time_end - time_start
    lahc_tempo.append(tempo_total)
    lahc_grid_results.append(best_solution_lahc)
    lahc_custos.append(best_cost_lahc)

    time_start = time.time()
    best_solution_sa, best_cost_sa = simulated_annealing(lista_matriz_distancias[i])
    time_end = time.time()
    tempo_total = time_end - time_start
    sa_tempo.append(tempo_total)
    sa_grid_results.append(best_solution_sa)
    sa_custos.append(best_cost_sa)

    time_start = time.time()
    best_solution_ils, best_cost_ils = iterated_local_search(lista_matriz_distancias[i])
    time_end = time.time()
    tempo_total = time_end - time_start
    ils_tempo.append(tempo_total)
    ils_grid_results.append(best_solution_ils)
    ils_custos.append(best_cost_ils)


lista_e0 = [e0] * tamanho_rol
lista_en = [en] * tamanho_rol
lista_d0 = [d0] * tamanho_rol
lista_dn = [dn] * tamanho_rol


resultados = {'qtd_times': lista_qtd_times_rol,"lahc_grid_results": lahc_grid_results, "lahc_custos": lahc_custos, "lahc_tempo": lahc_tempo, "sa_grid_results": sa_grid_results, "sa_custos": sa_custos, "sa_tempo": sa_tempo, "ils_grid_results": ils_grid_results, "ils_custos": ils_custos, "ils_tempo": ils_tempo, "e0": lista_e0, "en": lista_en, "d0": lista_d0, "dn": lista_dn}

df_resultados = pd.DataFrame(resultados)
df_resultados.to_csv(f'resultados_heuristica_len_{tamanho_rol}.csv', index=False)