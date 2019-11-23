import pandas as pd

dataFilme = pd.read_csv("ml-latest-small\\movies.csv") 
variavel = pd.DataFrame(dataFilme).loc[0][0]
variavel = str(variavel)
if "1" == "1.0":
    print(type(variavel))