import requests
import argparse

url = "http://api.weatherapi.com/v1/forecast.json" # Lien internet pour contacter l'API de OpenWeather
cle = "2c6da332f6aaccb45ccbcaeb7f9b773b" # Clé API
ville = "Dijon"

parametre = {
    "key": cle,
    "q":ville,
    "lang": "fr"
}

reponse = requests.get(url, parametre)

if reponse.headers["Content-Type"] == "application/json":
    data = reponse.json()

    for day in data["forecast"]["forecastday"]:
        date = day["date"]
        condition = day["day"]["condition"]["text"]
        temp = day["day"]["avgtemp_c"]
        print(f"{date} : {condition}, {temp}°C")

else:
    print("La réponse n’est pas du JSON :")
    print(reponse.text)