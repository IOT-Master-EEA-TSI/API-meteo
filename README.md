# API-météo

## Table des matières 

- [**Installation**](#Installation)
- [**Utilisation**](#Utilisation)
- [**Fonctionnalités**](#Fonctionnalités)

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



