from filme import Filme
from usuario import Usuario
import pandas as pd
import random
from progress.bar import Bar

class SistemaDeRecomendacao:

    def __init__(self,arquivoDeFilmes,arquivoDeLinks,arquivoDeNotas):
        self.dicionarioDeFilmePorIdC ,self.dicionarioDeFilmesPorCategoriaC = self.__gerarListaDeFilmes__(pd.DataFrame(arquivoDeFilmes),pd.DataFrame(arquivoDeLinks))
        self.dicionarioDeUsuariosC = self.__gerarListaDeUsuarios__(pd.DataFrame(arquivoDeNotas))
                
    #Metodo responsavel por gerar o dicionario e lista de Filmes
    '''
    O dataframe de filmes sera utilizado para se retornar o nome do filme, suas categorias e o seu id pelo csv, 
    já o dataframe de links sera utilizado para retornar o link do respectivom filme no site do imdb
    '''
    def __gerarListaDeFilmes__(self,dataFrameDeFilmes,dataFrameDeLinks):
      dicionarioDeFilmesPorId = dict()
      dicionarioDeFilmesPorCategoria = dict() 
      for linha in range(0,len(dataFrameDeFilmes)):
        idDoFilme = dataFrameDeFilmes.loc[linha][0]
        idImdbDoFilme = dataFrameDeLinks.loc[linha][1]
        nomedoFilme = dataFrameDeFilmes.loc[linha][1]
        vetorDeCategorias = dataFrameDeFilmes.loc[linha][2].split("|")
        novoFilme = Filme(idDoFilme,idImdbDoFilme,nomedoFilme,vetorDeCategorias)
        #Verificando vetor de categorias para que sejam adicionadas no dicionario de filme por categoria
        for categoria in vetorDeCategorias:
          if categoria in dicionarioDeFilmesPorCategoria:
            dicionarioDeFilmesPorCategoria[categoria].append(novoFilme)
          else:
            dicionarioDeFilmesPorCategoria[categoria] = [novoFilme]
        dicionarioDeFilmesPorId[idDoFilme] = novoFilme

      return dicionarioDeFilmesPorId,dicionarioDeFilmesPorCategoria
    
    #Metodo responsavel por gerar o dicionario e lista de Usuarios
    def __gerarListaDeUsuarios__(self,dataFrameDeNotas):
      dicionarioDeUsuarios = dict()
      for linha in range(0,len(dataFrameDeNotas)):
        idDoUsuario = dataFrameDeNotas.loc[linha][0]
        idDoFilme = dataFrameDeNotas.loc[linha][1]
        filmeDoUsuario = self.dicionarioDeFilmePorIdC.get(idDoFilme)
        notaDoFilme = dataFrameDeNotas.loc[linha][2]
        if idDoUsuario in dicionarioDeUsuarios:
          dicionarioDeUsuarios.get(idDoUsuario).insereFilmeAvaliado(filmeDoUsuario,notaDoFilme)
        else:
          novoUsuario = Usuario(idDoUsuario)
          novoUsuario.insereFilmeAvaliado(filmeDoUsuario,notaDoFilme)
          dicionarioDeUsuarios[idDoUsuario] = novoUsuario
              
      return dicionarioDeUsuarios
    

    #Metodo responsavel por informar se o filme passado por parametro deve ser ou nao recomendado para o usuario com o respextivo id informado
    def verificarSeFilmeDeveSerRecomendado(self,idDoUsuario,idDoFilme):
      dicionarioDeFilmesASeremRecomendados = self.recomendarFilmesParaUsuario(idDoUsuario,quantidadeDeFilmesPorCategoria = len(self.dicionarioDeFilmePorIdC))
      #Verificando se o filme com o respectivo id informado esta na lista de possiveis filmes que o usuario ira gostar
      for categoria in dicionarioDeFilmesASeremRecomendados:
        for filmeAtual in dicionarioDeFilmesASeremRecomendados[categoria]:
          if filmeAtual.getId() == idDoFilme:
            return True
      
      return False

    #METODO PRINCIPAL RESPONSAVEL POR RETORNAR O DICIONARIO DE FILMES DIVIDIDOS POR CATEGORIA QUE SERAO RECOMENDADOS AO USUARIO
    def recomendarFilmesParaUsuario(self,idDoUsuario,quantidadeDeFilmesPorCategoria = None):
      #Caso a quantidade de filmes por categoria a ser recomendada nao seja passada por parametro, serao retornados 6 elementos por categoria
      if quantidadeDeFilmesPorCategoria == None:
        quantidadeDeFilmesPorCategoria = 6

      dicionarioDeFilmesComMaiorNota = self.__retornaFilmesComMaiorNota__(idDoUsuario)
      dicionarioDeCategoriasMelhoresAvaliadas = self.__retornarCategoriasMelhoresAvaliadas__(dicionarioDeFilmesComMaiorNota)
      filmesASeremRecomendados,listaDeIdsFilmes = self.__retornarFilmesASeremRecomendadosPorCategoria__(dicionarioDeCategoriasMelhoresAvaliadas,quantidadeDeFilmesPorCategoria = quantidadeDeFilmesPorCategoria)

      return filmesASeremRecomendados,listaDeIdsFilmes

    '''
    Metodo responsavel por retornar um dicionario contendo tres chaves que serao as tres maiores notas dadas aos filmes
    e os respectivos filmes que possuem cada uma das notas
    '''   
    def __retornaFilmesComMaiorNota__(self,idDoUsuario):
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
    def __retornarCategoriasMelhoresAvaliadas__(self,dicionarioDasNotas):
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
    def __retornarFilmesASeremRecomendadosPorCategoria__(self,dicionarioDeCategoriasMelhoresAvaliadas,quantidadeDeFilmesPorCategoria):
      dicionarioDeFilmesASeremRecomendados = dict()
      '''
      Sera criada uma copia do dicionario de filmes para que assim os filmes possam ser escolhidos de maneira aleatoria e 
      removidos do vetor sem que se altere o vetor original
      '''
      dicionarioDeFilmesPorIdCopia = self.dicionarioDeFilmePorIdC.copy()
  
      #Iniciando o diciomnario de filmes a serem recomendados com a chave de cada categoria e uma lista de filmes em cada posicao
      for categoria in dicionarioDeCategoriasMelhoresAvaliadas:
        dicionarioDeFilmesASeremRecomendados[categoria] = list()
        listaDeIds = list()

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
            if (not self.contemFilme(filmeAtual,dicionarioDeCategoriasMelhoresAvaliadas[genero])) and (len(dicionarioDeFilmesASeremRecomendados[genero]) != quantidadeDeFilmesPorCategoria):
              dicionarioDeFilmesASeremRecomendados[genero].append(filmeAtual)
              listaDeIds.append(filmeAtual.getImdbID())
              break
    
      return dicionarioDeFilmesASeremRecomendados,listaDeIds

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

    def getHashDeFilmes(self):
      return self.dicionarioDeFilmePorIdC
      
