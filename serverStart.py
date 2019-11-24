import pandas as pd
from sistema_de_recomendacao import SistemaDeRecomendacao
from flask import render_template, request, Flask, render_template_string
import os
import json
from processa_filme import ProcessaImagem
import numpy as np

if __name__ == "__main__":

    app = Flask(__name__)

    print("Iniciando Leitura De Arquivos ...")
    dataFilme = pd.read_csv("ml-latest-small\\movies.csv",dtype=np.str) 
    dataUsuarios =  pd.read_csv("ml-latest-small\\ratings.csv",dtype=np.str) 
    dataDeLinks = pd.read_csv("ml-latest-small\\links.csv",dtype=np.str) 
    sistemaDeRecomendacao = SistemaDeRecomendacao(dataFilme,dataDeLinks,dataUsuarios)
    processaFilme = ProcessaImagem()
    print("Leitura de arquivos finalizada.")

    @app.after_request
    def after_request(response):
        header = response.headers
        header['Access-Control-Allow-Headers'] = '*'
        header['Access-Control-Allow-Origin'] = '*'
        return response

    @app.route('/', methods=['GET'])
    def inicial_page():
        return render_template('inicial.html')
    
    @app.route("/listarFilme/<id>",methods=['POST'])
    def pagina_de_recomendacao(id):
        dicionarioDeFilmesPorCategoria = sistemaDeRecomendacao.recomendarFilmesParaUsuario(id,quantidadeDeFilmesPorCategoria=3)
        dicionarioDeFilmesFinal = dict()

        for categoria in dicionarioDeFilmesPorCategoria:
            dicionarioDeFilmesFinal[categoria] = list()
            for filme in dicionarioDeFilmesPorCategoria[categoria]:
                dicionarioDeFilmesFinal[categoria].append({filme.getNomeDoFilme(): processaFilme.retornaLinkImagem(filme.getImdbID())})
        
        return render_template("paginaDeFilmes.html",dicionarioDeFilmes=dicionarioDeFilmesFinal)

    app.debug = False
    host = os.environ.get('IP', '0.0.0.0')
    port = int(os.environ.get('PORT', 8080))
    app.run(host=host, port=port)
