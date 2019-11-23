import pandas as pd
from sistema_de_recomendacao import SistemaDeRecomendacao
import time
from filme import Filme
from pprint import pprint

if __name__ == "__main__":
    dataFilme = pd.read_csv("ml-latest-small\\movies.csv") 
    dataUsuarios =  pd.read_csv("ml-latest-small\\ratings.csv") 
    dataDeLinks = pd.read_csv("ml-latest-small\\links.csv") 
    inicio = time.time()
    sistemaDeRecomendacao = SistemaDeRecomendacao(dataFilme,dataDeLinks,dataUsuarios)
    fim = time.time()

    temp = fim - inicio
    hours = temp//3600
    temp = temp - 3600*hours
    minutes = temp//60
    seconds = temp - 60*minutes
    print('%d:%d:%d' %(hours,minutes,seconds))

    while(True):
        idDoUsuario = input("Digite o id do usuario que deseja buscar os filmes melhores avaliados: ")
        dicionarioDeFilmesRecomendados = sistemaDeRecomendacao.recomendarFilmesParaUsuario(idDoUsuario)

        for i in dicionarioDeFilmesRecomendados:
            pprint(i)
            for y in dicionarioDeFilmesRecomendados[i]:
                pprint(str(y))

        idDoFilme = input("Digite o id do filme a ser recomendado: ")
        pprint(sistemaDeRecomendacao.verificarSeFilmeDeveSerRecomendado(idDoUsuario,idDoFilme))

