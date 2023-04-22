import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
import datetime as dt
import statistics 

with open('cat_dict.json') as f:
    cat_dict = json.load(f)
    
with open('cat_dict_filtros.json') as f:
    cat_dict_filtros = json.load(f)
    
with open('col_type_dict.json') as f:
    col_type_dict = json.load(f)

dataTelefonos = pd.read_csv("DatasetTelefonosCategorizacion.csv")

clasificacion = pd.DataFrame(columns=['Categoria', 'Columna', 'Valor', 'Min', 'Max', 'Count'])

for key in cat_dict.keys():
    if key not in ["Llave","Info"]:
        for ele in cat_dict[key]:
            col = ""
            if type(ele) is list:
                col=ele[0]
            else:
                col=ele
            if len(cat_dict_filtros[key])==3:
                for cat in cat_dict_filtros[key]:
                    res = dataTelefonos[((dataTelefonos[key]==cat) & (dataTelefonos[col]!=0))][col]
                    clasificacion.loc[len(clasificacion)] = [key, col, cat, res.min(), res.max(), res.count() ]        
                    
with open("ClasificacionTelefonos.csv", "w") as text_file:
    text_file.write(clasificacion.to_csv(index=False))
    
