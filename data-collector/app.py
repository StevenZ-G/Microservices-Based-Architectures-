from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Ruta al volumen compartido
VOLUME_PATH = "/mnt/data"
IMAGES_DIR = os.path.join(VOLUME_PATH, "images")

# Crear el directorio para guardar imágenes si no existe
os.makedirs(IMAGES_DIR, exist_ok=True)

@app.route('/collect', methods=['POST'])
def collect_data():
    """
    Recibe una imagen y la guarda en el directorio compartido.
    """
    try:
        # Verificar que se haya enviado una imagen
        if 'image' not in request.files:
            return jsonify({'error': "No se proporcionó ninguna imagen."}), 400

        # Leer la imagen del request
        image_file = request.files['image']

        # Generar un nombre único para la imagen
        image_filename = image_file.filename
        image_path = os.path.join(IMAGES_DIR, image_filename)

        # Guardar la imagen en el directorio compartido
        image_file.save(image_path)

        # Retornar respuesta exitosa con la ruta de la imagen
        return jsonify({'message': "Imagen guardada correctamente.", 'path': image_path}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
