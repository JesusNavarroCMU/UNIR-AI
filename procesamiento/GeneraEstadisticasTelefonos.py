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
import json
import pandas as pd

dataModel = pd.read_csv("DatasetTelefonosActivos.csv")
    
with open('col_type_dict.json') as f:
    col_type_dict = json.load(f)
    
cat_dict = {
    "Info" : ["Disponible","Colores","ImagenTelefono","URL","Marca","Sistema Operativo"],
    "Almacenamiento" : ["Memoria GB"],
    "Tiene SIM" : ["SIM"],
    "Bateria" : [["Bateria mAh",.7],["Horas Bateria",.2],["Horas Llamada Bateria",.05],["Vida Bateria",.05]],
    "Tiene Audifonos" : ["Audifonos"],
    "Tiene Bluetooth" : ["Bluetooth"],
    "Cable Conexion" : ["Conector"],
    "Camara" : [["Camara MP",.9],["Num Camaras",.1]],
    "Camara Video" : [["Video FPS",.2],["Video Pixeles",.8]],
    "Tiene Lector Huella" : ["Lector Huella"],
    "Llave": ["NombreTelefono"],
    "Tiene Localizacion" : ["GPS"],
    "Tiene Memoria Adicional" : ["Tarjeta Memoria"],
    "Tiene NFC": ["NFC"],
    "Tamanio" : [["Peso Gramos",.1],["Alto",.03],["Ancho",.03],["Grueso",.04],["Tamano Pulgadas",.8]],
    "Precio Fabrica": ["Precio"],
    "Procesamiento" : ["CPU GHz","Procesadores"],
    "Tiene Radio": ["Radio"],
    "RAM": ["RAM GB"],
    "Reciente" : ["Anio Anuncio"], #["Mes Anuncio",.08],["Dia Anuncio",.02]],
    "Reconocimiento Rostro" : ["Rec Facial"],
    "Resolucion" : [["Resolucion Pixeles Alto",.3],["Resolucion Pixeles Ancho",.3],["Resolucion PPI",.4]],
    "Selfie" : [["Num Selfie",.1],["Selfie MP",.9]],
    "Selfie Video" : [["Selfie Video FPS",.2],["Selfie Video Pixeles",.8]]
}

cat_dict_filtros = {
    "Info" : ["Disponible","Colores","ImagenTelefono","URL","Marca","Sistema Operativo"], # Ignorar estos
    "Almacenamiento" : ["Baja","Media","Alta"], # Capacidad
    "Tiene SIM" : ["No", "Si"],
    "Bateria" : ["Baja","Media","Alta"], # Duracion
    "Tiene Audifonos" : ["No","Si"],
    "Tiene Bluetooth" : ["No","Si"],
    "Cable Conexion" : [],
    "Camara" : ["Baja","Media","Alta"], # Calidad
    "Camara Video" : ["Baja","Mediana","Alta"], # Calidad
    "Tiene Lector Huella" : ["No","Si"],
    "Llave": ["NombreTelefono"], # Ignorar este
    "Tiene Localizacion" : ["No","Si"],
    "Tiene Memoria Adicional" : ["No","Si"],
    "Tiene NFC": ["No","Si"],
    "Tamanio" : ["Chico","Mediano","Grande"],
    "Precio Fabrica": ["Bajo","Medio","Alto"],
    "Procesamiento" : ["Baja","Media","Alta"], # Potencia
    "Tiene Radio": ["No","Si"],
    "RAM": ["Baja","Media","Alta"], # Capacidad
    "Reciente" : ["Viejo","Reciente","Nuevo"],
    "Reconocimiento Rostro" : ["No","Si"],
    "Resolucion" : ["Baja","Media","Alta"], # Calidad
    "Selfie" : ["Baja","Media","Alta"], # Calidad
    "Selfie Video" : ["Baja","Media","Alta"] # Calidad
}


def agregaCatColVal(dataCatRank, cat, col, peso, valor, posicion, valorFlt=-1.00 ):
    dataCatRank.loc[len(dataCatRank)] = [cat, col, peso, valor, valorFlt, posicion]
    #dataCatRank.append(renglon,ignore_index=True)

def rankColumnaPorEstadistica(dataCatRank, cat, col_nombre, col_peso, res):
    res = res[col_nombre].dropna()
    mn= statistics.mean(res)
    std = statistics.stdev(res)
    minval=res.min()
    if std>mn:
        maxval=res.max()
        untercio=maxval-minval
        agregaCatColVal(dataCatRank, cat, col_nombre, col_peso, minval, 1, float(minval))
        agregaCatColVal(dataCatRank, cat, col_nombre, col_peso, minval+untercio, 2, float(minval+untercio))
        agregaCatColVal(dataCatRank, cat, col_nombre, col_peso, minval+untercio*2, 3, float(minval+untercio*2))
    else:
        agregaCatColVal(dataCatRank, cat, col_nombre, col_peso, minval, 1, float(minval))
        agregaCatColVal(dataCatRank, cat, col_nombre, col_peso, mn-std, 2, float(mn-std))
        agregaCatColVal(dataCatRank, cat, col_nombre, col_peso, mn+std, 3, float(mn+std))
        
def obtenValoresColumna(dataCat, cat, col_nombre, col_peso, dataCatRank):
    #print(col_nombre)
    pivot_column="Anio Anuncio"
    if col_type_dict[col_nombre] in ["Categorica"]:
        #for val in vals:
        posicion =1
        dict_rank = {}
        # Comentado para quitar los anios 1900
        for anio in sorted(dataCat[dataCat[pivot_column]>1900][pivot_column].unique()):
        #for anio in sorted(dataCat[pivot_column].unique()):
            #res = dataCat[dataCat[pivot_column]==anio].groupby(col_nombre)[pivot_column].apply(np.mean).rank(method="dense", ascending=True)
            res = dataCat[dataCat[pivot_column]==anio][col_nombre].unique()
            for i in res:
                if i not in dict_rank:
                    dict_rank[i]=posicion
                    agregaCatColVal(dataCatRank, cat, col_nombre, col_peso, i, posicion)
            posicion+=1
    elif col_type_dict[col_nombre] in ["Binaria"]:
        agregaCatColVal(dataCatRank, cat, col_nombre, col_peso, 0, 0)
        agregaCatColVal(dataCatRank, cat, col_nombre, col_peso, 1, 1)
    elif col_type_dict[col_nombre] in ["Cont"]:
        # Comentado para quitar los anios 1900
        res = dataCat[dataCat[pivot_column]>1900][[col_nombre,pivot_column]].replace(0, np.NaN).groupby(pivot_column).mean()
        #res = dataCat[[col_nombre,pivot_column]].replace(0, np.NaN).groupby(pivot_column).mean()
        rankColumnaPorEstadistica(dataCatRank, cat, col_nombre, col_peso, res)
        
def normalizaPosicionPorColumna(x, dataCatRank):
    #print(x["Categoria"])
    res = dataCatRank[(dataCatRank["Categoria"]==x["Categoria"]) & (dataCatRank["Columna"]==x["Columna"])][["Posicion"]]
    maxPosicion = res.max()
    #print(maxPosicion)
    #maxPosicion=1
    return round(x["Posicion"]/maxPosicion,2)
    
def rankeaValores(cat_dict, dataCat):
    dataCatRank = pd.DataFrame(columns=['Categoria', 'Columna', 'Peso','Valor','ValorFlt','Posicion'])
    for cat in cat_dict:
        if cat not in ["Info","Llave"]:
            columnas = cat_dict[cat]
            if len(columnas)>1:
                for col in columnas:
                    if isinstance(col, list):
                        col_peso=col[1]
                        col_nombre=col[0]
                    else:
                        pesoColumna=1.00/len(columnas)
                        col_nombre=col
                    obtenValoresColumna(dataCat, cat, col_nombre, col_peso, dataCatRank)
                    
            else:
                col_peso=1
                col_nombre = columnas[0]
                obtenValoresColumna(dataCat, cat, col_nombre, col_peso, dataCatRank)
    dataCatRank["Posicion"] = dataCatRank.apply(lambda x: normalizaPosicionPorColumna(
                         x,
                        dataCatRank
                         ), axis=1)
    return dataCatRank

dataCatRank = rankeaValores(cat_dict, dataModel)

def obtenPesoValorPosicion(x, cat, col_nombre, dataCatRank):
    peso=0
    posicion=0
    if col_type_dict[col_nombre] == "Cont":
        #try:
        res = dataCatRank[(dataCatRank["Categoria"]==cat) & (dataCatRank["Columna"]==col_nombre)
        & (x[col_nombre]>=dataCatRank["ValorFlt"])][["Peso","Posicion"]]
        if len(res):
            peso=res["Peso"].iloc[0]
            posicion=res["Posicion"].max()
        #else:
            #print(x["Anio Anuncio"])
#         except Exception as e: 
#             print(res)
#             print(e)
#             traceback.print_exc()
    elif col_type_dict[col_nombre] in ["Binaria"]:
        return 1, x[col_nombre]
    elif col_type_dict[col_nombre] in ["Categorica"]:
        try:
            res = dataCatRank[(dataCatRank["Categoria"]==cat) & (dataCatRank["Columna"]==col_nombre)
                & (dataCatRank["Valor"]==x[col_nombre])][["Peso","Posicion"]]
            if len(res):
                peso = res["Peso"].iloc[0]
                posicion = res["Posicion"].iloc[0]
        except Exception as e: 
            print(col_nombre)
            print(x[col_nombre])
            print(res)
            print(e)
            traceback.print_exc()
            raise ValueError('A very specific bad thing happened.')
    return peso, posicion

def rankeaCategoria(x, cat, col_nombres, dataCatRank):
    res = 0
    for col in col_nombres:
        peso, posicion = obtenPesoValorPosicion(x, cat, col, dataCatRank)
        res += peso*posicion     
    return res
    
def agregaCategorias(cat_dict, df, dataCatRank):
    dataScore=df.copy(deep=True)
    for cat in cat_dict:
        if cat not in ["Info","Llave"]:
            columnas = cat_dict[cat]
            if len(columnas)>1:
                nom_columnas = []
                for col in columnas:
                    if isinstance(col, list):
                        nom_columnas.append(col[0])
                    else:
                        nom_columnas.append(col)
                #print(f"***** {nom_columnas}")
                dataScore[cat] = dataScore.apply(
                lambda x: rankeaCategoria(
                        x, cat, nom_columnas, dataCatRank
                         ), axis=1
                )
            else:
                col_nombre = columnas[0]
                #print(col_nombre)
                dataScore[cat] = dataScore.apply(
                    lambda x: rankeaCategoria(
                        x, cat, [col_nombre], dataCatRank
                         ), axis=1
                )
    return dataScore

dataScore = agregaCategorias(cat_dict, dataModel, dataCatRank)
    
with open("DatasetPropiedadesRankeadas.csv", "w") as text_file:
    text_file.write(dataCatRank.to_csv(index=False))
    

with open("DatasetTelefonosRankeados.csv", "w") as text_file:
    text_file.write(dataScore.to_csv(index=False))

with open('cat_dict.json', 'w') as f:
    json.dump(cat_dict, f)
    
with open('cat_dict_filtros.json', 'w') as f:
    json.dump(cat_dict_filtros, f)