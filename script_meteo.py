import requests
import argparse
import json
from tabulate import tabulate

parser = argparse.ArgumentParser(description="Script météo avec OpenWeatherMap") # Crée un parser pour les arguments de ligne de commande
parser.add_argument("--ville", type=str, default="Dijon", help="Nom de la ville") # Ajoute un argument pour spécifier la ville (par défaut : Dijon)
parser.add_argument("--prevision", action="store_true", help="Activer le mode prévison") # Ajoute un argument booléen pour activer le mode prévision (sur 5 jours par tranche de 3h)
parser.add_argument("--transfere", action="store_true", help="Activer le mode transfère") # Ajoute un argument booléen pour activer le mode transfert
args = parser.parse_args() # Analyse les arguments fournis par l'utilisateur

ville = args.ville # Récupère la ville depuis les arguments en ligne de commande
cle = "dea2acb30978b316029d8305f83d07cf" # Clé API pour authentifier la requête

if args.prevision :
    url = "https://api.openweathermap.org/data/2.5/forecast" # URL de l'API OpenWeatherMap pour obtenir la météo prévisionnelle sur 5 jours
else :
    url = "https://api.openweathermap.org/data/2.5/weather" # URL de l'API OpenWeatherMap pour obtenir la météo actuelle

# Création d'un dictionnaire contenant les paramètres de la requête à envoyer 
parametre = {
    "q" : ville, 
    "appid" : cle,
    "units" : "metric",
    "lang" : "fr"
}

try :
    reponse = requests.get(url, parametre) # Création et envoie d'une requête http avec les paramètres, et récuprère la réponse
    reponse.raise_for_status() # Lève une exception automatique si la réponse HTTP est une erreur

    donnee = reponse.json() # Transforme le contenu JSON reçu en dictionnaire Python

    if(int(donnee.get("cod"))) != 200 : # Vérifie si l'API renvoie une erreur dans le contenu
        raise ValueError(f"erreur API : {donnee.get('message', 'Erreur inconnue')}") # Déclenche une erreur volontaire de type ValueError et récupère le message d’erreur fourni par l’API, ou un défaut

    #print(json.dumps(donnee, indent=2, ensure_ascii=False))

    if args.prevision : # Si l'option --prevision est activée en ligne de commande
        previsionMeteo = {} # Dictionnaire pour stocker les prévisions météo

        for entree in donnee["list"]: # Parcourt chaque entrée de la liste des prévisions fournies par l'API
            heure = entree["dt_txt"] # Date et heure de la prévision
            meteo = entree["weather"][0]["description"] # Description météo
            temperature = entree["main"]["temp"] # Température actuelle
            Humidite = entree['main']['humidity'] # Taux d'humidité en %

            # Ajoute l'entrée au dictionnaire avec l'heure comme clé
            previsionMeteo[heure] = {"Meteo": meteo, "Temperature": temperature, "Humidite" : Humidite}

        if args.transfere :
            print(json.dumps(previsionMeteo, indent = 2, ensure_ascii=False)) # # Affiche les données en JSON lisible avec indentation et accents visibles
        else :
            print(tabulate(list(previsionMeteo.values()), headers="keys", tablefmt="fancy_grid")) # Affiche les données de prévisions météo sous forme de tableau lisible avec bordures

    else :
        # Extraction des données météo utiles
        Meteo = {
           "meteo" : donnee['weather'][0]['description'], # Description météo
            "temperature" : donnee['main']['temp'], # Température actuelle
            "humidite" : donnee['main']['humidity'], # Taux d'humidité en %
            "vent" : donnee['wind']['speed'] # Vitesse du vent en m/s
        }

        if args.transfere :
           print(json.dumps(Meteo, indent = 2, ensure_ascii=False)) # # Affiche les données en JSON lisible avec indentation et accents visibles
        else :
            print(tabulate([Meteo], headers="keys", tablefmt="fancy_grid")) # Affiche les données météo actuelles sous forme de tableau lisible avec bordures

# Gestion des différentes erreurs possibles :
except requests.exceptions.RequestException as erreur: # Problème de connexion ou réponse HTTP invalide
    print("Erreur de connexion ou de requête HTTP :", erreur)
    exit(1)
except ValueError as erreur: # Erreur retournée par l'API dans le contenu JSON
    print("Erreur de contenu JSON ou API :", erreur)
    exit(1)