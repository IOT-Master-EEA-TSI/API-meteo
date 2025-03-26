import requests
import argparse
import json

url = "https://api.openweathermap.org/data/2.5/weather" # URL de l'API OpenWeatherMap pour obtenir la météo
cle = "dea2acb30978b316029d8305f83d07cf" # Clé API pour authentifier la requête
ville = "Dijon" 

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

    if(donnee.get("cod")) != 200 : # Vérifie si l'API renvoie une erreur dans le contenu
        raise ValueError(f"erreur API : {donnee.get('message', 'Erreur inconnue')}") # Déclenche une erreur volontaire de type ValueError et récupère le message d’erreur fourni par l’API, ou un défaut

    # Extraction des données météo utiles
    meteo = donnee['weather'][0]['description'] # Description météo
    temperature = donnee['main']['temp'] # Température actuelle
    humidite = donnee['main']['humidity'] # Taux d'humidité en %
    vent = donnee['wind']['speed'] # Vitesse du vent en m/s

    # Affichage des résultats
    print(f"météo = {meteo}")
    print(f"temperature = {temperature}°C")
    print(f"Humidité = {humidite}%")
    print(f"vent = {vent} m/s")

# Gestion des différentes erreurs possibles :
except requests.exceptions.RequestException as erreur: # Problème de connexion ou réponse HTTP invalide
    print("Erreur de connexion ou de requête HTTP :", erreur)
except ValueError as erreur: # Erreur retournée par l'API dans le contenu JSON
    print("Erreur de contenu JSON ou API :", erreur)

