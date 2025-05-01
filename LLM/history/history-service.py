from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Definir la ruta del volumen compartido en Kubernetes
DB_PATH = os.getenv("DB_PATH", "/llm/data/system.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
db = SQLAlchemy(app)

# Modelos
class User(db.Model):
    __tablename__ = 'User'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    
    # Relación con el historial (opcional)
    history = db.relationship('History', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Song(db.Model):
    __tablename__ = 'Songs'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    songname = db.Column(db.String, nullable=False)
    album = db.Column(db.String, nullable=False)
    emotions = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)
    
    # Relación con el historial (opcional)
    history = db.relationship('History', backref='song', lazy=True)
    
    def __repr__(self):
        return f'<Song {self.songname} from {self.album}>'

class History(db.Model):
    __tablename__ = 'history'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('Songs.id'), nullable=False)
    date = db.Column(db.Date, server_default=db.func.current_date())
    
    def __repr__(self):
        return f'<History user:{self.user_id} song:{self.song_id} date:{self.date}>'

@app.route("/getHistory", methods=["GET"])
def get_history():
    history_records = History.query.all()
    history_list = [{
        "user_id": record.user_id,
        "song_id": record.song_id,
        "date": record.date.isoformat() if record.date else None
    } for record in history_records]
    return jsonify(history_list)

@app.route("/getHistorybyUser", methods=["GET"])
def get_history_by_user():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id es requerido"}), 400
    records = History.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "user_id": record.user_id,
        "song_id": record.song_id,
        "date": record.date.isoformat() if record.date else None
    } for record in records])

@app.route("/getHistorybySong", methods=["GET"])
def get_history_by_song():
    song_id = request.args.get("song_id")
    if not song_id:
        return jsonify({"error": "song_id es requerido"}), 400
    records = History.query.filter_by(song_id=song_id).all()
    return jsonify([{
        "user_id": record.user_id,
        "song_id": record.song_id,
        "date": record.date.isoformat() if record.date else None
    } for record in records])

@app.route("/getMostListened", methods=["GET"])
def get_most_listened():
    records = History.query.all()
    songs = [record.song_id for record in records]
    if not songs:
        return jsonify({"error": "No hay registros"}), 404
    most_listened = max(set(songs), key=songs.count)
    return jsonify({"song_id": most_listened})

@app.route("/getMostListenedbyUser", methods=["GET"])
def get_most_listened_by_user():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id es requerido"}), 400
    records = History.query.filter_by(user_id=user_id).all()
    songs = [record.song_id for record in records]
    if not songs:
        return jsonify({"error": "No hay registros para este usuario"}), 404
    most_listened = max(set(songs), key=songs.count)
    return jsonify({"song_id": most_listened})

@app.route("/getMostListenedbySong", methods=["GET"])
def get_most_listened_by_song():
    song_id = request.args.get("song_id")
    if not song_id:
        return jsonify({"error": "song_id es requerido"}), 400
    records = History.query.filter_by(song_id=song_id).all()
    users = [record.user_id for record in records]
    if not users:
        return jsonify({"error": "No hay registros para esta canción"}), 404
    most_listened = max(set(users), key=users.count)
    return jsonify({"user_id": most_listened})

@app.route("/addHistory", methods=["POST"])
def add_history():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se proporcionaron datos"}), 400

        try:
            user_id = int(data.get("user_id"))
            song_id = int(data.get("song_id"))
        except (TypeError, ValueError):
            return jsonify({"error": "user_id y song_id deben ser números enteros"}), 400

        # Verificar que existan el usuario y la canción
        if not User.query.get(user_id):
            return jsonify({"error": f"Usuario con id {user_id} no existe"}), 404
        if not Song.query.get(song_id):
            return jsonify({"error": f"Canción con id {song_id} no existe"}), 404

        new_record = History(user_id=user_id, song_id=song_id)
        db.session.add(new_record)
        db.session.commit()
        return jsonify({"message": "Historial añadido exitosamente"}), 201

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error en add_history: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5015)
