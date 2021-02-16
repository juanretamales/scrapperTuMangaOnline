import requests
from bs4 import BeautifulSoup
import json
import time, shutil, os
import os.path
import pandas as pd

# La función get_main_news retornará un diccionario con todas las urls y títulos de noticias encontrados en la sección principal.
def getRequest(url):

    return requests.get(
        url,
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }
    )

if __name__ == "__main__":
    respuesta = getRequest("https://lectortmo.com/library/manga/8119/SE-System-Engineer")
    
    downloadpath = os.getcwd()+"\\Download\\"
    if not os.path.exists(downloadpath):
        try:
            os.makedirs(downloadpath)
        except OSError as e:
            if e.errno != e.errno.EEXIST:
                raise

    contenido_web = BeautifulSoup(respuesta.text, 'html.parser')

    nombreManga = contenido_web.find('h2').text.strip()

    #creo la carpeta donde se depositaran las imagenes
    currentDirectory = os.path.join(downloadpath, nombreManga)

    if not os.path.exists(currentDirectory):
        try:
            os.makedirs(currentDirectory)
        except OSError as e:
            if e.errno != e.errno.EEXIST:
                raise

    capitulosBlock = contenido_web.find(id='chapters')

    capitulos = []

    #obtener enlaces de los capitulos
    for li in capitulosBlock.find_all('li'):

        nombre = li.find('h4')
        if nombre!=None:
            nombre = nombre.get_text().replace("\n", "").replace("\xa0", "").replace('\\', "").replace(':', "").replace("/", "").replace("?", "").replace("¿", "").strip()
        
        enlace = None
        scan = None
        fecha = None
        for link in li.find_all('a'):
            if link.get('href')!=None:
                if 'view_uploads' in link.get('href'):
                    enlace = link.get('href')
                elif 'group' in link.get('href'):
                    scan = link.get_text()
                    fecha = li.find(class_="badge badge-primary p-2").get_text()

        if nombre!=None and enlace!=None:
            if nombre!="" and enlace!="":
                # print("[{}] - {}".format(nombre, enlace))
                capitulos.append([nombre, enlace, fecha, scan])

    #aqui filtro scan y capitulos
    df = pd.DataFrame(capitulos, columns=['Nombre', 'Enlace', 'Fecha', 'Scan'])
    
    # df = df.groupby(df.Nombre).first()
    df.drop_duplicates(subset ="Nombre", keep = False, inplace = True)

    #obtener imagenes de los capitulos segun los enlaces
    for indice, row in df.iterrows():
    # for enlace in capitulos:
        cap = getRequest(row["Enlace"])
        if cap.status_code==200:
            #creo la carpeta donde se depositaran las imagenes
            currentDirectory = os.path.join(downloadpath, nombreManga, row["Nombre"])
            if not os.path.exists(currentDirectory):
                try:
                    os.makedirs(currentDirectory)
                except OSError as e:
                    if e.errno != e.errno.EEXIST:
                        raise

            enlaceCascada = BeautifulSoup(cap.text, 'html.parser').find(title="Cascada").get('href')
            capCascadaRespuesta = getRequest(enlaceCascada)
            capCascada = BeautifulSoup(capCascadaRespuesta.text, 'html.parser').find(id="main-container")

            for index, img in enumerate(capCascada.find_all('img')):
                if img.get("data-src")!=None:
                    if __name__ == "__main__":
                        print("[{}] - Page {} URL: {}".format(row["Nombre"], index, img.get("data-src")))
                    response = requests.get(img.get("data-src"), stream=True)
                    with open(currentDirectory+"\\"+'{}.png'.format(index), 'wb') as out_file:
                        shutil.copyfileobj(response.raw, out_file)
                    del response
    



    # for link in capitulos.find_all('a'):
    #     if link.get('href')!=None:
    #         if 'view_uploads' in link.get('href'):
    #             print(link.get('href'))

    print("Done.")