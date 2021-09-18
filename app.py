from flask import Flask, request, Response
from flask import render_template
import pathlib
import imgkit

app = Flask(__name__)
if __name__ == '__main__':
    app.run(debug=True)

@app.route('/')
def index():
    return '<h1>Hola</h1>'

@app.route('/postImage',methods=['POST'])
def start():
    json = request.json
    titulo:str = json['TITULO']
    titulo = titulo.replace('\"','')
    ancho = json['ANCHO']
    alto = json['ALTO']
    filas = json['FILAS']
    cols = json['COLUMNAS']
    celdas = json['CELDAS']
    colores = json['COLORES']
    #filtros = json['FILTROS']
    
    dict_celdas = dict()
    #Primero llenar las celdas que tengamos con TRUE
    for c in celdas:
        col = c[0]
        fila = c[1]
        estado = c[2]
        numero = c[3]
        if estado == 'TRUE':
            color = colores[numero]
            dict_celdas[f'{col}{fila}'] = color
    
    #Calculamos el tamaño de las celdas
    anchoC = float(ancho) / float(cols)
    altoC = float(alto) / float(filas)

    #Hacer un dict/json que tenga los datos de la tabla a crear
    JsonImg = {
        'titulo':titulo,
        'ancho':ancho,
        'alto':alto,
        'filas':filas,
        'cols':cols,
        'anchoC':anchoC,
        'altoC':altoC,
        'celdas':dict_celdas
    }
    saveHtml(titulo,'ORIGINAL',render_template('Imagen.html',**JsonImg))
    saveImage(titulo,'ORIGINAL',render_template('solo_imagen.html',**JsonImg),ancho)
    return Response()

def saveHtml(nombre,filtro,html):
    pathlib.Path(f'imagenes/html/{nombre}').mkdir(parents=True,exist_ok=True)
    with open(f'imagenes/html/{nombre}/{filtro}.html','w') as f:
        f.write(html)
        f.close()

def saveImage(nombre,filtro,html,ancho):
    pathlib.Path(f'imagenes/jpg/{nombre}').mkdir(parents=True,exist_ok=True)
    output = f'imagenes/jpg/{nombre}/{filtro}.jpg'
    css = 'static/imagen.css'
    options = {
        'disable-smart-width':'',
        'width': int(ancho) + 20
    }
    imgkit.from_string(html,output_path=output,options=options,css=css)

def aplicarFiltro(filtro):
    pass