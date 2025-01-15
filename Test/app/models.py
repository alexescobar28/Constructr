import sqlite3
from dataclasses import dataclass
from typing import Tuple, Dict, Union

@dataclass
class Producto:
    id: int
    nombre: str
    cantidad: int

def init_db():
    """Inicializa la base de datos con una tabla de productos"""
    conn = sqlite3.connect('instance/inventario.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS productos
        (id INTEGER PRIMARY KEY, nombre TEXT, cantidad INTEGER)
    ''')
    conn.commit()
    conn.close()

def consultar_producto(id_producto: int) -> Tuple[Dict[str, Union[str, int]], int]:
    try:
        conn = sqlite3.connect('instance/inventario.db')
        c = conn.cursor()
        c.execute('SELECT * FROM productos WHERE id = ?', (id_producto,))
        producto = c.fetchone()
        conn.close()

        if producto:
            return {"id": producto[0], "nombre": producto[1], "cantidad": producto[2]}, 200
        return {"error": "Producto no encontrado"}, 404
    except Exception as e:
        return {"error": f"Error en la base de datos: {str(e)}"}, 500

# app/validators.py
from functools import wraps
from flask import jsonify

def validar_id(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            id_producto = kwargs.get('id_producto') or args[0]
            if not isinstance(id_producto, int) or id_producto <= 0:
                return jsonify({"error": "ID de producto debe ser un número entero positivo"}), 400
        except (ValueError, TypeError):
            return jsonify({"error": "ID de producto inválido"}), 400
        return func(*args, **kwargs)
    return wrapper