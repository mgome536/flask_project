import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# La teva API Key de NewsAPI
API_KEY = "ac4a581e87f749018d8fbc172cadcca6"

@app.route('/noticies', methods=['GET'])
def obtenir_noticies():
    # Construcció de l'URL per obtenir les notícies
    url = f"https://newsapi.org/v2/everything?q=forex OR economia OR mercats&language=es&sortBy=publishedAt&apiKey={API_KEY}"
    
    # Realitzem la petició GET a NewsAPI
    resposta = requests.get(url)
    
    # Comprovem si la resposta és correcta (status code 200)
    if resposta.status_code == 200:
        dades = resposta.json()  # Convertim la resposta a format JSON
        articles = dades.get("articles", [])  # Obtenim la llista d'articles

        # Preparem les notícies per enviar-les com a resposta JSON
        noticies_formatades = []
        for article in articles[:10]:  # Limitem a 10 notícies per resposta
            noticies_formatades.append({
                "títol": article["title"],  # Títol de la notícia
                "descripció": article["description"],  # Descripció de la notícia
                "url": article["url"],  # URL de la notícia
                "publicat": article["publishedAt"]  # Data de publicació de la notícia
            })

        return jsonify(noticies_formatades)  # Retornem les notícies en format JSON
    else:
        return jsonify({"error": "No s'han pogut obtenir notícies"}), 500  # Si hi ha error, retornem un missatge d'error

if __name__ == '__main__':
    # Executem l'aplicació Flask
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
