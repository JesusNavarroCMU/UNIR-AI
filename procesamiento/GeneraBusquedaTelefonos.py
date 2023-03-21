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

dataCatRank = pd.read_csv("DatasetPropiedadesRankeadas.csv")

dataScore = pd.read_csv("DatasetTelefonosRankeados.csv")

def segregaCategoria(x, cat, cat_seg, min_val, max_val, mean_val, std_val, columnaCategorica=""):
    clasificacion=""
    num_seg=len(cat_seg)
    if columnaCategorica!="":
        #print(columnaCategorica)
        clasificacion=x[columnaCategorica]
    else:
        if num_seg==2 or num_seg>3:
            seg_tamanio = (max_val-min_val)/(num_seg)
            min_rango=min_val
            for i in range(1,num_seg):
                max_rango=min_rango+seg_tamanio
                if x[cat]>=min_rango and x[cat]<max_rango:
                    clasificacion= cat_seg[i-1]
                    #print(clasificacion)
                    break
                min_rango+=seg_tamanio
            if clasificacion=="":
                if x[cat]>=min_rango:
                    clasificacion= cat_seg[-1]
                    #print(clasificacion)
        elif num_seg==3:
            rangos=[min_val, mean_val-std_val, mean_val+std_val]
            for i in range(0,num_seg-1):
                min_rango=rangos[i]
                max_rango=rangos[i+1]
                if x[cat]>=min_rango and x[cat]<max_rango:
                    clasificacion= cat_seg[i]
                    #print(clasificacion)
                    break
            if clasificacion=="":
                if x[cat]>=rangos[-1]:
                    clasificacion= cat_seg[-1]
                    #print(clasificacion)
    return clasificacion
        
def obtenDataBusqueda(dataScore, dataCatRank):
    dataBusqueda= dataScore.copy(deep=True)
    columnas_bus = dataBusqueda.columns
    for cat in cat_dict_filtros:
        if cat not in ["Info","Llave"]: #and cat=="Almacenamiento":
            #print(cat)
            segmentos = cat_dict_filtros[cat]
            columnaCategorica=""
            columnas_a_usar=list()
            columnas_a_usar.append(cat)
            if len(segmentos)==0:
                columnaCategorica=list(dataCatRank[dataCatRank["Categoria"]==cat]["Columna"])[0]
                columnas_a_usar.append(columnaCategorica)
            #print(segmentos)
            min_val=dataBusqueda[cat].min()
            max_val=dataBusqueda[cat].max()
            mean_val=dataBusqueda[cat].mean()
            std_val=dataBusqueda[cat].std()
            dataBusqueda[cat]=dataBusqueda[columnas_a_usar].apply(
                lambda x: segregaCategoria(
                        x, cat, segmentos, min_val, max_val, mean_val, std_val, columnaCategorica
                         ), axis=1
            )
    for col in columnas_bus:
        if col not in cat_dict_filtros and col not in cat_dict_filtros["Info"] \
        and col not in cat_dict_filtros["Llave"]:
            dataBusqueda.drop(columns = [col], inplace = True)
    return dataBusqueda

dataBusqueda = obtenDataBusqueda(dataScore, dataCatRank)

with open("DatasetTelefonosBusqueda.csv", "w") as text_file:
    text_file.write(dataBusqueda.to_csv(index=False))

for i in dataBusqueda.columns:
    if i not in cat_dict_filtros["Llave"] and i not in cat_dict_filtros["Info"]:
        print(dataBusqueda[i].value_counts(dropna=False))