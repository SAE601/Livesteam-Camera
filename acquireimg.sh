#!/bin/bash

# Vérifie si deux arguments sont passés
if [ -z "$1" ]; then
    echo "[ERROR] Aucun fichier .ts en entrée spécifié."
    echo "Usage: $0 <fichier_ts_entree> <fichier_image_sortie>"
    exit 1
fi

if [ -z "$2" ]; then
    echo "[ERROR] Aucun nom de fichier image en sortie spécifié."
    echo "Usage: $0 <fichier_ts_entree> <fichier_image_sortie>"
    exit 1
fi

# Paramètres d'entrée
input_file="$1"
output_file="$2"

# Affiche les informations d'entrée
echo "[INFO] Entrée : $input_file"
echo "[INFO] Sortie : $output_file"

# Exécute FFmpeg pour capturer l'image
ffmpeg -i "$input_file" -vf "select=eq(n\,1)" -vsync vfr -q:v 1 "$output_file"

# Vérifie si la commande FFmpeg a réussi
if [ $? -ne 0 ]; then
    echo "[ERROR] La capture de l'image a échoué."
    exit 1
fi

echo "[INFO] Image capturée avec succès : $output_file"
exit 0