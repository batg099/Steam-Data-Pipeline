import json
import time
import requests
from datetime import datetime, timezone

URL_TOP = "https://api.steampowered.com/ISteamChartsService/GetMostPlayedGames/v1/"
URL_FICHE = "https://store.steampowered.com/api/appdetails"

# 1. Le top 100
top = requests.get(URL_TOP, timeout=30).json()
classement = top["response"]["ranks"]
maintenant = datetime.now(timezone.utc)

# 2. La fiche de chaque jeu
jeux = []

for ligne in classement:
    appid = ligne["appid"]
    parametres = {"appids": appid, "cc": "fr", "l": "english"}

    try:
        donnees = requests.get(URL_FICHE, params=parametres, timeout=30).json()
    except Exception:
        print("Erreur pour", appid)
        continue

    if not donnees or not donnees[str(appid)]["success"]:
        print("Pas de fiche pour", appid)
        continue

    fiche = donnees[str(appid)]["data"]
    prix = fiche.get("price_overview")

    jeux.append({
        "date_collecte": maintenant.strftime("%Y-%m-%d"),
        "rang": ligne["rank"],
        "rang_semaine_derniere": ligne.get("last_week_rank"),
        "appid": appid,
        "nom": fiche["name"],
        "gratuit": fiche["is_free"],
        "prix_eur": prix["final"] / 100 if prix else None,
        "reduction_pct": prix["discount_percent"] if prix else None,
        "genres": ", ".join(g["description"] for g in fiche.get("genres", [])),
        "pic_joueurs": ligne["peak_in_game"],
    })

    time.sleep(1.5)

# 3. Enregistrement : un jeu par ligne, dans le dossier data
nom_fichier = f"data/top_{maintenant.strftime('%Y-%m-%d')}.jsonl"

with open(nom_fichier, "w", encoding="utf-8") as fichier:
    for jeu in jeux:
        fichier.write(json.dumps(jeu, ensure_ascii=False) + "\n")

print("Fichier enregistré :", nom_fichier, "-", len(jeux), "jeux")
