import pandas as pd
from geradorDeMatriz import geradorDeMatriz

if __name__ == "__main__":
    dataFilme = pd.read_csv("ml-latest-small\\movies.csv") 
    dataNotas = pd.read_csv("ml-latest-small\\ratings.csv")
    geradorDeMatriz = geradorDeMatriz(dataNotas,dataFilme)
    matrizDeAdjacencia = geradorDeMatriz.gerarMatrizDeAdjacencia()
