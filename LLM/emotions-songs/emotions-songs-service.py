from flask import Flask, request, jsonify
import numpy as np
import requests

app = Flask(__name__)

OLLAMA_URL = "http://ollama-service:11434/api/embeddings"
OLLAMA_MODEL = "nomic-embed-text"

@app.route("/emotionsSongs", methods=["POST"])
def emotionsSongs():
    songs = request.json

    if not songs or not isinstance(songs, list):
        return jsonify({"error": "Formato incorrecto, se espera una lista de canciones"}), 400

    results = []
    for song in songs:
        songname = song.get("songname")
        emotion = song.get("emotions")

        if not songname or not emotion:
            return jsonify({"error": "Cada entrada debe tener 'songname' y 'emotions'"}), 400

        embedding, error = obtener_embedding(emotion)
        if embedding is None:
            return jsonify({"error": error}), 500

        results.append({"songname": songname, "emotions_embedding": embedding.tolist()})

    return jsonify(results)

def obtener_embedding(texto):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "prompt": texto},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        embedding = np.array(response.json()["embedding"])
        return embedding, None
    except Exception as e:
        return None, f"Error al obtener el embedding desde Ollama: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5013)