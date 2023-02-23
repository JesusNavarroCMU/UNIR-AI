# coding=utf-8
"""Este código es un scraper que recopila información de una página web y la guarda en un archivo JSON. Usa la biblioteca BeautifulSoup para parsear HTML y la biblioteca requests para hacer peticiones HTTP.
El código comienza con la definición de la URL y un "User-Agent" para hacer una petición a la página web. Luego, se realiza una petición a la URL especificada y se parsea el HTML usando BeautifulSoup.
Luego, se filtran las líneas que no son relevantes para el procesamiento y se itera sobre las líneas restantes. Para cada línea, se hace una petición a la URL especificada, se parsea el HTML y se buscan el nombre del dispositivo, las categorías y la información asociada a cada categoría.
Los resultados se guardan en un archivo JSON, y se imprime un progreso para informar al usuario sobre el proceso. El código también incluye una pausa de 3 segundos antes de hacer cada petición para evitar ser bloqueado por la página web."""

from bs4 import BeautifulSoup
import requests
import time
import json

 # Pagina de donde sale la lista de telefonos
url = "https://www.gsmarena.com/sitemap-phones.xml"
 # User-Agent usado
headers = {'User-Agent': 'Bingbot'}

response = requests.get(url, headers=headers)
soup = response.text
file2 = soup.split("\n")

file = []
for line in file2:
	# Se limpia para que no hayan links que no sean de telefono
	if not("related.php3" in str(line) or "pictures" in str(line) or "urlset" in str(line) or "xml" in str(line) or "3d-spin" in str(line)):
		file.append(line)
del file2


contador = 0
objetivo = 0
for line in file:
	if not("related.php3" in str(line) or "pictures" in str(line) or "urlset" in str(line) or "xml" in str(line) or "3d-spin" in str(line)):
		if  contador >= objetivo:
			# URL del dispositivo
			url = line.split("<loc>")[1].split("</loc>")[0]

			# hacer petición GET al URL
			response = requests.get(url, headers=headers)

			# parsear el HTML usando BeautifulSoup
			soup = BeautifulSoup(response.text, "html.parser")

			# buscar el nombre del dispositivo
			name = soup.find("h1", class_="specs-phone-name-title").text.strip()
			img = str(soup.find_all("div", class_="specs-photo-main")[0]).split('src="')[1].split('"/>')[0]
			
			# buscar las categorías del dispositivo
			categories = soup.find_all("td", class_="ttl")
			categories2 = soup.find_all("td", class_="nfo")

			# crear una lista para almacenar las categorías
			categories_list = []
			categories_list2 = []
			unkownVariableCounter = 0

			contador +=1

			arreglo_salida_variables = []
			arreglo_salida_valores = []
			# imprimir el nombre del dispositivo y la lista de categorías
			print(f"[{round((contador/len(file))*100,2)}% | {contador}/{len(file)}] : {name}")
			
			arreglo_salida_variables.append("URL")
			arreglo_salida_variables.append("PhoneName")
			for cat in categories:
				catName = cat.text.strip()
				area=''
				if catName=='' and cat.parent.parent.name=="table":
						area=cat.parent.parent.th.text.strip()
				if catName=='':
					unkownVariableCounter+=1
					if area!='':
						catName=area+str(unkownVariableCounter)
					else:
						catName='UnknownVar'+str(unkownVariableCounter)
				arreglo_salida_variables.append(catName)
			arreglo_salida_variables.append("PhoneImage")
			arreglo_salida_valores.append(url.strip())
			arreglo_salida_valores.append(name.strip())
			for cat in categories2:
				catValue = cat.text.strip()
				if ("\n" or "\r") in catValue:
					sub_arreglo_salida_valores =[]
					carac = catValue.split("\n")
					for subcar in range(0,len(carac)):
						sub_arreglo_salida_valores.append(carac[subcar].strip())
					arreglo_salida_valores.append(sub_arreglo_salida_valores)
				else:
					arreglo_salida_valores.append(catValue)
			arreglo_salida_valores.append(img.strip())

			salida = open("salida.json","a+",encoding="utf-8")
			salida.write(f"{json.dumps(dict(zip(arreglo_salida_variables, arreglo_salida_valores)))}"+"\n")
			salida.close()
			time.sleep(3)
		else:
			# Por si el proceso falla y quiere obtener los datos desde o hasta un cierto punto en el proceso
			print(f"Objetivo alcanzado {contador}")
			break
			#print(f"[{round((contador/len(file))*100,2)}% | {contador}/{len(file)}] : {name} PASS")
			#contador += 1