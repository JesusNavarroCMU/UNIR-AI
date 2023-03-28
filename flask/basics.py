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


@app.route('/product', methods=['POST','GET'])
def product():
    #if request.method == "POST":
    precio = request.form['precio']
    almacenamiento = request.form['almacenamiento']
    bateria = request.form['bateria']
    memoriaAdicional = request.form['memoriaAdicional']
    camara = request.form['camara']
    camaraVideo = request.form['camaraVideo']
    selfie = request.form['selfie']
    selfieVideo = request.form['selfieVideo']
    procesamiento = request.form['procesamiento']
    ram = request.form['ram']
    resolucion = request.form['resolucion']
    tamanio = request.form['tamanio']
    huella = request.form['huella']
    rostro = request.form['rostro']
    reciente = request.form['reciente']
    audifonos = request.form['audifonos']
    bluetooth = request.form['bluetooth']
    radio = request.form['radio']
    localizacion = request.form['localizacion']
    nfc = request.form['nfc']
    sim = request.form['sim']
    # Validacion de la info
    # Obtienes el nuevo producto
    with open('cat_dict_filtros.json') as f:
        cat_dict_filtros = json.load(f)

    print(json.dumps(cat_dict_filtros, indent=4))

    ## Primer Archivo - Para buscar los telefonos

    dataBusqueda = pd.read_csv("DatasetTelefonosBusqueda.csv")

    ## Segundo Arhcivo - Para Obtener los detalles del telefono

    dataModel = pd.read_csv("DatasetTelefonosActivos.csv")

    res = dataBusqueda[(dataBusqueda["Precio Fabrica"]==precio) \
             & (dataBusqueda["Almacenamiento"]==almacenamiento)
            & (dataBusqueda["Bateria"]==bateria)
            & (dataBusqueda["Tiene Memoria Adicional"]==memoriaAdicional)
            & (dataBusqueda["Camara"]==camara)
            & (dataBusqueda["Camara Video"]==camaraVideo)
            & (dataBusqueda["Selfie"]==selfie)
            & (dataBusqueda["Selfie Video"]==selfieVideo)
            & (dataBusqueda["Procesamiento"]==procesamiento)
            & (dataBusqueda["RAM"]==ram)
            & (dataBusqueda["Resolucion"]==resolucion)
            & (dataBusqueda["Tiene Lector Huella"]==huella)
            & (dataBusqueda["Reconocimiento Rostro"]==rostro)][["NombreTelefono"]]
    
    existe_en_res = dataModel["NombreTelefono"].isin(res["NombreTelefono"])
    #print(dataModel[existe_en_res])
    # printResult(dataModel[existe_en_res])

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
        
    print(resultados_list)
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
