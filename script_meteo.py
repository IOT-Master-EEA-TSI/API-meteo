import requests
import argparse
import sys
import os

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
            try :
                stdout_original = sys.stdout # Sauvegarde de la sortie standard actuelle
                sys.stdout = open(os.devnull, 'w') # Redirige temporairement stdout vers un "trou noir"
                sys.stdout.write(repr(previsionMeteo) + "\n") # Écrit directement dans la vraie sortie standard
                sys.stdout.flush() 

            except (OSError, IOError) as e:
                print("Erreur lors de la redirection du stdout :", e, file=sys.__stderr__)
                sys.exit(2)

            except (OSError, BrokenPipeError) as e:
                print("Erreur lors de l'envoi des données :", e, file=sys.__stderr__)
                sys.exit(3)

            except TypeError as e:
                print("Erreur de conversion du dictionnaire :", e, file=sys.__stderr__)
                sys.exit(4)

            finally :
                sys.stdout = stdout_original 
        else :
            print(previsionMeteo)

    else :
        # Extraction des données météo utiles
        Meteo = {
           "meteo" : donnee['weather'][0]['description'], # Description météo
            "temperature" : donnee['main']['temp'], # Température actuelle
            "humidite" : donnee['main']['humidity'], # Taux d'humidité en %
            "vent" : donnee['wind']['speed'] # Vitesse du vent en m/s
        }

        if args.transfere :
            print("DEBUG : Transfert actif")
            try :
                stdout_original = sys.stdout
                sys.stdout = open(os.devnull, 'w')
                sys.__stdout__.write(repr(Meteo))
                sys.__stdout__.flush()

            except (OSError, IOError) as e:
                print("Erreur lors de la redirection du stdout :", e, file=sys.__stderr__)
                sys.exit(2)

            except (OSError, BrokenPipeError) as e:
                print("Erreur lors de l'envoi des données :", e, file=sys.__stderr__)
                sys.exit(3)

            except TypeError as e:
                print("Erreur de conversion du dictionnaire :", e, file=sys.__stderr__)
                sys.exit(4)

            finally :
                sys.stdout = stdout_original 
        else :
            # Affichage des résultats
            print("DEBUG : Affichage de Meteo")
            print(Meteo)

# Gestion des différentes erreurs possibles :
except requests.exceptions.RequestException as erreur: # Problème de connexion ou réponse HTTP invalide
    print("Erreur de connexion ou de requête HTTP :", erreur)
    exit(1)
except ValueError as erreur: # Erreur retournée par l'API dans le contenu JSON
    print("Erreur de contenu JSON ou API :", erreur)
    exit(1)

