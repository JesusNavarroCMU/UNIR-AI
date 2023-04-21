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

col_type_dict = {"Memoria GB": "Cont",
"Audifonos":"Binaria",
"Bateria mAh":"Cont",
"Horas Bateria":"Cont",
"Horas Llamada Bateria":"Cont",
"Vida Bateria":"Cont",
"Bluetooth":"Binaria",
"Conector":"Categorica",
"Camara MP":"Cont",
"Num Camaras":"Categorica",
"Video FPS":"Cont",
"Video Pixeles":"Cont",
"Disponible":"Binaria",
"Marca":"Categorica",
"Misc | Colors":"Categorica",
"PhoneImage":"Info",
"URL":"Info",
"Lector Huella":"Binaria",
"PhoneName":"Info",
"GPS":"Binaria",
"Sistema Operativo":"Categorica",
"Tarjeta Memoria":"Binaria",
"NFC":"Binaria",
"Peso Gramos":"Cont",
"Precio":"Cont",
"CPU GHz":"Cont",
"Procesadores":"Categorica",
"Radio":"Binaria",
"RAM GB":"Cont",
"Anio Anuncio":"Categorica",
"Dia Anuncio":"Info",
"Mes Anuncio":"Info",
"Rec Facial":"Binaria",
"Resolucion Pixeles Alto":"Categorica",
"Resolucion Pixeles Ancho":"Categorica",
"Resolucion PPI":"Categorica",
"Dimensiones":"Info",
"Fecha Anuncio":"Info",
"Resolucion Pixeles":"Info",
"Teclado":"Binaria",
"Num Selfie":"Categorica",
"Selfie MP":"Cont",
"Selfie Video FPS":"Cont",
"Selfie Video Pixeles":"Cont",
"SIM":"Binaria",
"Alto":"Cont",
"Ancho":"Cont",
"Grueso":"Cont",
"Tamano Pulgadas":"Cont"}

col_unidades = {"Memoria GB": "GB (gigabytes)",
"Bateria mAh":"mAh (miliamperio hora)",
"Horas Bateria":"horas",
"Horas Llamada Bateria":"horas",
"Vida Bateria":"horas",
"Camara MP":"MP (megapixeles)",
"Video FPS":"FPS (fotogramas por segundo)",
"Video Pixeles":"pixeles",
"Peso Gramos":"gramos",
"Precio":"dolares",
"CPU GHz":"GHz (gigahertz)",
"RAM GB":"GB (gigabytes)",
"Rec Facial":"Binaria",
"Resolucion Pixeles": "pixeles",
"Resolucion Pixeles Alto":"pixeles",
"Resolucion Pixeles Ancho":"pixeles",
"Resolucion PPI":"PPI (pixeles por pulgada)",
"Selfie MP":"MP (megapixeles)",
"Selfie Video FPS":"FPS (fotogramas por segundo)",
"Selfie Video Pixeles":"pixeles",
"Alto":"pulgadas",
"Ancho":"pulgadas",
"Grueso":"pulgadas",
"Tamano Pulgadas":"pulgadas",
"Dimensiones":"pulgadas"
}

def formateaBinaria(x):
    if x:
        return 'Si'
    else:
        return 'No'

def formateaNumero(x, unidad=''):
    return str(x)+' '+unidad

with open('col_type_dict.json', 'w') as f:
    json.dump(col_type_dict, f)
    
df = pd.read_csv("DatasetLimpio.csv")

for col in col_type_dict:
    if col_type_dict[col]=='Binaria':
        df[col]=df[col].apply(formateaBinaria)
    elif col in col_unidades:
        df[col]=df[col].apply(formateaNumero,args=(col_unidades[col],))

with open("DatasetFormateado.csv", "w") as text_file:
    text_file.write(df.to_csv(index=False))
