from flask import Blueprint, request, jsonify

# Crear un blueprint para las rutas
main_routes = Blueprint('main', __name__)

# Ruta para crear datos (POST)
@main_routes.route('/create', methods=['POST'])
def create_data():
    data = request.get_json()  # Obtenemos los datos JSON que vienen en la solicitud
    if not data:
        return jsonify({"error": "No data provided"}), 400  # Si no hay datos, respondemos con error 400
    
    # Aquí normalmente guardarías los datos en la base de datos
    # En este ejemplo, solo los vamos a devolver como confirmación
    return jsonify({"message": "Data created", "data": data}), 201

# Ruta para obtener datos (GET)
@main_routes.route('/get', methods=['GET'])
def get_data():
    # Aquí normalmente consultarías los datos desde la base de datos
    # Para el ejemplo, vamos a devolver datos simulados
    sample_data = {
        "temperature": 22.5,
        "humidity": 60
    }
    return jsonify({"data": sample_data}), 200
