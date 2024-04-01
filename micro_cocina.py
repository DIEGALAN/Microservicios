from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import random
import sqlite3
import requests

app = Flask(__name__)

BODEGA_URL = 'http://localhost:5000/bodega/consultar/'

MESERO_URL = 'http://localhost:5000/mesero/recibir_plato/'

BD_PATH = 'C:/Users/Diego/Documents/Microservicios//BD_COCINA.db'

def elegir_receta():
    conn = sqlite3.connect(BD_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id_receta FROM RECETA_C")
    recetas = cursor.fetchall()
    conn.close()
    return random.choice(recetas)[0]

def obtener_ingredientes_receta(receta_id):
    conn = sqlite3.connect(BD_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre_ingr, cantidad FROM INGREDIENTES_RECETA_C JOIN INGREDIENTES_C ON INGREDIENTES_RECETA_C.id_ingrediente = INGREDIENTES_C.id_ingrediente WHERE id_receta=?", (receta_id,))
    ingredientes = cursor.fetchall()
    conn.close()
    return ingredientes

def solicitar_ingredientes(ingredientes):
    ingredientes_disponibles = {}
    for ingrediente, cantidad in ingredientes:
        response = requests.get(BODEGA_URL + ingrediente)
        data = response.json()
        cantidad_disponible = min(data.get('quantity', 0), cantidad)
        ingredientes_disponibles[ingrediente] = cantidad_disponible
    return ingredientes_disponibles

def preparar_plato(ingredientes):
    plato_preparado = f"Plato preparado con los ingredientes: {ingredientes}"
    return plato_preparado

@app.route('/cocina/preparar_plato', methods=['GET'])
def preparar_plato_api():
    receta_id = elegir_receta()
    ingredientes = obtener_ingredientes_receta(receta_id)
    ingredientes_disponibles = solicitar_ingredientes(ingredientes)
    plato_preparado = preparar_plato(ingredientes_disponibles)
    response = requests.post(MESERO_URL, json={'plato': plato_preparado})
    if response.status_code == 200:
        return jsonify({'message': 'Plato preparado y entregado al mesero exitosamente.'}), 200
    else:
        return jsonify({'message': 'Error al entregar el plato al mesero.'}), 500

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BD_COCINA.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Receta(db.Model):
    id_receta = db.Column(db.Integer, primary_key=True)
    nombre_receta = db.Column(db.String(100), nullable=False)

@app.route('/cocina/recetas', methods=['GET'])
def obtener_recetas():
    recetas = Receta.query.all()

    recetas_json = []
    for receta in recetas:
        receta_dict = {
            'id_receta': receta.id_receta,
            'nombre_receta': receta.nombre_receta
        }
        recetas_json.append(receta_dict)

    return jsonify(recetas_json)



if __name__ == "__main__":
    app.run(debug=True)
