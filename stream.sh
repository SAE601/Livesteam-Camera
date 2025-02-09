#!/bin/bash

# Vérifie si deux arguments sont passés
if [ -z "$1" ]; then
    echo "[ERROR] Aucun périphérique vidéo spécifié."
    echo "Usage: $0 <périphérique_vidéo> <fichier_sortie>"
    exit 1
fi

if [ -z "$2" ]; then
    echo "[ERROR] Aucun fichier de sortie spécifié."
    echo "Usage: $0 <périphérique_vidéo> <fichier_sortie>"
    exit 1
fi

# Paramètres d'entrée
VIDEO_STREAM="$1"
OUTPUT_FILE="$2"
KEY_FRAME=50

# Affiche les informations d'entrée
echo "[INFO] Périphérique vidéo : $VIDEO_STREAM"
echo "[INFO] Fichier de sortie : $OUTPUT_FILE"

# Exécute FFmpeg pour le streaming
ffmpeg -f v4l2 -i "$VIDEO_STREAM" -g $KEY_FRAME -c:v libx264 -preset ultrafast -sc_threshold 0 -f hls -hls_time 2 -hls_list_size 2 -hls_flags delete_segments "$OUTPUT_FILE"

exit 0