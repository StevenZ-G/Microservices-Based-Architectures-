from flask import Flask, request, jsonify
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Definir la ruta del volumen compartido en Kubernetes
DB_PATH = os.getenv("DB_PATH", "/llm/data/system.db")
#DB_PATH = os.getenv("DB_PATH", "C:/Users/User/TesisLLM/system.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
db = SQLAlchemy(app)

# Configuración de los microservicios

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    
    if not username or not email or not password:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400
    
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "El usuario ya existe"}), 400
    
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "Usuario registrado exitosamente"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    
    user = User.query.filter_by(email=email, password=password).first()
    if not user:
        return jsonify({"error": "Credenciales incorrectas"}), 401
    
    return jsonify({"message": "Inicio de sesión exitoso"})

if __name__ == "__main__":
    os.makedirs("/data", exist_ok=True)  # Asegurar que el directorio exista
    app.run(host="0.0.0.0", port=5010, debug=True)
