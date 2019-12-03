import sqlite3

'''
Este arquivo ira conter a classe representativa do banco de dados que ira conter duas tabelas:
1)Movies => Ira salvar os filmes que possuem links validos e existentes no imdb
2)InvalidMovies => Ira salvar todos os filmes que possuirem links invalidos(nao existentes no imdb).
'''
class DataBase:

    def __init__(self):
        self.conn = sqlite3.connect('..\\main_classes\\moviesLinks.db')
        self.c = self.conn.cursor()
    
    #----------------------------Metodos para filmes validos-----------------------------------------
    def insert_movie(self,id,link):
        with self.conn:
            self.c.execute("INSERT INTO Movie (id,link) VALUES (:id, :link)", {'id': id, 'link': link,})

    def get_movies_by_id(self,id):
        self.c.execute("SELECT * FROM Movie WHERE id=:id", {'id': id})
        return self.c.fetchall()
    
    def get_all_movies(self):
        self.c.execute("SELECT * FROM Movie")
        return self.c.fetchall()

    def remove_movies(self,id):
        with self.conn:
            self.c.execute("DELETE from Movie WHERE id = :id",
                    {'id': id})

    def insert_movies_massive(self,listaDeLinks):
        with self.conn:
            self.c.executemany("INSERT INTO Movie VALUES(?,?);",listaDeLinks)
            
    def get_number_of_rows(self):
        return len(self.c.execute("select (select count() from Movie) as count, * from Movie").fetchall())

    #------------------------------------Metodos para filmes invalidos-----------------------------------------

    def insert_movie_invalid(self,id,link):
        with self.conn:
            self.c.execute("INSERT INTO InvalidMovies (id,link) VALUES (:id, :link)", {'id': id, 'link': link,})

    def get_movies_by_id_invalid(self,id):
        self.c.execute("SELECT * FROM InvalidMovies WHERE id=:id", {'id': id})
        return self.c.fetchall()
    
    def get_all_invalid_movies(self):
        self.c.execute("SELECT * FROM InvalidMovies")
        return self.c.fetchall()

    def remove_movies_invalid(self,id):
        with self.conn:
            self.c.execute("DELETE from InvalidMovies WHERE id = :id",
                    {'id': id})

    def insert_movies_massive_invalid(self,listaDeLinksInvalidos):
        with self.conn:
            self.c.executemany("INSERT INTO InvalidMovies VALUES(?,?);",listaDeLinksInvalidos)
            
    def get_number_of_rows_invalid(self):
        return len(self.c.execute("select (select count() from InvalidMovies) as count, * from InvalidMovies").fetchall())