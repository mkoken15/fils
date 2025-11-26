import instaloader
import os
import json
import time

# --- Récupération des secrets d'environnement ---
L_USERNAME = os.environ.get('INSTA_USERNAME')
L_SESSION_ID = os.environ.get('INSTA_SESSION_ID')

TARGET_PROFILE = L_USERNAME # Le profil à scraper est généralement le vôtre
OUTPUT_FILE = 'fils/followers_data.json' # Assurez-vous que ce chemin est correct

# --- Initialisation Instaloader ---
L = instaloader.Instaloader()

# --- 1. Créer une session à partir du Session ID ---
try:
    # Simuler une connexion réussie en utilisant le session ID
    L.context.store_session_info(L_USERNAME, {"sessionid": L_SESSION_ID})
    
    # Charger le profil cible
    profile = instaloader.Profile.from_username(L.context, TARGET_PROFILE)
    
    # Récupérer le nombre d'abonnés
    follower_count = profile.followers
    
    # --- 2. Sauvegarde des données (Succès) ---
    data = {
        "timestamp": int(time.time()),
        "followers": follower_count,
        "status": "success"
    }

except Exception as e:
    # --- 3. Gestion des erreurs (Échec) ---
    print(f"Échec de la récupération Instaloader : {e}")
    # En cas d'échec critique, on écrit un statut d'échec
    data = {
        "timestamp": int(time.time()),
        "followers": 0,
        "status": f"failed_instaloader_auth: {e.__class__.__name__}"
    }

finally:
    # --- 4. Écriture du fichier JSON ---
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Données écrites dans {OUTPUT_FILE} avec statut: {data['status']}")
