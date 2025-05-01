from flask import Flask, request, jsonify
import tensorflow as tf
import os

app = Flask(__name__)

@app.route('/preprocess', methods=['POST'])
def preprocess():
    """
    Recibe una imagen, la decodifica y la redimensiona a [32, 32].
    Retorna el resultado procesado.
    """
    try:
        # Verificar que se haya enviado una imagen
        if 'image' not in request.files:
            return jsonify({'error': "No se proporcionó ninguna imagen."}), 400

        # Leer la imagen del request
        image_file = request.files['image'].read()

        # Decodificar la imagen
        image = tf.image.decode_image(image_file, channels=3)

        # Redimensionar la imagen a [32, 32]
        image = tf.image.resize(image, [32, 32])

        # Convertir la imagen a un array serializable (ejemplo: lista anidada)
        image_array = image.numpy().tolist()

        # Retornar la imagen procesada
        return jsonify({'features': image_array}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
