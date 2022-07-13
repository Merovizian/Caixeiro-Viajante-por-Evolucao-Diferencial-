from random import sample
import random
import numpy as np
tamanhoPopulacao = 10
matrizCidades = [[0, 3, 5], [2, 0, 8], [1, 4, 0]]
matrizElementos = [[0, 2, 1, 0], [2, 1, 0, 2], [1, 2, 0, 1]]
'''ordem = 3
steps = 3
povoacao = np.zeros((tamanhoPopulacao, steps + 1))
for a in range(tamanhoPopulacao):
    elementos = random.sample(range(0, ordem), steps)
    elementos.append(elementos[0])
    povoacao[a] = elementos

print(povoacao)
'''
matrizGeracaoNova = matrizElementos
ValorCaracteristicaRandom = random.randint(0, 5)

for elementos in range(len(matrizElementos)):
    ValorCaracteristicaRandom = random.randint(0, 5)
    while ValorCaracteristicaRandom not in matrizElementos[elementos]:
        print(ValorCaracteristicaRandom)
        ValorCaracteristicaRandom = random.randint(0, 5)
        PosicaoCaracteristicaRandom = random.randint(0, len(matrizElementos[1]) - 1)
        matrizGeracaoNova[elementos][PosicaoCaracteristicaRandom] = ValorCaracteristicaRandom

print(matrizElementos)
print(matrizGeracaoNova)