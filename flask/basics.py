from flask import Flask, redirect, url_for, render_template, request, flash, jsonify
import json
import pandas as pd

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/recomendacion', methods=['POST','GET'])
def recomendacion():
    return render_template('recomendacion.html')

@app.route('/criterio', methods=['POST','GET'])
def criterio():
    return render_template('criterio.html')

@app.route('/product', methods=['POST','GET'])
def product():
   
    with open('../procesamiento/cat_dict_filtros.json') as f:
        cat_dict_filtros = json.load(f)

    ## Primer Archivo - Para buscar los telefonos

    dataBusqueda = pd.read_csv("../procesamiento/DatasetTelefonosBusqueda.csv")

    ## Segundo Arhcivo - Para Obtener los detalles del telefono

    dataModel = pd.read_csv("../procesamiento/DatasetFormateado.csv")

    lista_parametros = ["precio",
                     "almacenamiento",
                     "bateria",
                     "memoriaAdicional",
                     "camara",
                     "camaraVideo",
                     "selfie",
                     "selfieVideo",
                     "procesamiento",
                     "ram",
                     "resolucion",
                     "tamanio",
                     "huella",
                     "rostro",
                     "reciente",
                     "audifonos",
                     "bluetooth",
                     "radio",
                     "localizacion",
                     "nfc",
                     "sim"]

    lista_campos = ["Precio Fabrica",
            "Almacenamiento",
            "Bateria",
            "Tiene Memoria Adicional",
            "Camara",
            "Camara Video",
            "Selfie",
            "Selfie Video",
            "Procesamiento",
            "RAM",
            "Resolucion",
            "Tamanio",
            "Tiene Lector Huella",
            "Reconocimiento Rostro",
            "Reciente",
            "Tiene Audifonos",
            "Tiene Bluetooth",
            "Tiene Radio",
            "Tiene Localizacion",
            "Tiene NFC",
            "Tiene SIM"]

    str_busqueda=""
    for i in range(len(lista_parametros)):
        val_filtro = request.form[lista_parametros[i]]
        if val_filtro!="":
            str_busqueda+= " `"+lista_campos[i]+"`=='"+val_filtro+"' &"
    str_busqueda=str_busqueda[:-1]

    print(request.form)
    print(str_busqueda)
    res = dataBusqueda.query(str_busqueda)
    
    existe_en_res = dataModel["NombreTelefono"].isin(res["NombreTelefono"])

    dataResultado = dataModel[existe_en_res]
    products_list = dataResultado.values.tolist()

    resultados_list = []

    for i in range(0, len(dataResultado)):
        individual_list = []
        individual_list.append(products_list[i][1])
        individual_list.append(products_list[i][2])
        individual_list.append(products_list[i][3])
        individual_list.append(products_list[i][4])
        individual_list.append(products_list[i][5])
        individual_list.append(products_list[i][6])
        individual_list.append(products_list[i][12])
        individual_list.append(products_list[i][16])
        individual_list.append(products_list[i][20])
        individual_list.append(products_list[i][21])
        individual_list.append(products_list[i][22])
        individual_list.append(products_list[i][24])
        individual_list.append(products_list[i][25])
        individual_list.append(products_list[i][30])
        individual_list.append(products_list[i][34])
        individual_list.append(products_list[i][39])
        individual_list.append(products_list[i][40])
        individual_list.append(products_list[i][41])
        individual_list.append(products_list[i][42])
        individual_list.append(products_list[i][43])
        individual_list.append(products_list[i][44])
        individual_list.append(products_list[i][46])
        individual_list.append(products_list[i][48])
        resultados_list.append(individual_list)
        
    #print(resultados_list)
    # return render_template('product.html', data=dataModel[existe_en_res])
    return render_template('product.html',
                           resultados_list = resultados_list,
                           length = len(resultados_list)
                           )

if __name__ == "__main__":
    app.run(debug=True)


def printResult(res):
    for i in res:
        for j in res[i]:
            print(res[i][j])



## Suponiendo que queremos buscar telefono con una capacidad de Almacenamiento Alta, con Lector de Huella,
## con Reconocimiento de Rostro y que tenga Camara de Mediana Calidad
