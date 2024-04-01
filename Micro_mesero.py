from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

COCINA_URL = 'http://localhost:5000/cocina/preparar_plato'

def solicitar_receta():
    response = requests.get(COCINA_URL)
    if response.status_code == 200:
        data = response.json()
        return data.get('plato')
    else:
        return None

@app.route('/mesero/recibir_plato', methods=['POST'])
def recibir_plato():
    plato = solicitar_receta()
    if plato:
        return jsonify({'plato': plato}), 200
    else:
        return jsonify({'message': 'Error al recibir el plato del microservicio de cocina.'}), 500

if __name__ == "__main__":
    app.run(debug=True)
