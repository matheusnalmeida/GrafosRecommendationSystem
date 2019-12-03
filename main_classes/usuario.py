class Usuario:

    def __init__(self,idDoUsuario):
        self.idDoUsuario = idDoUsuario
        self.dicionarioDeFilmesAvaliados = dict()

    def insereFilmeAvaliado(self,filme,nota):
        if nota in self.dicionarioDeFilmesAvaliados:
            self.dicionarioDeFilmesAvaliados.get(nota).append(filme)
        else:
            self.dicionarioDeFilmesAvaliados[nota] = list()
            self.dicionarioDeFilmesAvaliados.get(nota).append(filme)

    def getDicionarioDeFilmes(self):
        return self.dicionarioDeFilmesAvaliados

    def __eq__(self, obj):
        return isinstance(obj, Usuario) and obj.idDoUsuario == self.idDoUsuario

