import random
import numpy as np

# PROGRAMA QUE CRIA A MATRIZ DE DISTANCIA ENTRE AS CIDADES:
def escalaCidades(ordem, menor, maior):
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

#Programa que gera a primeira população
def populacao(tamanhoPopulacao,ordem):
    '''
    Inicia a população de individuos, de acordo com a quantidade de cidades existente.
    Cada individuo carrega consigo caracteristicas, que são as cidades por onde esse individuo irá passar
    :param tamanhoPopulacao: é a quantidade de individuos que existem nessa pupulação
    :param ordem: é a caracteristica de cada um dos individuos, ou seja por quais cidades eles vão percorrer, esse valor
    tem que ser igual a quantidade de cidades, sem repetir
    :return:
    '''
    elementos = list
    povoacao = np.zeros((tamanhoPopulacao, ordem + 1))
    for a in range(tamanhoPopulacao):
        elementos = random.sample(range(0, ordem), ordem)
        elementos.append(elementos[0])
        povoacao[a] = elementos

    return povoacao

def fitDistancia(matrizElementos):
    """
   Função que faz o calculo da distancia percorrida por cada um dos elementos
   :param matrizCidades: No momento, não é util essa função
   :param matrizElementos: é a matriz onde estão elencados os elementos(individuos, população)
   :return: uma matriz com o resultado desse calculo
   """
    matrizResultadoDistancia = np.zeros((len(matrizElementos), 1))
    for elemento in range(len(matrizElementos)):
        for caracteristica in range(len(matrizElementos[elemento])):
            matrizResultadoDistancia[elemento] += matrizElementos[elemento][caracteristica]
    return sum(matrizResultadoDistancia)

def cruzamento(matrizElementos, cruzamentoTaxa):
    '''
    Programa que faz o cruzamento de "genes" entre duas populaçoes, de acordo com a taxa de cruzamento
    a taxa de cruzamento é uma porcentagem da quantidade de caracteristicas do elemento. ou seja, se for setada
    em 0.5, 50% das caracteristicas de ambos os elementos serão cruzadas
    :param matrizElementos: é a matriz que possui os elementos, a população
    :param cruzamentoTaxa: é a porcentagem de caracteristicas que serão cruzadas
    :return: retorna uma matriz com novos elementos cruzados
    '''
    matrizGeracaoNova = np.zeros((len(matrizElementos), len(matrizElementos[1])))
    for elementos in range(len(matrizElementos)):
        for caracteristica in range(len(matrizElementos[elementos])):
            if caracteristica < cruzamentoTaxa * len(matrizElementos[elementos]):
                matrizGeracaoNova[elementos][caracteristica] = matrizElementos[elementos][caracteristica]
            else:
                try:
                    matrizGeracaoNova[elementos][caracteristica] = matrizElementos[elementos + 1][caracteristica]
                except:
                    matrizGeracaoNova[elementos][caracteristica] = matrizElementos[0][caracteristica]

    return matrizGeracaoNova

def mutacao(matrizElementos, mutacaoTaxa):
    '''
    Função que faz a "mutação" de caracteristicas de cada individuo, a quantidade de caracteristicas é definido pela taxa
    :param matrizElementos: Matriz que possui a população
    :param mutacaoTaxa: é a taxa de caracteristicas que serão mutacionadas
    :return: uma nova matriz com a nova geração
    '''
    qntRandom = round(len(matrizElementos[1]) * mutacaoTaxa)
    matrizGeracaoNova = matrizElementos.copy()
    for elementos in range(len(matrizElementos)):
        for caracteristica in range(len(matrizElementos[elementos])):
            if caracteristica < qntRandom:
                ValorCaracteristicaRandom = random.randint(0, 9)
                PosicaoCaracteristicaRandom = random.randint(0, len(matrizElementos[1]) - 1)
                matrizGeracaoNova[elementos][PosicaoCaracteristicaRandom] = ValorCaracteristicaRandom
    return matrizGeracaoNova

def aplicacao(geracoes, matrizElementos):
    '''
    É o programa principal, que faz a passagem das gerações
    :param geracoes:
    :param matrizElementos:
    :return:
    '''
    for linhagem in range(geracoes):
        novosElementos = matrizElementos.copy()
        print(fitDistancia(novosElementos))
        print(f"Geração: {linhagem}")
        novosElementos = cruzamento(novosElementos, cruzamentoTaxa)
        novosElementos = mutacao(novosElementos, mutacaoTaxa)
        if fitDistancia(novosElementos) < fitDistancia(matrizElementos):
            matrizElementos = novosElementos.copy()
        else:
            matrizElementos = matrizElementos.copy()

    return matrizElementos


# Parametros iniciais
quantidadeCidades = 3  # Para criar a matriz de cidades
pessoas = 5  # População
# viagens = 5  # Caracteristicas
geracoes = 50000

# Parametors para criação de novos individuos
cruzamentoTaxa = 0.5
mutacaoTaxa = 0.5


elementos = populacao(10,10)
print(elementos)




#matrizCidades = escalaCidades(quantidadeCidades)
#matrizCidades = [[0, 3, 5], [2, 0, 8], [1, 4, 0]]
#print(escalaCidades(5,2,5))
