from pprint import pprint
import random

if __name__ == "__main__":
    dicionario = {1: "ALdoViado",2: "Matheus",3: "Erik"}
    dicionario2 = dicionario.copy()

    while (len(dicionario2) != 0):
        valor = random.choice(list(dicionario2.keys()))
        pprint(valor)
        dicionario2.pop(valor)
    pprint(dicionario)
    pprint(dicionario2)