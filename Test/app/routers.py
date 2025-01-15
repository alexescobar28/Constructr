from flask import Blueprint, request, jsonify
from app.models import consultar_producto, init_db
from app.validators import validar_id

bp = Blueprint('api', __name__)

@bp.route('/producto/<int:id_producto>', methods=['GET'])
@validar_id
def get_producto(id_producto):
    return consultar_producto(id_producto)


@app.route('/producto', methods=['POST'])
def post_producto():
    """Endpoint para agregar un nuevo producto"""
    data = request.get_json()

    if not all(k in data for k in ('id', 'nombre', 'cantidad')):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    try:
        id_producto = int(data['id'])
        cantidad = int(data['cantidad'])

        if id_producto <= 0:
            return jsonify({"error": "ID debe ser un número positivo"}), 400
        if cantidad < 0:
            return jsonify({"error": "Cantidad debe ser un número no negativo"}), 400

        return agregar_producto(id_producto, data['nombre'], cantidad)
    except ValueError:
        return jsonify({"error": "ID y cantidad deben ser números"}), 400


@app.route('/producto/<int:id_producto>', methods=['PUT'])
@validar_id
def put_producto(id_producto):
    """Endpoint para actualizar el stock de un producto"""
    data = request.get_json()

    if 'cantidad' not in data:
        return jsonify({"error": "Falta el campo cantidad"}), 400

    try:
        nueva_cantidad = int(data['cantidad'])
        return actualizar_stock(id_producto, nueva_cantidad)
    except ValueError:
        return jsonify({"error": "Cantidad debe ser un número"}), 400
    except AssertionError as e:
        return jsonify({"error": str(e)}), 400