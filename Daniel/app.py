from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__)
 
@app.route('/')
def hello_world():
    titulo = "GeekyFlask"
    usuario = {'nombre': 'Alguien'}
    return render_template('index.html',
                           titulo=titulo,
                           usuario=usuario)
 
if __name__ == '__main__':
    app.run(host='0.0.0.0')

@app.route('/postData', methods=['POST'])
def create_image():
    json = request.json

    imgs = json["imgs"]

    i = 0
    for img in imgs:
        title = json[f'imagen{i}']['TITULO']
        width = json[f'imagen{i}']['ANCHO']
        height = json[f'imagen{i}']['ALTO']
        cols = json[f'imagen{i}']['COLUMNAS']
        rows = json[f'imagen{i}']['FILAS']
        cells = json[f'imagen{i}']['CELDAS']
        colors = json[f'imagen{i}']['COLORES']
        filters = json[f'imagen{i}']['FILTROS']

        widthCells = float(width) / float(cols)
        heightCells = float(height) / float(rows)
        i += 1


    return render_template('table.html', imagenes=imgs)