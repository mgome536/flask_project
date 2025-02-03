import os
import requests
import json
from flask import Flask, Response

app = Flask(__name__)

# La teva API Key de NewsAPI
API_KEY = "ac4a581e87f749018d8fbc172cadcca6"

@app.route('/noticies', methods=['GET'])
def obtenir_noticies():
    url = f"https://newsapi.org/v2/everything?q=forex OR economia OR mercats&language=es&sortBy=publishedAt&apiKey={API_KEY}"
    resposta = requests.get(url)
    
    if resposta.status_code == 200:
        dades = resposta.json()
        articles = dades.get("articles", [])

        noticies_formatades = []
        for article in articles[:10]:
            noticies_formatades.append({
                "títol": article["title"],
                "descripció": article["description"],
                "url": article["url"],
                "publicat": article["publishedAt"]
            })

        # Retornem la resposta com la codificació correcta
        return Response(json.dumps(noticies_formatades, ensure_ascii=False), mimetype='application/json')
    else:
        return jsonify({"error": "No s'han pogut obtenir notícies"}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
