from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from pprint import pprint
from re import findall, match

class ProcessaImagem:
    def __init__(self):
        self.url = "https://www.imdb.com/title/tt"

    def retornaLinkImagem(self,idDoFilme):
        urlFilmeAtual = self.url
        urlFilmeAtual += idDoFilme + "/"
        req = Request(urlFilmeAtual)
        webpage = urlopen(req).read()
        page_soup = soup(webpage, 'html.parser')
        
        divImagem = page_soup.find_all('div',{"class": "poster"})

        return divImagem[0].find('a').find('img').get('src')

