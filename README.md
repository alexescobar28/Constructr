# Constructr
#instalar 
pip install flask
#desde el terminal 
python run.py
# Agregar producto
curl -X POST http://localhost:5000/producto \
-H "Content-Type: application/json" \
-d '{"id": 1, "nombre": "Laptop", "cantidad": 10}'

# Consultar producto
curl http://localhost:5000/producto/1

# Actualizar stock
curl -X PUT http://localhost:5000/producto/1 \
-H "Content-Type: application/json" \
-d '{"cantidad": 20}'
