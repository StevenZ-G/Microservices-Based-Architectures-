from flask import Flask, render_template, request, jsonify
import requests
import base64  # Importar módulo base64

app = Flask(__name__)

# URL del orquestador
ORCHESTRATOR_URL = "http://localhost:5004/orchestrate"

# Diccionario para mapear las clases
CLASS_LABELS = {
    0: "Airplane", 1: "Automobile", 2: "Bird", 3: "Cat", 4: "Deer",
    5: "Dog", 6: "Frog", 7: "Horse", 8: "Ship", 9: "Truck"
}

@app.route("/", methods=["GET", "POST"])
def index():
    image_url = None  # Variable para almacenar la imagen en base64
    if request.method == "POST":
        if "image" not in request.files:
            return render_template("index.html", error="No se seleccionó ninguna imagen.")

        image_file = request.files["image"]

        # Convertir la imagen a Base64 para mostrarla después de la predicción
        image_bytes = image_file.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        image_url = f"data:image/jpeg;base64,{image_base64}"

        try:
            # Enviar la imagen al orquestador
            response = requests.post(ORCHESTRATOR_URL, files={"image": (image_file.filename, image_bytes, image_file.mimetype)})
            response_data = response.json()

            if response.status_code == 200:
                class_id = response_data.get("prediction", {}).get("class")
                predicted_label = CLASS_LABELS.get(class_id, "Clase desconocida")
                return render_template("index.html", prediction=predicted_label, image_url=image_url)
            else:
                return render_template("index.html", error=response_data.get("error", "Error desconocido."), image_url=image_url)

        except requests.exceptions.RequestException as e:
            return render_template("index.html", error=f"Error al conectar con el orquestador: {str(e)}", image_url=image_url)

    return render_template("index.html", image_url=image_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
