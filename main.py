from app import create_app, socketio
import datetime  # Importar para agregar un timestamp

# Crear la aplicación Flask
app = create_app()

# Configurar SocketIO
# socketio ya está configurado en el archivo __init__.py

# Ruta principal
@app.route('/')
def index():
    return "API con WebSockets en tiempo real"

# Evento para recibir datos del cliente (como el sensor de temperatura y humedad)
@socketio.on('send_data')
def handle_sensor_data(data):
    print(f"Datos recibidos del sensor: {data}")
    
    # Agregar un timestamp
    timestamp = datetime.datetime.now().isoformat()

    # Realizar un pequeño ajuste a la temperatura (por ejemplo, aumentarla en 1 grado)
    processed_data = {
        'temperature': data['temperature'],  # Ejemplo: aumentar la temperatura en 1.0
        'humidity': data['humidity'],
        'timestamp': timestamp  # Incluir timestamp
    }
    
    # Emitir los datos procesados a todos los clientes conectados
    socketio.emit('receive_data', processed_data)

# Ejecutar la aplicación con WebSockets
if __name__ == "__main__":
    # Cambia la configuración para que Flask escuche en todas las interfaces de red
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
