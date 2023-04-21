import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
import datetime as dt
import statistics 
from numpy.linalg import norm 
from numpy import dot
from scipy.spatial import distance
import re

def normalize(data):
    '''
    This function will normalize the input data to be between 0 and 1
    
    params:
        data (List) : The list of values you want to normalize
    
    returns:
        The input data normalized between 0 and 1
    '''
    min_val = min(data)
    if min_val < 0:
        data = [x + abs(min_val) for x in data]
    max_val = max(data)
    return [x/max_val for x in data]

df = pd.read_csv("DatasetLimpio.csv")

dataSim = df.copy(deep=True)
marcaDummies = pd.get_dummies(dataSim['Marca'], prefix="SO_",)
dataSim = pd.concat([dataSim,marcaDummies],axis=1)
conectorDummies = pd.get_dummies(dataSim['Conector'], prefix="Con_",)
dataSim = pd.concat([dataSim,conectorDummies],axis=1)
dataSim.drop(['Marca'], axis=1, inplace=True)
dataSim.drop(['Conector'], axis=1, inplace=True)
dataSim.drop(['Dimensiones'], axis=1, inplace=True)
dataSim.drop(['Sistema Operativo'], axis=1, inplace=True)
dataSim.drop(['Resolucion Pixeles'], axis=1, inplace=True)
dataSim.drop(['Fecha Anuncio'], axis=1, inplace=True)

columnas_ignorar = ["URL","Colores","ImagenTelefono"]
for i in columnas_ignorar:
    dataSim.drop([i], axis=1, inplace=True)

columnas_normalizar = ["Horas Bateria", "Horas Llamada Bateria", "Bateria mAh", "Peso Gramos", 
"Resolucion Pixeles Ancho", "Resolucion Pixeles Alto", "Resolucion PPI", "Tamano Pulgadas", 
"RAM GB", "Memoria GB", "CPU GHz", "Vida Bateria", "Procesadores", 
                       #"Anio Anuncio", "Mes Anuncio", "Dia Anuncio", 
"Alto", "Ancho", "Grueso", "Camara MP", "Num Camaras", "Selfie MP", "Num Selfie",
"Video Pixeles", "Video FPS", "Selfie Video Pixeles", "Selfie Video FPS", "Precio"]
for i in columnas_normalizar:
    dataSim[i+"_NORM"] = normalize(dataSim[i].values)
    dataSim.drop(columns = [i], inplace = True)
dataSim.drop(columns = [ "Anio Anuncio", "Mes Anuncio", "Dia Anuncio"], inplace = True)

with open("DatasetVectorizado.csv", "w") as text_file:
    text_file.write(dataSim.to_csv(index=False))