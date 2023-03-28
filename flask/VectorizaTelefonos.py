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

meses_cortos = ["jan", "feb", "mar", "apr","may","jun","jul","aug","sep","oct","nov","dec"]
meses_largos = ["january", "february", "march", "april","may","june","july","august","september","october","november","december"]
trimestres = ["q1","q2","q3","q4"]


# regexp = re.compile(r'[\s\w]+[0-9]')
# for col in df.columns:
#     if regexp.search(col):

def marcaTelefono(x):
    if "iphone" in x.lower() and not "prestigio" in x.lower():
        return "Apple"
    elif "motorola" in x.lower():
        return "Motorola"
    elif "samsung" in x.lower():
        return "Samsung"
    else:
        return "Other"
    
def renombraColumna(df, name, newName):
    df.rename(columns={name: newName}, inplace=True)
    
def hazValorBinario(x, yesValues=[], noValues=[], default=0):
    if x==np.nan:
        return 0
    if str(x).strip() in yesValues:
        return 1
    if str(x).strip() in noValues:
        return 0
    return default

def hazValorBinarioContieneSubstr(x, substr, default=0):
    if substr.lower() in str(x).strip().lower():
        return int(not default)
    else:
        return default
    
def categorizaPorPrimerPalabra(x):
    x=str(x).strip().lower()
    if len(x) and " " in x:
        x=x[:x.find(" ")]
        x=x.replace(",","")
        x=x.replace("^3","")
    return x


def categorizarPorValoresContieneSubstr(x, valoresSubstr, valoresNo, default="Other"):
    x=str(x).strip().lower()
    for i in valoresNo:
        if x==i.lower():
            return "No"
    for i in valoresSubstr:
        if i.lower() in x:
            return i
    return default

def obtenEnteroSeguidoLetras(x, letras):
    r = re.search("\s*(\d+)\s*"+letras+"\s*", x, re.IGNORECASE)
    s=0
    if r:
        s=int(r.group(1))
    return s

def obtenFlotanteSeguidoLetras(x, letras):
    r = re.search("\s*([\d\.]+)\s*"+letras+"\s*", x,  re.IGNORECASE)
    s=0
    if r:
        s=float(r.group(1))
    return s

def obtenHoras(x):
    x=str(x).strip().lower()
    return obtenEnteroSeguidoLetras(x, "h")

def obtenMinutos(x):
    x=str(x).strip().lower()
    return obtenEnteroSeguidoLetras(x, "min")

def obtenmAh(x):
    x=str(x).strip().lower()
    return obtenFlotanteSeguidoLetras(x, "mAh")

def obtenGramos(x):
    x=str(x).strip().lower()
    return obtenFlotanteSeguidoLetras(x, "g")

def obtenHorasBateriaTalk(x):
    x=str(x).strip().lower()
    horas =0
    horas = obtenHoras(x)
    horas += float(obtenMinutos(x))/60
    return round(horas,2)

def obtenResolucionPixeles(x):
    r = re.search("\s*(\d+\s+x\s+\d+)\s*pixels\s*", x)
    s=""
    if r:
        s=r.group(1)
    return s

def obtenResolucionAnchoPixeles(x):
    r = re.search("\s*(\d+)\s+x\s+\d+\s*pixels\s*", x)
    s=0
    if r:
        s=int(r.group(1))
    return s

def obtenResolucionAltoPixeles(x):
    r = re.search("\s*\d+\s+x\s+(\d+)\s*pixels\s*", x)
    s=0
    if r:
        s=int(r.group(1))
    return s

def obtenResolucionPPI(x):
    x=str(x).strip().lower()
    return obtenEnteroSeguidoLetras(x, "ppi")

def obtenInches(x):
    x=str(x).strip().lower()
    return obtenFlotanteSeguidoLetras(x, "inches")

def contienePalabra(x, palabra):
    x=str(x).strip().lower()
    r = re.search("\s*"+palabra.lower()+"\s*", x)
    s=0
    if r:
        s=1
    return s

def obtenRAM(x):
    res = 0
    res = obtenFlotanteSeguidoLetras(str(x), "MB\s+RAM") / 1024
    if res==0:
        res = obtenFlotanteSeguidoLetras(str(x), "GB\s+RAM")
    return res

def obtenMemoria(x):
    res = 0
    res = obtenFlotanteSeguidoLetras(str(x), "MB\s*(?!RAM)") / 1024
    if res==0:
        res = obtenFlotanteSeguidoLetras(str(x), "GB\s*(?!RAM)")
    return res

def obtenNumProcesadores(x):
    x=str(x).strip()
    num_procesadores =1
    if "Dual-core" in x:
        num_procesadores=2
    elif "Triple-core" in x:
        num_procesadores=3
    elif "Quad-core" in x or "quadcore" in x:
        num_procesadores=4
    elif "Hexa-core" in x:
        num_procesadores=6
    elif "Octa-core" in x:
        num_procesadores=8
        #print("8 procesadores")
    elif "Deca-core" in x:
        num_procesadores=10
    return num_procesadores

def obtenCPU(x):
    x=str(x).strip()
    cpu=0
    num_procesadores = obtenNumProcesadores(x)
    r = re.findall("\s*(\d+)x([\d\.]+)\s*GHz\s*", x, re.IGNORECASE)
    #print(r)
    if len(r)>0:
        #print("Encontro detalles")
        sum_proc = 0
        for i in r:
            sum_proc+=int(i[0])
            cpu+=int(i[0])*float(i[1])
            #print(f"{sum_proc} : {cpu}")
        if sum_proc!=num_procesadores:
            cpu=0
            #print(x)
    else:
        cpu=obtenFlotanteSeguidoLetras(str(x), "GHz")*num_procesadores
    if cpu==0:
        cpu=obtenFlotanteSeguidoLetras(str(x), "MHz")* num_procesadores /1000
    return cpu
            
def obtenVidaBateria(x):
    x=str(x).strip()
    r = re.search("\s*(\d+)h\s*", x)
    s=0
    if r:
        s=int(r.group(1))
    return s

def obtenerAnioMesDia(x, released=["released","exp. release","exp. announcement"]):
    x = str(x).strip().lower().replace(","," ")
    for i in released:
        if i in x:
            x=x[x.find(i)+len(i):].strip().lower()
    anio_encontrado = re.search("\d{4}", x)
    anio=""
    if anio_encontrado:
        anio = anio_encontrado.group(0)
    sin_anio = x.replace(anio, "").strip()
    mes_encontrado = list(set(meses_largos).intersection(sin_anio.split()))
    if len(mes_encontrado):
        mes_encontrado = mes_encontrado[0]
        sin_anio=sin_anio.replace(mes_encontrado,"").strip()
    if not len(mes_encontrado):
        mes_encontrado = list(set(meses_cortos).intersection(sin_anio.split()))
        if len(mes_encontrado):
            sin_anio=sin_anio.replace(mes_encontrado[0],"").strip()
            mes_encontrado=meses_largos[(meses_cortos.index(mes_encontrado[0]))]
    if not len(mes_encontrado):
        mes_encontrado = list(set(trimestres).intersection(sin_anio.split()))
        if len(mes_encontrado):
            sin_anio=sin_anio.replace(mes_encontrado[0],"").strip()
            mes_encontrado=meses_largos[((trimestres.index(mes_encontrado[0])+1)*3)-1]
    dia_encontrado = re.search("\d{1,2}", sin_anio)
    dia=""
    if dia_encontrado:
        dia = dia_encontrado.group(0)
    if not len(dia):
        dia = "1"
    if not len(mes_encontrado):
        mes_encontrado="july"
    if len(anio):
        return int(anio) , meses_largos.index(mes_encontrado)+1, int(dia)
    else:
        return 1900, 1, 1
    
def obtenerAnio(x):
    res, _, _ = obtenerAnioMesDia(x)
    return res

def obtenerMes(x):
    _, res, _ = obtenerAnioMesDia(x)
    return res

def obtenerDia(x):
    _, _, res = obtenerAnioMesDia(x)
    return res

def obtenerFecha(x):
    anio, mes, dia = obtenerAnioMesDia(x)
    d = dt.datetime(anio, mes, dia)
    return d.date()

def obtenPrecio(x):
    x=str(x).strip().lower()
    regexp_precio = "about (\d+) eur"
    enc_precio = re.search(regexp_precio, x)
    if enc_precio:
        return round(float(enc_precio.group(1).replace(",",""))/0.95,2)
    regexp_precio = "about (\d+) inr"
    enc_precio = re.search(regexp_precio, x)
    if enc_precio:
        return round(float(enc_precio.group(1).replace(",",""))/81.93,2)
    regexp_precio = "\$\s*((\d|\.|,)+)\s*"
    enc_precio = re.search(regexp_precio, x)
    if enc_precio:
        return round(float(enc_precio.group(1).replace(",","")),2)
    regexp_precio = "€\s*((\d|\.|,)+)\s*"
    enc_precio = re.search(regexp_precio, x)
    if enc_precio:
        return round(float(enc_precio.group(1).replace(",",""))/0.95,2)
    regexp_precio = "\s*rp\s+((\d|\.|,)+)\s*"
    enc_precio = re.search(regexp_precio, x)
    if enc_precio:
        return round(float(enc_precio.group(1).replace(",",""))/15384.62,2)
    regexp_precio = "\s*£\s+((\d|\.|,)+)\s*"
    enc_precio = re.search(regexp_precio, x)
    if enc_precio:
        return round(float(enc_precio.group(1).replace(",",""))/0.85,2)
    regexp_precio = "\s*₹\s+((\d|\.|,)+)\s*"
    enc_precio = re.search(regexp_precio, x)
    if enc_precio:
        return round(float(enc_precio.group(1).replace(",",""))/81.93,2)
    return 0.00

def obtenDimensiones(x):
    res=""
    regexp_tamanio = "\(([\d.]+)\sx\s([\d.]+)\sx\s([\d.]+)\sin\)"
    enc_tamanio = re.search(regexp_tamanio, x)
    if enc_tamanio:
        res = re.sub("\(|\)|i|n", "", enc_tamanio.group(0)).strip()
    return res

def obtenAltoAnchoGrueso(x):
    regexp_tamanio = "\(([\d.]+)\sx\s([\d.]+)\sx\s([\d.]+)\sin\)"
    enc_tamanio = re.search(regexp_tamanio, x)
    alto, ancho, grueso = 0, 0, 0
    if enc_tamanio:
        alto = enc_tamanio.group(1)
        ancho = enc_tamanio.group(2)
        grueso = enc_tamanio.group(3)
    return round(float(alto),2), round(float(ancho),2), round(float(grueso),2)

def obtenAlto(x):
    res, _, _ =obtenAltoAnchoGrueso(x)
    return res

def obtenAncho(x):
    _, res, _ =obtenAltoAnchoGrueso(x)
    return res
    
def obtenGrueso(x):
    _, _, res=obtenAltoAnchoGrueso(x)
    return res

def obtenNumCamaras(x1, x2, x3, x4=None, x5=None):
    if isinstance(x1, list):
        x1=x1[0]
    if isinstance(x2, list):
        x2=x2[0]
    if isinstance(x3, list):
        x3=x3[0]
    if isinstance(x4, list):
        x4=x4[0]
    if isinstance(x5, list):
        x5=x5[0]
    if "main camera" in str(x2).lower() or "main camera" in str(x3).lower():
        return 0
    if not pd.isnull(x1):
        return 1
    elif not pd.isnull(x2):
        return 2
    elif not pd.isnull(x3):
        return 3
    elif not pd.isnull(x4):
        return 4
    elif not pd.isnull(x5):
        return 5
    return 0

def obtenCamaraMP(x1, x2, x3, x4=None, x5=None):
    if isinstance(x1, list):
        x1=x1[0]
    if isinstance(x2, list):
        x2=x2[0]
    if isinstance(x3, list):
        x3=x3[0]
    if isinstance(x4, list):
        x4=x4[0]
    if isinstance(x5, list):
        x5=x5[0]
    numCamaras = obtenNumCamaras(x1, x2, x3, x4, x5)
    regexp_MP = "([\d\.]+)\sMP"
    camaraMP = 0
    enc_camaraMP = None
    if numCamaras==1:
        enc_camaraMP = re.search(regexp_MP, x1)
    elif numCamaras==2:
        enc_camaraMP = re.search(regexp_MP, x2)
    elif numCamaras==3:
        enc_camaraMP = re.search(regexp_MP, x3)
    elif numCamaras==4:
        enc_camaraMP = re.search(regexp_MP, x4)
    elif numCamaras==5:
        enc_camaraMP = re.search(regexp_MP, x5)
    if enc_camaraMP:
        camaraMP =enc_camaraMP.group(1)
    return round(float(camaraMP),2)

def obtenVideoPixeles(x):
    x=str(x)
    regexp_pixeles = "(\d+)K"
    enc_pixeles  = re.search(regexp_pixeles, x)
    if enc_pixeles:
        return int(enc_pixeles.group(1))*1024
    regexp_pixeles = "(\d+)p"
    enc_pixeles  = re.search(regexp_pixeles, x)
    if enc_pixeles:
        return int(enc_pixeles.group(1))
    return 0

def obtenVideoFPS(x):
    x=str(x)
    regexp_pixeles = "(\d+)fps"
    enc_pixeles  = re.search(regexp_pixeles, x)
    if enc_pixeles:
        return int(enc_pixeles.group(1))
    return 0

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


file1 = open('../data/telefonos.json', 'r')
Lines = file1.readlines()
  
count = 0
pandas_list=[]
for line in Lines:
    count += 1
    json_object = json.loads(line)
    pandas_list.append(json_object)
file1.close()

df = pd.read_json(json.dumps(pandas_list))

pd.set_option('display.max_rows', None)

df["Marca"]=df["PhoneName"].apply(marcaTelefono)
df["Audifonos"] = df["Sound | 3.5mm jack"].apply(hazValorBinario, args=(['Yes'], [], 0))
df["Bluetooth"] = df["Comms | Bluetooth"].apply(hazValorBinario, args=(['Yes'], ["No","TBC","TBD",""], 1))
df["GPS"] = df["Comms | Positioning"].apply(hazValorBinarioContieneSubstr, args=("GPS", 0))
df["Radio"] = df["Comms | Radio"].apply(hazValorBinario, args=([], ["No","TBC","TBD","","-","Unspecified","To be confirmed","Nо"], 1))
df["Teclado"] = df["Body | Keyboard"].apply(hazValorBinario, args=(['QWERTY'], [], 0))
df["Horas Bateria"] = df["Battery | Stand-by"].apply(obtenHoras)
df["Horas Llamada Bateria"] = df["Battery | Talk time"].apply(obtenHorasBateriaTalk)
df["Bateria mAh"] = df["Battery | Type"].apply(obtenmAh)
df["SIM"] = df["Body | SIM"].apply(hazValorBinario, args=([],["eSIM","No"],1))
df["Peso Gramos"] = df["Body | Weight"].apply(obtenGramos)
df["NFC"] = df["Comms | NFC"].apply(hazValorBinario, args=([],["No","TBC","TBC","Unspecified","To be confirmed"],1))
df["Resolucion Pixeles"] = df["Display | Resolution"].apply(obtenResolucionPixeles)
df["Resolucion Pixeles Ancho"] = df["Display | Resolution"].apply(obtenResolucionAnchoPixeles)
df["Resolucion Pixeles Alto"] = df["Display | Resolution"].apply(obtenResolucionAltoPixeles)
df["Resolucion PPI"] = df["Display | Resolution"].apply(obtenResolucionPPI)
df["Tamano Pulgadas"] = df["Display | Size"].apply(obtenInches)
df["Lector Huella"] = df["Features | Sensors"].apply(contienePalabra, args=("Fingerprint",))
df["Rec Facial"] = df["Features | Sensors"].apply(contienePalabra, args=("Face ID",))
df["Tarjeta Memoria"]= df["Memory | Card slot"].apply(hazValorBinario, args=([],["No","To be confirmed","Unspecified",""],1))
df["RAM GB"] = df["Memory | Internal"].apply(obtenRAM)
df["Memoria GB"] = df["Memory | Internal"].apply(obtenMemoria)
df["CPU GHz"] = df["Platform | CPU"].apply(obtenCPU)
df["Vida Bateria"] = df["Tests | Battery life"].apply(obtenVidaBateria)
df["Procesadores"] = df["Platform | CPU"].apply(obtenNumProcesadores)
df["Fecha Anuncio"] = df["Launch | Announced"].apply(obtenerFecha)
df["Anio Anuncio"] = df["Launch | Announced"].apply(obtenerAnio)
df["Mes Anuncio"] = df["Launch | Announced"].apply(obtenerMes)
df["Dia Anuncio"] = df["Launch | Announced"].apply(obtenerDia)
df["Disponible"]=df["Launch | Status"].apply(hazValorBinarioContieneSubstr,args=("Available",0))
df["Sistema Operativo"] = df["Platform | OS"].apply(categorizaPorPrimerPalabra)
df["Conector"]=df["Comms | USB"].apply(categorizarPorValoresContieneSubstr, args=(["microUSB","miniUSB","USB Type-C"], ["","No","TBC"]))
df["Alto"]=df["Body | Dimensions"].apply(obtenAlto)
df["Ancho"]=df["Body | Dimensions"].apply(obtenAncho)
df["Grueso"]=df["Body | Dimensions"].apply(obtenGrueso)
df["Dimensiones"]=df["Body | Dimensions"].apply(obtenDimensiones)
df["Camara MP"]=df.apply(lambda x: obtenCamaraMP(
                        x["Main Camera | Single"],
                        x["Main Camera | Dual"],
                        x["Main Camera | Triple"],
                        x["Main Camera | Quad"],
                        x["Main Camera | Five"]
                         #"Main Camera | Dual or Triple",
                         ), axis=1)
df["Num Camaras"]=df.apply(lambda x: obtenNumCamaras(
                        x["Main Camera | Single"],
                        x["Main Camera | Dual"],
                        x["Main Camera | Triple"],
                        x["Main Camera | Quad"],
                        x["Main Camera | Five"]
                         ), axis=1)
df["Selfie MP"]=df.apply(lambda x: obtenCamaraMP(
                        x["Selfie camera | Single"],
                        x["Selfie camera | Dual"],
                        x["Selfie camera | Triple"]
                         ), axis=1)
df["Num Selfie"]=df.apply(lambda x: obtenNumCamaras(
                         x["Selfie camera | Single"],
                        x["Selfie camera | Dual"],
                        x["Selfie camera | Triple"]
                         ), axis=1)
df["Video Pixeles"]=df["Main Camera | Video"].apply(obtenVideoPixeles)
df["Video FPS"]=df["Main Camera | Video"].apply(obtenVideoFPS)
df["Selfie Video Pixeles"]=df["Selfie camera | Video"].apply(obtenVideoPixeles)
df["Selfie Video FPS"]=df["Selfie camera | Video"].apply(obtenVideoFPS)
df["Precio"]=df["Misc | Price"].apply(obtenPrecio)
renombraColumna(df, "Misc | Colors", "Colores")
renombraColumna(df, "PhoneName", "NombreTelefono")
renombraColumna(df, "PhoneImage", "ImagenTelefono")

columnasAEliminar=[
    # Eliminadas porque no se utilizan
    "Network | Technology", "Type", "Misc | Models",
    "Network | 2G bands","Network | GPRS","Network | EDGE","Memory | Phonebook",
    "Memory | Call records","Sound | ", "Sound | Loudspeaker","Sound | Alert types","Comms | WLAN", 
    "Features | Messaging","Features | Browser","Features | Clock","Features | Alarm",
    "Features | Games","Features | Languages","Features | Java","Comms | Infrared port",
    "Misc | SAR","Misc | SAR EU","Network | 3G bands", "Network | Speed", "Platform | Chipset",
    "Main Camera | Features","Battery | Music play","Display | Protection","Platform | GPU",
    "Tests | Loudspeaker", "Tests | Audio quality", "Tests | Camera", "Battery | Charging",
    "Tests | Display", "Body | Build", "Network | 4G bands", "Network | 5G bands",
    "Tests | Performance",
    "Main Camera | Penta", 
    #"Main Camera | Dual or Triple", "Main Camera | Five", 
    "Battery | Charging", "Body | ","Camera | ","Display | ","Display | Type","Features | ",
    "Main Camera | ", "Memory | ", "Network | ", "Selfie camera | ", "Selfie camera | Dual",
    "Selfie camera | Features", "Selfie camera | Triple",
    # Eliminadas despues de Derivar columnas limpias
    "Battery | Stand-by", "Battery | Talk time", "Battery | Type", "Body | Keyboard", "Body | SIM", 
    "Body | Weight", "Comms | Bluetooth", "Comms | NFC", "Comms | Radio", "Comms | USB", "Display | Resolution",
    "Display | Size", "Features | Sensors", "Launch | Announced", "Launch | Status", "Main Camera | Dual",
    "Main Camera | Dual or Triple", "Main Camera | Five", "Main Camera | Quad", "Main Camera | Single",
    "Main Camera | Triple", "Main Camera | Video", "Memory | Card slot", "Memory | Internal", "Misc | Price",
    "Platform | CPU", "Platform | OS", "Selfie camera | Single", "Selfie camera | Dual",
    "Selfie camera | Triple", "Selfie camera | Video", "Sound | 3.5mm jack", "Tests | Battery life",
    "Comms | Positioning", "Body | Dimensions"
    ]
for col in columnasAEliminar:
    if col in df.columns:
        df.drop(col, axis=1, inplace=True)

with open("DatasetLimpio.csv", "w") as text_file:
    text_file.write(df.to_csv(index=False))

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

