import json
import pandas as pd
import numpy as np
##import matplotlib.pyplot as plt
##import seaborn as sns
import math
import datetime as dt
import statistics 

with open('cat_dict_filtros.json') as f:
    cat_dict_filtros = json.load(f)
    
## Estas son las columnas por las que se pueden buscar los telefonos y los valores que acepta la busqueda
print("Columnas por las que buscar y valores de busqueda")
print("IGNORAR LAS COLUMNAS DE CATEGORIAS INFO O LLAVE, ESAS NO SON PARA BUSQUEDA, SOLO SON INFORMATIVAS")
print("Revisar el archivo GeneraEstadisticasTelefonos donde la variable cat_dict_filtros esta definida")

#print(json.dumps(cat_dict_filtros, indent=4))

## Abres dos archivos - Uno que te permite buscar los telefonos y, ya con la lista de telefonos encontrados, 
## en el segundo archivo buscas los detalles del telefono y los despliegas

## Primer Archivo - Para buscar los telefonos

dataBusqueda = pd.read_csv("DatasetTelefonosBusqueda.csv")

## Segundo Arhcivo - Para Obtener los detalles del telefono

dataModel = pd.read_csv("DatasetTelefonosActivos.csv")

## Suponiendo que queremos buscar telefono con una capacidad de Almacenamiento Alta, con Lector de Huella,
## con Reconocimiento de Rostro y que tenga Camara de Mediana Calidad

res = dataBusqueda[(dataBusqueda["Almacenamiento"]=="Alta") \
             & (dataBusqueda["Tiene Lector Huella"]=="Si")
            & (dataBusqueda["Camara"]=="Media")
            & (dataBusqueda["Tamanio"]=="Grande")][["NombreTelefono"]]

## Buscas los telefonos resultantes en la tabla de detalles y los muestras

existe_en_res = dataModel["NombreTelefono"].isin(res["NombreTelefono"])

#print(dataModel[existe_en_res])

dataResultado = dataModel[existe_en_res]
#print()
print(dataResultado.head(10))

for col in dataResultado.columns:
    print(col)

products_list = dataResultado.values.tolist()
print(products_list)

