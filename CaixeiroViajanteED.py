import random
import numpy as np
import matplotlib.pyplot as plt


def matrizDistancias(ordem, menor=1, maior=9):
    """
    FUNCAO QUE CRIA UMA MATRIZ DE DISTANCIA ENTRE AS CIDADES ou Pontos
    :param ordem: tamanho da matriz, ou seja, quantidade de cidade ou pontos
    :param menor: menor distancia entre as cidades
    :param maior: maior distancia entre as cidades
    :return escala: retorna a matriz contendo as cidades e a distancia entre elas
    """
    # Cria uma matriz quadrada de zeros. Para ser manipulada
    escala = np.zeros((ordem, ordem))

    # loop que gera a matriz randomica
    for a in range(ordem):
        for b in range(ordem):
            # condição para evitar que a diagonal difira de zero.
            if a != b:
                escala[a][b] = random.randint(menor, maior)
    return escala


def fitDistancia(matrizPopulacao, matrizDistancias):
    """
   Função que faz o cálculo da distância percorrida por cada um dos elementos, esse calculo é feito pegando pares de
   caracteristicas de cada pessoa e aplicando na matriz de distancia.
   :param matrizPopulacao: é a matriz que possui a população de cada geração
   :param matrizDistancias: No momento, não é util essa função

   :return matrizResultadoDistancia: uma matriz com o resultado desse calculo
   """
    # cria uma matriz (1)linha com o tamanho igual à quantidade de pessoas que há na população
    matrizResultadoDistancia = np.zeros((len(matrizPopulacao), 1))

    # primeiro laço para percorrer a matriz da população e manipular cada um dos elementos(pessoas)
    for count, value in enumerate(matrizPopulacao):
        # Laço para manipular cada elemento [countA serve para achar a posição do laço. valueA retorna o valor
        # daquela posição]
        for countA, valueA in enumerate(matrizPopulacao[count]):
            try:
                # transforma em inteiros os valores das caracteristicas de cada pessoa da população
                valorA = int(valueA)
                valorB = int(matrizPopulacao[count][countA + 1])
                # faz o cálculo da distância, onde se pega duas caracteristicas sequenciais de uma pessoa e aplica na
                # matriz de distâncias
                matrizResultadoDistancia[count] += matrizDistancias[valorA][valorB]
            except:
                # O try serve, pois, após pegar as duas últimas caracteristicas o programa tentará pegar um valor
                # que extrepola o vetor de pessoa
                pass
    # Retorna uma matriz com o valor da distância percorrida por cada um dos individuos.
    return matrizResultadoDistancia


def populacao(tamanhoPopulacao, viagens, quantidadeCidades):
    """
    Inicia a população de individuos. Cada individuo carrega consigo caracteristicas, as cidades por onde esse
    individuo irá passar.
    :param tamanhoPopulacao: é a quantidade de individuos que existem nessa pupulação.
    :param viagens: é a quantidade de viagens que cada individuo irá dar, ou seja, a quantidade de caracteristicas.
    :param quantidadeCidades: é a caracteristica de cada um dos individuos, ou seja, por quais cidades eles vão
    percorrer, esse valor tem que ser igual ou menor que a quantidade de cidades, sem repetir..
    :return povoacao: matriz contendo todos os individuos e suas caracteristicas
    """
    # Inicia a matriz de individuos, e as suas caracteristicas todas zeradas. Cria-se uma caracteristica a mais, pois
    # esta função indica que cada um dos individuos irá retornar ao ponto inicial
    povoacao = np.zeros((tamanhoPopulacao, viagens + 1))

    # Loop para preecher aleatoriamente e sem repetição cada um dos individuos
    for a in range(tamanhoPopulacao):
        # Cada individuo terá caracteristicas que vão de 0 até a quantidade de cidades existentes.
        elementos = random.sample(range(0, quantidadeCidades), viagens)

        # Adiciona como última caracteristica a cidade inicial, indicando que o individuo irá retornar à sua cidade
        elementos.append(elementos[0])
        povoacao[a] = elementos

    return povoacao


def mutacao(matrizElementos, mutacaoTaxa):
    '''
    Função que faz a "mutação" de caracteristicas de cada individuo, a quantidade de caracteristicas é definido pela taxa
    :param matrizElementos: Matriz que possui a população
    :param mutacaoTaxa: é a taxa de caracteristicas que serão mutacionadas
    :return: uma nova matriz com a nova geração
    '''
    valorMaximo = (max([valor for linha in matrizElementos for valor in linha]))
    qntRandom = round(len(matrizElementos[1]) * mutacaoTaxa)
    matrizGeracaoNova = matrizElementos.copy()
    aux = 1
    contador = 0
    for elementos in range(len(matrizElementos)):
        for caracteristica in range(len(matrizElementos[elementos])):
            if caracteristica < qntRandom:
                ValorCaracteristicaRandom = random.randint(0, valorMaximo)
                PosicaoCaracteristicaRandom = random.randint(0, len(matrizElementos[1]) - 1)
                while not (ValorCaracteristicaRandom not in matrizGeracaoNova[elementos]):
                    contador += 1
                    ValorCaracteristicaRandom = random.randint(0, valorMaximo)
                    if contador >= 99:
                        aux = 0
                        contador = 0
                        break
                if aux == 1:
                    matrizGeracaoNova[elementos][PosicaoCaracteristicaRandom] = ValorCaracteristicaRandom
    return matrizGeracaoNova


def cruzamento(matrizElementos, cruzamentoTaxa):
    '''
    Programa que faz o cruzamento de "genes" entre duas populaçoes, de acordo com a taxa de cruzamento
    a taxa de cruzamento é uma porcentagem da quantidade de caracteristicas do elemento. ou seja, se for setada
    em 0.5, 50% das caracteristicas de ambos os elementos serão cruzadas
    :param matrizElementos: é a matriz que possui os elementos, a população
    :param cruzamentoTaxa: é a porcentagem de caracteristicas que serão cruzadas
    :return: retorna uma matriz com novos elementos cruzados
    '''
    matrizGeracaoNova = matrizElementos.copy()
    # matrizGeracaoNova = np.zeros((len(matrizElementos), len(matrizElementos[1])))
    for elementos in range(len(matrizElementos)):
        for caracteristica in range(len(matrizElementos[elementos])):
            if caracteristica < cruzamentoTaxa * len(matrizElementos[elementos]):
                if int(matrizElementos[elementos][caracteristica]) not in (matrizGeracaoNova[elementos]):
                    matrizGeracaoNova[elementos][caracteristica] = matrizElementos[elementos][caracteristica]
            else:
                try:
                    if int(matrizElementos[elementos + 1][caracteristica]) not in (matrizGeracaoNova[elementos]):
                        matrizGeracaoNova[elementos][caracteristica] = matrizElementos[elementos + 1][caracteristica]
                except:
                    if int(matrizElementos[0][caracteristica]) not in matrizGeracaoNova[elementos]:
                        matrizGeracaoNova[elementos][caracteristica] = matrizElementos[0][caracteristica]

    return matrizGeracaoNova


def aplicacao(geracoes, matrizElementos, matrizCidade):
    '''
    É o programa principal, que faz a passagem das gerações
    :param geracoes:
    :param matrizElementos:
    :return:
    '''
    matrizFit = list()
    try:
        for linhagem in range(geracoes):
            novosElementos = matrizElementos.copy()
            print(sum(fitDistancia(novosElementos, matrizCidade)) / (len(matrizElementos) * (len(matrizElementos[0]))))
            matrizFit.append(int(sum(fitDistancia(novosElementos, matrizCidade))))
            print(f"Geração: {linhagem}")
            novosElementos = cruzamento(novosElementos, cruzamentoTaxa)
            novosElementos = mutacao(novosElementos, mutacaoTaxa)
            if sum(fitDistancia(novosElementos, matrizCidade)) < sum(fitDistancia(matrizElementos, matrizCidade)):
                matrizElementos = novosElementos.copy()
            else:
                matrizElementos = matrizElementos.copy()
    except:
        return matrizElementos, matrizFit

    return matrizElementos, matrizFit


# Parametros iniciais
quantidadeCidades = 20  # Para criar a matriz de cidades
pessoas = 10  # População
viagens = 5  # Caracteristicas
geracoes = 10000

# Parametors para criação de novos individuos
cruzamentoTaxa = 0.2
mutacaoTaxa = 0.15

# APLICACAO DO PROGRAMA
matrizCidades = matrizDistancias(quantidadeCidades)
elementos = populacao(pessoas, viagens, quantidadeCidades)
print(elementos)

#novos = cruzamento(elementos, cruzamentoTaxa)
#resultado, matrizfit = aplicacao(geracoes, elementos, matrizCidades)

'''print("***MATRIZ PRINCIPAL DAS ROTAS***")
print(matrizCidades)
print("***** PRIMEIRA GERAÇÃO ******")
print(elementos)
print("*** DISTANCIA PERCORRRIDA POR CADA ELEMENTO INICIAL ***")
print(sum(fitDistancia(elementos, matrizCidades)))
print("***** ULTIMA GERAÇÃO ******")
print(resultado)
print("*** DISTANCIA PERCORRRIDA POR CADA ELEMENTO FINAL  ***")
print(sum(fitDistancia(resultado, matrizCidades)))

plt.plot(matrizfit)
plt.title("Caixeiro Viajante por Evolucao Diferencial")
plt.grid(True)
plt.xlabel("GERAÇÕES")
plt.ylabel("SOMA DAS DISTANCIAS")
plt.show()

print("ericgmicaela@gmail")
'''