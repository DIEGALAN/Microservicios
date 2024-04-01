from flask import Flask, jsonify, request, g
from flask_httpauth import HTTPBasicAuth
import sqlite3

app = Flask(__name__)
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):

    conn = sqlite3.connect('BD_USUARIOS.db')
    c = conn.cursor()
    
    c.execute('SELECT username, password, perfilusu FROM USUARIOS WHERE username = ?', (username,))
    user = c.fetchone()
    
    if user and user[0] == username and user[1] == password:
        g.perfil = user[2]
        return True
    return False

@app.route('/estado_c', methods=['GET'])
@auth.login_required
def get_estado_c():
    if g.perfil == 'Mesero':
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('SELECT * FROM ESTADO_C')
        estado_c = c.fetchall()
        conn.close()
        return jsonify(estado_c)
    elif g.perfil == 'Cocinero':
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('SELECT * FROM estado_c')
        estado_c = c.fetchall()
        conn.close()
        return jsonify(estado_c)
    else:
        return jsonify({'message': 'Acceso denegado'})

@app.route('/estado_c/<int:id>', methods=['GET'])
@auth.login_required
def get_usuario(id):
    if g.perfil == 'Mesero':
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('SELECT * FROM estado_c WHERE id_estado = ?', (id,))
        estado_c = c.fetchall()
        conn.close()
        return jsonify(estado_c)
    elif g.perfil == 'Cocinero':
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('SELECT * FROM estado_c WHERE id_estado = ?', (id,))
        estado_c = c.fetchall()
        conn.close()
        return jsonify(estado_c)
    else:
        return jsonify({'message': 'Acceso denegado'})

@app.route('/estado_c/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_usuario(id):
    if g.perfil == 'Mesero':
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('DELETE FROM estado_c WHERE id_estado = ?', (id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Estado eliminado correctamente'})
    else:
        return jsonify({'message': 'Acceso denegado'})

@app.route('/estado_c', methods=['POST'])
@auth.login_required
def add_usuario():
    if g.perfil == 'Mesero':
        nuevo_Estado = request.get_json()
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('INSERT INTO estado_c (descrip_estado) VALUES (?)',
                  (nuevo_Estado['descrip_estado']))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Estado agregado correctamente'})
    else:
        return jsonify({'message': 'Acceso denegado'})

@app.route('/estado_c/<int:id>', methods=['PATCH'])
@auth.login_required
def update_usuario(id):
    if g.perfil == 'Mesero':
        estadp_actualizado = request.get_json()
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('UPDATE estado_c SET descrip_estado = ?',
                  (estadp_actualizado['descrip_estado'], id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Estado actualizado correctamente'})
    elif g.perfil == 'Cocinero':
        estadp_actualizado = request.get_json()
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('UPDATE estado_c SET descrip_estado = ?',
                  (estadp_actualizado['descrip_estado'], id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Estado actualizado correctamente'})
    else:
        return jsonify({'message': 'Acceso denegado'})

#-----------------------------------------------------------
#-----------------------------------------------------------
#-----------------------------------------------------------
#-----------------TABLA ORDEN_C---------------------------

@app.route('/orden_c', methods=['GET'])
@auth.login_required
def get_orden_c():
    if g.perfil == 'Mesero':
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('SELECT * FROM orden_c')
        orden_c = c.fetchall()
        conn.close()
        return jsonify(orden_c)
    elif g.perfil == 'Cocinero':
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('SELECT * FROM orden_c')
        orden_c = c.fetchall()
        conn.close()
        return jsonify(orden_c)
    else:
        return jsonify({'message': 'Acceso denegado'})

@app.route('/orden_c/<int:id>', methods=['GET'])
@auth.login_required
def get_orden_cs(id):
    if g.perfil == 'Mesero':
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('SELECT * FROM orden_c WHERE id_orden = ?', (id,))
        orden_c = c.fetchall()
        conn.close()
        return jsonify(orden_c)
    elif g.perfil == 'Cocinero':
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('SELECT * FROM orden_c WHERE id_orden = ?', (id,))
        orden_c = c.fetchall()
        conn.close()
        return jsonify(orden_c)
    else:
        return jsonify({'message': 'Acceso denegado'})

@app.route('/orden_c/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_orden(id):
    if g.perfil == 'Mesero':
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('DELETE FROM orden_c WHERE id_orden = ?', (id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'orden eliminado correctamente'})
    else:
        return jsonify({'message': 'Acceso denegado'})

@app.route('/orden_c', methods=['POST'])
@auth.login_required
def add_orden():
    if g.perfil == 'Mesero':
        nuevo_orden = request.get_json()
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('INSERT INTO orden_c (id_orden, tiempo_orden, id_estado, id_receta) VALUES (?, ?, ?, ?', 
                   (nuevo_orden['id_orden'], nuevo_orden['tiempo_orden'], nuevo_orden['id_estado'], nuevo_orden['id_receta']))
        conn.commit()
        conn.close()
        return jsonify({'message': 'orden agregado correctamente'})
    else:
        return jsonify({'message': 'Acceso denegado'})

@app.route('/orden_c/<int:id>', methods=['PATCH'])
@auth.login_required
def update_orden(id):
    if g.perfil == 'Mesero':
        orden_actualizado = request.get_json()
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('UPDATE orden_c SET tiempo_orden = ?, id_estado = ?, id_receta = ? WHERE id_orden = ?', 
                   (orden_actualizado['tiempo_orden'], orden_actualizado['id_estado'], orden_actualizado['id_receta'], id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Orden actualizado correctamente'})
    elif g.perfil == 'Cocinero':
        orden_actualizado = request.get_json()
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('UPDATE orden_c SET tiempo_orden = ?, id_estado = ?, id_receta = ? WHERE id_orden = ?', 
                   (orden_actualizado['tiempo_orden'], orden_actualizado['id_estado'], orden_actualizado['id_receta'], id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'orden actualizado correctamente'})
    else:
        return jsonify({'message': 'Acceso denegado'})

#-----------------------------------------------------------
#-----------------------------------------------------------
#-----------------------------------------------------------
#-----------------TABLA RECETA_C---------------------------


@app.route('/receta_c', methods=['GET'])
@auth.login_required
def get_receta_c():
    if g.perfil == 'Mesero':
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('SELECT * FROM receta_c')
        receta_c = c.fetchall()
        conn.close()
        return jsonify(receta_c)
    elif g.perfil == 'Cocinero':
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('SELECT * FROM receta_c')
        receta_c = c.fetchall()
        conn.close()
        return jsonify(receta_c)
    else:
        return jsonify({'message': 'Acceso denegado'})

@app.route('/receta_c/<int:id>', methods=['GET'])
@auth.login_required
def get_receta_cs(id):
    if g.perfil == 'Mesero':
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('SELECT * FROM receta_c WHERE id_receta = ?', (id,))
        receta_c = c.fetchall()
        conn.close()
        return jsonify(receta_c)
    elif g.perfil == 'Cocinero':
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('SELECT * FROM receta_c WHERE id_receta = ?', (id,))
        receta_c = c.fetchall()
        conn.close()
        return jsonify(receta_c)
    else:
        return jsonify({'message': 'Acceso denegado'})

@app.route('/receta_c/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_receta_c(id):
    if g.perfil == 'Mesero':
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('DELETE FROM receta_c WHERE id_receta = ?', (id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'receta_c eliminado correctamente'})
    else:
        return jsonify({'message': 'Acceso denegado'})

@app.route('/receta_c', methods=['POST'])
@auth.login_required
def add_receta_c():
    if g.perfil == 'Mesero':
        nueva_receta_c = request.get_json()
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('INSERT INTO receta_c (id_receta, nombre_receta) VALUES (?, ?)', 
                   (nueva_receta_c['id_receta'], nueva_receta_c['nombre_receta']))
        conn.commit()
        conn.close()
        return jsonify({'message': 'receta_c agregado correctamente'})
    else:
        return jsonify({'message': 'Acceso denegado'})

@app.route('/receta_c/<int:id>', methods=['PATCH'])
@auth.login_required
def update_receta_c(id):
    if g.perfil == 'Mesero':
        receta_c_actualizado = request.get_json()
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('UPDATE receta_c SET nombre_receta = ?', 
                   (receta_c_actualizado['nombre_receta'], id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'receta_c actualizado correctamente'})
    elif g.perfil == 'Cocinero':
        receta_c_actualizado = request.get_json()
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('UPDATE receta_c SET nombre_receta = ? WHERE receta_c = ?', 
                   (receta_c_actualizado['nombre_receta'], id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'receta_c actualizado correctamente'})
    else:
        return jsonify({'message': 'Acceso denegado'})


#-----------------------------------------------------------
#-----------------------------------------------------------
#-----------------------------------------------------------
#-----------------TABLA INGREDIENTES_RECETA_C-----------------------------


@app.route('/ingredientes_receta_c', methods=['GET'])
@auth.login_required
def get_eingredientes_receta_c():
    if g.perfil == 'Mesero':
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('SELECT * FROM ingredientes_receta_c')
        ingredientes_receta_c = c.fetchall()
        conn.close()
        return jsonify(ingredientes_receta_c)
    elif g.perfil == 'Cocinero':
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('SELECT * FROM ingredientes_receta_c')
        ingredientes_receta_c = c.fetchall()
        conn.close()
        return jsonify(ingredientes_receta_c)
    else:
        return jsonify({'message': 'Acceso denegado'})

@app.route('/ingredientes_receta_c/<int:id>', methods=['GET'])
@auth.login_required
def get_ingredientes_receta_cs(id):
    if g.perfil == 'Mesero':
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('SELECT * FROM ingredientes_receta_c WHERE id_ingr_rec = ?', (id,))
        ingredientes_receta_c = c.fetchall()
        conn.close()
        return jsonify(ingredientes_receta_c)
    elif g.perfil == 'Cocinero':
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('SELECT * FROM ingredientes_receta_c WHERE id_ingr_rec = ?', (id,))
        ingredientes_receta_c = c.fetchall()
        conn.close()
        return jsonify(ingredientes_receta_c)
    else:
        return jsonify({'message': 'Acceso denegado'})

@app.route('/ingredientes_receta_c/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_ingredientes_receta_c(id):
    if g.perfil == 'Mesero':
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('DELETE FROM ingredientes_receta_c WHERE id_ingr_rec = ?', (id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'ingredientes_receta_c eliminado correctamente'})
    else:
        return jsonify({'message': 'Acceso denegado'})

@app.route('/ingredientes_receta_c', methods=['POST'])
@auth.login_required
def add_ingredientes_receta_c():
    if g.perfil == 'Mesero':
        nuevo_ingredientes_receta_c = request.get_json()
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('INSERT INTO ingredientes_receta_c (id_ingr_rec, id_ingrediente, id_receta, cantidad) VALUES (?, ?, ?, ?)', 
                   (nuevo_ingredientes_receta_c['id_ingr_rec'], nuevo_ingredientes_receta_c['id_ingrediente'], nuevo_ingredientes_receta_c['id_receta'], nuevo_ingredientes_receta_c['cantidad']))
        conn.commit()
        conn.close()
        return jsonify({'message': 'ingredientes_receta_c agregado correctamente'})
    else:
        return jsonify({'message': 'Acceso denegado'})

@app.route('/ingredientes_receta_c/<int:id>', methods=['PATCH'])
@auth.login_required
def update_ingredientes_receta_c(id):
    if g.perfil == 'Mesero':
        ingredientes_receta_c_actualizado = request.get_json()
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('UPDATE ingredientes_receta_c SET id_ingr_rec = ?, id_ingrediente = ?, id_receta = ?, cantidad = ? WHERE id_ingr_rec = ?', 
                   (ingredientes_receta_c_actualizado['id_ingr_rec'], ingredientes_receta_c_actualizado['id_ingrediente'], ingredientes_receta_c_actualizado['id_receta'], ingredientes_receta_c_actualizado['cantidad'], id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'ingredientes_receta_c actualizado correctamente'})
    elif g.perfil == 'Cocinero':
        ingredientes_receta_c_actualizado = request.get_json()
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('UPDATE ingredientes_receta_c SET id_ingr_rec = ?, id_ingrediente = ?, id_receta = ?, cantidad = ? WHERE id_ingr_rec = ?', 
                   (ingredientes_receta_c_actualizado['id_ingr_rec'], ingredientes_receta_c_actualizado['id_ingrediente'], ingredientes_receta_c_actualizado['id_receta'], ingredientes_receta_c_actualizado['cantidad'], id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'ingredientes_receta_c actualizado correctamente'})
    else:
        return jsonify({'message': 'Acceso denegado'})


#-----------------------------------------------------------
#-----------------------------------------------------------
#-----------------------------------------------------------
#-----------------TABLA INGREDIENTES_C---------------------------

@app.route('/ingredientes_c', methods=['GET'])
@auth.login_required
def get_ingredientes_ces():
    if g.perfil == 'Mesero':
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('SELECT * FROM ingredientes_c')
        ingredientes_c = c.fetchall()
        conn.close()
        return jsonify(ingredientes_c)
    elif g.perfil == 'Cocinero':
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('SELECT * FROM ingredientes_c')
        ingredientes_c = c.fetchall()
        conn.close()
        return jsonify(ingredientes_c)
    else:
        return jsonify({'message': 'Acceso denegado'})

@app.route('/ingredientes_c/<int:id>', methods=['GET'])
@auth.login_required
def get_ingredientes_c(id):
    if g.perfil == 'Mesero':
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('SELECT * FROM ingredientes_c WHERE id_ingrediente = ?', (id,))
        ingredientes_c = c.fetchall()
        conn.close()
        return jsonify(ingredientes_c)
    elif g.perfil == 'Cocinero':
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('SELECT * FROM ingredientes_c WHERE id_ingrediente = ?', (id,))
        ingredientes_c = c.fetchall()
        conn.close()
        return jsonify(ingredientes_c)
    else:
        return jsonify({'message': 'Acceso denegado'})

@app.route('/ingredientes_c/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_ingredientes_c(id):
    if g.perfil == 'Mesero':
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('DELETE FROM ingredientes_c WHERE id_ingrediente = ?', (id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'ingredientes_c eliminado correctamente'})
    else:
        return jsonify({'message': 'Acceso denegado'})

@app.route('/ingredientes_c', methods=['POST'])
@auth.login_required
def add_ingredientes_c():
    if g.perfil == 'Mesero':
        nuevo_ingredientes_c = request.get_json()
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('INSERT INTO ingredientes_c (id_ingrediente, nombre_ingr, cantidad) VALUES (?, ?, ?)', 
                   (nuevo_ingredientes_c['id_ingrediente'], nuevo_ingredientes_c['nombre_ingr'], nuevo_ingredientes_c['cantidad']))
        conn.commit()
        conn.close()
        return jsonify({'message': 'ingredientes_c agregado correctamente'})
    else:
        return jsonify({'message': 'Acceso denegado'})

@app.route('/ingredientes_c/<int:id>', methods=['PATCH'])
@auth.login_required
def update_ingredientes_c(id):
    if g.perfil == 'Mesero':
        ingredientes_c_actualizado = request.get_json()
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('UPDATE ingredientes_c SET id_ingrediente = ?, nombre_ingr = ?, cantidad = ? WHERE id_ingrediente = ?', 
                   (ingredientes_c_actualizado['id_ingrediente'], ingredientes_c_actualizado['nombre_ingr'], ingredientes_c_actualizado['cantidad'], id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Usuario actualizado correctamente'})
    elif g.perfil == 'Cocinero':
        ingredientes_c_actualizado = request.get_json()
        conn = sqlite3.connect('BD_COCINA.db')
        c = conn.cursor()
        c.execute('UPDATE ingredientes_c SET id_ingrediente = ?, nombre_ingr = ?, cantidad = ? WHERE id_ingrediente = ?', 
                   (ingredientes_c_actualizado['id_ingrediente'], ingredientes_c_actualizado['nombre_ingr'], ingredientes_c_actualizado['cantidad'], id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'ingredientes_c actualizado correctamente'})
    else:
        return jsonify({'message': 'Acceso denegado'})

#-----------------------------------------------------------
#-----------------------------------------------------------
#-----------------------------------------------------------
#-----------------------------------------------------------
#-----------------------------------------------------------
#-----------------------------------------------------------
#-----------------------------------------------------------
#-----------------------------------------------------------
#-----------------------------------------------------------
#-----------------------------------------------------------
#-----------------------------------------------------------
#-----------------------------------------------------------
#-----------------TABLA ESTADO_R---------------------------
    
@app.route('/estado_r', methods=['GET'])
@auth.login_required
def get_estado_r():
    if g.perfil == 'Mesero':
        conn = sqlite3.connect('BD_RECEPCION.db')
        c = conn.cursor()
        c.execute('SELECT * FROM estado_r')
        estado_r = c.fetchall()
        conn.close()
        return jsonify(estado_r)
    elif g.perfil == 'Cocinero':
        conn = sqlite3.connect('BD_RECEPCION.db')
        c = conn.cursor()
        c.execute('SELECT * FROM estado_r')
        estado_r = c.fetchall()
        conn.close()
        return jsonify(estado_r)
    else:
        return jsonify({'message': 'Acceso denegado'})

@app.route('/estado_r/<int:id>', methods=['GET'])
@auth.login_required
def get_estado_rs(id):
    if g.perfil == 'Mesero':
        conn = sqlite3.connect('BD_RECEPCION.db')
        c = conn.cursor()
        c.execute('SELECT * FROM estado_r WHERE id_estado = ?', (id,))
        estado_r = c.fetchall()
        conn.close()
        return jsonify(estado_r)
    elif g.perfil == 'Cocinero':
        conn = sqlite3.connect('BD_RECEPCION.db')
        c = conn.cursor()
        c.execute('SELECT * FROM estado_r WHERE id_estado = ?', (id,))
        estado_r = c.fetchall()
        conn.close()
        return jsonify(estado_r)
    else:
        return jsonify({'message': 'Acceso denegado'})

@app.route('/estado_r/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_estado_r(id):
    if g.perfil == 'Mesero':
        conn = sqlite3.connect('BD_RECEPCION.db')
        c = conn.cursor()
        c.execute('DELETE FROM estado_r WHERE id_estado = ?', (id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'estado_r eliminado correctamente'})
    else:
        return jsonify({'message': 'Acceso denegado'})

@app.route('/estado_r', methods=['POST'])
@auth.login_required
def add_estado_r():
    if g.perfil == 'Mesero':
        nuevo_estado_r = request.get_json()
        conn = sqlite3.connect('BD_RECEPCION.db')
        c = conn.cursor()
        c.execute('INSERT INTO estado_r (id_estado, descrip_estado) VALUES (?, ?)', 
                   (nuevo_estado_r['id_estado'], nuevo_estado_r['descrip_estado']))
        conn.commit()
        conn.close()
        return jsonify({'message': 'estado_r agregado correctamente'})
    else:
        return jsonify({'message': 'Acceso denegado'})

@app.route('/estado_r/<int:id>', methods=['PATCH'])
@auth.login_required
def update_estado_r(id):
    if g.perfil == 'Mesero':
        estado_r_actualizado = request.get_json()
        conn = sqlite3.connect('BD_RECEPCION.db')
        c = conn.cursor()
        c.execute('UPDATE estado_r SET id_estado = ?, descrip_estado = ? WHERE id_estado = ?', 
                   (estado_r_actualizado['id_estado'], estado_r_actualizado['descrip_estado'], id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Usuario actualizado correctamente'})
    elif g.perfil == 'Cocinero':
        estado_r_actualizado = request.get_json()
        conn = sqlite3.connect('BD_RECEPCION.db')
        c = conn.cursor()
        c.execute('UPDATE estado_r SET id_estado = ?, descrip_estado = ? WHERE id_estado = ?', 
                   (estado_r_actualizado['id_estado'], estado_r_actualizado['descrip_estado'], id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'estado_r actualizado correctamente'})
    else:
        return jsonify({'message': 'Acceso denegado'})

#-----------------------------------------------------------
#-----------------------------------------------------------
#-----------------TABLA ORDEN_R---------------------------
    
@app.route('/orden_r', methods=['GET'])
@auth.login_required
def get_orden_r():
    if g.perfil == 'Mesero':
        conn = sqlite3.connect('BD_RECEPCION.db')
        c = conn.cursor()
        c.execute('SELECT * FROM orden_r')
        orden_r = c.fetchall()
        conn.close()
        return jsonify(orden_r)
    elif g.perfil == 'Cocinero':
        conn = sqlite3.connect('BD_RECEPCION.db')
        c = conn.cursor()
        c.execute('SELECT * FROM orden_r')
        orden_r = c.fetchall()
        conn.close()
        return jsonify(orden_r)
    else:
        return jsonify({'message': 'Acceso denegado'})

@app.route('/orden_r/<int:id>', methods=['GET'])
@auth.login_required
def get_orden_rs(id):
    if g.perfil == 'Mesero':
        conn = sqlite3.connect('BD_RECEPCION.db')
        c = conn.cursor()
        c.execute('SELECT * FROM orden_r WHERE id_orden = ?', (id,))
        orden_r = c.fetchall()
        conn.close()
        return jsonify(orden_r)
    elif g.perfil == 'Cocinero':
        conn = sqlite3.connect('BD_RECEPCION.db')
        c = conn.cursor()
        c.execute('SELECT * FROM orden_r WHERE id_orden = ?', (id,))
        orden_r = c.fetchall()
        conn.close()
        return jsonify(orden_r)
    else:
        return jsonify({'message': 'Acceso denegado'})

@app.route('/orden_r/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_orden_r(id):
    if g.perfil == 'Mesero':
        conn = sqlite3.connect('BD_RECEPCION.db')
        c = conn.cursor()
        c.execute('DELETE FROM orden_r WHERE id_orden = ?', (id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'orden_r eliminado correctamente'})
    else:
        return jsonify({'message': 'Acceso denegado'})

@app.route('/orden_r', methods=['POST'])
@auth.login_required
def add_orden_r():
    if g.perfil == 'Mesero':
        orden_orden_r = request.get_json()
        conn = sqlite3.connect('BD_RECEPCION.db')
        c = conn.cursor()
        c.execute('INSERT INTO orden_r (id_orden, tiempo_orden, id_estado, id_receta) VALUES (?, ?, ?, ?)', 
                   (orden_orden_r['id_orden'], orden_orden_r['tiempo_orden'], orden_orden_r['id_estado'], orden_orden_r['id_receta']))
        conn.commit()
        conn.close()
        return jsonify({'message': 'orden_r agregado correctamente'})
    else:
        return jsonify({'message': 'Acceso denegado'})

@app.route('/orden_r/<int:id>', methods=['PATCH'])
@auth.login_required
def update_orden_r(id):
    if g.perfil == 'Mesero':
        orden_r_actualizado = request.get_json()
        conn = sqlite3.connect('BD_RECEPCION.db')
        c = conn.cursor()
        c.execute('UPDATE orden_r SET id_orden = ?, tiempo_orden = ?, id_estado = ?, id_receta = ? WHERE id_orden = ?', 
                   (orden_r_actualizado['id_orden'], orden_r_actualizado['tiempo_orden'], orden_r_actualizado['id_estado'], orden_r_actualizado['id_receta'], id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Usuario actualizado correctamente'})
    elif g.perfil == 'Cocinero':
        orden_r_actualizado = request.get_json()
        conn = sqlite3.connect('BD_RECEPCION.db')
        c = conn.cursor()
        c.execute('UPDATE orden_r SET id_orden = ?, tiempo_orden = ?, id_estado = ?, id_receta = ? WHERE id_orden = ?', 
                   (orden_r_actualizado['id_orden'], orden_r_actualizado['tiempo_orden'], orden_r_actualizado['id_estado'], orden_r_actualizado['id_receta'], id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'orden_r actualizado correctamente'})
    else:
        return jsonify({'message': 'Acceso denegado'})


#-----------------------------------------------------------
#-----------------------------------------------------------
#-----------------TABLA RECETA_R---------------------------
    
@app.route('/receta_r', methods=['GET'])
@auth.login_required
def get_receta_r():
    if g.perfil== 'Mesero':
        conn = sqlite3.connect('BD_RECEPCION.db')
        c = conn.cursor()
        c.execute('SELECT * FROM receta_r')
        receta_r = c.fetchall()
        conn.close()
        return jsonify(receta_r)
    elif g.perfil == 'Cocinero':
        conn = sqlite3.connect('BD_RECEPCION.db')
        c = conn.cursor()
        c.execute('SELECT * FROM receta_r')
        receta_r = c.fetchall()
        conn.close()
        return jsonify(receta_r)
    else:
        return jsonify({'message': 'Acceso denegado'})

@app.route('/receta_r/<int:id>', methods=['GET'])
@auth.login_required
def get_receta_rs(id):
    if g.perfil == 'Mesero':
        conn = sqlite3.connect('BD_RECEPCION.db')
        c = conn.cursor()
        c.execute('SELECT * FROM receta_r WHERE id_receta = ?', (id,))
        receta_r = c.fetchall()
        conn.close()
        return jsonify(receta_r)
    elif g.perfil == 'Cocinero':
        conn = sqlite3.connect('BD_RECEPCION.db')
        c = conn.cursor()
        c.execute('SELECT * FROM receta_r WHERE id_receta = ?', (id,))
        receta_r = c.fetchall()
        conn.close()
        return jsonify(receta_r)
    else:
        return jsonify({'message': 'Acceso denegado'})

@app.route('/receta_r/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_receta_r(id):
    if g.perfil == 'Mesero':
        conn = sqlite3.connect('BD_RECEPCION.db')
        c = conn.cursor()
        c.execute('DELETE FROM receta_r WHERE id_receta = ?', (id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'receta_r eliminado correctamente'})
    else:
        return jsonify({'message': 'Acceso denegado'})

@app.route('/receta_r', methods=['POST'])
@auth.login_required
def add_receta_r():
    if g.perfil == 'Mesero':
        nuevo_receta_r = request.get_json()
        conn = sqlite3.connect('BD_RECEPCION.db')
        c = conn.cursor()
        c.execute('INSERT INTO receta_r (id_receta, nombre_receta) VALUES (?, ?)', 
                   (nuevo_receta_r['id_receta'], nuevo_receta_r['nombre_receta']))
        conn.commit()
        conn.close()
        return jsonify({'message': 'receta_r agregado correctamente'})
    else:
        return jsonify({'message': 'Acceso denegado'})

@app.route('/receta_r/<int:id>', methods=['PATCH'])
@auth.login_required
def update_receta_r(id):
    if g.perfil == 'Mesero':
        receta_r_actualizado = request.get_json()
        conn = sqlite3.connect('BD_RECEPCION.db')
        c = conn.cursor()
        c.execute('UPDATE receta_r SET id_receta = ?, nombre_receta = ? WHERE id_receta = ?', 
                   (receta_r_actualizado['id_receta'], receta_r_actualizado['nombre_receta'], id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Usuario actualizado correctamente'})
    elif g.perfil == 'Cocinero':
        receta_r_actualizado = request.get_json()
        conn = sqlite3.connect('BD_RECEPCION.db')
        c = conn.cursor()
        c.execute('UPDATE receta_r SET id_receta = ?, nombre_receta = ? WHERE id_receta = ?', 
                   (receta_r_actualizado['id_receta'], receta_r_actualizado['nombre_receta'], id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'receta_r actualizado correctamente'})
    else:
        return jsonify({'message': 'Acceso denegado'})




if __name__ == '__main__':
    app.run(debug=True)
