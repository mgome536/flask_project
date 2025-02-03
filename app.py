import os
import requests
from flask import Flask, Response
import json

app = Flask(__name__)

# La teva API Key de NewsAPI
API_KEY = "ac4a581e87f749018d8fbc172cadcca6"

@app.route('/noticies', methods=['GET'])
def obtenir_noticies():
    # Obtenim els primers 100 articles
    url_1 = f"https://newsapi.org/v2/everything?q=forex OR economia OR mercats&language=es&sortBy=publishedAt&apiKey={API_KEY}&pageSize=100&page=1"
    resposta_1 = requests.get(url_1)

    # Obtenim els següents 100 articles
    url_2 = f"https://newsapi.org/v2/everything?q=forex OR economia OR mercats&language=es&sortBy=publishedAt&apiKey={API_KEY}&pageSize=100&page=2"
    resposta_2 = requests.get(url_2)

    # Comprovar si la primera petició va bé
    if resposta_1.status_code == 200:
        dades_1 = resposta_1.json()
        articles_1 = dades_1.get("articles", [])
    else:
        return jsonify({"error": "No s'han pogut obtenir notícies (primera petició)"}), 500

    # Comprovar si la segona petició va bé
    if resposta_2.status_code == 200:
        dades_2 = resposta_2.json()
        articles_2 = dades_2.get("articles", [])
    else:
        return jsonify({"error": "No s'han pogut obtenir notícies (segona petició)"}), 500

    # Combinar els articles de les dues peticions
    articles = articles_1 + articles_2

    # Format de les notícies
    noticies_formatades = []
    for article in articles[:200]:  # Limitem a 200 notícies per resposta
        noticies_formatades.append({
            "títol": article["title"],
            "descripció": article["description"],
            "url": article["url"],
            "publicat": article["publishedAt"]
        })

    return Response(json.dumps(noticies_formatades, ensure_ascii=False), mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
