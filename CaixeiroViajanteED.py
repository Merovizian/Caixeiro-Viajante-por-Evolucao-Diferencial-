import random
import numpy as np
import matplotlib.pyplot as plt


def matrizDistancias(ordem, menor=1, maior=9):
    """
    FUNCAO QUE CRIA UMA MATRIZ DE DISTÂNCIA ENTRE AS CIDADES ou Pontos.
    :param ordem: tamanho da matriz, ou seja, quantidade de cidade ou pontos.
    :param menor: menor distancia entre as cidades.
    :param maior: maior distancia entre as cidades.
    :return escala: retorna a matriz contendo as cidades e a distância entre elas.
    """
    # Cria uma matriz quadrada de zeros. Para ser manipulada
    matrizItinerario = np.zeros((ordem, ordem))

    # loop que gera a matriz randomica
    for a in range(ordem):
        for b in range(ordem):
            # condição para evitar que a diagonal difira de zero.
            if a != b:
                matrizItinerario[a][b] = random.randint(menor, maior)
    return matrizItinerario


def fitDistancia(matrizPopulacao, matrizItinerario):
    """
   Função que faz o cálculo da distância percorrida por cada um dos elementos, esse calculo é feito pegando pares de
   caracteristicas de cada pessoa e aplicando na matriz de distância.
   :param matrizPopulacao: é a matriz que possui a população de cada geração.
   :param matrizItinerario: é a matriz de distâncias, que possui a distância entre os pontos (cidades)

   :return matrizResultadoDistancia: uma matriz com o resultado desse cálculo.
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
                matrizResultadoDistancia[count] += matrizItinerario[valorA][valorB]
            except IndexError:
                # O try serve, pois, após pegar as duas últimas caracteristicas o programa tentará pegar um valor
                # que extrepola o vetor de pessoa
                pass
    # Retorna uma matriz com o valor da distância percorrida por cada um dos individuos.
    return matrizResultadoDistancia


def populacao(tamanhoPopulacao, qntCaracteristicas, maxCaracteristicas):
    """
    Inicia a população de individuos. Cada individuo carrega consigo caracteristicas, as cidades por onde esse
    individuo irá passar.
    :param tamanhoPopulacao: é a quantidade de individuos que existem nessa pupulação.
    :param qntCaracteristicas: é a quantidade de viagens que cada individuo irá dar, ou seja,
     a quantidade de caracteristicas.
    :param maxCaracteristicas: é a caracteristica de cada um dos individuos, ou seja, por quais cidades eles vão
    percorrer, esse valor tem que ser igual ou menor que a quantidade de cidades, sem repetir..
    :return povoacao: matriz contendo todos os individuos e as suas caracteristicas
    """
    # Inicia a matriz de individuos, e as suas caracteristicas todas zeradas. Cria-se uma caracteristica a mais, pois
    # esta função indica que cada um dos individuos irá retornar ao ponto inicial
    povoacao = np.zeros((tamanhoPopulacao, qntCaracteristicas + 1))

    # ‘Loop’ para preecher aleatoriamente e sem repetição cada um dos individuos
    for a in range(tamanhoPopulacao):
        # Cada individuo terá caracteristicas que vão de 0 até a quantidade de cidades existentes.
        individuo = random.sample(range(0, maxCaracteristicas), qntCaracteristicas)

        # Adiciona como última caracteristica a cidade inicial, indicando que o individuo irá retornar à sua cidade
        individuo.append(individuo[0])
        povoacao[a] = individuo

    return povoacao


def mutacao(matrizElementos, taxa, ordem):
    """
    Função que faz a "mutação" de caracteristicas de cada indivíduo, a quantidade de caracteristicas a sofrerem
    multações é definido pela taxa. Por exemplo, se a taxa for 0.5, a metade das caracteristicas sofrerão mutações.
    :param matrizElementos: Matriz que possui a população.
    :param taxa: é a taxa de caracteristicas que serão mutacionadas.
    :param ordem: é a ordem da matriz de distâncias. Serve para quando ocorrer uma multação, o novo valor dessa
    mutação não seja maior que a quantidade de pontos(cidades) existentes.
    :return: uma nova matriz com a nova geração
    """
    # Como as cidades começam com 0:
    ordem = ordem - 1
    # Variavel que armazena a quantidades de caracteristicas que serão modificadas com a mutação. Conforme a taxa.
    qntRandom = round(len(matrizElementos[1]) * taxa)

    # variavel que armazena as posições das caracteristicas que irão sofrer a mutação
    posRandom = random.sample(range(0, len(matrizElementos[1])), qntRandom)
    # Copia-se a matriz de individuos para uma nova matriz.
    matrizGeracaoNova = matrizElementos.copy()
    contador = 0
    # ‘Loop’ que percorre cada individuo da população
    for elemento in matrizGeracaoNova:
        aux = 1
        # 'Loop' que percorre cada posição das caracteristica de cada indivíduo
        for contCaracteristica in range(len(elemento)):
            contCaracteristica = int(contCaracteristica)
            # Se a posição da caracteristica estiver nas posições randomicas há a mutação naquela posição
            if contCaracteristica in posRandom:
                # É gerado então um valor aleatório para substituir uma caracteristica (Mutação)
                ValorCaracteristicaRandom = random.randint(0, ordem)
                # Faz a checagem para não repetir
                while not (ValorCaracteristicaRandom not in elemento):
                    contador += 1
                    # Como o valor aleatorio coincidiu com um já existente, repete-se o 'random'
                    ValorCaracteristicaRandom = random.randint(0, ordem)
                    # Faz a tentativa 50 vezes.
                    if contador >= 50:
                        aux = 0
                        contador = 0
                        break
                if aux == 1:
                    elemento[contCaracteristica] = ValorCaracteristicaRandom
    return matrizGeracaoNova


def cruzamento(matrizElementos, taxa):
    """
    Programa que faz o cruzamento de "genes" entre duas populaçoes, conforme a taxa de cruzamento, sendo uma porcentagem
    da quantidade de caracteristicas do elemento, ou seja, se for setada em 0.5, 50% das caracteristicas de ambos os
    elementos serão cruzadas.
    :param matrizElementos: é a matriz que possui os elementos, a população.
    :param taxa: é a porcentagem de caracteristicas que serão cruzadas.
    :return: retorna uma matriz com novos elementos cruzados.
    """

    matrizGeracaoNova = matrizElementos.copy()
    # 'Loop' para percorrer a posição de cada um dos individuos
    for elemento in range(len(matrizElementos)):
        # 'Loop' para percorrer a posição de cada caracteristica de cada indivíduo
        for caracteristica in range(len(matrizElementos[elemento])):
            # Priorizei posições em sequência, pois faz mais sentido assim, ao inves de usar posições randônicas
            if caracteristica < taxa * len(matrizElementos[elemento]):
                # A nova matriz terá os mesmos elementos iniciais da matriz anterior(mãe) até chegar na taxa
                if int(matrizElementos[elemento][caracteristica]) not in (matrizGeracaoNova[elemento]):
                    matrizGeracaoNova[elemento][caracteristica] = matrizElementos[elemento][caracteristica]
                # Alcançando a taxa, a nova matriz terá caracteristicas do individuo seguinte(pai)
            else:
                # Try serve para não travar a função quando o elemento seguinte(pai) extrapole a quantidade
                # de matriz de elementos
                try:
                    # Condição para evitar repetir caracteristicas em sequência. Pois, não faz sentido sair de uma
                    # cidade e ir para a mesma cidade logo em seguida.
                    if int(matrizElementos[elemento + 1][caracteristica]) not in (matrizGeracaoNova[elemento]):
                        matrizGeracaoNova[elemento][caracteristica] = matrizElementos[elemento + 1][caracteristica]
                # Caso ocorra de extrapolar a matriz de elementos, o elemento a ser pego(pai) será o primeiro
                except IndexError:
                    if int(matrizElementos[0][caracteristica]) not in matrizGeracaoNova[elemento]:
                        matrizGeracaoNova[elemento][caracteristica] = matrizElementos[0][caracteristica]

    return matrizGeracaoNova


def aplicacao(qntgeracao, matrizElementos, matrizCidade):
    """
    É o programa principal, que faz o ‘loop’ de gerações.
    :param qntgeracao: quantidade de gerações, ou seja, quantas vezes o 'loop' irá rodar.
    :param matrizElementos: é a matriz de individuos.
    :param matrizCidade: matriz das cidades, dos itinerarios.

    :return:
    """
    # Inicia uma matriz que irá ter a soma dos fit
    matrizFit = list()
    # Try serve para caso o usuário queira parar em algum momento, o programa não retorne erro.
    try:
        for linhagem in range(qntgeracao):
            novosElementos = matrizElementos.copy()
            # Printa um parametro para ter uma noção de como estão os fit.
            print(sum(fitDistancia(novosElementos, matrizCidade)) / (len(matrizElementos) * (len(matrizElementos[0]))))
            # Adiciona as fits na matriz
            matrizFit.append(int(sum(fitDistancia(novosElementos, matrizCidade))))
            print(f"Geração: {linhagem}")
            # Aplicação dos otimizadores.
            novosElementos = cruzamento(novosElementos, cruzamentoTaxa)
            novosElementos = mutacao(novosElementos, mutacaoTaxa, len(matrizCidade))
            # É o metodo de Seleção! importante para determinar quais gerações serão melhores
            # A condição, neste caso, serve para selecionar a matriz de individuos que tem o menor fit
            if sum(fitDistancia(novosElementos, matrizCidade)) < sum(fitDistancia(matrizElementos, matrizCidade)):
                matrizElementos = novosElementos.copy()
            else:
                matrizElementos = matrizElementos.copy()
    except KeyboardInterrupt:
        return matrizElementos, matrizFit

    return matrizElementos, matrizFit


# Parametros iniciais (A quantidade de cidades tem que ser obrigatoriamente maior que o número de viagens)
quantidadeCidades = 10  # Para criar a matriz de cidades
pessoas = 5  # População
viagens = 3  # Caracteristicas
geracoes = 500000

# Parametors para criação de novos individuos
cruzamentoTaxa = 0.4
mutacaoTaxa = 0.2

# APLICACAO DO PROGRAMA
matrizCidades = matrizDistancias(quantidadeCidades)
elementos = populacao(pessoas, viagens, quantidadeCidades)
print(elementos)
print(cruzamento(elementos, cruzamentoTaxa))
resultado, matrizfit = aplicacao(geracoes, elementos, matrizCidades)

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

plt.plot(matrizfit)
plt.title("Caixeiro Viajante por Evolucao Diferencial")
plt.grid(True)
plt.xlabel("GERAÇÕES")
plt.ylabel("SOMA DAS DISTANCIAS")
plt.show()
print("ericgmicaela@gmail")
