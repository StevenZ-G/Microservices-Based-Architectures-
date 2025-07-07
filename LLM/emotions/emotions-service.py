from flask import Flask, request, jsonify
import numpy as np
import requests

app = Flask(__name__)

OLLAMA_URL = "http://ollama-service:11434/api/embeddings"
OLLAMA_MODEL = "nomic-embed-text"

@app.route("/emotions", methods=["POST"])
def emotions():
    data = request.json
    text = data.get("text")
    if not text:
        return jsonify({"error": "El campo 'text' es obligatorio"}), 400

    embedding, error = obtener_embedding(text)
    if embedding is None:
        return jsonify({"error": error}), 500

    return jsonify({"emotion": embedding.tolist()})

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
    app.run(host='0.0.0.0', port=5011)
