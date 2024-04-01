import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

MARKETPLACE_URL = "https://microservices-utadeo-arq-fea471e6a9d4.herokuapp.com/api/v1/software-architecture/market-place"

def get_ingredient_quantity(ingredient_name):
    response = requests.get(f"{MARKETPLACE_URL}?ingredient={ingredient_name}")

    if response.status_code == 200:
        data = response.json()
        if 'data' in data and ingredient_name in data['data']:
            return data['data'][ingredient_name]
    return None

@app.route('/marketplace', methods=['GET'])
def get_ingredient_from_marketplace():
    ingredient_name = request.args.get('ingredient')

    if not ingredient_name:
        return jsonify({"error": "Missing ingredient parameter"}), 400

    while True:
        ingredient_quantity = get_ingredient_quantity(ingredient_name)
        if ingredient_quantity is not None and ingredient_quantity != 0:
            return jsonify({"ingredient": ingredient_name, "quantity": ingredient_quantity})
    
    return jsonify({"error": "Failed to retrieve ingredient quantity from marketplace"}), 500

if __name__ == '__main__':
    app.run(debug=True)
