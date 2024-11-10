from flask import Flask
from flask_pymongo import PyMongo
from flask_socketio import SocketIO  # Importamos SocketIO
from .config import Config

# Creamos las instancias de PyMongo y SocketIO
mongo = PyMongo()
socketio = SocketIO()  # Inicializamos SocketIO

def create_app():
    # Inicializar la aplicación Flask
    app = Flask(__name__)
    
    # Cargar la configuración desde el objeto Config
    app.config.from_object(Config)

    # Inicializar MongoDB con la aplicación Flask
    mongo.init_app(app)

    # Inicializar SocketIO con la aplicación Flask
    socketio.init_app(app)

    # Registrar las rutas o Blueprints aquí
    from .controllers.sensor_controller import sensor_bp  # Asegúrate de que esta ruta existe y está bien estructurada
    app.register_blueprint(sensor_bp)

    return app
