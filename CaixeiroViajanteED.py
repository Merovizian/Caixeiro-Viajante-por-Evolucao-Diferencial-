import random
import numpy as np
import matplotlib.pyplot as plt

def escalaCidades(ordem, menor=1, maior=9):
    '''
    FUNCAO QUE CRIA UMA MATRIZ DE DISTANCIA ENTRE AS CIDASDES
    :param ordem: tamanho da matriz, ou seja, quantidade de cidade
    :param menor: menor distancia entre as cidades
    :param maior: maior distancia entre as cidades
    :return: retorna a matriz contendo as cidades e a distancia entre elas
    '''
    escala = np.zeros((ordem, ordem))
    for a in range(ordem):
        for b in range(ordem):
            if a != b:
                escala[a][b] = random.randint(menor, maior)
    return escala

def fitDistancia(matrizElemento, matrizCidades):
    """
   Função que faz o calculo da distancia percorrida por cada um dos elementos
   :param matrizCidades: No momento, não é util essa função
   :return: uma matriz com o resultado desse calculo
   """
    matrizResultadoDistancia = np.zeros((len(matrizElemento), 1))
    for count, value in enumerate(matrizElemento):
        for countA, valueA in enumerate(matrizElemento[count]):
            try:
                valorA = int(valueA)
                valorB = int(matrizElemento[count][countA + 1])
                matrizResultadoDistancia[count] += matrizCidades[valorA][valorB]
            except:
                pass
    return matrizResultadoDistancia

def populacao(tamanhoPopulacao,viagens ,ordem):
    '''
    Inicia a população de individuos, de acordo com a quantidade de cidades existente.
    Cada individuo carrega consigo caracteristicas, que são as cidades por onde esse individuo irá passar
    :param tamanhoPopulacao: é a quantidade de individuos que existem nessa pupulação
    :param ordem: é a caracteristica de cada um dos individuos, ou seja por quais cidades eles vão percorrer, esse valor
    tem que ser igual a quantidade de cidades, sem repetir
    :return:
    '''
    povoacao = np.zeros((tamanhoPopulacao, viagens + 1))
    for a in range(tamanhoPopulacao):
        elementos = random.sample(range(0, ordem), viagens)
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
                while not(ValorCaracteristicaRandom not in matrizGeracaoNova[elementos]):
                    contador += 1
                    ValorCaracteristicaRandom = random.randint(0, valorMaximo)
                    if contador >= 99:
                        aux = 0
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
    #matrizGeracaoNova = np.zeros((len(matrizElementos), len(matrizElementos[1])))
    for elementos in range(len(matrizElementos)):
        for caracteristica in range(len(matrizElementos[elementos])):
            if caracteristica < cruzamentoTaxa * len(matrizElementos[elementos]):
                if (int(matrizElementos[elementos][caracteristica]) not in (matrizGeracaoNova[elementos])):
                    matrizGeracaoNova[elementos][caracteristica] = matrizElementos[elementos][caracteristica]
            else:
                try:
                    if (int(matrizElementos[elementos + 1][caracteristica]) not in (matrizGeracaoNova[elementos])):
                        matrizGeracaoNova[elementos][caracteristica] = matrizElementos[elementos + 1][caracteristica]
                except:
                    if (int(matrizElementos[0][caracteristica]) not in matrizGeracaoNova[elementos]):
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
    for linhagem in range(geracoes):
        novosElementos = matrizElementos.copy()
        print(sum(fitDistancia(novosElementos,matrizCidade))/len(matrizElementos))
        matrizFit.append(int(sum(fitDistancia(novosElementos,matrizCidade))))
        print(f"Geração: {linhagem}")
        novosElementos = cruzamento(novosElementos, cruzamentoTaxa)
        novosElementos = mutacao(novosElementos, mutacaoTaxa)
        if sum(fitDistancia(novosElementos, matrizCidade)) < sum(fitDistancia(matrizElementos,matrizCidade)):
            matrizElementos = novosElementos.copy()
        else:
            matrizElementos = matrizElementos.copy()

    return matrizElementos, matrizFit

# Parametros iniciais
quantidadeCidades = 4  # Para criar a matriz de cidades
pessoas = 5  # População
viagens = 4 # Caracteristicas
geracoes = 1000

# Parametors para criação de novos individuos
cruzamentoTaxa = 0.4
mutacaoTaxa = 0.2

#APLICACAO DO PROGRAMA
matrizCidades = [[0,3,2,8],[4,0,9,1],[3,9,0,5],[9,6,5,0]]
#matrizCidades = escalaCidades(quantidadeCidades)
elementos = populacao(pessoas, viagens, quantidadeCidades)
novos = cruzamento(elementos,cruzamentoTaxa)
resultado, matrizfit = aplicacao(geracoes,elementos,matrizCidades)

print("***MATRIZ PRINCIPAL DAS ROTAS***")
print(matrizCidades)
print("***** PRIMEIRA GERAÇÃO ******")
print(elementos)
print("*** DISTANCIA PERCORRRIDA POR CADA ELEMENTO INICIAL ***")
print(sum(fitDistancia(elementos, matrizCidades)))
print("***** ULTIMA GERAÇÃO ******")
print(resultado)
print("*** DISTANCIA PERCORRRIDA POR CADA ELEMENTO FINAL  ***")
print(sum(fitDistancia(resultado, matrizCidades)))

plt.plot( matrizfit )
plt.title("Caixeiro Viajante por Evolucao Diferencial")
plt.grid(True)
plt.xlabel("GERAÇÕES")
plt.ylabel("SOMA DAS DISTANCIAS")
plt.show()

print("ericgmicaela@gmail")