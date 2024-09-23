import pandas as pd
import time
from otimiza import Calendario



max_partidas_por_dia_por_time = 1

# Definindo hyperparâmetros do AG
num_equipes = 10
max_confrontos_por_dia = 10
taxa_crossover = 0.8
taxa_mutacao = 0.1
tamanho_populacao = 50
num_geracoes = 100

times_importantes = {}
dias_exclusos_para_times = {}

c = Calendario(
    num_equipes=num_equipes,
    max_partidas_por_dia_por_time=max_partidas_por_dia_por_time,
    max_confrontos_por_dia=max_confrontos_por_dia,
    times_importantes=times_importantes,
    dias_exclusos_para_time=dias_exclusos_para_times,
    tamanho_populacao=tamanho_populacao,
    num_geracoes=num_geracoes,
    taxa_crossover=taxa_crossover,
    taxa_mutacao=taxa_mutacao
)

# Amostras para teste
num_equipes1 = 20
resticao1 = {1:[(0,1),(2,3)],
            2:[(1,2)],
            }

num_equipes2 = 10
resticao2 = {7:[(0,1),(2,3)],
            8:[(1,2)],
            }

num_equipes3 = 9
resticao3 = {5:[(5,6),(0,2)],
            6:[(1,7)],
            7:[(0,1),(2,3)],
            8:[(1,2)],
            }

num_equipes4 = 10
resticao4 = {0:[(0,3)],
            1:[(0,2)],
            2:[(0,7)],
            3:[(0,1)],
            4:[(0,9)],
            5:[(0,6)],
            6:[(0,4)],
            7:[(0,5)],
            8:[(0,8)],
            }

num_equipes5 = 10
resticao5 = {2:[(1,3),(4,6)],
            3:[(5,6)],
            5:[(2,7)]}

num_equipes6 = 10
resticao6 = {1:[(0,1),(2,3),(4,5),(6,7),(8,9)],
            2:[(1,3),(4,6)],
            3:[(5,6)],
            5:[(2,7)]}

instancias_restricao = [resticao1, resticao2, resticao3, resticao4, resticao5, resticao6]
instancias_num_equipes = [num_equipes1, num_equipes2, num_equipes3, num_equipes4, num_equipes5, num_equipes6]

# realizar teste e coletar resultados
resultados = []

for i in range(len(instancias_restricao)):
    print(f"\n_________________________Testes Instancia: {i}_____________________________\n")

    tempo_inicio = time.time()
    grade = c.main_criar_tabela_com_restricoes(instancias_num_equipes[i], instancias_restricao[i])
    tempo_fim = time.time()
    tempo_total = tempo_fim - tempo_inicio

    resultados.append({
        'num_equipes': instancias_num_equipes[i],
        'num_rodadas': len(grade),
        'restricao': instancias_restricao[i],
        'tempo': tempo_total,
        'Total_custo': c.return_penalidade()
    })

    # c.grade = grade.copy()
    # c.show_grade()

# Converter a lista de dicionários para um DataFrame
df_resultado = pd.DataFrame(resultados)

# Salvar o DataFrame em um arquivo CSV
df_resultado.to_csv('resultados.csv', index=False)
