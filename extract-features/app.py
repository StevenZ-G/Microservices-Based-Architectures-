from flask import Flask, request, jsonify
import tensorflow as tf

app = Flask(__name__)

@app.route('/extract', methods=['POST'])
def extract_features():
    try:
        # Leer los datos de la solicitud
        data = request.json
        processed_image = data.get('processed_image')

        if processed_image is None:
            return jsonify({'error': "La imagen procesada no fue proporcionada."}), 400

        # Convertir la imagen en un tensor
        image = tf.convert_to_tensor(processed_image, dtype=tf.float32)

        # Expandir la dimensión de la imagen a [1, 32, 32, 3]
        image = tf.expand_dims(image, 0)

        # Verificar la forma antes de retornar
        if image.shape != (1, 32, 32, 3):
            return jsonify({'error': f"La forma del tensor es incorrecta: {image.shape}"}), 500

        expanded_image = image.numpy().tolist()
        return jsonify({'expanded_image': expanded_image}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
