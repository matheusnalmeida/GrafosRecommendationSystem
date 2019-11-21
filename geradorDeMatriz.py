import numpy as np

class geradorDeMatriz:

    def __init__(self,ratings,filmes):
        self.ratings = ratings
        self.filmes = filmes
    
    #Metodo responsavel por gerar a matriz de adjacencia de usuarios X filmes
    def gerarMatrizDeAdjacencia(self):
      listaDeFilmes = list(self.filmes["movieId"].unique())
      listaDeUsuarios = list(self.ratings["userId"].unique())
      matrizDeAdjacencia = np.zeros((len(listaDeUsuarios),len(listaDeFilmes)))
    
      #Salvando lista de usuarios,filmes e notas na ordem do arquivo ratings
      usuariosRatings = list(self.ratings["userId"])
      filmesRatings = list(self.ratings["movieId"])
      ratings = list(self.ratings["rating"])

      #Preenchendo a matriz bipartida que representara o grafo
      for i in range(0,len(ratings)):
        posicaoDoUsuario = listaDeUsuarios.index(usuariosRatings[i])
        posicaoDoFilme = listaDeFilmes.index(filmesRatings[i])
        matrizDeAdjacencia[posicaoDoUsuario,posicaoDoFilme] = ratings[i]

      return matrizDeAdjacencia

      
