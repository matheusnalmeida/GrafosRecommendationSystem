import numpy as np
from filme import Filme
from usuario import Usuario
import pandas as pd

class geradorDeMatriz:

    def __init__(self,arquivoDeFilmes,arquivoDeNotas):
        #Foram criados um dicionario e lista para cada entidade para que se torne mais rapida a busca e a leitura de dados
        self.listaDeFilmesC , self.dicionarioDeFilmesC = self.__gerarListaDeFilmes__(pd.DataFrame(arquivoDeFilmes))
        self.listaDeUsuariosC, self.dicionarioDeUsuariosC = self.__gerarListaDeUsuarios__(pd.DataFrame(arquivoDeNotas))
                
    #Metodo responsavel por gerar o dicionario e lista de Filmes
    def __gerarListaDeFilmes__(self,dataFrameDeFilmes):
      listaDeFilmes = list()
      dicionarioDeFIlmes = dict()
      for linha in range(0,len(dataFrameDeFilmes)):
        idDoFilme = dataFrameDeFilmes.loc[linha][0]
        nomedoFilme = dataFrameDeFilmes.loc[linha][1]
        vetorDeCategorias = dataFrameDeFilmes.loc[linha][2].split("|")
        novoFilme = Filme(idDoFilme,nomedoFilme,vetorDeCategorias)
        listaDeFilmes.append(novoFilme)
        dicionarioDeFIlmes[idDoFilme] = novoFilme

      return listaDeFilmes,dicionarioDeFIlmes 
    
    #Metodo responsavel por gerar o dicionario e lista de Usuarios
    def __gerarListaDeUsuarios__(self,dataFrameDeNotas):
      listaDeUsuarios = list()
      dicionarioDeUsuarios = dict()
      for linha in range(0,len(dataFrameDeNotas)):
        idDoUsuario = str(int(dataFrameDeNotas.loc[linha][0]))
        filmeDoUsuario = self.dicionarioDeFilmesC.get(dataFrameDeNotas.loc[linha][1])
        notaDoFilme = dataFrameDeNotas.loc[linha][2]
        if idDoUsuario in dicionarioDeUsuarios:
          dicionarioDeUsuarios.get(idDoUsuario).insereFilmeAvaliado(filmeDoUsuario,notaDoFilme)
        else:
          novoUsuario = Usuario(idDoUsuario)
          novoUsuario.insereFilmeAvaliado(filmeDoUsuario,notaDoFilme)
          dicionarioDeUsuarios[idDoUsuario] = novoUsuario
          listaDeUsuarios.append(novoUsuario)
              
      return listaDeUsuarios,dicionarioDeUsuarios

    def retornaFilmesComMaiorNota(self,idDoUsuario):
      #Retornando o usuario com o respectivo id e retornando o seu dicionario de filmes 
      #print(self.dicionarioDeUsuariosC)
      usuario = self.dicionarioDeUsuariosC.get(idDoUsuario)
      dicionarioDeFilmesAvaliados = usuario.getDicionarioDeFilmes()
      
      #Retornando o vetor de filmes avaliados na ordem decrescente para que sejam retornados as tres maiores avaliacoes
      vetorDeNotas = list(dicionarioDeFilmesAvaliados.keys())
      vetorDeNotas = sorted(vetorDeNotas,reverse=True)

      #Salvando as listas de filmes com as tres maiores notas
      dicionarioDasNotas = dict()
      for i in range(0,3):
        dicionarioDasNotas[vetorDeNotas[i]] = dicionarioDeFilmesAvaliados.get(vetorDeNotas[i])

      return dicionarioDasNotas
    
    def recomendacao():
      pass

    def getDicionarioDeFilmes(self):
      return self.dicionarioDeFilmesC
    
    def getDicionarioDeUsuarios(self):
      return self.dicionarioDeUsuariosC

      
