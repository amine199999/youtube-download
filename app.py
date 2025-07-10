from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import yt_dlp
import os
import uuid

app = Flask(__name__)
CORS(app)

DOSSIER_VIDEOS = "videos"
os.makedirs(DOSSIER_VIDEOS, exist_ok=True)


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route('/telecharger', methods=['POST'])
def telecharger():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL manquante"}), 400

    try:
        nom_fichier = str(uuid.uuid4()) + ".mp4"
        chemin = os.path.join(DOSSIER_VIDEOS, nom_fichier)

        ydl_opts = {
            'format': '22/18/best',
            'outtmpl': chemin,
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return jsonify({
            "message": "Téléchargement terminé",
            "lien": f"/video/{nom_fichier}"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/video/<nom_fichier>')
def servir_video(nom_fichier):
    return send_from_directory(DOSSIER_VIDEOS, nom_fichier, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)








