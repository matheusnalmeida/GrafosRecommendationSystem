class Filme:
    def __init__(self,id,nomeDoFilme,generos):
        self.id = id
        self.nomeDoFilme = nomeDoFilme
        self.genero = generos

    def getListaDeGeneros(self):
        return self.genero
    
    def getId(self):
        return self.id

    def __str__(self):
        return self.nomeDoFilme
    
    def __eq__(self, obj):
        return isinstance(obj, Filme) and obj.id == self.id