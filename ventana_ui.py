# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainTitle.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import requests
from bs4 import BeautifulSoup
import json
import time, shutil, os
import os.path
import pandas as pd
import string

valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)

# La función get_main_news retornará un diccionario con todas las urls y títulos de noticias encontrados en la sección principal.
def getRequest(url):

    return requests.get(
        url,
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }
    )

capitulos = []
df = ""

class Ui_dialog(object):
    def setupUi(self, dialog):
        dialog.setObjectName("dialog")
        dialog.resize(688, 332)
        self.txtUrl = QtWidgets.QTextEdit(dialog)
        self.txtUrl.setGeometry(QtCore.QRect(20, 20, 501, 41))
        self.txtUrl.setObjectName("txtUrl")
        self.progressBar = QtWidgets.QProgressBar(dialog)
        self.progressBar.setGeometry(QtCore.QRect(290, 280, 381, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.btnClean = QtWidgets.QPushButton(dialog)
        self.btnClean.setGeometry(QtCore.QRect(610, 20, 51, 41))
        self.btnClean.setObjectName("btnClean")
        self.txtScan = QtWidgets.QPlainTextEdit(dialog)
        self.txtScan.setEnabled(True)
        self.txtScan.setGeometry(QtCore.QRect(130, 80, 201, 41))
        self.txtScan.setObjectName("plainTextEdit")
        self.label = QtWidgets.QLabel(dialog)
        self.label.setGeometry(QtCore.QRect(30, 80, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(dialog)
        self.label_2.setGeometry(QtCore.QRect(340, 90, 321, 21))
        self.label_2.setObjectName("label_2")
        self.imgPreview = QtWidgets.QGraphicsView(dialog)
        self.imgPreview.setGeometry(QtCore.QRect(20, 130, 261, 181))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.imgPreview.setFont(font)
        self.imgPreview.setObjectName("imgPreview")
        self.label_3 = QtWidgets.QLabel(dialog)
        self.label_3.setGeometry(QtCore.QRect(290, 150, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(dialog)
        self.label_4.setGeometry(QtCore.QRect(290, 190, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.lblNombre = QtWidgets.QLabel(dialog)
        self.lblNombre.setGeometry(QtCore.QRect(390, 150, 281, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lblNombre.setFont(font)
        self.lblNombre.setObjectName("lblNombre")
        self.lblCapitulos = QtWidgets.QLabel(dialog)
        self.lblCapitulos.setGeometry(QtCore.QRect(390, 200, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lblCapitulos.setFont(font)
        self.lblCapitulos.setObjectName("lblCapitulos")
        self.pushButton = QtWidgets.QPushButton(dialog)
        self.pushButton.setGeometry(QtCore.QRect(290, 230, 371, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(voidDownload)
        self.pushButton_2 = QtWidgets.QPushButton(dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(520, 20, 91, 41))
        self.pushButton_2.clicked.connect(getPreview)
        font = QtGui.QFont()
        font.setKerning(True)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.lblProcess = QtWidgets.QLabel(dialog)
        self.lblProcess.setGeometry(QtCore.QRect(300, 280, 321, 16))
        self.lblProcess.setText("")
        self.lblProcess.setObjectName("lblProcess")

        self.retranslateUi(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "TuMangaOnline Downloader"))
        self.btnClean.setText(_translate("dialog", "Clean"))
        self.label.setText(_translate("dialog", "Scanlation"))
        self.label_2.setText(_translate("dialog", "Si esta vacio, utilizara la ultima subida de los capitulos"))
        self.label_3.setText(_translate("dialog", "Nombre:"))
        self.label_4.setText(_translate("dialog", "Capitulos:"))
        self.lblNombre.setText(_translate("dialog", " "))
        self.lblCapitulos.setText(_translate("dialog", " "))
        self.pushButton.setText(_translate("dialog", "Descargar"))
        self.pushButton_2.setText(_translate("dialog", "Vista Previa"))

def getPreview():                                                                                     
    url = ui.txtUrl.toPlainText() #obtengo el texto del input
    
    respuesta = getRequest(url)

    contenido_web = BeautifulSoup(respuesta.text, 'html.parser')

    nombreManga = contenido_web.find('h2').text.strip()

    capitulosBlock = contenido_web.find(id='chapters')

    for li in capitulosBlock.find_all('li'):
    
        nombre = li.find('h4')
        if nombre!=None:
            nombre = nombre.get_text().strip()
            nombre = ''.join(c for c in nombre if c in valid_chars)
        
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

    ui.lblCapitulos.setText("{}".format(len(df["Nombre"])))
    
    ui.lblNombre.setText(nombreManga)

def voidDownload():  
    if len(capitulos)==0:
        getPreview()
    # if df=='': #crash when compare
    downloadpath = os.getcwd()+"\\Download\\"

    nombreManga = ui.lblNombre.text()
    nombreManga = ''.join(c for c in nombreManga if c in valid_chars)

    df = pd.DataFrame(capitulos, columns=['Nombre', 'Enlace', 'Fecha', 'Scan'])
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

            tamanio = len(df["Nombre"])
            domain = respuesta.url[:respuesta.url.index("/contents")]

            for index, img in enumerate(capCascada.find_all('img')):
                if img.get("data-src")!=None:
                    log = "[{}] - Page {}".format(row["Nombre"], index, img.get("data-src"))
                    ui.lblProcess.setText(log)
                    app.processEvents() #update gui for pyqt
                    response = getRequest(img.get("data-src"))
                    extension = img.get("data-original").split(".")
                    with open(currentDirectory+"\\"+'{}.{}'.format(index, extension[-1]), 'wb') as out_file:
                        out_file.write(response.content)
                    # response = requests.get(img.get("data-src"), stream=True)
                    # with open(currentDirectory+"\\"+'{}.png'.format(index), 'wb') as out_file:
                    #     shutil.copyfileobj(response.raw, out_file)
                    del response

            
            ui.progressBar.setProperty("value", int(((indice+1)/tamanio)*100))
            app.processEvents() #update gui for pyqt

    ui.lblProcess.setText("Descarga Completada")
    app.processEvents() #update gui for pyqt

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    ui = Ui_dialog()
    ui.setupUi(dialog)
    dialog.show()
    sys.exit(app.exec_())
    print("Done")

