from flask import Flask, request, jsonify

app = Flask(__name__)

# Ruta para recolectar datos
@app.route('/collect', methods=['POST'])
def collect_data():
    data = request.json  # Recibe el dato enviado como JSON
    # Aquí podrías almacenar el dato o pasarlo a otro servicio
    print(f"Data collected: {data}")
    return jsonify({"message": "Data collected successfully"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
