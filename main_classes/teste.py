import sys
sys.path.append('..')

from dataBase_generator.bancoDeDadosSQLlite import DataBase


data = DataBase()
dicionario = dict(data.get_all_invalid_movies())
if ("33" not in dicionario):
    print("cu")