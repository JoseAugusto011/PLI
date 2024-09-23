import random
import numpy as np

class Calendario:
    def __init__(self, num_equipes, max_partidas_por_dia_por_time, max_confrontos_por_dia,
                 times_importantes, dias_exclusos_para_time, tamanho_populacao,
                 num_geracoes, taxa_crossover, taxa_mutacao):
        self.num_equipes = num_equipes
        self.max_confrontos_por_dia = max_confrontos_por_dia
        self.times_importantes = times_importantes
        self.taxa_crossover = taxa_crossover
        self.taxa_mutacao = taxa_mutacao

        self.max_partidas_por_dia_por_time = max_partidas_por_dia_por_time
        self.dias_exclusos_para_times = dias_exclusos_para_time
        self.grade = []  # Matriz dos jogos que precisa ser ordenada
        self.erro_por_dia = [0 for _ in range(self.num_equipes - 1)]  # Lista com o erro de cada dia

        self.tamanho_populacao = tamanho_populacao  
        self.num_geracoes = num_geracoes

    # Grade inicial - Gulosos
    def gerar_grade_inicial(self):  # criar todas as possibilidades - resultado pode ser infeasible
        grade = []
        possibilidades = []
        for i in range(self.num_equipes - 1):
            for j in range(i + 1, self.num_equipes):
                possibilidades.append((i, j))

        if self.max_partidas_por_dia_por_time * self.num_equipes / 2 < self.max_confrontos_por_dia:
            limite_de_jogos = self.max_partidas_por_dia_por_time * self.num_equipes // 2
        else:
            limite_de_jogos = self.max_confrontos_por_dia

        random.shuffle(possibilidades)
        contador = 0
        dia = []
        for jogo in possibilidades:
            dia.append(jogo)
            contador += 1
            if contador == limite_de_jogos:
                grade.append(dia)
                contador = 0
                dia = []
        if dia:
            grade.append(dia)
        return grade
    
    def gerar_grade_inicial_priorizando_importantes_e_exclusivos(self):
        # Ajusta o número máximo de confrontos por dia com base nas restrições
        limite_por_time = self.max_partidas_por_dia_por_time * self.num_equipes // 2
        if limite_por_time < self.max_confrontos_por_dia:
            self.max_confrontos_por_dia = limite_por_time

        # Verifica se o número de equipes é ímpar e adiciona uma equipe fictícia (bye)
        Impar = False
        if self.num_equipes % 2 == 1:
            self.num_equipes += 1
            Impar = True

        grade = []  # Lista que armazenará os confrontos por dia
        confrontos_ja_feitos = set()  # Confrontos já alocados para evitar duplicação

        # 1. Agendar os confrontos importantes primeiro
        dias_importantes = sorted(self.times_importantes.keys())
        for dia in dias_importantes:
            dia_confrontos = []

            # Adiciona confrontos importantes do dia, se ainda não foram feitos
            importantes_dia = self.times_importantes.get(dia, [])
            for confronto in importantes_dia:
                if confronto not in confrontos_ja_feitos:
                    dia_confrontos.append(confronto)
                    confrontos_ja_feitos.add(confronto)

            # Obtém as exclusões para o dia atual
            exclusoes_dia = self.dias_exclusos_para_times.get(dia, [])

            # Encontra confrontos restantes que não envolvam os times excluídos e ainda não foram feitos
            restantes = [
                (i, j) for i in range(self.num_equipes)
                for j in range(i + 1, self.num_equipes)
                if (i, j) not in confrontos_ja_feitos and i not in exclusoes_dia and j not in exclusoes_dia
            ]

            random.shuffle(restantes)  # Embaralha para distribuir os confrontos de forma aleatória

            # Preenche o dia com confrontos adicionais até atingir o limite
            for confronto in restantes:
                if len(dia_confrontos) < self.max_confrontos_por_dia:
                    dia_confrontos.append(confronto)
                    confrontos_ja_feitos.add(confronto)
                else:
                    break

            grade.append(dia_confrontos)

        # 2. Agendar os confrontos restantes em dias adicionais
        # Calcula todos os confrontos possíveis
        todos_confrontos = set(
            (i, j) for i in range(self.num_equipes)
            for j in range(i + 1, self.num_equipes)
        )

        # Determina os confrontos que ainda não foram alocados
        confrontos_restantes = list(todos_confrontos - confrontos_ja_feitos)
        random.shuffle(confrontos_restantes)  # Embaralha para distribuir aleatoriamente

        dia_atual = len(grade) + 1  # Inicia a contagem de dias após os dias importantes

        while confrontos_restantes:
            dia_confrontos = []

            # Obtém as exclusões para o dia atual, se houver
            exclusoes_dia = self.dias_exclusos_para_times.get(dia_atual, [])

            # Filtra os confrontos possíveis que não envolvam times excluídos
            confrontos_possiveis = [
                confronto for confronto in confrontos_restantes
                if confronto[0] not in exclusoes_dia and confronto[1] not in exclusoes_dia
            ]

            random.shuffle(confrontos_possiveis)  # Embaralha novamente para aleatoriedade

            # Preenche o dia com confrontos possíveis até atingir o limite
            for confronto in confrontos_possiveis:
                if len(dia_confrontos) < self.max_confrontos_por_dia:
                    dia_confrontos.append(confronto)
                    confrontos_restantes.remove(confronto)
                else:
                    break

            # Adiciona o dia à grade apenas se houver confrontos alocados
            if dia_confrontos:
                grade.append(dia_confrontos)

            dia_atual += 1  # Incrementa o dia para a próxima iteração

        # 3. Remove a equipe fictícia se o número de equipes era ímpar
        if Impar:
            self.num_equipes -= 1

        return grade

    def gerar_grade_inicial_padronizada(self):
        # Ajustar o max_confrontos_por_dia
        if self.max_partidas_por_dia_por_time * self.num_equipes / 2 < self.max_confrontos_por_dia:
            self.max_confrontos_por_dia = self.max_partidas_por_dia_por_time * self.num_equipes // 2

        # Verificar se o número de times é ímpar
        Impar = False
        if self.num_equipes % 2 == 1:
            self.num_equipes += 1
            Impar = True

        # Programa principal
        self.grade = []
        for i in range(self.num_equipes - 2):
            pen = [(0, i + 1)]  # o primeiro time joga com todos os outros
            self.grade.append(pen)

        if not Impar:
            self.grade.append([(0, self.num_equipes - 1)])
        if Impar:
            self.grade.append([])

        for i in range(1, self.num_equipes):
            inicio = i * 2 - 1 
            for j in range(i + 1, self.num_equipes):
                checar = inicio + j - i - 1
                if checar == inicio:
                    checar %= self.num_equipes - 1
                    if not Impar:
                        self.grade[checar].append((i, self.num_equipes - 1))
                else:
                    checar %= self.num_equipes - 1
                    self.grade[checar].append((i, j - 1))

        # Remove a equipe fictícia se necessário
        if Impar:
            self.num_equipes -= 1

        return self.grade

    # Funções de avaliação

    def restricao_max_partidas_por_dia_por_time_grade(self, grade):
        penalidade = 0
        for i in range(self.num_equipes):  # para cada time
            contador = 0
            for jogo in grade:  # conta quantos jogos ele tem no dia
                if i in jogo:
                    contador += 1
            if contador > self.max_partidas_por_dia_por_time:  # se for maior que o permitido, soma a penalidade
                penalidade += contador - self.max_partidas_por_dia_por_time
        return penalidade

    def restricao_max_confrontos_por_dia_grade(self, grade):
        penalidade = 0
        contador = len(grade)
        if contador > self.max_confrontos_por_dia:
            penalidade += contador - self.max_confrontos_por_dia
        return penalidade

    def restricao_times_importantes_grade(self, grade_dia_i, importantes_dia_i):
        penalidade = 0
        for confronto in importantes_dia_i:
            if confronto not in grade_dia_i:
                penalidade += 1
        return penalidade

    def restricao_times_exclusivos_grade(self, grade_dia_i, exclusivos_dia_i):
        penalidade = 0
        for time in exclusivos_dia_i:
            for jogo in grade_dia_i:
                if time in jogo:
                    penalidade += 1
                    break
        return penalidade

    def avaliar_grade_dia_i(self, grade_dia_i, dia):
        importantes_dia_i = self.times_importantes.get(dia, [])
        penalidade = 0

        penalidade += self.restricao_max_partidas_por_dia_por_time_grade(grade_dia_i) * 10
        penalidade += self.restricao_max_confrontos_por_dia_grade(grade_dia_i) * 10
        penalidade += self.restricao_times_importantes_grade(grade_dia_i, importantes_dia_i) * 20
        penalidade += self.restricao_times_exclusivos_grade(grade_dia_i, self.dias_exclusos_para_times.get(dia, [])) * 20

        return penalidade

# Métodos para reorganizar a grade - Movimentos
    def swap_confrontos(self, grade):
        # Seleciona dois dias com penalidade > 0
        dias_com_penalidade = [i for i, penalidade in enumerate(self.erro_por_dia) if penalidade > 0]
        if len(dias_com_penalidade) < 2:
            return grade  # Não há dias suficientes para trocar

        dia1, dia2 = random.sample(dias_com_penalidade, 2)

        # Seleciona um jogo aleatório de cada dia
        if grade[dia1] and grade[dia2]:
            jogo1 = random.choice(grade[dia1])
            jogo2 = random.choice(grade[dia2])

            # Troca os jogos entre os dias
            grade[dia1].remove(jogo1)
            grade[dia1].append(jogo2)

            grade[dia2].remove(jogo2)
            grade[dia2].append(jogo1)

        return grade

    def swap_dias(self, grade):
        if len(grade) < 2:
            return grade  # Não há dias suficientes para trocar

        dia1, dia2 = random.sample(range(len(grade)), 2)
        grade[dia1], grade[dia2] = grade[dia2], grade[dia1]
        return grade

    def move_game(self, grade):
        dia_origem, dia_destino = random.sample(range(len(grade)), 2)
        if grade[dia_origem]:
            jogo = random.choice(grade[dia_origem])
            grade[dia_origem].remove(jogo)
            grade[dia_destino].append(jogo)
        return grade

    def rearranjar_e_minimizar_penalidade(self):
        # Avaliar a penalidade inicial da grade atual
        self.erro_por_dia = [self.avaliar_grade_dia_i(dia, dia_idx + 1) 
                             for dia_idx, dia in enumerate(self.grade)]
        penalidade_inicial = sum(self.erro_por_dia)
        melhor_penalidade = penalidade_inicial
        melhor_grade = self.grade.copy()
        
        for _ in range(1000):  # Executa 1000 iterações de rearranjos
            nova_grade = self.swap_confrontos(self.grade.copy())
            penalidade_atual = sum([self.avaliar_grade_dia_i(dia, dia_idx + 1) 
                                    for dia_idx, dia in enumerate(nova_grade)])  # Penalidade total da nova grade

            if penalidade_atual == 0:  # Se a penalidade for 0, não há necessidade de continuar
                melhor_penalidade = 0
                melhor_grade = nova_grade.copy()
                break

            if penalidade_atual < melhor_penalidade:
                melhor_penalidade = penalidade_atual
                melhor_grade = nova_grade.copy()

        # Atualizar a grade para a melhor encontrada
        self.grade = melhor_grade.copy()
        self.erro_por_dia = [self.avaliar_grade_dia_i(dia, dia_idx + 1) 
                             for dia_idx, dia in enumerate(self.grade)]
        return melhor_grade, melhor_penalidade

    # Mutação e cruzamento
    def crossover(self, grade1, grade2):
        # Extrai apenas a grade (primeiro elemento da tupla)
        grade1 = grade1[0]
        grade2 = grade2[0]
        
        # Verifica se as grades são grandes o suficiente
        if len(grade1) <= 2 or len(grade2) <= 2:
            # Se as grades forem muito pequenas, apenas retorna uma cópia de uma das grades
            return grade1[:]
        
        # Seleciona um ponto de corte aleatório
        ponto_corte = random.randint(1, min(len(grade1), len(grade2)) - 1)
        
        # Cria uma nova grade com a parte inicial da grade1 e a parte final da grade2
        nova_grade = grade1[:ponto_corte] + grade2[ponto_corte:]
        
        return nova_grade

    def mutar(self, grade):
        # Aplica uma mutação aleatória, pode ser um swap ou mover um confronto
        if random.random() < self.taxa_mutacao:
            return self.swap_confrontos(grade)
        else:
            return self.swap_dias(grade)

    def selecionar_pais(self, k=3):
        # Seleção por torneio
        selecionados = []
        for _ in range(2):
            competidores = random.sample(self.populacao, k)
            vencedor = min(competidores, key=lambda x: x[1])
            selecionados.append(vencedor)
        return selecionados

    def evoluir(self):
        for geracao in range(self.num_geracoes):
            nova_populacao = []
            
            for _ in range(self.tamanho_populacao // 2):
                # Seleciona dois indivíduos (grades) usando seleção por torneio
                pais = self.selecionar_pais()
                pai1, pai2 = pais[0], pais[1]
                
                if random.random() < self.taxa_crossover:
                    # Aplica crossover
                    filho = self.crossover(pai1, pai2)
                else:
                    filho = pai1[0].copy()  # Copia o primeiro pai se não houver crossover
                
                # Aplica mutação
                filho = self.mutar(filho)
                
                # Avalia a nova grade
                penalidade_filho = sum([self.avaliar_grade_dia_i(dia, dia_idx + 1) 
                                        for dia_idx, dia in enumerate(filho)])
                
                nova_populacao.append((filho, penalidade_filho))
            
            # Combina a população antiga com a nova e seleciona os melhores
            self.populacao += nova_populacao
            self.populacao = sorted(self.populacao, key=lambda x: x[1])[:self.tamanho_populacao]

    def inicializar_populacao(self):
        self.populacao = []
        for _ in range(self.tamanho_populacao):
            # Gera uma grade inicial e minimiza penalidade
            grade = self.gerar_grade_inicial()
            grade_minimizada, penalidade = self.rearranjar_e_minimizar_penalidade()
            # Adiciona à população
            self.populacao.append((grade_minimizada, penalidade))

    # Funções auxiliares - print

    def show_grade(self):
        for dia_idx, dia in enumerate(self.grade):
            print(dia, " penalidade --> ", self.erro_por_dia[dia_idx])
        print("Penalidade total: ", self.return_penalidade())

    def return_penalidade(self):
        return sum(self.erro_por_dia)

    # Alg. Gulloso - Solução Ótima Garantida - Arthur

    def show_inviabilidades(self, inviabilidades):
        for i in range(len(inviabilidades)):
            print(inviabilidades[i])

    def criar_tabela(self,num_equipes):
        # na ocasião de o numero de times ser impar
        Impar = False
        if num_equipes%2 == 1:
            num_equipes+=1
            Impar = True

        # o programa principal
        mat = []
        for i in range(num_equipes-2):
            pen =[(0,i+1)]
            mat.append(pen)

        if not Impar:
            mat.append([(0,num_equipes-1)])
        if  Impar:
            mat.append([])


        for i in range(1,num_equipes):
            inicio = i*2-1 
            checar = inicio
            for j in range(i+1,num_equipes):
                if (checar == inicio):
                    checar%=num_equipes-1
                    if not Impar:
                        mat[checar].append((i,num_equipes-1))
                else:
                    checar%=num_equipes-1
                    mat[checar].append((i,j-1))
                checar+=1

        return(mat)

    def achar_vazio(self,num_equipes,times_associados,ver_associados,lista_rep,time,visto,unicos,mat):
        r  = 0
        entrou = False
        while True:
            if r == num_equipes:
                if unicos:
                    return(False, 0,0,0,0)
                r = 0
                unicos = True

            if (times_associados[r] == -1) and ((len(lista_rep[r]) > 0) or unicos):

                posi_x = 0
                while True:
                    if posi_x not in times_associados:
                        times_associados[r] = posi_x
                        ver_associados.append(r)

                        retorno, ta,uni,vis,va = self.associar(num_equipes,times_associados,ver_associados,lista_rep,time,visto,unicos,mat)

                        if retorno:
                            return(True, ta,uni,vis,va)
                        
                        times_associados[r] = -1

                    posi_x+=1
                    if posi_x == num_equipes:
                        return(False, 0,0,0,0)

            r+=1

    def associar(self,num_equipes,times_associados,ver_associados,lista_rep,time,visto,unicos,mat):
        while len(visto) < num_equipes:

            # achar um outro chute
            if len(ver_associados) == 0:
                retorno, ta,uni,vis,va = self.achar_vazio(num_equipes,times_associados,ver_associados,lista_rep,time,visto,unicos,mat)
                if not retorno:
                    return(False, 0,0,0,0)
                else:
                    times_associados = ta
                    unicos = uni
                    visto = vis
                    ver_associados = va
    
            

            if len(ver_associados) > 0:
                time = ver_associados.pop(0)

                valor_associado_time = times_associados[time]

                for  posi in lista_rep[time]:

                    if posi[0][0] == time:
                        posi_time_atual = 0
                        posi_time_comparar = 1
                    else:
                        posi_time_atual = 1
                        posi_time_comparar = 0


                    if (posi[0][posi_time_comparar] not in visto) and (posi[0][posi_time_comparar] not in ver_associados):

                        for item in mat[posi[1]]:

                            if (valor_associado_time in item):

                                if item[0] == valor_associado_time:

                                    if item[1] in times_associados:
                                        return(False, 0,0,0,0)

                                    times_associados[posi[0][posi_time_comparar]] = item[1]

                                else:
                                    if item[0] in times_associados:
                                        return(False, 0,0,0,0)
                                    times_associados[posi[0][posi_time_comparar]]= item[0]

                                ver_associados.append(posi[0][posi_time_comparar])
                    
                    else:
                        if times_associados[posi[0][posi_time_comparar]] < times_associados[posi[0][posi_time_atual]]:
                            if (times_associados[posi[0][posi_time_comparar]],times_associados[posi[0][posi_time_atual]]) not in mat[posi[1]]:
                                return(False, 0,0,0,0)
                        else:
                            if (times_associados[posi[0][posi_time_atual]],times_associados[posi[0][posi_time_comparar]]) not in mat[posi[1]]:
                                return(False, 0,0,0,0)
            
                visto.append(time)
        
        return(True, times_associados,unicos,visto,ver_associados)

    def associacao(self,num_equipes,resticao,mat):

        lista_rep =[]

        for vc in range(num_equipes):
            lista_rep.append([])
        for x in resticao:
            for y in resticao[x]:
                lista_rep[y[0]].append([y,x])
                lista_rep[y[1]].append([y,x])
        maior = 0
        maior_valor =len(lista_rep[0])

        for x in range(1,len(lista_rep)):
            if len(lista_rep[x])> maior_valor:
                maior = x
                maior_valor = len(lista_rep[x])

                

        time = maior
        resposta =False

        for go in range(num_equipes):
            times_associados = np.full((num_equipes), -1)
            ver_associados = [maior]
            visto = []
            unicos = False
            times_associados[maior] = go
            retorno, ta,uni,vis,va = self.associar(num_equipes,times_associados,ver_associados,lista_rep,time,visto,unicos,mat)
            if retorno:
                return(True,ta)
        
        print("resposta não encontrada")
        return(False,times_associados)

    def main_criar_tabela_com_restricoes(self,num_equipes,resticao):
        
        mat = self.criar_tabela(num_equipes)
        retorno, ta = self.associacao(num_equipes,resticao,mat)

        if not retorno:
            print("resposta não encontrada")
            return(mat)
        
        times_alocados = []
        for _ in range(num_equipes):
            for x in range(num_equipes):
                if ta[x] == _:
                    times_alocados.append(x)
                    break

        mat
        lim_i = len(mat)
        lim_j = len(mat[0])

        for i in range(lim_i):
            for j in range(lim_j):
                mat[i][j] = (times_alocados[mat[i][j][0]],times_alocados[mat[i][j][1]])
        
        return(mat)
            
# def show_grade(c, grade):
#     # Mostra a grade
#     # recebe como a grade
#     for dia_idx, dia in enumerate(grade):
#         c.erro_por_dia[dia_idx] = c.avaliar_grade_dia_i(dia, dia_idx + 1)
#         print(dia, " penalidade --> ", c.erro_por_dia[dia_idx])
#     print("Penalidade total: ", sum(c.erro_por_dia))

# def show_inviabilidades(inviabilidades):
#     for i in range(len(inviabilidades)):
#         print(inviabilidades[i])
   

if __name__ == "__main__":

    # chave é o dia e o valor é uma lista com os confrontos importantes que devem jogar obrigatoriamente naquele dia
    times_importantes  = {
        1: [(0,1), (2,3), (4,5), (6,7)],
        2: [(0,2), (1,3), (4,6), (5,7)],
        3: [(0,3), (1,2), (4,7), (5,6)],
        4: [(0,4), (1,5), (2,6), (3,7)],
        5: [(0,5), (1,4), (2,7), (3,6)]
    }
    # times_importantes = {}

    dias_exclusos_para_times = {}  # chave é o dia e o valor é uma lista com os times que não podem jogar naquele dia
    # dias_exclusos_para_times = {1: [0,2,1,3,4,6,5,7], ...}

    max_partidas_por_dia_por_time = 1


    # Definindo hyperparâmetros do AG
    num_equipes = 10
    max_confrontos_por_dia = 10
    taxa_crossover = 0.8
    taxa_mutacao = 0.1
    tamanho_populacao = 50
    num_geracoes = 100

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

    print("\n_________________________Grade Inicial_____________________________\n")

    # Gerar e mostrar a grade inicial padronizada
    # grade = c.gerar_grade_inicial_padronizada()
    grade = c.main_criar_tabela_com_restricoes(num_equipes, times_importantes)
    c.grade = grade.copy()
    c.show_grade()
    print("\n_________________________Movimentos Simples_____________________________\n")

    # # chamar função rearranjar e minimizar penalidade
    grade_minimizada, penalidade = c.rearranjar_e_minimizar_penalidade()
    # show_grade(c, grade_minimizada)
    c.grade = grade_minimizada.copy()
    c.show_grade()

    print("\n__________________________Algoritmo Genético____________________________\n")


    c.grade = grade.copy()

    # # Inicializa a população com grades minimizadas
    c.inicializar_populacao()

    # # Executa a evolução
    c.evoluir()


    # Mostra a melhor grade
    melhor_grade, menor_penalidade = min(c.populacao, key=lambda x: x[1])
    c.grade = melhor_grade.copy()
    c.show_grade()

