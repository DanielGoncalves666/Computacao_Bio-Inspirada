import numpy as np
from ucimlrepo import fetch_ucirepo
import random
import math
import argparse
import copy

class Individuo:
    cromossomo: [float]
    aptidao: float

class perceptron:
    _pop: [Individuo]
    _pesos: [float] = [0.0,0.0,0.0,0.0,0.0]
    _taxa_crossover = float
    _taxa_mutacao = float
    # primeira posição é o peso do bias
    # as 4 restantes são os pesos das entradas

    def __init__(self, pop_size, taxa_crossover, taxa_mutacao):
        self._inicializar_pop(pop_size)
        self._taxa_crossover = taxa_crossover
        self._taxa_mutacao = taxa_mutacao

    def _inicializar_pop(self, pop_size, num_weights=5):
        self._pop = [Individuo() for _ in range(pop_size)]
        for ind in self._pop:
            ind.cromossomo = [np.random.uniform(-1, 1) for _ in range(num_weights)]

    def _calcular_aptidao_pop(self, dados, classes, especies_disponiveis):
        for ind in self._pop:
            total_corretos = 0
            for entrada in range(len(dados)):
                produto_escalar = self._juncao_aditiva(ind.cromossomo, dados[entrada])
                result = self._func_sigmoide(produto_escalar)

                if result <= 0.5:
                    classe_obtida = 0
                else:
                    classe_obtida = 1

                classe_correta = 0 if "Iris-" + especies_disponiveis[0] == classes[entrada] else 1
                if classe_obtida == classe_correta:
                    total_corretos += 1

            ind.aptidao = total_corretos / len(dados)

        self._pop.sort(key=lambda i: i.aptidao)

    def _juncao_aditiva(self, cromossomo, entrada):
        somatorio = sum([entrada[i] * cromossomo[1 + i] for i in range(len(entrada))])
        return somatorio + (1 * cromossomo[0])
    def _func_sigmoide(self, valor):
        return 1.0 / (1 + math.exp(-valor))

    def _selecao_torneio(self):
        pop_intermediaria = []

        for _ in range(len(self._pop)):
            competidores = random.sample(self._pop, 2)
            competidores_ordenados = sorted(competidores, key=lambda x: x.aptidao)
            # Ordena os competidores, em ordem crescente
            vencedor_torneio = competidores_ordenados[-1]
            pop_intermediaria.append(copy.deepcopy(vencedor_torneio))

        return pop_intermediaria

    def _crossover_pop(self, pop_intermediaria):
        pop_intermediaria_final = []

        for i in range(0,len(self._pop),2):
            pop_intermediaria_final += self._crossover_1ponto(pop_intermediaria[i], pop_intermediaria[i + 1])

        return pop_intermediaria_final

    def _crossover_1ponto(self, pai1: Individuo, pai2: Individuo):
        chance = random.random()
        if chance > self._taxa_crossover:  # crossover não ocorre
            return [pai1, pai2]

        n = len(pai1.cromossomo)
        ponto_corte = random.randint(0, n - 2)
        #cromossomo com n genes tem n - 1 pontos de corte

        filho1 = Individuo()
        filho2 = Individuo()

        filho1.cromossomo = pai1.cromossomo[:ponto_corte + 1] + pai2.cromossomo[ponto_corte + 1:]
        filho2.cromossomo = pai2.cromossomo[:ponto_corte + 1] + pai1.cromossomo[ponto_corte + 1:]

        return [filho1, filho2]

    def _mutacao(self, pop_intermediaria: [Individuo], desvio_padrao = 1):
        pop_mutada = copy.deepcopy(pop_intermediaria)

        # taxa de mutação no formato de ponto_flutuante: 0,01
        for ind in pop_mutada:
            for alelo in range(5):
                if random.random() < self._taxa_mutacao:
                    ind.cromossomo[alelo] += np.random.normal(0, desvio_padrao)

        return pop_mutada

    def treinar_perceptron(self, dados, classes, especies_disponiveis, geracoes):

        for _ in range(geracoes):
            self._calcular_aptidao_pop(dados,classes, especies_disponiveis)

            pop_selecionada = self._selecao_torneio()
            pop_crossover = self._crossover_pop(pop_selecionada)
            pop_mutada = self._mutacao(pop_crossover)

            self._pop = pop_mutada

        self._calcular_aptidao_pop(dados,classes,especies_disponiveis)
        self._pesos = self._pop[-1].cromossomo

    def testar_perceptron(self, dados, classes, especies_disponiveis):
        corretos = 0
        for i in range(len(dados)):
            produto_escalar = self._juncao_aditiva(self._pesos, dados[i])

            result = self._func_sigmoide(produto_escalar)

            classe_obtida = "Iris-"
            if result <= 0.5:
                classe_obtida += especies_disponiveis[0]
            else:
                classe_obtida += especies_disponiveis[1]

            if classe_obtida == classes[i]:
                corretos += 1

        print(f"\nTeste padrão.\nAcurácia: {(corretos / len(dados)) * 100}%.")

    def testar_terceira_classse(self, dados, especies_disponiveis):

        classe_um = 0
        classe_dois = 0
        for i in range(len(dados)):
            produto_escalar = self._juncao_aditiva(self._pesos, dados[i])

            result = self._func_sigmoide(produto_escalar)

            if result <= 0.5:
                classe_um += 1
            else:
                classe_dois += 1


        print(f"\nTeste terceira classe.")
        print(f"{classe_um} de {len(dados)} classificados como {especies_disponiveis[0]}.")
        print(f"{classe_dois} de {len(dados)} classificados como {especies_disponiveis[1]}.")

def normalizar_dados(setosa, versicolor, virginica, nao_treinamento):

    menor = [math.inf for _ in range(4)]
    maior = [-math.inf for _ in range(4)]

    for h in range(4):
        for i in range(50):
            if nao_treinamento != 1:
                if setosa[i][h] < menor[h]:
                    menor[h] = setosa[i][h]

                if setosa[i][h] > maior[h]:
                    maior[h] = setosa[i][h]

            if nao_treinamento != 2:
                if versicolor[i][h] < menor[h]:
                    menor[h] = versicolor[i][h]

                if versicolor[i][h] > maior[h]:
                    maior[h] = versicolor[i][h]

            if nao_treinamento != 3:
                if virginica[i][h] < menor[h]:
                    menor[h] = virginica[i][h]

                if virginica[i][h] > maior[h]:
                    maior[h] = virginica[i][h]

    for i in range(50):
        for h in range(4):
            setosa[i][h] = (setosa[i][h] - menor[h]) / (maior[h] - menor[h])
            versicolor[i][h] = (versicolor[i][h] - menor[h]) / (maior[h] - menor[h])
            virginica[i][h] = (virginica[i][h] - menor[h]) / (maior[h] - menor[h])

def obter_dados(iris, especies, proporcao, nao_treinamento):
    final_index = int(50 * proporcao)

    entradas = iris.data.features
    classes = iris.data.targets

    setosa = []
    for i in range(50):
        setosa.append([entradas["sepal length"][i], entradas["sepal width"][i], entradas["petal length"][i],
                       entradas["petal width"][i]])

    versicolor = []
    for i in range(50,100):
        versicolor.append([entradas["sepal length"][i], entradas["sepal width"][i], entradas["petal length"][i],
                          entradas["petal width"][i]])

    virginica = []
    for i in range(100, 150):
        virginica.append([entradas["sepal length"][i], entradas["sepal width"][i], entradas["petal length"][i],
                         entradas["petal width"][i]])

    class_setosa = []
    for i in range(50):
        class_setosa.append(classes['class'][i])

    class_versicolor = []
    for i in range(50,100):
        class_versicolor.append(classes['class'][i])

    class_virginica = []
    for i in range(100,150):
        class_virginica.append(classes['class'][i])

    normalizar_dados(setosa, versicolor, virginica, nao_treinamento)

    dados_entrada = []
    dados_teste = []
    dados_teste_extendidos = []
    classes_entrada = []
    classes_teste = []
    classes_teste_extendidas = []


    if "setosa" in especies:
        dados_entrada.extend(setosa[0:final_index])
        dados_teste.extend(setosa[final_index:])
        classes_entrada.extend(class_setosa[0:final_index])
        classes_teste.extend(class_setosa[final_index:])
    else:
        dados_teste_extendidos.extend(setosa)
        classes_teste_extendidas.extend(class_setosa)

    if "versicolor" in especies:
        dados_entrada.extend(versicolor[0:final_index])
        dados_teste.extend(versicolor[final_index:])
        classes_entrada.extend(class_versicolor[0:final_index])
        classes_teste.extend(class_versicolor[final_index:])
    else:
        dados_teste_extendidos.extend(versicolor)
        classes_teste_extendidas.extend( class_versicolor)

    if "virginica" in especies:
        dados_entrada.extend(virginica[0:final_index])
        dados_teste.extend(virginica[final_index:])
        classes_entrada.extend(class_virginica[0:final_index])
        classes_teste.extend(class_virginica[final_index:])
    else:
        dados_teste_extendidos.extend(virginica)
        classes_teste_extendidas.extend(class_virginica)

    return (dados_entrada, dados_teste, dados_teste_extendidos, classes_entrada, classes_teste, classes_teste_extendidas)

def creating_arg_parser():
    disponiveis = ["setosa","versicolor","virginica"]

    # a instância de ArgumentParser irá conter todas as informações da interface de linha de comando
    parser = argparse.ArgumentParser(description='Perceptron para classificação binária da base de dados Iris.')
    # add_argument adiciona argumentos que podem ser inseridos na linha de comando
    parser.add_argument('especies', choices=disponiveis, nargs=2, help="Quais espécies de Iris (duas) devem ser usadas para treinar o Percéptron.")
    parser.add_argument('--geracoes', '-g', nargs='?', default=10, type=int, help="Número de gerações.")
    parser.add_argument('--populacao', '-pop', nargs='?', default=50, type=int, help="Tamanho da população a ser gerada.")
    parser.add_argument('--taxa_crossover', '-tc', nargs="?", default=0.7, type=float,
                        help="Taxa de crossover. Deve ser inserido um valor entre 0 e 1.")
    parser.add_argument('--taxa_mutacao', '-tm', nargs='?', default=0.01, type=float,
                        help="Taxa de mutação. Deve ser inserido um valor entre 0 e 1.")
    parser.add_argument('--proporcao', '-p', nargs='?', default=0.2, type=float,
                        help="Proporção da base que deve ser usada para treinamento. Deve ser inserido um valor entre 0 e 1.")

    return parser

def main():
    iris = fetch_ucirepo(id=53)
    command_line = creating_arg_parser().parse_args()
    if command_line.especies[0] == command_line.especies[1]:
        print("Espécies diferentes devem ser informadas.")
        exit(0)

    if int(command_line.proporcao * 100) % 2 == 1:
        command_line.proporcao += 0.01

    if command_line.populacao % 2 == 1:
        command_line.populacao += 1

    if "setosa" not in command_line.especies:
        nao_treinamento = 1
    elif "versicolor" not in command_line.especies:
        nao_treinamento = 2
    else:
        nao_treinamento = 3

    (dados_entrada, dados_teste, dados_teste_extendidos, classes_entrada, classes_teste, classes_teste_extendidas) = obter_dados(iris, command_line.especies, command_line.proporcao, nao_treinamento)

    p_iris = perceptron(command_line.populacao, command_line.taxa_crossover, command_line.taxa_mutacao)
    p_iris.treinar_perceptron(dados_entrada, classes_entrada, command_line.especies, command_line.geracoes)

    print(f"Especies de treino: {command_line.especies[0]} e {command_line.especies[1]}.")
    print(f"Número de Gerações: {command_line.geracoes}.")
    print(f"Tamanho da população: {command_line.populacao}.")
    print(f"Taxa de crossover: {int(command_line.taxa_crossover * 100)}%.")
    print(f"Taxa de mutação: {int(command_line.taxa_mutacao * 100)}%.")
    print(f"Proporção de treinamento: {int(command_line.proporcao * 100)}%.")
    p_iris.testar_perceptron(dados_teste,classes_teste,command_line.especies)
    p_iris.testar_terceira_classse(dados_teste_extendidos, command_line.especies)


if __name__ == "__main__":
    main()
