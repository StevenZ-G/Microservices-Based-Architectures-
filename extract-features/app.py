from flask import Flask, request, jsonify

app = Flask(__name__)

# Método personalizado para calcular características
def custom_feature_extraction(data):
    features = {}
    for key, value in data.items():
        # Si el valor es un texto, calculamos longitud, número de palabras, etc.
        if isinstance(value, str):
            features[key + '_length'] = len(value)  # Longitud del texto
            features[key + '_word_count'] = len(value.split())  # Número de palabras
        # Si es un número, realizamos algunas operaciones simples
        elif isinstance(value, (int, float)):
            features[key + '_square'] = value ** 2  # Cuadrado del número
            features[key + '_half'] = value / 2  # La mitad del número
        # Para otro tipo de datos, podemos definir más reglas
        else:
            features[key] = value
    return features

# Ruta para extraer las características
@app.route('/extract', methods=['POST'])
def extract():
    data = request.json  # Recibe los datos preprocesados
    features = custom_feature_extraction(data)  # Extrae las características
    return jsonify(features), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
