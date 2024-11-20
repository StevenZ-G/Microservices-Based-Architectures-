from flask import Flask, request, jsonify

app = Flask(__name__)

# Modelo basado en reglas simples para la clasificación
def rule_based_model(features):
    # Reglas condicionales en base a las características
    name_length = features.get('name_length', 0)
    age_square = features.get('age_square', 0)
    age_half = features.get('age_half', 0)

    # Reglas simples para clasificación
    if name_length > 10 and age_square > 400:
        return 1  # Clase positiva
    elif name_length <= 10 and age_half < 20:
        return 0  # Clase negativa
    else:
        # Clasificación basada en reglas adicionales
        if name_length > 5 and age_half > 10:
            return 1  # Clase positiva
        else:
            return 0  # Clase negativa

# Ruta para realizar predicciones
@app.route('/predict', methods=['POST'])
def predict():
    features = request.json  # Recibe las características
    prediction = rule_based_model(features)  # Realiza la predicción usando reglas
    return jsonify({"prediction": prediction}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
