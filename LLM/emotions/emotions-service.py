# Este es el código del servicio de emociones que se encarga de recibir un texto y devolver un vector de emociones.
from flask import Flask, request, jsonify
import os
import openai
import numpy as np

# Configurar la API Key de OpenAI
app = Flask(__name__)
openai.api_key = "sk-proj-CkPMCwKCI532qRmbD7k0T3BlbkFJZzepifI760gMZo5GpDto"
print("API Key de OpenAI configurada correctamente")

@app.route("/emotions", methods=["POST"])
def emotions():
    data = request.json
    text = data.get("text")
    if not text:
        return jsonify({"error": "El campo 'text' es obligatorio"}), 400

    def obtener_embedding(texto):
        try:
            respuesta = openai.embeddings.create(
                model="text-embedding-ada-002", 
                input=texto
            )
            embedding = np.array(respuesta.data[0].embedding)
            return embedding, None  # ✅ Devuelve el embedding y None como error
        except Exception as e:
            return None, f"Error al obtener el embedding: {str(e)}"

    # ✅ Ahora obtenemos los dos valores correctamente
    emotion, error = obtener_embedding(text)

    if emotion is None:
        return jsonify({"error": error}), 500

    return jsonify({"emotion": emotion.tolist()})  # ✅ Convertimos ndarray a lista

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5011)