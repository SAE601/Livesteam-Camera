#!/bin/bash

# Vérifie si deux arguments sont passés
if [ -z "$1" ]; then
    echo "[ERROR] Aucun périphérique vidéo spécifié."
    echo "Usage: $0 <périphérique_vidéo> <format_video>"
    exit 1
fi

if [ -z "$2" ]; then
    echo "[ERROR] Aucun fichier de sortie spécifié."
    echo "Usage: $0 <périphérique_vidéo> <format_video>"
    exit 1
fi

VIDEO_SIZE="$2"
VIDEO_STREAM="$1"

ffmpeg -f v4l2 -video_size $VIDEO_SIZE -t 0.5 -i $VIDEO_STREAM stream/dimw.mp4
rm stream/dimw.mp4