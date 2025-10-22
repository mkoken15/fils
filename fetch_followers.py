import instaloader
import json
import time
import os

# ----------------------------------------------------------------------
# CONFIGURATION
# ----------------------------------------------------------------------
# Le nom d'utilisateur dont on veut le nombre d'abonnés (celui qui a 700)
INSTAGRAM_USERNAME_TO_SCRAPE = "merickkn"
# Le nom du fichier de sortie
OUTPUT_FILE = "./followers_data.json" 

# Lecture des secrets passés par GitHub Actions (INSTA_USERNAME et INSTA_PASSWORD)
LOGIN_USERNAME = os.environ.get("INSTA_USERNAME") 
LOGIN_PASSWORD = os.environ.get("INSTA_PASSWORD") 
# ----------------------------------------------------------------------

try:
    L = instaloader.Instaloader()
    
    # ÉTAPE CLÉ : Connexion pour contourner le blocage 401 Unauthorized
    if LOGIN_USERNAME and LOGIN_PASSWORD:
        print(f"Tentative de connexion pour scraper {INSTAGRAM_USERNAME_TO_SCRAPE}...")
        L.login(LOGIN_USERNAME, LOGIN_PASSWORD)
        
    # Scraping du profil cible (merickkn)
    profile = instaloader.Profile.from_username(L.context, INSTAGRAM_USERNAME_TO_SCRAPE)
    follower_count = profile.followers

    # Création du JSON en cas de SUCCÈS
    data = {
        "timestamp": int(time.time()),
        "followers": follower_count,
        "status": "success (authenticated Instaloader)"
    }

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"Nombre d'abonnés ({follower_count}) mis à jour avec succès.")

except Exception as e:
    # Code de secours en cas d'ÉCHEC (pour éviter de mettre le compteur à 0)
    print(f"Échec critique de scraping. Erreur : {e}")
    try:
        # Tente de retenir l'ancienne valeur lue
        with open(OUTPUT_FILE, 'r') as f:
            old_data = json.load(f)
            data = {
                "timestamp": old_data.get('timestamp', int(time.time())),
                "followers": old_data.get('followers', 0),
                "status": "failed_retaining_old_data (Instaloader)"
            }
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except:
        pass
