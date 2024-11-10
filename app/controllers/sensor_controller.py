from flask import Blueprint, request, jsonify
from bson import ObjectId  # Importar para manejar ObjectId
from app import mongo, socketio  # Importamos socketio para poder emitir eventos
import datetime  # Para agregar un timestamp

# Crear un Blueprint para las rutas del controlador de sensores
sensor_bp = Blueprint('sensor', __name__)

# Ruta para obtener todos los datos de los sensores (GET)
@sensor_bp.route('/sensor', methods=['GET'])
def get_sensors():
    sensors = mongo.db.sensors.find()
    sensors_list = []
    
    for sensor in sensors:
        sensor_data = {
            'temperature': sensor.get('temperature'),
            'humidity': sensor.get('humidity'),
            '_id': str(sensor['_id']),  # Convertir el ObjectId a string para poder devolverlo en JSON
            'timestamp': sensor.get('timestamp')  # Incluir el timestamp en la respuesta
        }
        sensors_list.append(sensor_data)
    
    return jsonify(sensors_list), 200

# Ruta para crear varios sensores (POST)
@sensor_bp.route('/sensor/create', methods=['POST'])
def create_sensor():
    data = request.get_json()  # Obtener los datos JSON enviados en el cuerpo de la solicitud

    if not isinstance(data, list):  # Verificar que los datos sean una lista
        return jsonify({"message": "Data must be an array of sensors"}), 400

    # Validación de cada sensor
    for sensor in data:
        temperature = sensor.get('temperature')
        humidity = sensor.get('humidity')

        if not temperature or not humidity:
            return jsonify({"message": "Temperature and humidity are required for each sensor"}), 400

    # Agregar timestamp al crear el sensor
    for sensor in data:
        sensor['timestamp'] = datetime.datetime.now().isoformat()

    # Insertar los datos en la base de datos MongoDB
    result = mongo.db.sensors.insert_many(data)

    # Convertir ObjectIds a strings
    inserted_ids = [str(id) for id in result.inserted_ids]

    # Emitir un evento a los clientes conectados con la información de los nuevos sensores
    socketio.emit('new_sensor_data', {'sensors': data})  # Emite los datos de los sensores recién creados a todos los clientes

    return jsonify({"message": f"{len(data)} sensors created successfully", "inserted_ids": inserted_ids}), 201
