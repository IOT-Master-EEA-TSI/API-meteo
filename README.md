# API-météo

## Table des matières 

- [**Installation**](#Installation)
- [**Utilisation**](#Utilisation)
- [**Fonctionnalités**](#Fonctionnalités)
- [**Intégration du script API-Météo dans Node-RED**](#intégration-du-script-api-météo-dans-node-red)

# **Installation**

Avant la première utilisation de ce script, il est nécessaire d’installer plusieurs bibliothèques Python :

- requests
- argparse

Ouvrez votre invite de commande, puis vérifiez dans un premier temps que Python est bien installé sur votre machine en exécutant la commande suivante :

- `python -v`

Une fois que vous avez confirmé que Python est installé, entrez les commandes suivantes pour installer les bibliothèques nécessaires. Patientez quelques instants après chaque commande afin de laisser le temps aux bibliothèques de s’installer correctement :

- `pip install requests`
- `pip install argparse`

# **Fonctionnalités**

| Commande                                      | Comportement                          |
|----------------------------------------------|---------------------------------------|
| `python script.py`                           | Par défaut : météo actuelle à Dijon   |
| `python script.py --ville Paris`             | Météo actuelle à Paris                |
| `python script.py --prevision`               | Prévision 5 jours pour Dijon          |
| `python script.py --ville Nice --prevision`  | Prévision 5 jours pour Nice           |
| `python script.py --transfere`               | Envoie discret de la météo actuelle   |
| `python script.py --prevision --transfere`   | Envoie discret des prévisions         |

# **Fonctionnalités**

Ce script propose deux modes de fonctionnement pour la transmission des informations météo, en fonction du besoin :

**1. Mode Affichage** (Par défaut)

Dans ce mode, les données météo sont affichées directement à l'écran, dans l'invite de commande, sous forme lisible et formatée. Ce mode est idéal pour une consultation humaine rapide.

**2. Mode Silencieux**

Ce mode est conçu pour les cas d'utilisation automatisés. Le script n'affiche rien à l'écran, mais sérialise les données (au format JSON) et les envoie directement sur la sortie standard (stdout). Cela permet à un autre programme ou script d'intercepter et de traiter ces données de manière transparente, que ce soit via un pipeline (|, >, etc.) ou directement en Python avec le module subprocess, comme dans l'exemple ci-dessous :

`import subprocess`

`result = subprocess.run(['python', 'script_meteo.py', '--ville', 'Paris', '--prevision'], capture_output=True, text=True)`

`stdout_output = result.stdout`

`stderr_output = result.stderr`

Ce code utilise le module subprocess pour exécuter un autre script Python (meteo.py) en lui passant des arguments (--ville Paris). Grâce à l’option capture_output=True, la sortie standard (stdout) et la sortie d’erreur (stderr) du script exécuté sont capturées, tandis que text=True permet de récupérer ces sorties sous forme de chaînes de caractères plutôt que d’octets. Ensuite, result.stdout contient les données météo générées par le script (au format JSON), et result.stderr contiendra d’éventuels messages d’erreur.

# **Intégration du script API-Météo dans Node-RED**

Dans cette partie, nous allons voir comment utiliser Node-RED pour :

- Injecter un paramètre (exemple : une ville) 

- Construire dynamiquement une commande pour exécuter un script Python avec un paramètre de type --ville 

- Exécuter ce script 

- Récupérer sa sortie au format JSON 

- Afficher les données dans l'interface de Node-RED

## Ajouter un node inject

  Objectif : Envoyer la valeur du paramètre (ex : "Paris").

  Procédure :

  1. Dans Node-RED, ajouter un node inject.
  
  2. Double-cliquer pour configurer :
  
  3. Payload : choisir "string".
  
  4. Valeur : entrer "Dijon".
  
  5. Renommer le node, par exemple en "Ville injectée".

  ## Ajouter un node function

  Objectif : Construire une commande shell valide avec le paramètre --ville.

  Procédure :

  1. Ajouter un node function.
    
  2. Insérer le code suivant :
       `msg.payload = "python3 /chemin/vers/API.py --ville " + msg.payload;
        return msg;`   
  Remplacer /chemin/vers/API.py par le chemin réel de votre script Python.


  ## Ajouter un node exec

  Objectif : Exécuter la commande Python préparée.

  Procédure :

  1. Ajouter un node exec
  
  2. Configurer :
       - Command : laisser vide (car nous utilisons msg.payload)
       - Append : activé
       - Return : sélectionner stdout
  
  3. (Optionnel) Renommer le node, par exemple en "Exécuter API.py"

  ## Ajouter un node json
  
  Objectif : Convertir le texte JSON reçu en un objet JSON exploitable dans Node-RED.

  Procédure :

  1. Ajouter un node json.

  2. Laisser les paramètres par défaut.

**Connecter les nodes dans cet ordre :**
  [inject] → [function] → [exec] → [json] → [debug]
