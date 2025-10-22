import requests
import json
import time # Ajout du module time pour le timestamp
from bs4 import BeautifulSoup

INSTAGRAM_USERNAME = "merickkn" # VOTRE NOM D'UTILISATEUR
OUTPUT_FILE = "./followers_data.json" # Le fichier de données dans le même dossier

try:
    # 1. Requête la page Instagram
    url = f"https://www.instagram.com/{INSTAGRAM_USERNAME}/"
    # Important : Utiliser un User-Agent pour simuler un navigateur réel
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
    response.raise_for_status()

    # 2. Analyse du HTML pour trouver le nombre d'abonnés
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Tentative d'extraction basée sur la balise meta og:description (méthode la plus fiable sans API)
    follower_count = 0
    meta_tag = soup.find('meta', property='og:description')
    
    if meta_tag:
        content = meta_tag['content']
        # Exemple de contenu: "X,XXX Followers, Y,YYY Following, Z posts - See Instagram..."
        parts = content.split(' Followers')
        if parts and len(parts[0].split(' - ')) > 0:
            # Nettoyage de la chaîne de caractères pour n'avoir que le nombre
            follower_str = parts[0].split(' - ')[0].split(' ')[0].replace(',', '').replace('.', '')
            try:
                follower_count = int(follower_str.strip())
            except ValueError:
                 print("Erreur: Impossible de convertir le nombre d'abonnés.")
                 pass

    # Si le scraping échoue, nous chargeons l'ancienne valeur pour ne pas afficher 0
    if follower_count == 0:
        with open(OUTPUT_FILE, 'r') as f:
            old_data = json.load(f)
            data = {
                "timestamp": old_data.get('timestamp', int(time.time())),
                "followers": old_data.get('followers', 0),
                "status": "error_retaining_old_data"
            }
    else:
        # 3. Sauvegarde dans un fichier JSON
        data = {
            "timestamp": int(time.time()),
            "followers": follower_count,
            "status": "success"
        }

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"Nombre d'abonnés ({follower_count}) mis à jour dans {OUTPUT_FILE}")

except Exception as e:
    print(f"Erreur de scraping ou de requête: {e}")
