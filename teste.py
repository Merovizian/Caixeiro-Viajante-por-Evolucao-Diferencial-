from random import sample
import random
import numpy as np
ordem = 3
elementos = list
povoacao = escala = np.zeros((10, ordem+1))
for a in range(10):
    elementos= random.sample(range(0, ordem), ordem)
    elementos.append(elementos[0])
    povoacao[a] = elementos

print(povoacao)
