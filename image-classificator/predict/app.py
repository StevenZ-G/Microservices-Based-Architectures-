from flask import Flask, request, jsonify
import tensorflow as tf
import os

app = Flask(__name__)

# Ruta al modelo en el volumen compartido
MODEL_PATH = "/mnt/data/image_recognition_model"

# Cargar el modelo en formato SavedModel
try:
    model = tf.saved_model.load(MODEL_PATH)
    infer = model.signatures['serving_default']  # Obtener la firma predeterminada
    print(f"Modelo cargado correctamente desde {MODEL_PATH}")
except Exception as e:
    print(f"Error al cargar el modelo: {e}")
    model, infer = None, None  # Establecer como None si ocurre un error

@app.route('/health', methods=['GET'])
def health_check():
    """
    Verifica si el modelo está cargado correctamente.
    """
    if infer is None:
        return jsonify({"status": "error", "details": "El modelo no está cargado correctamente."}), 500
    return jsonify({"status": "ok"}), 200

@app.route('/predict', methods=['POST'])
def predict():
    """
    Realiza predicciones basadas en un conjunto de características.
    """
    try:
        if infer is None:
            return jsonify({"error": "El modelo no está cargado correctamente."}), 500

        # Leer las características desde la solicitud
        data = request.json
        features = data.get('features')

        if features is None:
            return jsonify({"error": "No se proporcionaron características."}), 400

        # Convertir las características en un tensor adecuado para el modelo
        input_tensor = tf.convert_to_tensor([features], dtype=tf.float32)

        # Realizar la predicción
        predictions = infer(conv2d_input=input_tensor)

        # Obtener la clase predicha
        predicted_class = tf.argmax(predictions['dense_1'], axis=1).numpy().item()

        return jsonify({"class": int(predicted_class)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
