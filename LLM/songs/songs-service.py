from flask import Flask, request, jsonify
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)

# Definir la ruta del volumen compartido en Kubernetes
DB_PATH = os.getenv("DB_PATH", "/llm/data/system.db")
#DB_PATH = os.getenv("DB_PATH", "C:/Users/User/TesisLLM/system.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
db = SQLAlchemy(app)

class Songs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    songname = db.Column(db.String(80), unique=True, nullable=False)
    album = db.Column(db.String(120), unique=False, nullable=False)
    emotions = db.Column(db.String(200), nullable=False)
    link = db.Column(db.String(200), nullable=False)

@app.route("/getSongsEmotions", methods=["GET"])
def getSongsEmotions():
    songs = Songs.query.all()
    return jsonify([{"songname": song.songname, "emotions": song.emotions} for song in songs])

@app.route("/getSongs", methods=["GET"])
def getSongs():
    songs = Songs.query.all()
    return jsonify([{"songname": song.songname} for song in songs])

@app.route("/getLink", methods=["GET"])
def getLink():
    songname = request.args.get("songname")
    song = Songs.query.filter_by(songname=songname).first()
    return jsonify({"link": song.link})

@app.route("/getSongById", methods=["GET"])
def getSongById():
    id = request.args.get("id")
    song = Songs.query.filter_by(id=id).first()

    if not song:
        return jsonify({"error": "Song not found"}), 404
    
    return jsonify({"song_id": song.id, "songname": song.songname, "link": song.link})

@app.route("/getLinkByName", methods=["GET"])
def getLinkByName():
    songname = request.args.get("songname")
    song = Songs.query.filter_by(songname=songname).first()

    if not song:
        return jsonify({"error": "Song not found"}), 404

    return jsonify({"link": song.link})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5012)