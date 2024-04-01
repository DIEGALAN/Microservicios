from flask import Flask, request, jsonify
import sqlite3
import requests

app = Flask(__name__)

BD_COCINA_PATH = 'C:/Users/Diego/Documents/Microservicios/BD_COCINA.db'
BD_USUARIOS_PATH = 'C:/Users/Diego/Documents/Microservicios/BD_USUARIOS.db'

def consultar_cantidad_ingrediente(nombre_ingrediente):
    conn = sqlite3.connect(BD_COCINA_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT cantidad FROM INGREDIENTES_C WHERE nombre_ingr=?", (nombre_ingrediente,))
    cantidad = cursor.fetchone()
    conn.close()
    return cantidad[0] if cantidad else None

def actualizar_cantidad_ingrediente(nombre_ingrediente, nueva_cantidad):
    conn = sqlite3.connect(BD_COCINA_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE INGREDIENTES_C SET cantidad=? WHERE nombre_ingr=?", (nueva_cantidad, nombre_ingrediente))
    conn.commit()
    conn.close()

def actualizar_desde_plaza_mercado(nombre_ingrediente):
    response = requests.get("http://localhost:5000/marketplace?ingredient=" + nombre_ingrediente)
    data = response.json()
    nueva_cantidad = data.get('quantity', 0)
    actualizar_cantidad_ingrediente(nombre_ingrediente, nueva_cantidad)

def autenticar_usuario(username, password):
    conn = sqlite3.connect(BD_USUARIOS_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM USUARIOS WHERE username=? AND password=?", (username, password))
    count = cursor.fetchone()[0]
    conn.close()
    return count == 1

@app.route('/bodega/actualizar', methods=['POST'])
def actualizar_cantidad_ingrediente_api():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        ingrediente = data.get('ingredient')

        if autenticar_usuario(username, password):
            nueva_cantidad = actualizar_desde_plaza_mercado(ingrediente)
            if nueva_cantidad is not None:
                actualizar_cantidad_ingrediente(ingrediente, nueva_cantidad)
                return jsonify({'message': f'Se ha actualizado la cantidad de {ingrediente} en la base de datos.'}), 200
            else:
                return jsonify({'message': f'No se pudo obtener la cantidad de {ingrediente} desde la plaza de mercado.'}), 500
        else:
            return jsonify({'message': 'Usuario o contraseña incorrectos.'}), 401

@app.route('/bodega/consultar/<nombre_ingrediente>', methods=['GET'])
def consultar_cantidad_ingrediente_api(nombre_ingrediente):
    cantidad = consultar_cantidad_ingrediente(nombre_ingrediente)
    if cantidad is not None:
        return jsonify({'ingredient': nombre_ingrediente, 'quantity': cantidad}), 200
    else:
        return jsonify({'message': 'El ingrediente no existe en la base de datos.'}), 404

if __name__ == "__main__":
    app.run(debug=True)
