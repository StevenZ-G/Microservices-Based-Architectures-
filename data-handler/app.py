from flask import Flask, request, jsonify

app = Flask(__name__)

# Función de preprocesamiento
def preprocess_data(data):
    # Aquí puedes agregar lógica de preprocesamiento, por ejemplo:
    cleaned_data = {key: value.strip().lower() if isinstance(value, str) else value for key, value in data.items()}
    return cleaned_data

# Ruta para manejar los datos
@app.route('/preprocess', methods=['POST'])
def preprocess():
    data = request.json  # Recibe los datos en formato JSON
    cleaned_data = preprocess_data(data)  # Aplica el preprocesamiento
    return jsonify(cleaned_data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
