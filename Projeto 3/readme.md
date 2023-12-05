# Projeto 3 - Perceptron com treinamento usando algoritmos genéticos na classificação da base de dados Iris

## Alunos
- Artur Amaro
- Daniel Gonçalves
- João Victor Fernandes de Souza Silva
- Luiz André da Silva Carvalho

## Sobre 
O presente projeto compreende um perceptron de uma única camada e de um único neurônio, cujo treinamento de 
seus pesos é realizado por meio de um algoritmo genético. Este perceptron é capaz de classificar as espécies 
da base de dados Iris duas a duas.

Em relação ao AG usado para o treinamento dos pesos da rede, ele utiliza como cromossomo um vetor com os 5
pesos em ponto flutuante. A medida de aptidão adotada é a precisão, a selação é feita por meio de torneio,
o crossover é de apenas 1 ponto e a mutação usa a distribuição normal com média 0 e desvio padrão 1 para adicionar
valores nos alelos. 

O programa obrigatoriamente deve receber quais as duas espécies que serão usadas para o 
treinamento do perceptron e, opcionalmente, pode receber o número de gerações, a taxa de crossover,
a taxa de mutação, o tamanho da população e a proporção da base que será utilizada para o treinamento.

Por padrão, o número de gerações está definido como 10, a população com 50, a taxa de crossover em 70%,
a taxa de mutação em 1% e a proporção para treinamento em 20%.

## Como usar

```bash
usage: main.py [-h] [--geracoes [GERACOES]] [--populacao [POPULACAO]] [--taxa_crossover [TAXA_CROSSOVER]] [--taxa_mutacao [TAXA_MUTACAO]]
               [--proporcao [PROPORCAO]]
               {setosa,versicolor,virginica} {setosa,versicolor,virginica}

Perceptron para classificação binária da base de dados Iris.

positional arguments:
  {setosa,versicolor,virginica}
                        Quais espécies de Iris (duas) devem ser usadas para treinar o Percéptron.

options:
  -h, --help            show this help message and exit
  --geracoes [GERACOES], -g [GERACOES]
                        Número de gerações.
  --populacao [POPULACAO], -pop [POPULACAO]
                        Tamanho da população a ser gerada.
  --taxa_crossover [TAXA_CROSSOVER], -tc [TAXA_CROSSOVER]
                        Taxa de crossover. Deve ser inserido um valor entre 0 e 1.
  --taxa_mutacao [TAXA_MUTACAO], -tm [TAXA_MUTACAO]
                        Taxa de mutação. Deve ser inserido um valor entre 0 e 1.
  --proporcao [PROPORCAO], -p [PROPORCAO]
                        Proporção da base que deve ser usada para treinamento. Deve ser inserido um valor entre 0 e 1.
```

## Instalação
Execute `./install.sh` para instalar todas as dependências necessárias.

## Execução
Execute `./perceptron.sh`, passando os argumentos e opções necessárias.

## Saída
O programa imprime na saída padrão as informações gerais do treinamento (gerações, tamanho da população, 
taxas, proporção e espécies) seguidas pela acurácia dos testes referentes às duas espécies escolhidas.
Em seguida, testa a base da terceira espécie no modelo treinado e imprime quantos indivíduos
foram classificados em cada uma das classes.
