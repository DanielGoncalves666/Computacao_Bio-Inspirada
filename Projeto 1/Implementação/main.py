import copy
import random
import time

TAXA_MUTACAO = 0.01
TAXA_CROSSOVER = 0.7
TAM_POP = -1

class Objeto:
    valor: int
    peso: int

    def __init__(self, valor, peso):
        self.valor = valor
        self.peso = peso

    def printar(self):
        print(f"v = {self.valor} p = {self.peso}")
class Individuo:
    cromossomo: []
    aptidao: int = -1
    peso_total: int = 0

    def printar(self):
        print(f"{self.cromossomo} {self.aptidao}")

def gerar_pop_inicial(num_individuos, num_genes, limite, objetos):
    pop = []

    while len(pop) != num_individuos:
        ind = [ random.randint(0,1) for _ in range(num_genes)]
        novo = Individuo()
        novo.cromossomo = ind
        calcular_aptidão(novo, limite, objetos)

        if novo.aptidao == -1:
            consertar(novo,limite, objetos)

        pop.append(novo)

    return pop

def consertar(ind: Individuo, limite, objetos: list[Objeto]):
    peso = ind.peso_total
    alelo = random.randint(0, len(objetos) - 1)
    while peso > limite:
        if ind.cromossomo[alelo] == 1:
            ind.aptidao -= objetos[alelo].valor
            peso -= objetos[alelo].peso
            ind.cromossomo[alelo] = 0

        if alelo + 1 == len(objetos):
            alelo = 0
        else:
            alelo += 1

    ind.peso_total = peso

def calcular_aptidão(ind: Individuo, limite, objetos):
    total_valor = 0
    total_peso = 0
    for i in range(len(ind.cromossomo)):
        if ind.cromossomo[i] == 1:
            total_valor += objetos[i].valor
            total_peso += objetos[i].peso

    if total_peso > limite:
        total_valor = -1

    ind.peso_total = total_peso
    ind.aptidao = total_valor

def calcular_aptidão_pop(pop: list[Individuo], limite, obj: list[Objeto]):
    for i in pop:
        if i.aptidao != -1: # cromossomo que não sofreu crossover ou mutação
            continue

        calcular_aptidão(i,limite, obj)

def torneio(pop: list[Individuo], qtd):
    pop_intermediaria = []
    for i in range(len(pop)):

        todos = [h for h in range(0,TAM_POP)]
        indices = []
        for _ in range(qtd):
            escolha = random.choice(todos)
            indices.append(escolha)
            todos.remove(escolha)

        indices.sort()

        candidatos = [pop[h] for h in indices]
        pop_intermediaria.append(copy.deepcopy(candidatos[-1]))

    return pop_intermediaria

def crossover_1ponto(pai1: Individuo, pai2: Individuo):
    chance = random.random()
    if chance > TAXA_CROSSOVER: # crossover não ocorre
        return [pai1, pai2]

    n = len(pai1.cromossomo)
    corte = random.randint(0,n - 2) # um cromossomo com n genes tem n - 1 pontos de corte

    filho1 = Individuo()
    filho2 = Individuo()

    filho1.cromossomo = pai1.cromossomo[:corte+1] + pai2.cromossomo[corte+1:]
    filho2.cromossomo = pai2.cromossomo[:corte+1] + pai1.cromossomo[corte+1:]

    mutacao(filho1)
    mutacao(filho2)

    return [filho1, filho2]

def crossover_2ponto(pai1: Individuo, pai2: Individuo):
    chance = random.random()
    if chance > TAXA_CROSSOVER:
        return [pai1, pai2]

    n = len(pai1.cromossomo)
    corte1 = random.randint(0, n - 2)
    corte2 = random.randint(0, n - 2)

    while corte2 == corte1:
        corte2 = random.randint(0, n - 2)

    if corte2 < corte1:
        aux = corte1
        corte1 = corte2
        corte2 = aux

    filho1 = Individuo()
    filho2 = Individuo()

    filho1.cromossomo = pai1.cromossomo[:corte1 + 1] + pai2.cromossomo[corte1 + 1:corte2 + 1] + pai1.cromossomo[corte2 + 1:]
    filho2.cromossomo = pai2.cromossomo[:corte1 + 1] + pai1.cromossomo[corte1 + 1:corte2 + 1] + pai2.cromossomo[corte2 + 1:]

    mutacao(filho1)
    mutacao(filho2)

    return [filho1, filho2]

def mutacao(ind: Individuo):
    for i in range(len(ind.cromossomo)):
        if random.random() < TAXA_MUTACAO: # mutação ocorre
            if ind.cromossomo[i] == 0:
                ind.cromossomo[i] = 1
            else:
                ind.cromossomo[i] = 0

def convergiu(pop, resultado):
    valores = [ i.aptidao for i in pop]
    if valores[-1] == resultado:
        return True
    elif valores[-1] == -1:
        return False
    else:
        # resultado não especificado
        qtd = 0
        # convergência se >= 90%
        for h in range(TAM_POP):
            if valores[h] == valores[-1]:
                qtd += 1

        return qtd >= int(TAM_POP * 0.8)

def imprimir_solucao(ind: Individuo, objetos: list[Objeto]):
    total_valor = 0
    for i in range(len(ind.cromossomo)):
        if ind.cromossomo[i] == 1:
            total_valor += objetos[i].valor
            # print(f"Item #{i} - Valor {objetos[i].valor} e Peso {objetos[i].peso}")
    print(f"{total_valor}", end="")

def um(N, limite, objetos,resultado):
    # torneio
    # crossover de 1 ponto
    # sem elitismo

    pop = gerar_pop_inicial(TAM_POP,N,limite,objetos)
    pop.sort(key=lambda Individuo: Individuo.aptidao)

    while True:
        pop_intermediaria = torneio(pop,4)

        pop = []
        for i in range(0,TAM_POP,2):
            novos = crossover_1ponto(pop_intermediaria[i], pop_intermediaria[i+1])
            pop.extend(novos)

        calcular_aptidão_pop(pop, limite, objetos)
        pop.sort(key=lambda Individuo: Individuo.aptidao)

        if convergiu(pop,resultado):
            imprimir_solucao(pop[-1],objetos)
            break

def dois(N, limite, objetos,resultado):
    # torneio
    # crossover de 2 ponto
    # sem elitismo

    pop = gerar_pop_inicial(TAM_POP,N,limite,objetos)
    pop.sort(key=lambda Individuo: Individuo.aptidao)

    while True:
        pop_intermediaria = torneio(pop,4)

        pop = []
        for i in range(0,TAM_POP,2):
            novos = crossover_2ponto(pop_intermediaria[i], pop_intermediaria[i+1])
            pop.extend(novos)

        calcular_aptidão_pop(pop, limite, objetos)
        pop.sort(key=lambda Individuo: Individuo.aptidao)

        if convergiu(pop,resultado):
            imprimir_solucao(pop[-1],objetos)
            break


def main():
    start_time = time.time()
    N = int(input())  # quantidade de objetos
    limite = int(input())
    global TAM_POP
    TAM_POP = N * 4

    objetos = []
    for _ in range(N):
        valor, peso = input().split(" ")
        objetos.append(Objeto(int(valor), int(peso)))

    try:
        resultado = int(input())
    except EOFError:
        resultado = -2

    base = time.time() - start_time

    for i in range(10):
        start_time = time.time()
        #um(N, limite, objetos, resultado)
        dois(N, limite, objetos, resultado)
        execution_time = (time.time() - start_time) + base
        print(f" {execution_time}")

if __name__ == "__main__":
    main()