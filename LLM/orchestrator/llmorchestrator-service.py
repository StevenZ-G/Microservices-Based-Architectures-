from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Microservices URLs
USER_REGISTER_API_URL = "http://user-interface-service:5010/user/register"
USER_LOGIN_API_URL = "http://user-interface-service:5010/user/login"
EMOTION_API_URL = "http://emotions-service:5011/emotions"
SONG_API_URL = "http://songs-service:5012/getSongsEmotions"
EMOTION_SONG_API_URL = "http://emotions-songs-service:5013/emotionsSongs"
RECOMMENDATION_API_URL = "http://recommendations-service:5014/recommendation"
HISTORY_ADD_API_URL = "http://history-service:5015/addHistory"

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200

@app.route('/orchestrate', methods=['POST'])
def orchestrate():
    data = request.json
    user_id = data.get("user_id")
    user_emotion = data.get("emotion")

    if not user_id or not user_emotion:
        return jsonify({"error": "user_id y emotion son obligatorios"}), 400

    # Paso 1: Obtener emoción embebida del usuario
    try:
        emotion_response = requests.post(EMOTION_API_URL, json={"text": user_emotion})
        emotion_response.raise_for_status()
        emotion_embedding = emotion_response.json()["emotion"]
    except Exception as e:
        return jsonify({"error": f"Error obteniendo embedding de emoción: {str(e)}"}), 500

    # Paso 2: Obtener canciones y emociones asociadas
    try:
        songs_response = requests.get(SONG_API_URL)
        songs_response.raise_for_status()
        canciones = songs_response.json()
    except Exception as e:
        return jsonify({"error": f"Error obteniendo canciones: {str(e)}"}), 500

    # Paso 3: Obtener embeddings de emociones de las canciones
    try:
        emotion_songs_response = requests.post(EMOTION_SONG_API_URL, json=canciones)
        emotion_songs_response.raise_for_status()
        canciones_con_embedding = emotion_songs_response.json()
    except Exception as e:
        return jsonify({"error": f"Error obteniendo embeddings de canciones: {str(e)}"}), 500

    # Paso 4: Obtener la canción recomendada
    try:
        recommendation_response = requests.get(RECOMMENDATION_API_URL, json={
            "emotion": emotion_embedding,
            "emotions": canciones_con_embedding
        })
        recommendation_response.raise_for_status()
        recommended_song = recommendation_response.json()["recommendation"]
    except Exception as e:
        return jsonify({"error": f"Error obteniendo recomendación: {str(e)}"}), 500

    # Paso 5: Registrar recomendación en historial
    # try:
    #     history_response = requests.post(HISTORY_ADD_API_URL, json={
    #         "user_id": user_id,
    #         "song_id": recommended_song["songname"]  # Aquí asumo que `songname` es el ID, corrige si es un campo distinto
    #     })
    #     history_response.raise_for_status()
    # except Exception as e:
    #     return jsonify({"error": f"Error registrando en historial: {str(e)}"}), 500

    return jsonify({"recommendation": recommended_song}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5016)
