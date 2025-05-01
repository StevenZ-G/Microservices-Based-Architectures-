from flask import Flask, request, jsonify
import os
import openai
import numpy as np

# Configurar la API Key de OpenAI
openai.api_key = "sk-proj-CkPMCwKCI532qRmbD7k0T3BlbkFJZzepifI760gMZo5GpDto"
app = Flask(__name__)

@app.route("/recommendation", methods=["GET"])
def recommendation():
    
    # Obtener los embeddings de las canciones y las emociones
    data = request.json
    embeddingEmotion = data.get('emotion')  # Embedding de la emoción del usuario
    embeddingCanciones = data.get('emotions')  # Lista de canciones con sus embeddings

    if not embeddingCanciones or not embeddingEmotion:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400
    
    def calcular_similitud(embeddingCanciones, embeddingEmotion):
        # Función de similitud del coseno
        return np.dot(embeddingCanciones, embeddingEmotion) / (np.linalg.norm(embeddingCanciones) * np.linalg.norm(embeddingEmotion))
    
    # Encontrar la canción más similar a la emoción del usuario
    cancion_recomendada = max(embeddingCanciones, key=lambda c: calcular_similitud(c['emotions_embedding'], embeddingEmotion))

    # Devolver la canción recomendada
    return jsonify({"recommendation": cancion_recomendada})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5014)