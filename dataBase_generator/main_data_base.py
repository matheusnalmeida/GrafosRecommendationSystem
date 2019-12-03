from progress.bar import Bar
import pandas as pd
import os
import json
from processa_filme import ProcessaImagem
import numpy as np
from myThread import myThread
from bancoDeDadosSQLlite import DataBase

def generate_interval(frequencia_do_intervalo):
    listaDeIntervalos = []
    for i in range(10):
        if frequencia_do_intervalo == 9740:
            listaDeIntervalos.append(frequencia_do_intervalo-974)
            listaDeIntervalos.append(frequencia_do_intervalo+2)
        else:
            listaDeIntervalos.append(frequencia_do_intervalo-974)
            listaDeIntervalos.append(frequencia_do_intervalo) 
            frequencia_do_intervalo += 974
    return listaDeIntervalos

def generate_threads(dataframeFilmes,listaDeIntervalos,listaDeFilmesLink,listaDeFilmesLinkInvalido):
    vetorDeThreads = []
    contador = 0
    for i in range(10):
        thread = myThread(1, "Thread-{}".format(i+1),listaDeIntervalos[contador],listaDeIntervalos[contador+1],dataframeFilmes,listaDeFilmesLink,listaDeFilmesLinkInvalido)
        vetorDeThreads.append(thread)
        contador = contador + 2
    return vetorDeThreads

dataFilme = pd.read_csv("..\\ml-latest-small\\links.csv",dtype=np.str) 
dataBase = DataBase()
dataframeFilmes = pd.DataFrame(dataFilme)
listaDeFilmesLink = list()
listaDeFilmesLinkInvalido = list()
listaDeIntervalos = generate_interval(974)
vetorDeThreads = generate_threads(dataframeFilmes,listaDeIntervalos,listaDeFilmesLink,listaDeFilmesLinkInvalido)

for thread in vetorDeThreads:
    thread.start()

for thread in vetorDeThreads:
    thread.join()

print("Threads Finished")
dataBase.insert_movies_massive(listaDeFilmesLink)
dataBase.insert_movies_massive_invalid(listaDeFilmesLinkInvalido)
print("DataBase completed")