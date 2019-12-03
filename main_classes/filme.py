class Filme:
    def __init__(self,id,imdbID,nomeDoFilme,generos):
        self.id = id
        self.imdbID = imdbID
        self.nomeDoFilme = nomeDoFilme
        self.genero = generos

    def getListaDeGeneros(self):
        return self.genero
    
    def getId(self):
        return self.id

    def getImdbID(self):
        return self.imdbID

    def getNomeDoFilme(self):
        return self.nomeDoFilme
        
    def __str__(self):
        return self.nomeDoFilme
    
    def __eq__(self, obj):
        return isinstance(obj, Filme) and obj.id == self.id