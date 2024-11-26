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


# Servicio de orquestación para coordinar los microservicios
@app.route('/orchestrate', methods=['POST'])
@app.route('/orchestrate', methods=['POST'])
def orchestrate():
    try:
        # Paso 1: Recolectar los datos
        data = request.json
        collected_response = requests.post(DATA_COLLECTOR_URL, json=data)
        collected_response.raise_for_status()  # Verificar si hay errores HTTP
        collected_data = collected_response.json()
        
        # Paso 2: Preprocesar los datos
        preprocessed_response = requests.post(DATA_HANDLER_URL, json=collected_data)
        preprocessed_response.raise_for_status()
        preprocessed_data = preprocessed_response.json()
        
        # Paso 3: Extraer características
        features_response = requests.post(FEATURE_EXTRACTION_URL, json=preprocessed_data)
        features_response.raise_for_status()
        features = features_response.json()
        
        # Paso 4: Hacer la predicción
        prediction_response = requests.post(PREDICT_SERVICE_URL, json=features)
        prediction_response.raise_for_status()
        prediction = prediction_response.json()
        
        return jsonify({"prediction": prediction}), 200

    except requests.exceptions.HTTPError as errh:
        return jsonify({"error": f"Http Error: {errh}"}), 500
    except requests.exceptions.ConnectionError as errc:
        return jsonify({"error": f"Error Connecting: {errc}"}), 500
    except requests.exceptions.Timeout as errt:
        return jsonify({"error": f"Timeout Error: {errt}"}), 500
    except requests.exceptions.RequestException as err:
        return jsonify({"error": f"Something went wrong: {err}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
    