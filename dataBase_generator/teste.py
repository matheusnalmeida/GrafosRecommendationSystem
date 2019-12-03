from progress.bar import Bar
import pandas as pd
import os
import json
from processa_filme import ProcessaImagem
import numpy as np
from myThread import myThread
from bancoDeDadosSQLlite import DataBase
from imdb import IMDb,IMDbError
from pprint import pprint
from urllib.error import URLError,HTTPError
a = []
try:
    imdb = IMDb(reraiseExceptions=True)
    movie = imdb.get_movie("2492564")
    pprint(movie.data)
except IMDbError as aa:
    errorType = aa.args[0]['original exception']
    print(type(errorType))
    ass = URLError(TimeoutError(10060, 'Uma tentativa de conexão falhou porque o componente conectado não respondeu\r\ncorretamente após um período de tempo ou a conexão estabelecida falhou\r\nporque o host conectado não respondeu', None, 10060, None))
    print(ass.args[0].args)
    if type(errorType) == HTTPError:
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

print(a)