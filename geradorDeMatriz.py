from filme import Filme
from usuario import Usuario
import pandas as pd
import random

class geradorDeMatriz:

    def __init__(self,arquivoDeFilmes,arquivoDeNotas):
        #Foram criados um dicionario e lista para cada entidade para que se torne mais rapida a busca e a leitura de dados
        self.listaDeFilmesC , self.dicionarioDeFilmePorIdC ,self.dicionarioDeFilmesPorCategoriaC = self.__gerarListaDeFilmes__(pd.DataFrame(arquivoDeFilmes))
        self.listaDeUsuariosC, self.dicionarioDeUsuariosC = self.__gerarListaDeUsuarios__(pd.DataFrame(arquivoDeNotas))
                
    #Metodo responsavel por gerar o dicionario e lista de Filmes
    def __gerarListaDeFilmes__(self,dataFrameDeFilmes):
      listaDeFilmes = list()
      dicionarioDeFilmesPorId = dict()
      dicionarioDeFilmesPorCategoria = dict() 
      for linha in range(0,len(dataFrameDeFilmes)):
        idDoFilme = dataFrameDeFilmes.loc[linha][0]
        nomedoFilme = dataFrameDeFilmes.loc[linha][1]
        vetorDeCategorias = dataFrameDeFilmes.loc[linha][2].split("|")
        novoFilme = Filme(idDoFilme,nomedoFilme,vetorDeCategorias)
        #Verificando vetor de categorias para que sejam adicionadas no dicionario de filme por categoria
        for categoria in vetorDeCategorias:
          if categoria in dicionarioDeFilmesPorCategoria:
            dicionarioDeFilmesPorCategoria[categoria].append(novoFilme)
          else:
            dicionarioDeFilmesPorCategoria[categoria] = [novoFilme]
        listaDeFilmes.append(novoFilme)
        dicionarioDeFilmesPorId[idDoFilme] = novoFilme

      return listaDeFilmes,dicionarioDeFilmesPorId,dicionarioDeFilmesPorCategoria
    
    #Metodo responsavel por gerar o dicionario e lista de Usuarios
    def __gerarListaDeUsuarios__(self,dataFrameDeNotas):
      listaDeUsuarios = list()
      dicionarioDeUsuarios = dict()
      for linha in range(0,len(dataFrameDeNotas)):
        idDoUsuario = str(int(dataFrameDeNotas.loc[linha][0]))
        filmeDoUsuario = self.dicionarioDeFilmePorIdC.get(dataFrameDeNotas.loc[linha][1])
        notaDoFilme = dataFrameDeNotas.loc[linha][2]
        if idDoUsuario in dicionarioDeUsuarios:
          dicionarioDeUsuarios.get(idDoUsuario).insereFilmeAvaliado(filmeDoUsuario,notaDoFilme)
        else:
          novoUsuario = Usuario(idDoUsuario)
          novoUsuario.insereFilmeAvaliado(filmeDoUsuario,notaDoFilme)
          dicionarioDeUsuarios[idDoUsuario] = novoUsuario
          listaDeUsuarios.append(novoUsuario)
              
      return listaDeUsuarios,dicionarioDeUsuarios

    #Metodo responsavel por informar se o filme passado por parametro deve ser ou nao recomendado para o usuario com o respextivo id informado
    # def verificarSeFilmeDeveSerRecomendado(self,)
    #   listaDeFilmesASerem

    def recomendarFilmesParaUsuario(self,idDoUsuario):
      dicionarioDeFilmesComMaiorNota = self.retornaFilmesComMaiorNota(idDoUsuario)
      dicionarioDeCategoriasMelhoresAvaliadas = self.retornarCategoriasMelhoresAvaliadas(dicionarioDeFilmesComMaiorNota)
      filmesASeremRecomendados = self.retornarFilmesASeremRecomendadosPorCategoria(dicionarioDeCategoriasMelhoresAvaliadas,quantidadeDeElementosPorCategoria = 6)

      return filmesASeremRecomendados

    def retornaFilmesComMaiorNota(self,idDoUsuario):
      #Retornando o usuario com o respectivo id e retornando o seu dicionario de filmes 
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
    
    '''
    Metodo responsavel por retornar as categorias dos filmes mellhores avaliados por um determinado usuario. Sera passado como parametro
    o dicionario dos filmes melhores avaliados por um determinado usuario.
    '''
    def retornarCategoriasMelhoresAvaliadas(self,dicionarioDasNotas):
      dicionarioDeCategoriasMelhoresAvaliadas = dict()
      for i in dicionarioDasNotas:
        for filme in dicionarioDasNotas.get(i):
            listaDeCategoriasFilmeAtual = filme.getListaDeGeneros()
            for categoria in listaDeCategoriasFilmeAtual:
              if categoria not in dicionarioDeCategoriasMelhoresAvaliadas:
                dicionarioDeCategoriasMelhoresAvaliadas[categoria] = [filme]
              else:
                dicionarioDeCategoriasMelhoresAvaliadas[categoria].append(filme)

      return dicionarioDeCategoriasMelhoresAvaliadas

    #Metodo responsavel por retornar o dicionario contendo os filmes a serem recomendados dividados por categorias
    def retornarFilmesASeremRecomendadosPorCategoria(self,dicionarioDeCategoriasMelhoresAvaliadas,quantidadeDeElementosPorCategoria = None):
      '''
      Caso a quantidade de filmes por genero a ser recomendada nao seja passada por parametro, serao retornados o maximo possivel 
      de elementos por categoria
      '''
      if (quantidadeDeElementosPorCategoria == None):
        quantidadeDeElementosPorCategoria = len(self.dicionarioDeFilmePorIdC)

      dicionarioDeFilmesASeremRecomendados = dict()
      '''
      Sera criada uma copia do dicionario de filmes para que assim os filmes possam ser escolhidos de maneira aleatoria e 
      removidos do vetor sem que se altere o vetor original
      '''
      dicionarioDeFilmesPorIdCopia = self.dicionarioDeFilmePorIdC.copy()
  
      #Iniciando o diciomnario de filmes a serem recomendados com a chave de cada categoria e uma lista de filmes em cada posicao
      for categoria in dicionarioDeCategoriasMelhoresAvaliadas:
        dicionarioDeFilmesASeremRecomendados[categoria] = list()

      #Serao percorridos todos os filmes que estao cadastrados no sistema
      while(len(dicionarioDeFilmesPorIdCopia) != 0):
        #Sera entao escolhido um filme de id randomico, sendo o mesmo salvo e removido do dicionario copia de filmes
        idDoFilmeAtual = random.choice(list(dicionarioDeFilmesPorIdCopia.keys()))
        filmeAtual = dicionarioDeFilmesPorIdCopia[idDoFilmeAtual]   
        dicionarioDeFilmesPorIdCopia.pop(idDoFilmeAtual)

        #Com isso sera verificado se o filme possui genero(s) em comum com algum dos generos melhores avaliados pelo usuario  
        listaDeGenerosEmComum = self.__verificaCategoriasSimilares__(dicionarioDeCategoriasMelhoresAvaliadas,filmeAtual.getListaDeGeneros())  
        if len(listaDeGenerosEmComum) > 0:
          '''
          Tendo os generos em comum em maos, sera verificado para cada genero em comum, se o filme ja foi assistido pelo usuario e se a 
          respectiva categoria ja possui a quantidade maxima de filmes a serem recomendados(nesse caso serao 6)
          '''
          for genero in listaDeGenerosEmComum:
            if (not self.contemFilme(filmeAtual,dicionarioDeCategoriasMelhoresAvaliadas[genero])) and (len(dicionarioDeFilmesASeremRecomendados[genero]) != quantidadeDeElementosPorCategoria):
              dicionarioDeFilmesASeremRecomendados[genero].append(filmeAtual)
              break
    
      return dicionarioDeFilmesASeremRecomendados

    '''
    Metodo responsavel por dada uma lista de categorias melhores avaliadas por um determinado usuario e 
    uma lista de categorias de determinado filme, o mesmo ira retornar um vetor contendo as categorias do filme atual que sao comuns
    com as categorias mais bem avaliadas pelo usuario.
    '''
    def __verificaCategoriasSimilares__(self,dicionarioDeCategoriasMelhoresAvaliadas,listaDeCategoriasFilmeAtual):
      vetorDeCategoriasEmComum = list()
      for categoria in listaDeCategoriasFilmeAtual:
        if categoria in dicionarioDeCategoriasMelhoresAvaliadas:
          vetorDeCategoriasEmComum.append(categoria)
      
      return vetorDeCategoriasEmComum
    
    '''
    Verificar se a respectiva lista de filmes passada como parametro contem o respectivo filme passado como parametro
    '''
    def contemFilme(self,filmeAtual,listaDeFilmes):
      for filme in listaDeFilmes:
        if filme.__eq__(filmeAtual):
          return True

      return False

    def getDicionarioDeFilmes(self):
      return self.dicionarioDeFilmePorIdC
    
    def getDicionarioDeUsuarios(self):
      return self.dicionarioDeUsuariosC

      
