from pyzbar import pyzbar     #identificar codigo de barras
import argparse
import cv2    #habilita la opcion de usar la camara
from flask import Flask, Blueprint, render_template, request, url_for, redirect
# from routes.product import producto 
import json
app = Flask(__name__)

# app.register_blueprint(producto)
# Crear una ruta con Blueprint
# producto = Blueprint("producto", __name__)
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True, help="path to input image")
#args = vars(ap.parse_args())

@app.route("/" , methods=['GET', 'POST'])
def index():
 if request.method == 'POST':

        cap = cv2.VideoCapture(0)   #guardamos en la variable cap lo que graba la camara con cv2.videocapture

        if not cap.isOpened():      # si la camara no esta abierta imprimir error
            print("Error")
        while cap.isOpened():        # mientras la camara este abierta
            ret, frame = cap.read()    #ret devuelve un valor booleano y en frame se guarda cap.read que lee lo que recibe de la camara
            if ret:                     #si esto es true
                barcodes = pyzbar.decode(frame)         #en barcodes se guarda en forma de lista la decodificacion de la imagen guardada en frame
                for barcode in barcodes:                  #el iterador barcode recorre cada elemento de la imagen decodificada de barcodes 
                    (x, y, w, h) = barcode.rect                                      #Enmarca el codigo de barras 
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)     
                    barcodeData = barcode.data.decode("utf-8")     #se guarda en barcodeData la codificacion de cada elemento de la imagen en el iterador en formato utf-8 , es decir, convierte la informacion de bits a texto entendible 
                    # barcodeType = barcode.type
                    # text = "{} ({})".format(barcodeData, barcodeType)                                       #utilizando 
                    # cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    # print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))

                    with open ("basededatos.json") as base_de_datos:

                      #milista = base_de_datos.read().splitlines()
                        biblioteca = json.load(base_de_datos)
                      #  print(type(biblioteca))
                        productos = biblioteca["producto"]
                       #print(len(productos))
                    
                    
                    for i in range(len(productos)):
                        codigo_de_producto = biblioteca["producto"][i]["codigo_de_barras"]  
                        imagen_de_producto = biblioteca["producto"][i]["imagen"]
                        marca_de_producto = biblioteca["producto"][i]["marca"]
                        material_de_producto = biblioteca["producto"][i]["material"]

                        if codigo_de_producto == barcodeData:
                            print("lo hicimooooooooooos")
                            return render_template('vista3.html',material=material_de_producto, marca=marca_de_producto, imagen=imagen_de_producto)
                            #return render_template("vista3.html",imagen=imagen_de_producto, marca=marca_de_producto, material=material_de_producto)
                        else:
                            # return redirect("vista4.html")
                            print("No hay")
                            # return render_template(url_for('vista4'))
                    # condicional que revise si barcodeData == "codigo de barras"

                cv2.imshow('Frame', frame)
                if cv2.waitKey(1)  == ord('q'):
                    break
            else:
                break
        barcodeData
        cap.release()
        cv2.destroyAllWindows() 
 return render_template('vista1.html')


@app.route("/succes", methods=['GET'])
def succes():
    return render_template('vista3.html')

@app.route("/error", methods=['GET', 'POST'])
def error():
    return render_template('vista4.html')


'''
@app.route("product/:product_name")
def consultar_producto():
    if method == "GET":
        data = data.json()
        response = url[0]
'''
