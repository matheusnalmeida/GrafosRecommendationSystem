from pprint import pprint
from imdb import IMDb

class ProcessaImagem:
    def __init__(self):
        self.dataSet = IMDb(reraiseExceptions=True)

    def retornaLinkImagem(self,idDoFilme):
            try:
                movie = self.dataSet.get_movie(idDoFilme)
                return movie['cover url']
            except KeyError:
                return "https://image.shutterstock.com/image-vector/no-image-available-sign-internet-600w-261719003.jpg"
            
        

