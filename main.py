import pandas as pd
from geradorDeMatriz import geradorDeMatriz

dataFilme = pd.read_csv("ml-latest-small\\movies.csv") 
dataNotas = pd.read_csv("ml-latest-small\\ratings.csv")
geradorDeMatriz = geradorDeMatriz(dataNotas,dataFilme)
#matrizDeAdjacencia = geradorDeMatriz.gerarMatrizDeAdjacencia()
matrizDeAdjacencia = geradorDeMatriz.biparteMatrix(dataFilme,dataNotas)

#print(matrizDeAdjacencia)  