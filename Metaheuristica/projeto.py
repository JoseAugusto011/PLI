import random

class Calendario:
    def __init__(self, num_equipes, max_confrontos_por_dia, times_importantes, max_partidas_por_dia_por_time):
        self.num_equipes = num_equipes
        self.max_confrontos_por_dia = max_confrontos_por_dia
        self.times_importantes = times_importantes
        self.max_partidas_por_dia_por_time = max_partidas_por_dia_por_time

        if not self.num_equipes >= 2 * self.max_confrontos_por_dia:
            self.max_confrontos_por_dia = self.max_confrontos_por_dia // 2
            print("Alteração no número de confrontos por dia para atender a condição de num_equipes >= 2*max_confrontos_por_dia")

        if not self.max_partidas_por_dia_por_time < self.num_equipes:
            self.max_partidas_por_dia_por_time = self.num_equipes - 1
            print("Alteração no número de partidas por time por dia para atender a condição de max_partidas_por_dia_por_time < num_equipes")

        self.grade = self.gerar_grade_inicial()
        self.ajustar_partidas()

    def gerar_grade_inicial(self):
        grade = []
        confrontos_usados = set()
        for _ in range(self.num_equipes // 2):
            dia = []
            for _ in range(self.max_confrontos_por_dia):
                while True:
                    time1, time2 = random.sample(range(self.num_equipes), 2)
                    confronto = (min(time1, time2), max(time1, time2))
                    if confronto not in confrontos_usados:
                        dia.append(confronto)
                        confrontos_usados.add(confronto)
                        break
            grade.append(dia)
        return grade

    def ajustar_partidas(self):
        partidas = {i: 0 for i in range(self.num_equipes)}
        for dia in self.grade:
            for confronto in dia:
                partidas[confronto[0]] += 1
                partidas[confronto[1]] += 1

        media = sum(partidas.values()) // self.num_equipes
        for time, num_jogos in partidas.items():
            if num_jogos < media:
                deficit = media - num_jogos
                for _ in range(deficit):
                    for dia in self.grade:
                        if len(dia) < self.max_confrontos_por_dia:
                            time2 = random.choice([t for t in range(self.num_equipes) if t != time])
                            confronto = (min(time, time2), max(time, time2))
                            if confronto not in [c for c in dia]:
                                dia.append(confronto)
                                partidas[time] += 1
                                partidas[time2] += 1
                                break

        # Corrigir limites de partidas por dia
        self.grade = self.corrigir_max_partidas_por_dia(self.grade)

    def cruzar(self, outro):
        ponto_corte = random.randint(0, len(self.grade))
        filho1_grade = self.grade[:ponto_corte] + outro.grade[ponto_corte:]
        filho2_grade = outro.grade[:ponto_corte] + self.grade[ponto_corte:]

        filho1_grade = self.corrigir_max_partidas_por_dia(filho1_grade)
        filho2_grade = self.corrigir_max_partidas_por_dia(filho2_grade)

        filho1 = Calendario(self.num_equipes, self.max_confrontos_por_dia, self.times_importantes, self.max_partidas_por_dia_por_time)
        filho1.grade = filho1_grade

        filho2 = Calendario(self.num_equipes, self.max_confrontos_por_dia, self.times_importantes, self.max_partidas_por_dia_por_time)
        filho2.grade = filho2_grade

        return filho1, filho2

    def corrigir_max_partidas_por_dia(self, grade):
        nova_grade = []
        for dia in grade:
            partidas_por_time = {i: 0 for i in range(self.num_equipes)}
            novo_dia = []
            for confronto in dia:
                time1, time2 = confronto
                if (partidas_por_time[time1] < self.max_partidas_por_dia_por_time and 
                    partidas_por_time[time2] < self.max_partidas_por_dia_por_time):
                    novo_dia.append(confronto)
                    partidas_por_time[time1] += 1
                    partidas_por_time[time2] += 1
            if novo_dia:
                nova_grade.append(novo_dia)

        return nova_grade

    def mutar(self):
        dia1_idx, dia2_idx = random.sample(range(len(self.grade)), 2)
        dia1 = self.grade[dia1_idx]
        dia2 = self.grade[dia2_idx]

        if not dia1 or not dia2:
            return

        confronto1 = random.choice(dia1)
        confronto2 = random.choice(dia2)

        dia1_temp = dia1.copy()
        dia2_temp = dia2.copy()
        dia1_temp.remove(confronto1)
        dia2_temp.remove(confronto2)
        dia1_temp.append(confronto2)
        dia2_temp.append(confronto1)

        if self.verificar_limite_partidas(dia1_temp) and self.verificar_limite_partidas(dia2_temp):
            self.grade[dia1_idx] = dia1_temp
            self.grade[dia2_idx] = dia2_temp

        self.ajustar_partidas()

    def verificar_limite_partidas(self, dia):
        partidas_por_time = {i: 0 for i in range(self.num_equipes)}
        for confronto in dia:
            time1, time2 = confronto
            partidas_por_time[time1] += 1
            partidas_por_time[time2] += 1
        return all(count <= self.max_partidas_por_dia_por_time for count in partidas_por_time.values())

    def avaliar(self):
        penalidade = 0
        confrontos_usados = set()
        
        for (time1, time2), rodadas in self.times_importantes.items():
            presente = False
            for rodada in rodadas:
                if rodada - 1 < len(self.grade) and (time1, time2) in self.grade[rodada - 1]:
                    presente = True
                    break
            if not presente:
                penalidade += 10

        for dia in self.grade:
            partidas_por_time = {}
            for confronto in dia:
                time1, time2 = confronto
                partidas_por_time[time1] = partidas_por_time.get(time1, 0) + 1
                partidas_por_time[time2] = partidas_por_time.get(time2, 0) + 1
                if confronto in confrontos_usados:
                    penalidade += 15  # Penalidade por confrontos repetidos
                confrontos_usados.add(confronto)
            for count in partidas_por_time.values():
                if count > self.max_partidas_por_dia_por_time:
                    penalidade += (count - self.max_partidas_por_dia_por_time) * 5

        return len(self.grade) + penalidade

    def verificar_calendario_valido(self):
        for dia in self.grade:
            partidas_por_time = {}
            for confronto in dia:
                time1, time2 = confronto
                partidas_por_time[time1] = partidas_por_time.get(time1, 0) + 1
                partidas_por_time[time2] = partidas_por_time.get(time2, 0) + 1
            if any(count > self.max_partidas_por_dia_por_time for count in partidas_por_time.values()):
                return False
        return True

    def __str__(self) -> str:
        resultado = []
        for dia_num, confrontos in enumerate(self.grade):
            confrontos_str = ', '.join([f"{c[0]} vs {c[1]}" for c in confrontos])
            resultado.append(f"Dia {dia_num + 1}: {confrontos_str}")
        return '\n'.join(resultado)

def gerar_populacao_inicial(tamanho_populacao, num_equipes, max_confrontos_por_dia, times_importantes, max_partidas_por_dia_por_time):
    return [Calendario(num_equipes, max_confrontos_por_dia, times_importantes, max_partidas_por_dia_por_time) for _ in range(tamanho_populacao)]

def avaliar_populacao(populacao):
    return [individuo.avaliar() for individuo in populacao]

def selecao(populacao):
    torneio = random.sample(populacao, 3)
    torneio.sort(key=lambda x: x.avaliar())
    return torneio[0], torneio[1]

def crossover(pai1, pai2):
    return pai1.cruzar(pai2)

def mutacao(individuo):
    individuo.mutar()

def selecionar_sobreviventes(populacao_antiga, nova_populacao):
    populacao_combinada = populacao_antiga + nova_populacao
    populacao_combinada.sort(key=lambda x: x.avaliar())
    return populacao_combinada[:len(populacao_antiga)]

def obter_melhor_individuo(populacao):
    return min(populacao, key=lambda x: x.avaliar())

def somar(lista):
    return sum(lista)

# Definindo hyperparâmetros do AG
num_equipes = 10
max_confrontos_por_dia = 10
times_importantes = {}
max_partidas_por_dia_por_time = 1

taxa_crossover = 0.8
taxa_mutacao = 0.1
tamanho_populacao = 50
num_geracoes = 100

# Inicialização
t = 0
populacao = gerar_populacao_inicial(tamanho_populacao, num_equipes, max_confrontos_por_dia, times_importantes, max_partidas_por_dia_por_time)

ultimos_5_avaliados = [0, 1, 2, 3, 4]
contador = 0
anterior = 0

# Loop principal do AG
while t < num_geracoes:
    t += 1

    # Seleção e reprodução
    nova_populacao = []
    for _ in range(tamanho_populacao // 2):
        pai1, pai2 = selecao(populacao)

        if random.random() < taxa_crossover:
            filho1, filho2 = crossover(pai1, pai2)
        else:
            filho1, filho2 = pai1, pai2

        if random.random() < taxa_mutacao:
            mutacao(filho1)
        if random.random() < taxa_mutacao:
            mutacao(filho2)

        nova_populacao.append(filho1)
        nova_populacao.append(filho2)

    # Avaliação da nova população
    x_total = avaliar_populacao(nova_populacao)
    populacao = selecionar_sobreviventes(populacao, nova_populacao)

    parar_forcado = False
    for x in x_total:
        ultimos_5_avaliados[contador % 5] = abs(x - anterior)
        anterior = x
        contador += 1
        soma = somar(ultimos_5_avaliados)

        if soma == 0:
            print('Break')
            parar_forcado = True
            print(f"Convergência detectada na geração {t}. Parando...")
            break
        else:
            print("Somatório", soma)

    if parar_forcado:
        break

# Saída: melhor solução encontrada
melhor_solucao = obter_melhor_individuo(populacao)
print(f"\nValor da melhor solução: {melhor_solucao.avaliar()}")
print("\nMelhor solução encontrada:")

# Exibir o calendário final, com a grade de confrontos por dia
for dia, confrontos in enumerate(melhor_solucao.grade):
    print(f"Dia {dia + 1}: {confrontos}")
