
# Livesteam-Camera - Guide d'installation et d'utilisation

Ce code a pour objectif de fournir un serveur de stream vidéo clé en main. Il est conçu pour fonctionner sur Windows et Linux. Par ailleurs, il implémente une fonction de prise de screenshot pour la réalisation de timelapse.

```
└── 📁Livesteam-Camera
    └── 📁images
        └── ...
    └── 📁stream
        └── ...
    └── 📁test
        └── index.html
        └── stream.js
        └── styles.css
    └── .gitignore
    └── acquireimg.bat
    └── acquireimg.sh
    └── config.json
    └── README.md
    └── requirements.txt
    └── server.py
    └── stream.bat
    └── stream.sh
```

## Installation

1. **Installer les dépendances Python** :

   ```sh
   pip install -r requirements.txt
   ```

2. **Installer FFmpeg** :

   - Assurez-vous que FFmpeg est installé et accessible via la ligne de commande.
   - Sous Windows, vous pouvez télécharger FFmpeg depuis [ffmpeg.org](https://github.com/BtbN/FFmpeg-Builds/releases), puis ajouter le chemin du binaire à la variable d'environnement `PATH`.
   - Sous Linux, installez-le avec :

     ```sh
     sudo apt update && sudo apt install ffmpeg
     ```

3. **Configurer `config.json`** :

   - Le fichier `config.json` contient les paramètres de configuration du logiciel.
   - La valeur `video_device` doit être correctement définie et elle doit pointer sur un périphérique vidéo.
   - Pour lister les périphériques vidéo disponibles, exécutez la commande suivante :

    **Windows**:

     ```sh
     ffmpeg -list_devices true -f dshow -i dummy
     ```

    **Linux**:

     ```sh
     sudo apt install v4l-utils
     ```

     ```sh
     v4l2-ctl --list-devices
     ```

   - La valeur `base_directory` est uniquement nécessaire si les dossiers sources ne sont pas dans le même répertoire que le serveur.

## Utilisation

### Lancer le serveur

Une fois l'installation terminée, vous pouvez démarrer le serveur avec :

```sh
python server.py
```

Le serveur lancera FFmpeg en arrière-plan et commencera à diffuser le flux vidéo en HLS.

### Tester avec une interface Web

Un site web est fourni pour tester le logiciel. Il inclut un fichier `stream.js` qui facilite la lecture du flux.

Pour afficher la vidéo dans une page HTML, utilisez le code suivant :

```html
<video controls autoplay>
  <source src="http://<IP_DU_SERVEUR>:5000/livestream/stream/video.m3u8" type="application/x-mpegURL">
</video>
```

Le fichier `stream.js` et la balise `<video>` peuvent être utilisés n'importe où tant que le client est sur le même réseau que le serveur HTTP.

## Fonctionnalités supplémentaires

- Capture d'une image à intervalle régulier :
  - Une image est prise à partir du flux vidéo et enregistrée dans un dossier défini dans `config.json`.

## Problèmes et dépannage

- **Le périphérique vidéo n'est pas détecté** : Vérifiez que le nom du périphérique est correctement renseigné dans `config.json`.
- **Le flux vidéo ne s'affiche pas** : Vérifiez que le serveur est bien lancé et que le port 5000 est accessible depuis votre navigateur.
- **FFmpeg ne se lance pas** : Assurez-vous qu'il est bien installé et que son chemin est défini dans les variables d'environnement.

---
