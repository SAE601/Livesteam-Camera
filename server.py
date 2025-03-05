import os
import sys
import subprocess
from flask import Flask, send_from_directory
from flask_cors import CORS
import time
import threading
import signal
import json

import mysql.connector



unix_like_flag = sys.platform.startswith('linux')

# _______________________________________________________
# Configurations variables
configuration_filename = "./config.json"

# Load configuration
configJSON = {}
if os.path.exists(configuration_filename) and os.path.getsize(configuration_filename) > 0:  # Check if the file exists and is not empty
    try:
        with open(configuration_filename, "r", encoding="utf-8") as cFile:
            configJSON = json.load(cFile)
        print("JSON file successfully loaded:", configJSON)
    except json.JSONDecodeError:
        print("[ERROR]: The file contains invalid JSON.")
        exit(-1)
else:
    print("[ERROR]: The file is empty or does not exist.")
    exit(-1)

video_device = configJSON["video_device"]
video_format = configJSON["video_format"]
stream_output_file = f'{configJSON["base_directory"]}/{configJSON["stream_output_file"]}'
stream_output_directory = f'{configJSON["base_directory"]}/{configJSON["stream_output_directory"]}'
images_output_directory = f'{configJSON["base_directory"]}/{configJSON["images_output_directory"]}'

image_period = configJSON["image_period"]



if unix_like_flag:
    stream_script_path = f'{configJSON["base_directory"]}/{configJSON["script"]["linux"]["stream"]}'
    image_script_path = f'{configJSON["base_directory"]}/{configJSON["script"]["linux"]["image"]}'
    dimw_script_path = f'{configJSON["base_directory"]}/{configJSON["script"]["linux"]["dimw"]}'
else:
    stream_script_path = f'{configJSON["base_directory"]}\\{configJSON["script"]["win"]["stream"]}'
    image_script_path = f'{configJSON["base_directory"]}\\{configJSON["script"]["win"]["image"]}'

# _______________________________________________________
# Adapter le lancement suivant l'OS

# Verifier si l'OS est Linux
if unix_like_flag:
    print("[INFO] The script is running on a UNIX-like system.")
    print("[INFO] Starting the Dark Intergalactic Magic Wizard (DIMW)...")

    stdoutput_type = sys.stdout.buffer
    dimw_command = [
        dimw_script_path,
        video_device,
        video_format
    ]
    ffmpeg_process = subprocess.run(dimw_command, stdout=stdoutput_type, stderr=stdoutput_type)

    print("[INFO] Dark Intergalactic Magic Wizard successfully resolve the problem\n\n")
else:
    print("[INFO] The script is running on a non-Linux system.")

ffmpeg_process = None  # Pour stocker l'instance du processus FFmpeg
# _______________________________________________________
# Create working directory

if not os.path.exists(stream_output_directory):
    os.makedirs(stream_output_directory)

if not os.path.exists(images_output_directory):
    os.makedirs(images_output_directory)

# _______________________________________________________
# Fonction pour enregistrer l'image dans la base de données
def save_image_to_db(pathPicture, takenDate):
    conn = None
    try:
        # Connexion à la base de données
        conn = mysql.connector.connect(
            host=configJSON["bdd"]["host"],
            user=configJSON["bdd"]["user"],
            password=configJSON["bdd"]["password"],
            database=configJSON["bdd"]["database"],
        )
        cursor = conn.cursor()

        # Requête SQL pour insérer l'image
        query = "INSERT INTO Picture (pathPicture, takenDate) VALUES (%s, %s)"
        values = (pathPicture, takenDate)

        # Exécution de la requête
        cursor.execute(query, values)
        conn.commit()  # Valider la transaction

        print(f"[INFO] Image enregistrée dans la base de données : {pathPicture}")

    except mysql.connector.Error as err:
        print(f"[ERREUR] Erreur lors de l'insertion dans la base de données : {err}")

    finally:
        # Fermer la connexion
        if conn != None and conn.is_connected():
            cursor.close()
            conn.close()

# _______________________________________________________
# SERVER STREAMING HTTP
app = Flask(__name__)

# Activer CORS pour toutes les origines pour permettre d'acceder au stream
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/livestream/stream/<path:filename>')
def serve_video(filename):
    return send_from_directory(stream_output_directory, filename)

# _______________________________________________________
# STREAMING VIDEO

# Fonction pour lancer FFmpeg en mode daemon pour le streaming
def start_ffmpeg_stream():
    global ffmpeg_process
    print("[INFO] Start ffmpeg")

    ffmpeg_command = [
        stream_script_path,
        video_device,
        stream_output_file
    ]

    stdoutput_type = sys.stdout.buffer
    ffmpeg_process = subprocess.Popen(ffmpeg_command, stdout=stdoutput_type, stderr=stdoutput_type)

# Fonction pour capturer une image toutes les x secondes
def capture_image():
    while True:
        # Recuperer le dernier fichier .ts genere pour capturer l'image
        ts_files = [f for f in os.listdir(stream_output_directory) if f.endswith('.ts')]

        if ts_files:
            # Trouver le fichier .ts le plus recent
            ts_file = max(ts_files, key=lambda f: os.path.getmtime(f'{stream_output_directory}/{f}'))

            # Generer un nom d'image avec timestamp
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            output_img = os.path.join(images_output_directory, f'output_{timestamp}.jpg')

            # Executer la commande FFmpeg pour capturer l'image
            acquire_img_command = [
                image_script_path,
                stream_output_directory + "/" + ts_file,
                output_img
            ]
            subprocess.Popen(acquire_img_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f'[INFO] Image capturee et sauvegardee sous {output_img}')

            # Enregistrer l'image dans la base de données
            save_image_to_db(output_img, time.strftime('%Y-%m-%d %H:%M:%S'))

        time.sleep(image_period)

# Fonction pour fermer FFmpeg proprement lors de l'arrêt du serveur
def shutdown_ffmpeg(signum, frame):
    global ffmpeg_process
    if ffmpeg_process:
        print("[INFO] Interruption reçue, arrêt du processus FFmpeg")
        ffmpeg_process.terminate()  # Terminer FFmpeg
        ffmpeg_process.wait()  # Attendre la fin du processus FFmpeg
    sys.exit(0)  # Quitter proprement le programme

# _______________________________________________________
# MAIN FUNCTION
if __name__ == '__main__':
    # Attacher le signal SIGINT (CTRL+C) pour fermer proprement FFmpeg
    signal.signal(signal.SIGINT, shutdown_ffmpeg)

    # Demarrer FFmpeg en mode daemon
    start_ffmpeg_stream()

    # Lancer la capture d'images dans un thread separe
    image_capture_thread = threading.Thread(target=capture_image, daemon=True)
    image_capture_thread.start()

    # Lancer le serveur Flask
    app.run(host='0.0.0.0', port=5000)
