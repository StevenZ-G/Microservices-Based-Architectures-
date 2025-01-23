from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Direcciones de los otros microservicios (Localhost)
# DATA_COLLECTOR_URL = "http://localhost:5000/collect"
# DATA_HANDLER_URL = "http://localhost:5001/preprocess"
# FEATURE_EXTRACTION_URL = "http://localhost:5002/extract"
# PREDICT_SERVICE_URL = "http://localhost:5003/predict"


# Direcciones de los otros microservicios
DATA_COLLECTOR_URL = "http://data-collector-service:5000/collect"
DATA_HANDLER_URL = "http://data-handler-service:5001/preprocess"
FEATURE_EXTRACTION_URL = "http://feature-extraction-service:5002/extract"
PREDICT_SERVICE_URL = "http://predict-service:5003/predict"

# import os

# DATA_COLLECTOR_URL = os.getenv("DATA_COLLECTOR_URL")
# DATA_HANDLER_URL = os.getenv("DATA_HANDLER_URL")
# FEATURE_EXTRACTION_URL = os.getenv("FEATURE_EXTRACTION_URL")
# PREDICT_SERVICE_URL = os.getenv("PREDICT_SERVICE_URL")
# MODEL_FILE = os.getenv("MODEL_FILE")

@app.route('/health', methods=['GET'])
def health_check():
    """
    Verifica si el orquestador está operativo.
    """
    return jsonify({"status": "ok"}), 200

@app.route('/orchestrate', methods=['POST'])
def orchestrate():
    try:
        # Verificar que se haya enviado una imagen al orquestador
        if 'image' not in request.files:
            return jsonify({'error': "No se proporcionó ninguna imagen."}), 400

        # Paso 1: Enviar la imagen al microservicio de recolección
        image_file = request.files['image']
        collected_response = requests.post(DATA_COLLECTOR_URL, files={'image': image_file})
        collected_response.raise_for_status()
        collected_data = collected_response.json()

        # Paso 2: Extraer la ubicación de la imagen almacenada por el data-collector
        image_path = collected_data.get('path')
        if not image_path:
            return jsonify({'error': "El data-collector no devolvió la ubicación de la imagen."}), 500

        # Leer la imagen directamente del archivo para enviarla al data-handler
        with open(image_path, 'rb') as img:
            preprocessed_response = requests.post(DATA_HANDLER_URL, files={'image': img})
        preprocessed_response.raise_for_status()
        preprocessed_data = preprocessed_response.json()

        # Paso 3: Enviar directamente los datos preprocesados al microservicio de predicción
        features = preprocessed_data.get('features')  # Ajusta si el nombre de la clave es diferente
        if features is None:
            return jsonify({"error": "El data-handler no devolvió características procesadas."}), 500

        # Enviar las características al microservicio predict
        prediction_response = requests.post(PREDICT_SERVICE_URL, json={"features": features})
        prediction_response.raise_for_status()
        prediction = prediction_response.json()


        # Responder con la predicción final
        return jsonify({"prediction": prediction}), 200

    except requests.exceptions.HTTPError as http_err:
        return jsonify({"error": f"HTTP error occurred: {http_err}"}), 500
    except requests.exceptions.ConnectionError as conn_err:
        return jsonify({"error": f"Connection error occurred: {conn_err}"}), 500
    except requests.exceptions.Timeout as timeout_err:
        return jsonify({"error": f"Timeout error occurred: {timeout_err}"}), 500
    except requests.exceptions.RequestException as req_err:
        return jsonify({"error": f"An error occurred: {req_err}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
      
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
