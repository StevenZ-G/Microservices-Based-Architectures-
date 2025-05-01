from flask import Flask, request, jsonify
import requests
import os
import openai
import numpy as np

# Configurar la API Key de OpenAI
openai.api_key = "sk-proj-CkPMCwKCI532qRmbD7k0T3BlbkFJZzepifI760gMZo5GpDto"


app = Flask(__name__)

@app.route("/emotionsSongs", methods=["POST"])  # Cambia a POST
def emotionsSongs():
    songs = request.json  # Se espera una lista de diccionarios

    if not songs or not isinstance(songs, list):
        return jsonify({"error": "Formato incorrecto, se espera una lista de canciones"}), 400

    def obtener_embedding(texto):
        try:
            respuesta = openai.embeddings.create(
                model="text-embedding-ada-002", 
                input=texto
            )
            embedding = np.array(respuesta.data[0].embedding)
            return embedding, None
        except Exception as e:
            return None, f"Error al obtener el embedding: {str(e)}"

    results = []
    for song in songs:
        songname = song.get("songname")
        emotion = song.get("emotions")

        if not songname or not emotion:
            return jsonify({"error": "Cada entrada debe tener 'songname' y 'emotions'"}), 400

        embedding, error = obtener_embedding(emotion)
        if error:
            return jsonify({"error": error}), 500

        results.append({"songname": songname, "emotions_embedding": embedding.tolist()})

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5013)