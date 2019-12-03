import threading
import time
from progress.bar import Bar
from processa_filme import ProcessaImagem
from imdb import IMDbError
from urllib.error import URLError,HTTPError

class myThread (threading.Thread):
   def __init__(self, threadID, name,linhaInicio,linhaFim,dataSetLinks,listaDeFilmesLink,listaDeFilmesLinksNaoValidos):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.linhaInicio = linhaInicio
      self.linhaFim = linhaFim
      self.dataFrameDeLinks = dataSetLinks
      self.listaDeFilmesLink = listaDeFilmesLink
      self.listaDeFilmesLinksNaoValidos = listaDeFilmesLinksNaoValidos
      self.processaFilme = ProcessaImagem()

   def run(self):
      bar = self.bar = Bar(self.name, max=(self.linhaFim-self.linhaInicio))
      i = self.linhaInicio
      while i < self.linhaFim:
         idDoFilme = self.dataFrameDeLinks.loc[i][0]
         idImdbDoFilme = self.dataFrameDeLinks.loc[i][1]
         try:
            self.listaDeFilmesLink.append((idDoFilme,self.processaFilme.retornaLinkImagem(idImdbDoFilme)))
            print("")
            bar.next()
         except IMDbError as error:
            errorType = error.args[0]['original exception']
            if type(errorType) == HTTPError:
               self.listaDeFilmesLinksNaoValidos.append((idDoFilme,idImdbDoFilme))
               print("")
               bar.next()
            else:
               time.sleep(15)
               i = i - 1
         i += 1
      bar.finish()

