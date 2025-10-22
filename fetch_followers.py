import instaloader
import json
import time

INSTAGRAM_USERNAME = "merickkn"  # VOTRE NOM D'UTILISATEUR
OUTPUT_FILE = "./followers_data.json" # Le fichier de données dans le même dossier

try:
    # Initialise Instaloader
    L = instaloader.Instaloader()
    
    # Récupère le profil 
    profile = instaloader.Profile.from_username(L.context, INSTAGRAM_USERNAME)
    
    # Extrait le nombre d'abonnés
    follower_count = profile.followers

    # Sauvegarde dans un fichier JSON
    data = {
        "timestamp": int(time.time()),
        "followers": follower_count,
        "status": "success (Instaloader)"
    }

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"Nombre d'abonnés ({follower_count}) mis à jour avec Instaloader dans {OUTPUT_FILE}")

except Exception as e:
    print(f"Erreur de scraping avec Instaloader: {e}")
    # En cas d'échec, lit l'ancienne valeur pour ne pas afficher 0
    try:
        with open(OUTPUT_FILE, 'r') as f:
            old_data = json.load(f)
            data = {
                "timestamp": old_data.get('timestamp', 0),
                "followers": old_data.get('followers', 0),
                "status": "error_retaining_old_data (Instaloader)"
            }
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except:
        pass
