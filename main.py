import pandas as pd
from geradorDeMatriz import geradorDeMatriz
import time
from filme import Filme

if __name__ == "__main__":
    dataFilme = pd.read_csv("ml-latest-small\\movies.csv") 
    dataUsuarios =  pd.read_csv("ml-latest-small\\ratings.csv") 
    filmeTEsT = Filme(1,"Aldo",2)
    filmeTEsT2 = Filme(2,"Matheus",2)
    filmeTEsT3 = Filme(3,"Erik",2)
    filmeTEsT4 = Filme(4,"Gabriel",2)    
    vetor1 = [filmeTEsT,filmeTEsT2]
    vetor2 = [filmeTEsT3,filmeTEsT4]
    dicionario = {1: vetor1,2:vetor2}

    inicio = time.time()
    geradorDeMatriz = geradorDeMatriz(dataFilme,dataUsuarios)
    fim = time.time()

    idDoUsuario = input("Digite o id do usuario que deseja buscar os filmes melhores avaliados: ")
    dicionarioDeFilmesMelhoresAvaliados = geradorDeMatriz.retornaFilmesComMaiorNota(idDoUsuario)
    
    for i in dicionarioDeFilmesMelhoresAvaliados:
        print("%s = " % i,end="")
        for y in dicionarioDeFilmesMelhoresAvaliados.get(i):
            print(y, end= ' ')
        print()

    temp = fim - inicio
    hours = temp//3600
    temp = temp - 3600*hours
    minutes = temp//60
    seconds = temp - 60*minutes
    print('%d:%d:%d' %(hours,minutes,seconds))

    #listaDeFilmes = []
    # listaDeFilmes.append(filmeTEsT)
    # listaDeFilmes.append(filmeTEsT2)
    # print(str(listaDeFilmes))
    # dataNotas = pd.read_csv("ml-latest-small\\ratings.csv")

    # matrizDeAdjacencia = geradorDeMatriz.gerarMatrizDeAdjacencia()]
    # df = pd.DataFrame(dataUsuarios)
    # print(df)
    # vetorCategorias = dataFilme.loc
    # for posicao in range(0,len(df)):
    #     print(df.loc[posicao][0])
